# test_hash_db.py
import mysql.connector
from werkzeug.security import check_password_hash

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'proyecto_desarrollo_web',
}

email = "h@gmail.com"        # <- deja así
pw = "h"    # <- reemplaza esto localmente por la contraseña que crees correcta

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, email, password, CHAR_LENGTH(password) AS len FROM usuarios WHERE email = %s", (email,))
row = cursor.fetchone()
cursor.close()
conn.close()

print("ROW raw:", row)
if row:
    stored = row['password']
    print("repr(stored):", repr(stored))
    print("len stored:", row['len'])
    print("repr(pw):", repr(pw), "len pw:", len(pw))
    try:
        print("check_password_hash ->", check_password_hash(stored, pw))
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("No se encontró usuario con ese email.")
