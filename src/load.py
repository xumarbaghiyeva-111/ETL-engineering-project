import logging
import psycopg2
from psycopg2 import extras
import pandas as pd

DB_PARAMS = {
    "host": "localhost",
    "port": "5433",
    "database": "engineering_db",
    "user": "data_user",
    "password": "data_password"
}

def create_table_if_not_exists():
    """Bazada birləşdirilmiş məlumatların yazılacağı cədvəli yaradır."""
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        create_query = """
        CREATE TABLE IF NOT EXISTS integrated_diamonds (
            id SERIAL PRIMARY KEY,
            user_id INT UNIQUE,
            carat NUMERIC(5, 2),
            cut VARCHAR(50),
            color VARCHAR(50),
            clarity VARCHAR(50),
            depth NUMERIC(5, 2),
            table_width NUMERIC(5, 2),
            price INT,
            x NUMERIC(5, 2),
            y NUMERIC(5, 2),
            z NUMERIC(5, 2),
            name VARCHAR(150),
            username VARCHAR(100),
            email VARCHAR(150),
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_query)
        conn.commit()
        logging.info("PostgreSQL: 'integrated_diamonds' cədvəli yoxlanıldı/yaradıldı.")
    except psycopg2.OperationalError as op_err:
        logging.critical(f"PostgreSQL-ə qoşulmaq mümkün olmadı (Baza söndürülüb və ya port səhvdir): {op_err}")
        raise
    except psycopg2.Error as db_err:
        logging.error(f"Cədvəl yaradılarkən verilənlər bazası xətası: {db_err}")
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()

def load_data_to_postgres(df: pd.DataFrame):
    """Birləşdirilmiş DataFrame-i Idempotency (ON CONFLICT) ilə bazaya yükləyir."""
    if df.empty:
        logging.warning("Yükləmə Mərhələsi: DataFrame boşdur, yüklənəcək data yoxdur.")
        return

    try:
        create_table_if_not_exists()
    except Exception as e:
        logging.error(f"Cədvəl yoxlanışı uğursuz olduğu üçün yükləmə dayandırıldı: {e}")
        return
    
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        insert_query = """
        INSERT INTO integrated_diamonds (
            user_id, carat, price, x, y, z, name, username, email
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET 
            carat = EXCLUDED.carat,
            price = EXCLUDED.price,
            x = EXCLUDED.x,
            y = EXCLUDED.y,
            z = EXCLUDED.z,
            name = EXCLUDED.name,
            username = EXCLUDED.username,
            email = EXCLUDED.email,
            updated_at = CURRENT_TIMESTAMP;
        """
        
        required_cols = ['user_id', 'carat', 'price', 'x', 'y', 'z', 'name', 'username', 'email']
        
        for col in required_cols:
            if col not in df.columns:
                df[col] = None
                
        data_to_insert = [tuple(x) for x in df[required_cols].values]
        
        extras.execute_batch(cur, insert_query, data_to_insert)
        conn.commit()
        logging.info(f"Yükləmə Mərhələsi Uğurlu: {len(data_to_insert)} sətir bazaya yazıldı/yeniləndi.")
    except psycopg2.Error as db_err:
        if conn:
            conn.rollback()
        logging.error(f"Bazaya execute_batch zamanı SQL xətası baş verdi (Rollback olundu): {db_err}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Məlumat hazırlığı və ya yükləmə zamanı gözlənilməyən xəta: {e}")
        raise
    finally:
        if cur: cur.close()
        if conn: conn.close()