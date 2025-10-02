import os
import pandas as pd
from sqlalchemy import create_engine, text

# Simpan SQLite selalu di folder file ini (independen dari CWD)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.path.join(SCRIPT_DIR, "evaluation.db")
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

# Ambil DATABASE_URL dari environment
POSTGRESQL_URL = os.getenv("DATABASE_URL", "postgresql://user:rekompari@localhost:5432/pariwisata")

def migrate_data_raw_sql():
    # 1) Hard fail jika DATABASE_URL belum di-set
    if not POSTGRESQL_URL:
        raise RuntimeError(
            "ENV DATABASE_URL belum di-set. Set variabel environment terlebih dahulu.\n\n"
            "Contoh set DATABASE_URL:\n"
            "  • Windows PowerShell:\n"
            '      $env:DATABASE_URL = "postgresql://user:pass@localhost:5432/dbname"\n'
            "  • Windows CMD:\n"
            '      set DATABASE_URL=postgresql://user:pass@localhost:5432/dbname\n'
            "  • Linux/macOS (bash/zsh):\n"
            '      export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"\n'
        )

    print(f"SQLite target: {SQLITE_PATH}")

    # 2) Koneksi ke Postgres (akan error jika driver belum ada)
    #    Jika psycopg2 belum terpasang, errornya: ModuleNotFoundError: No module named 'psycopg2'
    pg_engine = create_engine(POSTGRESQL_URL, echo=False)
    sqlite_engine = create_engine(SQLITE_URL, echo=False)

    # 3) Ambil daftar tabel di schema public
    with pg_engine.connect() as pg_conn:
        tables = pg_conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        ).scalars().all()

        if not tables:
            raise ValueError("Tidak ada tabel di schema 'public' PostgreSQL.")

        print(f"Tabel terdeteksi: {tables}")

        # 4) Migrasikan setiap tabel
        for t in tables:
            df = pd.read_sql(f'SELECT * FROM "{t}"', pg_conn)
            df.to_sql(t, sqlite_engine, if_exists="replace", index=False)
            print(f"OK: {t} -> {len(df)} baris")

    print(f"Selesai. File SQLite ada di: {SQLITE_PATH}")

if __name__ == "__main__":
    migrate_data_raw_sql()