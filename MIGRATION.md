# Migration System Documentation

## Aksara AI Backend - Database Migrations

Sistem migration ini menggunakan Alembic untuk mengelola perubahan skema database PostgreSQL.

## Struktur Migration

```
migrations/
├── env.py                     # Konfigurasi environment Alembic
├── script.py.mako            # Template untuk file migration
└── versions/                 # Folder berisi file-file migration
    ├── 001_initial_migration.py
    └── 002_refresh_tokens.py
```

## Cara Menggunakan Migration

### Prerequisites

1. Pastikan PostgreSQL sudah running
2. Set environment variable `DATABASE_CONN` di file `.env`:
   ```
   DATABASE_CONN=postgresql://username:password@localhost:5432/database_name
   ```

### Commands

#### 1. Membuat Migration Baru
```bash
python migrate.py create "Deskripsi perubahan"
```

#### 2. Upgrade Database (Apply Migrations)
```bash
# Upgrade ke versi terbaru
python migrate.py upgrade

# Upgrade ke versi tertentu
python migrate.py upgrade <revision_id>
```

#### 3. Downgrade Database
```bash
python migrate.py downgrade <revision_id>
```

#### 4. Cek Status Migration
```bash
# Lihat revision saat ini
python migrate.py current

# Lihat history migration
python migrate.py history

# Lihat head revisions
python migrate.py heads
```

### Seed Database (Data Awal)

Setelah apply migration, jalankan seed untuk mengisi data awal:

```bash
python seed.py
```

Ini akan membuat:
- User admin dengan username "admin" dan password "admin123"

## Migration Files yang Tersedia

### 1. 001_initial_migration.py
- Membuat tabel `user` untuk data pengguna
- Membuat tabel `user_profile` untuk profil pengguna
- Menambahkan indexes dan foreign keys

### 2. 002_refresh_tokens.py
- Membuat tabel `refresh_tokens` untuk mengelola JWT refresh tokens
- Menambahkan relasi ke tabel `user`

## Model yang Tersedia

### User Models (`src/user/models.py`)
- `User`: Model untuk pengguna sistem
- `UserProfile`: Model untuk profil pengguna

### Refresh Token Models (`src/refresh_token/models.py`)
- `RefreshToken`: Model untuk JWT refresh tokens

## Menambahkan Model Baru

1. Buat model baru di file yang sesuai (misalnya `src/new_module/models.py`)
2. Import model di `migrations/env.py`
3. Buat migration baru:
   ```bash
   python migrate.py create "Add new table"
   ```
4. Review dan edit file migration yang dihasilkan
5. Apply migration:
   ```bash
   python migrate.py upgrade
   ```

## Best Practices

### 1. Penamaan Migration
- Gunakan nama yang deskriptif
- Format: "Action - Description"
- Contoh: "Add user email verification table"

### 2. Rollback Strategy
- Selalu implementasikan fungsi `downgrade()`
- Test rollback sebelum deploy ke production
- Backup database sebelum migration besar

### 3. Data Migration
- Untuk migration data, buat script terpisah
- Jangan lupa handle edge cases
- Test dengan data production (anonymized)

### 4. Index Management
- Tambahkan index untuk kolom yang sering di-query
- Pertimbangkan performance impact
- Monitor query performance setelah migration

## Troubleshooting

### Error: "Module not found"
Pastikan semua dependencies terinstall:
```bash
pip install -r requirements.txt
```

### Error: "Database connection failed"
Periksa:
1. PostgreSQL service running
2. Environment variable `DATABASE_CONN` benar
3. Credentials dan permission database

### Error: "Migration conflict"
1. Cek history migration: `python migrate.py history`
2. Resolve conflict secara manual
3. Merge branches jika diperlukan

## Environment Variables

Pastikan file `.env` berisi konfigurasi berikut:

```env
# Database Configuration
DATABASE_CONN=postgresql://username:password@localhost:5432/database_name

# Environment
ENVIRONMENT=dev

# JWT Settings
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
```

## Production Deployment

### 1. Backup Database
```bash
pg_dump -h hostname -U username database_name > backup.sql
```

### 2. Apply Migrations
```bash
python migrate.py upgrade
```

### 3. Verify Migration
```bash
python migrate.py current
```

### 4. Test Application
Pastikan aplikasi berfungsi normal setelah migration.

## Monitoring

Setelah apply migration:

1. **Check Database Size**
   ```sql
   SELECT pg_size_pretty(pg_database_size('database_name'));
   ```

2. **Check Table Sizes**
   ```sql
   SELECT schemaname,tablename,attname,n_distinct,correlation
   FROM pg_stats WHERE tablename = 'table_name';
   ```

3. **Monitor Performance**
   - Check slow query logs
   - Monitor application response time
   - Watch database connections

## Support

Jika mengalami masalah dengan migration system:
1. Check logs aplikasi
2. Verify database connection
3. Review migration files
4. Contact development team
