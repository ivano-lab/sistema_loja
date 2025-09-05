import sqlite3

conn = sqlite3.connect('loja.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo_cliente TEXT CHECK(tipo_cliente IN ('PF', 'PJ')) NOT NULL,
    cpf TEXT,
    cnpj TEXT,
    data_nascimento TEXT,
    CHECK (
        (tipo_cliente = 'PF' AND cpf IS NOT NULL AND cnpj IS NULL) OR
        (tipo_cliente = 'PJ' AND cnpj IS NOT NULL AND cpf IS NULL)
        )
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        preco_compra REAL NOT NULL,
        preco_venda REAL NOT NULL,
        estoque INTEGER NOT NULL
    )
""")

cursor.execute("""
   CREATE TABLE IF NOT EXISTS vendas (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       cliente_id INTEGER NOT NULL,
       data TEXT NOT NULL,
       forma_pagamento TEXT NOT NULL CHECK(forma_pagamento IN ('Dinheiro', 'Cartão', 'Pix')),
       valor_total REAL NOT NULL,
       FOREIGN KEY (cliente_id) REFERENCES clientes(id)
   );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (venda_id) REFERENCES vendas(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
""")

conn.commit()
conn.close()
