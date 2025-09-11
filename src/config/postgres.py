from decouple import config
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import SQLModel
import logging

# Konfigurasi logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# URL koneksi database dari environment variables
SQLALCHEMY_DATABASE_URL = config("DATABASE_CONN")

print("DB URLNYA:", SQLALCHEMY_DATABASE_URL)

# Membuat engine dengan pengaturan tambahan
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"options": "-c timezone=Asia/Jakarta"},  # Mengatur zona waktu
    echo=True,
    pool_size=10,  # Mengatur ukuran pool
    max_overflow=20,  # Jumlah koneksi yang dapat dibuat melebihi pool_size
    pool_timeout=30,  # Waktu timeout untuk menunggu koneksi tersedia
    pool_recycle=1800,  # Mengatur waktu daur ulang pool (dalam detik)
    pool_pre_ping=True,  # Memeriksa koneksi sebelum meminjamkan dari pool
)

# Membuat sesi lokal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklarasi base untuk model
Base = declarative_base()


def get_db():
    """Dependency untuk mendapatkan sesi database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inisialisasi database."""
    logger.debug("Connect to DB ....")
    # Menggunakan SQLModel.metadata.create_all untuk compatibility dengan Alembic
    SQLModel.metadata.create_all(bind=engine)


# Inisialisasi database saat modul diimpor
init_db()
