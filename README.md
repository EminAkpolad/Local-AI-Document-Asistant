# 📚 Yerel Yapay Zekâ Doküman Asistanı (Local AI Document Assistant)

Bu proje, tamamen yerel cihazınızda (offline) çalışan, yüklediğiniz PDF dokümanlarını anlamsal olarak analiz eden ve içerisinden nokta atışı arama yapmanızı sağlayan **ChromaDB ve Streamlit tabanlı bir RAG (Retrieval-Augmented Generation) prototipidir.**

Verilerinizi harici bulut servislerine göndermez, internet bağlantısı gerektirmez ve tamamen güvenlidir.

---

## 🚀 Öne Çıkan Özellikler & Mimari Yaklaşım

### 🔹 Neden JSON Değil de Vektör Veritabanı (ChromaDB)?
Projenin ilk tasarım aşamasında verilerin JSON formatında saklanması düşünülmüş, ancak **performans, güvenlik ve ölçeklenebilirlik** kriterleri göz önüne alınarak harici bir JSON yapısından vazgeçilmiştir.
* **ANN (Approximate Nearest Neighbor):** Doküman boyutu büyüdükçe geleneksel backend indekslerindeki gibi (`B-Tree`) kelime kelime arama yapmak yerine, anlamsal uzayda en yakın komşuları bulan **HNSW** algoritması entegre edilmiştir. Bu sayede milisaniyeler içinde arama tamamlanır.
* **Gömülü (Persistent) Mod:** Proje, ChromaDB'yi ayrı bir sunucu olarak çalıştırmak (Standalone) yerine Python kodu içine gömülü çalıştıran **PersistentClient** mimarisiyle yapılandırılmıştır. Bilgisayarı yormaz ve verileri proje dizinindeki `./assistan_brain` klasöründe binary olarak şifreli/optimize saklar.

### 🔹 Akıllı Metin Parçalama (Text Chunking)
PDF içerisindeki sayfalar düz metne çevrildikten sonra, anlam bütünlüğünün korunması adına `langchain-text-splitters` kütüphanesinin **RecursiveCharacterTextSplitter** aracı kullanılmıştır. Metinler kelime ortasından bölünmeden 600 karakterlik lokmalara (chunk) ayrılır ve 100 karakterlik kesişim kümeleriyle (overlap) bilgi kaybı önlenir.

### 🔹 Tamamen Yerel Vektörleştirme (Embedding)
ChromaDB'nin Python 3.15 ortamındaki `onnxruntime` kısıtlamalarını ve çakışmalarını aşmak adına, yapay zekâ ekosisteminin altın standardı olan **Python 3.11** kararlı sürümüne geçilmiştir. Metinleri sayı dizilerine dönüştürmek için HuggingFace'in internet gerektirmeyen şampiyon yerel modeli **`all-MiniLM-L6-v2`** (`sentence-transformers`) kullanılmıştır.

---

## 🛠️ Teknoloji Yığını (Tech Stack)

* **Arayüz:** Streamlit (Python tabanlı Chat ve Dosya Yönetim Arayüzü)
* **Vektör Veritabanı:** ChromaDB (Persistent / Embedded Mod)
* **Embedding Modeli:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Metin İşleme:** PyPDF (PDF Extraction) & LangChain (Recursive Splitter)
* **Çalışma Ortamı:** Python 3.11.9 (Venv)

---


## 📦 Kurulum ve Çalıştırma

### 1. Gereksinimler
Bilgisayarınızda **Python 3.11** yüklü olmalıdır. Eğer yüklü değilse Windows terminalinden terminal tabanlı akıllı başlatıcıyı kullanarak kurabilirsiniz:
```bash
py install 3.11
```

### 2. Proje Kurulumu
Proje klasörünüzün içine girin ve aşağıdaki komutları sırasıyla çalıştırarak sanal ortamı kurup bağımlılıkları yükleyin:

```bash
# Sanal ortamı Python 3.11 ile oluşturun
py -3.11 -m venv .venv

# Sanal ortamı aktif edin (Windows PowerShell için)
.\.venv\Scripts\activate

# Tüm yapay zekâ bağımlılıklarını temiz önbellekle yükleyin
pip install streamlit chromadb pypdf langchain-text-splitters sentence-transformers --no-cache-dir
```

### 3. Uygulamayı Başlatma
Her şey yüklendikten sonra yerel web arayüzünü ayağa kaldırmak için şu komutu çalıştırın:
```bash
.\.venv\Scripts\streamlit.exe run app.py
```
Tarayıcınızda otomatik olarak `http://localhost:8501` adresi açılacaktır.

---PROGRAMIN GÖRÜNTÜLERİ---

<img width="1909" height="918" alt="Ekran görüntüsü 2026-11-26 160259" src="https://github.com/user-attachments/assets/44755926-863a-43f7-96a6-b4248f113ed6" />
<img width="1919" height="907" alt="Ekran görüntüsü 2026-11-26 160216" src="https://github.com/user-attachments/assets/cd49e77e-0083-4ca5-8d34-a347c763378c" />
