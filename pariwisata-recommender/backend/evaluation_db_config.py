# evaluation_db_config.py - Versi Sederhana
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Konfigurasi database SQLite untuk evaluasi
EVALUATION_DATABASE_URL = 'sqlite:///./evaluation.db'

def setup_evaluation_db():
    """Setup database SQLite untuk evaluasi"""
    
    # Buat engine SQLite
    evaluation_engine = create_engine(EVALUATION_DATABASE_URL, echo=False)
    EvaluationSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=evaluation_engine)
    
    return evaluation_engine, EvaluationSessionLocal

def load_evaluation_data():
    """Load data untuk evaluasi dari SQLite"""
    
    engine, session_local = setup_evaluation_db()
    
    try:
        # Cek tabel yang ada
        with engine.connect() as conn:
            tables_query = text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables_result = conn.execute(tables_query)
            available_tables = [row[0] for row in tables_result]
            
        print(f"📋 Tabel tersedia: {available_tables}")
        
        # Load data berdasarkan nama tabel yang umum
        data = {}
        
        # Coba berbagai nama tabel yang mungkin
        table_mappings = {
            'ratings': ['ratings', 'rating', 'user_ratings', 'reviews'],
            'destinations': ['destinations', 'destination', 'places', 'tourism_places'],
            'users': ['users', 'user', 'user_profiles']
        }
        
        for data_type, possible_names in table_mappings.items():
            for table_name in possible_names:
                if table_name in available_tables:
                    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
                    data[data_type] = df
                    print(f"✅ Loaded {data_type}: {len(df)} records from table '{table_name}'")
                    break
            else:
                print(f"⚠️ Tidak ditemukan tabel untuk {data_type}")
                data[data_type] = pd.DataFrame()  # DataFrame kosong
        
        return data, engine, session_local
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return {}, engine, session_local