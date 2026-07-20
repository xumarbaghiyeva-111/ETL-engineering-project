import logging
import os
import pandas as pd

from api_reader import read_api
from csv_reader import read_csv
from transformer import transform_data
from load import load_data_to_postgres

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_etl():
    logging.info("=== ETL PİPELİNE İŞƏ DÜŞDÜ ===")
    csv_file_path = "diamonds.csv"
    
    try:
        # ---------------------------------------------------------
        # 1. ETAP: EXTRACT (Məlumatların Çıxarılması)
        # ---------------------------------------------------------
        logging.info("Extract: CSV faylı oxunur...")
        try:
            diamonds_df = read_csv(csv_file_path)
        except Exception as e:
            logging.error(f"Kritik Extract Xətası (CSV oxuna bilmədi): {e}. Proses dayandırılır.")
            return

        logging.info("Extract: API-dan istifadəçi məlumatları çəkilir...")
        try:
            users_df = read_api()
        except Exception as e:
            logging.error(f"Kritik Extract Xətası (API məlumatı çəkilə bilmədi): {e}. Proses dayandırılır.")
            return
            
        logging.info("Extract Mərhələsi Tamamlandı.")

        # ---------------------------------------------------------
        # 2. ETAP: TRANSFORM (Məlumatların Təmizlənməsi və Birləşməsi)
        # ---------------------------------------------------------
        logging.info("Transform: Məlumatların transformasiyası başladı...")
        try:
            integrated_df = transform_data(diamonds_df, users_df)
        except Exception as e:
            logging.error(f"Kritik Transform Xətası (Data birləşdirilə bilmədi): {e}. Proses dayandırılır.")
            return

        # ---------------------------------------------------------
        # 3. ETAP: LOAD (Məlumatların Verilənlər Bazasına Yazılması)
        # ---------------------------------------------------------
        logging.info("Load: İnteqrasiya olunmuş datanın bazaya yüklənməsi başladı...")
        try:
            load_data_to_postgres(integrated_df)
        except Exception as e:
            logging.error(f"Kritik Load Xətası (Bazaya yazmaq uğursuz oldu): {e}.")
            return
        
        logging.info("=== ETL PİPELİNE UĞURLA TAMAMLANDI ===")

    except Exception as main_err:
        logging.critical(f"ETL Axınında Gözlənilməyən Qlobal Xəta: {main_err}")

if __name__ == "__main__":
    run_etl()