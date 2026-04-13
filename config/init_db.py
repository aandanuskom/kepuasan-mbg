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
    db = koneksi()
    cursor = db.cursor()

    try:
        # =====================
        # CEK DATABASE SUDAH ADA
        # =====================
        cursor.execute("SHOW TABLES LIKE 'admin'")
        result = cursor.fetchone()

        if result:
            print("✅ Database sudah ada, skip import")
            return

        print("🚀 Import database dimulai...")

        # =====================
        # BACA FILE SQL
        # =====================
        with open("db_kepuasan.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        # =====================
        # NONAKTIFKAN FOREIGN KEY
        # =====================
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # =====================
        # FILTER QUERY BERBAHAYA
        # =====================
        statements = []

        for line in sql_script.splitlines():

            # skip komentar & baris kosong
            if line.strip().startswith("--") or line.strip() == "":
                continue

            # skip command yang bikin error
            if "START TRANSACTION" in line:
                continue
            if "COMMIT" in line:
                continue
            if "/*!40101" in line:
                continue

            statements.append(line)

        # gabungkan kembali
        final_sql = "\n".join(statements)

        # eksekusi query
        for statement in final_sql.split(";"):
            if statement.strip():
                cursor.execute(statement)

        # =====================
        # AKTIFKAN KEMBALI FK
        # =====================
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        db.commit()

        print("✅ Database berhasil diimport otomatis")

    except Exception as e:
        print("❌ Error import:", e)

    finally:
        cursor.close()
        db.close()