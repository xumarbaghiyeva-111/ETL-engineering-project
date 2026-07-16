import os  # [1] Əməliyyat sistemi və qovluq yolları ilə işləmək üçün 'os' modulunu daxil edirik.
from csv_reader import read_csv  # [2] 'csv_reader.py' daxilindəki funksiyamızı bura çağırırıq.
from api_reader import read_api  # [3] 'api_reader.py' daxilindəki funksiyamızı bura çağırırıq.

def run_pipeline():
    print("======= DATA ENGINEERING PIPELINE: TAPŞIRIQ 1 =======")
    
    # ----------------- 1. MƏRHƏLƏ: CSV-NİN OXUNMASI -----------------
    try:  # [4] CSV oxuma mərhələsində yarana biləcək hər hansı bir xətanı nəzarətə alırıq.
        # [5] Bu kodun işlədiyi qovluğun mütləq yolunu tapır (məsələn: C:/Users/../src)
        current_folder = os.path.dirname(os.path.abspath(__file__))
        
        # [6] 'src'-dən bir addım geri çıxıb 'data/diamonds.csv' faylına dinamik yol qurur.
        file_path = os.path.join(current_folder, "../data/diamonds.csv")
        
        print("=== [1] CSV Çıxarışı Başladı ===")
        diamonds_df = read_csv(file_path)  # [7] Digər modulu çağırıb CSV-ni oxuyuruq.
        print(f"Uğurlu! CSV-dən {len(diamonds_df)} sətir oxundu.")
        print(diamonds_df.head(2))  # [8] Konsola nəticənin doğruluğunu görmək üçün ilk 2 sətri yazdırırıq.
        
    except Exception as e:
        # [9] Əgər yuxarıdakı 'try' daxilində hər hansı bir xəta (fayl tapılmadı, pandas xətası və s.) baş verərsə:
        print(f"❌ Kritik Xəta: CSV oxunarkən problem baş verdi. Proses dayandırılır! \nDetallar: {e}")
        return  # [10] ÇOX VACİB: Burada 'return' etməklə proqramı dərhal dayandırırıq və 2-ci mərhələyə (API) keçmirik!
        
    print("-" * 50)
    
    # ----------------- 2. MƏRHƏLƏ: API-DƏN ÇƏKİLMƏK -----------------
    try:  # [11] API mərhələsini də təhlükəsizlik blokuna salırıq.
        users_df = read_api()  # [12] API modulunu çağırırıq.
        print(f"Uğurlu! API-dan {len(users_df)} istifadəçi məlumatı çəkildi.")
        print(users_df[['id', 'name', 'email', 'username']].head(2))  # [13] Yoxlamaq üçün ilk 2 istifadəçini yazdırırıq.
        
    except Exception as e:
        # [14] Əgər internet kəsilibsə və ya API çökübsə, bura işə düşür:
        print(f"❌ Kritik Xəta: API ilə əlaqə qurularkən problem baş verdi. \nDetallar: {e}")
        return

    print("\n=====================================================")
    print("TƏBRİKLƏR! Hər iki mənbədən məlumat ardıcıl olaraq uğurla çıxarıldı.")
    print("=====================================================")

if __name__ == "__main__":
    run_pipeline()  # [15] Python bu skripti birbaşa işə salanda 'run_pipeline' funksiyasını tetikləyir.