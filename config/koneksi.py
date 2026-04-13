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
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        if tables:
            print("✅ Database sudah ada")
            return

        with open("db_kepuasan.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        for statement in sql_script.split(";"):
            if statement.strip():
                cursor.execute(statement)

        db.commit()
        print("✅ Database berhasil diimport")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        cursor.close()
        db.close()
