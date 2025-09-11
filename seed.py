#!/usr/bin/env python3
"""
Seed script untuk mengisi data awal database
"""
import os
import sys
from pathlib import Path

# Tambahkan root project ke sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from src.config.postgres import engine, SessionLocal
from src.user.models import User, UserProfile
import uuid
from datetime import datetime
import hashlib


def create_admin_user(db: Session):
    """Buat user admin default"""
    # Hash password sederhana (gunakan library proper di production)
    password_hash = hashlib.sha256("admin123".encode()).hexdigest()

    user = User(
        username="admin",
        password=password_hash,
        is_active=True,
        created_by="system",
        updated_by="system",
        created_date=datetime.now(),
        updated_date=datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Buat profile untuk admin
    profile = UserProfile(
        id_user=user.id,
        nama_lengkap="Administrator",
        email="admin@aksara.ai",
        tipe_akun="ADMIN",
        role="SUPER_ADMIN",
        created_by="system",
        updated_by="system",
        created_date=datetime.now(),
        updated_date=datetime.now(),
    )
    db.add(profile)
    db.commit()

    return user, profile


def seed_database():
    """Mengisi database dengan data awal"""
    print("🌱 Starting database seeding...")

    db = SessionLocal()
    try:

        print("👤 Creating admin user...")
        user, profile = create_admin_user(db)
        print(f"✅ Created admin user: {user.username}")
        print(f"✅ Created admin profile: {profile.nama_lengkap}")

        print("🎉 Database seeding completed successfully!")
        print("\n📋 Default credentials:")
        print(f"   Username: {user.username}")
        print(f"   Password: admin123")
        print(f"   Email: {profile.email}")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
