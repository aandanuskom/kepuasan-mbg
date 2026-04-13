import mysql.connector

def koneksi():
    return mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="iXENEWaVoTYsIMxgHKUwIyTHvoDzyXtI",
        database="railway",
        port=46288
    )

def init_database():
    conn = koneksi()
    cursor = conn.cursor()

    # =====================
    # TABEL ADMIN
    # =====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id_admin INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50),
        password VARCHAR(255)
    )
    """)

    # =====================
    # TABEL RESPONDEN
    # =====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responden (
        id_responden INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100),
        kelas VARCHAR(20),
        jenis_kelamin VARCHAR(20),
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================
    # TABEL KOMENTAR
    # =====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS komentar (
        id_komentar INT AUTO_INCREMENT PRIMARY KEY,
        id_responden INT,
        isi_komentar TEXT,
        tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================
    # TABEL HASIL SENTIMEN
    # =====================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hasil_sentimen (
        id_hasil INT AUTO_INCREMENT PRIMARY KEY,
        id_komentar INT UNIQUE,
        hasil VARCHAR(20),
        confidence FLOAT
    )
    """)

    # =====================
    # TABEL LOG TRAINING
    # =====================
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

    # =====================
    # INSERT ADMIN DEFAULT
    # =====================
    cursor.execute("SELECT * FROM admin LIMIT 1")
    if cursor.fetchone() is None:
        import hashlib
        password = hashlib.sha256("admin123".encode()).hexdigest()

        cursor.execute("""
        INSERT INTO admin (username, password)
        VALUES (%s, %s)
        """, ("admin", password))

    conn.commit()
    cursor.close()
    conn.close()
