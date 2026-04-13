import mysql.connector
import hashlib

def koneksi():
    return mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="iXENEWaVoTYsIMxgHKUwIyTHvoDzyXtI",
        database="railway",
        port=46288
    )

def init_database():
    db = koneksi()
    cursor = db.cursor()

    # ===================== ADMIN
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id_admin INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100),
        username VARCHAR(50),
        password VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== DATASET TRAINING
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_training (
        id_training INT AUTO_INCREMENT PRIMARY KEY,
        komentar TEXT,
        label ENUM('PUAS','NETRAL','TIDAK PUAS'),
        sumber VARCHAR(100),
        tanggal_upload DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== DATASET TESTING
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_testing (
        id_testing INT AUTO_INCREMENT PRIMARY KEY,
        komentar TEXT,
        label VARCHAR(20),
        tanggal_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== RESPONDEN
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responden (
        id_responden INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100),
        sekolah VARCHAR(100),
        kelas VARCHAR(50),
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== KOMENTAR
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS komentar (
        id_komentar INT AUTO_INCREMENT PRIMARY KEY,
        id_responden INT,
        isi_komentar TEXT,
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== HASIL SENTIMEN
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hasil_sentimen (
        id_hasil INT AUTO_INCREMENT PRIMARY KEY,
        id_komentar INT,
        hasil VARCHAR(20),
        confidence FLOAT,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== HASIL PREDIKSI
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hasil_prediksi (
        id_prediksi INT AUTO_INCREMENT PRIMARY KEY,
        komentar TEXT,
        hasil ENUM('PUAS','NETRAL','TIDAK PUAS'),
        confidence DECIMAL(5,2),
        tanggal DATETIME
    )
    """)

    # ===================== LOG TRAINING
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log_training (
        id_log INT AUTO_INCREMENT PRIMARY KEY,
        jumlah_data INT,
        akurasi DECIMAL(5,2),
        precision_score DECIMAL(5,2),
        recall_score DECIMAL(5,2),
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ===================== INSERT ADMIN SAJA
    cursor.execute("SELECT * FROM admin LIMIT 1")
    if cursor.fetchone() is None:
        pwd = hashlib.sha256("admin".encode()).hexdigest()

        cursor.execute("""
        INSERT INTO admin (nama, username, password)
        VALUES (%s, %s, %s)
        """, ("Administrator", "admin", pwd))

    db.commit()
    cursor.close()
    db.close()
