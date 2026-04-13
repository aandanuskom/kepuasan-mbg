import mysql.connector

def koneksi():
    return mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="iXENEWaVoTYsIMxgHKUwIyTHvoDzyXtI",
        database="railway",
        port=46288
    )
