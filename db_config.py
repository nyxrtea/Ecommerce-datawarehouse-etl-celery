# File: C:\Users\ANDRA ERLANGGA\OneDrive\Documents\Revalina\Datawerehouse\test_db.py
import psycopg2
from queries import DB_CONFIG

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Koneksi berhasil:", result)
    cursor.close()
    conn.close()
except Exception as e:
    print("Koneksi gagal:", str(e))