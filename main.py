from pathlib import Path

def show_file_info(file_path:Path)->None:
    if not file_path.exists():
        print("Hata:Boyle bir dosya bulunamadi")
        return

    if not file_path.is_file():
        print("Girilen yol bir dosya degil")
        return




    file_name=file_path.name
    file_extension=file_path.suffix
    file_size=file_path.stat().st_size

    print(f"{file_extension} dosyasi secildi")

    print("\n -----DOSYA BİLGİLERİ-----")
    print(f"Dosya Adi: {file_name}")
    print(f"Uzanti : {file_extension}")
    print(f"Boyut : {file_size}")
    print(f"Boyut : {file_size/1024:.2f} KB");




def main() -> None:
    raw_path = input("Dosya yolunu gir: ").strip().strip('"')

    file_path = Path(raw_path)

    show_file_info(file_path)


if __name__=="__main__":
    main()



# PDF ve DOCX gibi dosya türlerinden metin çıkarma
# Metinleri anlamlı parçalara (Chucking) ayırma
# Embedding üretme
# Vektör Veritabanına kayıt
# Kullanıcının sorusuna göre en alakalı parçaları bulma
# Bulunan kaynakları LLM'e gönderme
# Kaynak göstererek cevap üretme
# Hataları Yönetme,test yazma ve performansı değerlendirme