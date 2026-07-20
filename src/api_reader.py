import requests 
import pandas as pd  
import logging

def read_api():  
    api_url = "https://jsonplaceholder.typicode.com/users" 
    
    print("=== [2] API Çıxarışı Başladı ===")
    try:
        # 10 saniyəlik timeout əlavə edirik ki, sorğu sonsuz bloklanmasın
        response = requests.get(api_url, timeout=10)  
        
        # HTTP 4xx və ya 5xx status kodları gəldikdə birbaşa xəta (HTTPError) fırladır
        response.raise_for_status()  
        
        data = response.json()  
        df = pd.DataFrame(data)  
        return df  
        
    except requests.exceptions.Timeout:
        logging.error("API Xətası: Sorğu vaxtı bitdi (Timeout).")
        raise
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"API HTTP Xətası: {http_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        logging.error(f"API Şəbəkə/Bağlantı Xətası: {req_err}")
        raise
    except Exception as e:
        logging.error(f"API JSON və ya DataFrame formatlama xətası: {e}")
        raise