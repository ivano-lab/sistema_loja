import sqlite3

conn = sqlite3.connect("loja.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(vendas);")
for coluna in cursor.fetchall():
    print(coluna)

conn.close()
