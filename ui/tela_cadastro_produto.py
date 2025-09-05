# tela_cadastro_produto.py
import tkinter as tk
from tkinter import messagebox
from navecacao import trocar_tela
import sqlite3

class TelaCadastroProduto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()

        # Garantir tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT NOT NULL,
                codigo TEXT NOT NULL UNIQUE,
                preco_compra REAL NOT NULL,
                preco_venda REAL NOT NULL,
                estoque INTEGER NOT NULL
            )
        """)
        self.conn.commit()

        # Interface
        tk.Label(self, text="Nome do Produto*").pack()
        self.entry_nome_produto = tk.Entry(self)
        self.entry_nome_produto.pack()

        tk.Label(self, text="Código*").pack()
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        tk.Label(self, text="Preço de Compra*").pack()
        self.entry_preco_compra = tk.Entry(self)
        self.entry_preco_compra.pack()

        tk.Label(self, text="Preço de Venda*").pack()
        self.entry_preco_venda = tk.Entry(self)
        self.entry_preco_venda.pack()

        tk.Label(self, text="Quantidade em Estoque*").pack()
        self.entry_estoque = tk.Entry(self)
        self.entry_estoque.pack()

        tk.Button(self, text="Cadastrar Produto", command=self.cadastrar_produto).pack(pady=10)

        tk.Button(self, text="Voltar",
                  command=lambda: trocar_tela(self.master, TelaInicialProduto)).pack(pady=10)

    def cadastrar_produto(self):
        nome_produto = self.entry_nome_produto.get()
        codigo = self.entry_codigo.get()
        preco_compra = self.entry_preco_compra.get()
        preco_venda = self.entry_preco_venda.get()
        estoque = self.entry_estoque.get()

        if not nome_produto or not preco_compra or not preco_venda or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        try:
            self.cursor.execute("""
                INSERT INTO produtos (nome_produto, codigo, preco_compra, preco_venda, estoque)
                VALUES (?, ?, ?, ?, ?)
            """, (nome_produto, codigo, float(preco_compra), float(preco_venda), int(estoque)))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def limpar_campos(self):
        self.entry_nome_produto.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)
        self.entry_preco_compra.delete(0, tk.END)
        self.entry_preco_venda.delete(0, tk.END)
        self.entry_estoque.delete(0, tk.END)
