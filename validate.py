#!/usr/bin/env python3
"""
Validation script untuk memastikan migration berjalan dengan benar
"""
import os
import sys
from pathlib import Path

# Tambahkan root project ke sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from sqlalchemy.orm import Session
from src.config.postgres import engine, SessionLocal


def check_database_connection():
    """Cek koneksi database"""
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        db.close()
        print(f"✅ Database connection successful")
        print(f"   PostgreSQL version: {version}")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_tables_exist():
    """Cek apakah tabel-tabel penting sudah ada"""
    required_tables = ["user", "user_profile", "refresh_tokens"]

    try:
        db = SessionLocal()
        existing_tables = []

        for table in required_tables:
            result = db.execute(
                text(
                    f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """
                )
            )

            if result.fetchone()[0]:
                existing_tables.append(table)

        db.close()

        print(f"📊 Table status:")
        for table in required_tables:
            status = "✅" if table in existing_tables else "❌"
            print(f"   {status} {table}")

        return len(existing_tables) == len(required_tables)

    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False


def check_foreign_keys():
    """Cek foreign key constraints"""
    try:
        db = SessionLocal()

        # Cek foreign key dari user_profile ke user
        result = db.execute(
            text(
                """
            SELECT 
                tc.constraint_name, 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = 'public';
        """
            )
        )

        foreign_keys = result.fetchall()
        db.close()

        print(f"🔗 Foreign Key Constraints:")
        for fk in foreign_keys:
            print(
                f"   ✅ {fk.table_name}.{fk.column_name} -> {fk.foreign_table_name}.{fk.foreign_column_name}"
            )

        return True

    except Exception as e:
        print(f"❌ Error checking foreign keys: {e}")
        return False


def check_indexes():
    """Cek indexes yang sudah dibuat"""
    try:
        db = SessionLocal()

        result = db.execute(
            text(
                """
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM pg_indexes 
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname;
        """
            )
        )

        indexes = result.fetchall()
        db.close()

        print(f"📇 Database Indexes:")
        current_table = None
        for idx in indexes:
            if idx.tablename != current_table:
                current_table = idx.tablename
                print(f"   📋 {current_table}:")

            index_type = "🔑 PRIMARY KEY" if "pkey" in idx.indexname else "📇 INDEX"
            unique_indicator = " (UNIQUE)" if "UNIQUE" in idx.indexdef else ""
            print(f"      {index_type} {idx.indexname}{unique_indicator}")

        return True

    except Exception as e:
        print(f"❌ Error checking indexes: {e}")
        return False


def check_sample_data():
    """Cek apakah ada sample data (dari seeding)"""
    try:
        db = SessionLocal()

        # Cek jumlah records di tabel utama
        tables_to_check = {
            "user": 'SELECT COUNT(*) FROM "user" WHERE deleted = false',
            "user_profile": "SELECT COUNT(*) FROM user_profile WHERE deleted = false",
        }

        print(f"📊 Sample Data:")
        all_have_data = True

        for table, query in tables_to_check.items():
            result = db.execute(text(query))
            count = result.fetchone()[0]

            if count > 0:
                print(f"   ✅ {table}: {count} records")
            else:
                print(f"   ⚠️  {table}: No data found")
                all_have_data = False

        db.close()
        return all_have_data

    except Exception as e:
        print(f"❌ Error checking sample data: {e}")
        return False


def check_migration_history():
    """Cek history migration di database"""
    try:
        db = SessionLocal()

        # Cek apakah tabel alembic_version ada
        result = db.execute(
            text(
                """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alembic_version'
            );
        """
            )
        )

        if not result.fetchone()[0]:
            print(
                "⚠️  Alembic version table not found - migrations may not have been applied"
            )
            db.close()
            return False

        # Cek current revision
        result = db.execute(text("SELECT version_num FROM alembic_version;"))
        current_revision = result.fetchone()

        db.close()

        if current_revision:
            print(f"📋 Migration Status:")
            print(f"   ✅ Current revision: {current_revision[0]}")
            return True
        else:
            print("⚠️  No migration revision found")
            return False

    except Exception as e:
        print(f"❌ Error checking migration history: {e}")
        return False


def run_validation():
    """Jalankan semua validasi"""
    print("🔍 Running database validation...")
    print("=" * 50)

    checks = [
        ("Database Connection", check_database_connection),
        ("Tables Existence", check_tables_exist),
        ("Foreign Keys", check_foreign_keys),
        ("Indexes", check_indexes),
        ("Migration History", check_migration_history),
        ("Sample Data", check_sample_data),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if check_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Validation Results: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All validations passed! Database is ready.")
        return True
    else:
        print("⚠️  Some validations failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
