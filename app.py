import streamlit as st
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import ollama

st.set_page_config(page_title="Yerel AI Döküman Asistan",page_icon=None)
st.title("YEREL AI DÖKÜMAN ASİSTAN")

@st.cache_resource
def load_embedding_model():

    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()


@st.cache_resource # Veritabanını kilitledim
def get_chroma_client():

    return chromadb.PersistentClient(path="./assistan_brain") 

chroma_client = get_chroma_client() # Client ayağa kalktı


def extract_text_from_pdf(uploaded_file)->str:
    pdf_reader=PdfReader(uploaded_file)
    text=""
    for page in pdf_reader.pages:
        page_text=page.extract_text()
        if page_text:
            text+=page_text+"\n"
    return text

def split_text_into_chunks(text:str):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        length_function=len
    )

    return text_splitter.split_text(text)


def save_chunks_to_chroma(chunks: list, file_name: str) -> None:
    collection = chroma_client.get_or_create_collection(name="pdf_dokumanlari")

    computed_embeddings = embedding_model.encode(chunks).tolist()

    prepared_ids = [f"id_{file_name}_{i}" for i in range(len(chunks))]
    prepared_metadatas = [{"kaynak": file_name, "parca_no": i} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=computed_embeddings, 
        metadatas=prepared_metadatas,
        ids=prepared_ids
    )

def search_in_documents(query:str,n_results:int=3)->list:
       collection=chroma_client.get_or_create_collection(name="pdf_dokumanlari")
       query_embedding=embedding_model.encode([query]).tolist()
       results=collection.query(
          query_embeddings=query_embedding,
          n_results=n_results
       )
       return results.get("documents",[[]])[0]


def generate_ai_response(prompt:str,context_chunks:list)->str:
    
    context="\n\n".join(context_chunks)
    
    system_prompt=(
        "Sen yerel bir döküman asistanısın. Sana verilen 'Bağlam' (Context) içerisindeki"
        "bilgileri kullanarak kullanıcının sorusuna net ,doğru ve Türkçe cevaplar vermelisin."
        "Eğer cevap bağlam içerisinde yoksa, dışarıdan bilgi uydurma ve dürüstçe dökümanda "
        "bulamadığını belirt."
    )
    
    user_prompt=f"Bağlam:\n{context}\n\nSoru:{prompt}\n\nCevap:"
    
    response=ollama.generate(
        model="qwen3:4b" if "qwen3:4b" in [m['model'] for m in  ollama.list()['models']] else "llama3",
        prompt=user_prompt,
        system=system_prompt
    )
    return response['response']
    

with st.sidebar:
    st.header("Döküman Yönetimi")
    uploaded_file=st.file_uploader("Bir Pdf dosyası seçin",type="pdf")

    if uploaded_file:
        file_size_kb=uploaded_file.size/1024
        st.write("---")
        st.markdown(f"Dosya Adı:{uploaded_file.name}")
        st.markdown(f"Boyut:{file_size_kb:.2f} KB")



if uploaded_file and "chunks" not in st.session_state:
    with st.spinner("Döküman İşleniyor..."):
        try:
            raw_text=extract_text_from_pdf(uploaded_file)

            if raw_text:
                chunks=split_text_into_chunks(raw_text)

                save_chunks_to_chroma(chunks,uploaded_file.name)

                st.session_state["chunks"]=chunks
                st.session_state["file_name"]=uploaded_file.name
                st.success("Döküman başarı ile yüklendi ve Indexlendi")

        except Exception as e:
            st.sidebar.error(f"Süreç sırasında bir hata oluştu: {e}")


if "chunks" not in st.session_state:
    st.info("Lütfen sol taraftaki panelden bir PDF dökümanı yükleyerek başlayın.")

else:
    st.sidebar.metric(label="Oluşan Toplam Parça(Chunk)",value=len(st.session_state["chunks"]))

    if user_query:=st.chat_input(f"'{st.session_state['file_name']}' Hakkında birşey sorun.."):
      with st.chat_message("user"):
          st.write(user_query)

      with st.chat_message("assistant"):
            with st.spinner("Döküman İnceleniyor ve Cevap Üretiliyor..."):
                try:
                    bulunan_parcalar = search_in_documents(user_query)

                    if bulunan_parcalar:
                        yapay_zeka_cevabi = generate_ai_response(user_query, bulunan_parcalar)
                        
                        st.markdown(yapay_zeka_cevabi)
                        
                        with st.expander("ChromaDB'den Beslenen Kaynak Paragraflar"):
                            for i, parca in enumerate(bulunan_parcalar):
                                st.info(f"Eşleşen parça {i+1}: \n{parca}")
                    else:
                        st.warning("Dökümanda bu soruyla ilgili hiçbir içerik bulunamadı")
                except Exception as e: 
                    st.error(f"Arama İşlemi sırasında bir hata oluştu {e}")