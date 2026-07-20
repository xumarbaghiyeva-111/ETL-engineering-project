import pandas as pd
import logging

def transform_data(diamonds_df, users_df):
    logging.info("Data Transformation Stage Started.")
    
    if diamonds_df is None or users_df is None:
        raise ValueError("Transformasiya üçün ötürülən DataFrame-lər Null (None) ola bilməz.")
        
    # --- 1. CSV DATA CLEANING & TYPES ---
    logging.info("Cleaning and formatting diamonds data...")
    cleaned_diamonds = diamonds_df.copy()
    
    if 'price' in cleaned_diamonds.columns:
        cleaned_diamonds = cleaned_diamonds.dropna(subset=['price'])
        try:
            cleaned_diamonds['price'] = cleaned_diamonds['price'].astype(int)
        except (ValueError, TypeError) as e:
            logging.warning(f"'price' sütununu int tipinə çevirmək mümkün olmadı, sətirlər silinir: {e}")
            cleaned_diamonds = cleaned_diamonds[pd.to_numeric(cleaned_diamonds['price'], errors='coerce').notnull()]
            cleaned_diamonds['price'] = cleaned_diamonds['price'].astype(int)
    
    if 'carat' in cleaned_diamonds.columns:
        try:
            cleaned_diamonds['carat'] = cleaned_diamonds['carat'].astype(float)
        except (ValueError, TypeError) as e:
            logging.warning(f"'carat' sütununda xətalı tiplər tapıldı: {e}")
            cleaned_diamonds['carat'] = pd.to_numeric(cleaned_diamonds['carat'], errors='coerce')
    
    for col in ['x', 'y', 'z']:
        if col in cleaned_diamonds.columns:
            try:
                median_value = cleaned_diamonds[col].median()
                cleaned_diamonds[col] = cleaned_diamonds[col].replace(0, median_value)
            except Exception as e:
                logging.error(f"'{col}' sütunu emal edilərkən xəta: {e}. Növbəti sütuna keçilir...")
                continue

    # --- 2. API DATA CLEANING ---
    logging.info("Cleaning and structuring users data from API...")
    cleaned_users = users_df.copy()
    
    if 'id' in cleaned_users.columns:
        cleaned_users = cleaned_users.rename(columns={'id': 'user_id'})
    
    # Lazımi sütunların mövcudluğunu yoxlayırıq
    available_user_cols = [col for col in ['user_id', 'name', 'username', 'email'] if col in cleaned_users.columns]
    cleaned_users = cleaned_users[available_user_cols]

    # --- 3. MERGING ON A COMMON KEY ---
    logging.info("Merging both data sources on simulated 'user_id'...")
    
    if not cleaned_diamonds.empty:
        cleaned_diamonds['user_id'] = (cleaned_diamonds.index % 10) + 1
    else:
        cleaned_diamonds['user_id'] = pd.Series(dtype=int)
    
    try:
        merged_df = pd.merge(cleaned_diamonds, cleaned_users, on='user_id', how='left')
        logging.info(f"Transformation completed successfully! Total integrated rows: {len(merged_df)}")
        return merged_df
    except Exception as e:
        logging.error(f"Merge mərhələsində kritik xəta: {e}")
        raise