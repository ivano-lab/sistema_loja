import sqlite3

conn = sqlite3.connect('loja.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        data_nascimento TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        preco_compra REAL NOT NULL,
        preco_venda REAL NOT NULL,
        estoque INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
    )
""")

cursor.execute("""
    CREATE TABLE itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        valor_total REAL NOT NULL,
        FOREIGN KEY (venda_id) REFERENCES vendas (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
""")

conn.commit()
conn.close()
