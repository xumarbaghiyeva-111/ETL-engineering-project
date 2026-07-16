import requests  # [1] HTTP sorğuları göndərmək üçün 'requests' kitabxanasını daxil edirik.
import pandas as pd  # [2] JSON məlumatını cədvələ çevirmək üçün Pandas-ı daxil edirik.

def read_api():  # [3] Parametr qəbul etməyən 'read_api' funksiyasını yaradırıq.
    api_url = "https://jsonplaceholder.typicode.com/users"  # [4] Məlumatı çəkəcəyimiz test API ünvanı (URL).
    
    print("=== [2] API Çıxarışı Başladı ===")
    response = requests.get(api_url)  # [5] API ünvanına HTTP "GET" sorğusu göndəririk və cavabı 'response' dəyişəninə yığırıq.
    
    if response.status_code == 200:  # [6] Əgər server "200 OK" (uğurlu) cavabı veribsə:
        data = response.json()  # [7] Gələn cavabı JSON (Python lüğəti/siyahısı) formatına çeviririk.
        df = pd.DataFrame(data)  # [8] Həmin JSON-u sütun və sətirlərdən ibarət Pandas DataFrame-nə çeviririk.
        return df  # [9] DataFrame-i geri qaytarırıq.
    else:
        # [10] Əgər internet və ya server xətası olubsa (məs: 404 və ya 500), xətanı fırladırıq.
        raise Exception(f"API-dan məlumat çəkilə bilmədi! Status kodu: {response.status_code}")