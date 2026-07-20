import pandas as pd
import logging
import os

def read_csv(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"'{file_path}' adlı fayl sistemdə tapılmadı.")
            
        df = pd.read_csv(file_path)
        
        if df.empty:
            logging.warning(f"Diqqət: '{file_path}' faylı boşdur.")
            
        return df
        
    except FileNotFoundError as fnf_err:
        logging.error(f"CSV Oxuma Xətası: {fnf_err}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"CSV Oxuma Xətası: '{file_path}' faylı tamamilə boşdur və oxuna bilməz.")
        raise
    except pd.errors.ParserError:
        logging.error(f"CSV Parsing Xətası: Faylın formatı korlanıb (sətirlər düzgün ayrılmayıb).")
        raise
    except Exception as e:
        logging.error(f"CSV ilə bağlı gözlənilməyən xəta: {e}")
        raise