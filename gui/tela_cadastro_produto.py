import tkinter as tk
from tkinter import messagebox
import sqlite3
from navegacao import trocar_tela

class TelaCadastroProduto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()
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

        tk.Label(self, text="Cadastro de Produto", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Nome").pack()
        self.entry_nome_produto = tk.Entry(self)
        self.entry_nome_produto.pack()

        tk.Label(self, text="Código").pack()
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        tk.Label(self, text="Preço Compra").pack()
        self.entry_pc = tk.Entry(self)
        self.entry_pc.pack()

        tk.Label(self, text="Preço Venda").pack()
        self.entry_pv = tk.Entry(self)
        self.entry_pv.pack()

        tk.Label(self, text="Estoque").pack()
        self.entry_estoque = tk.Entry(self)
        self.entry_estoque.pack()

        tk.Button(self, text="Cadastrar", command=self.cadastrar_produto).pack(pady=10)

        tk.Button(self, text="Voltar",
                  command=self.voltar_tela_inicial).pack(pady=10)

    def voltar_tela_inicial(self):
        from tela_inicial_produto import TelaInicialProduto
        trocar_tela(self.master, TelaInicialProduto)

    def cadastrar_produto(self):
        nome_produto = self.entry_nome_produto.get()
        codigo = self.entry_codigo.get()
        pc = self.entry_pc.get()
        pv = self.entry_pv.get()
        estoque = self.entry_estoque.get()

        if not nome_produto or not codigo or not pc or not pv or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        try:
            self.cursor.execute("""
                INSERT INTO produtos (nome_produto, codigo, preco_compra, preco_venda, estoque)
                VALUES (?, ?, ?, ?, ?)
            """, (nome_produto, codigo, float(pc), float(pv), int(estoque)))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu: {e}")

    def limpar_campos(self):
        self.entry_nome_produto.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)
        self.entry_pc.delete(0, tk.END)
        self.entry_pv.delete(0, tk.END)
        self.entry_estoque.delete(0, tk.END)
