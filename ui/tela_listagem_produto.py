import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TelaListagemProdutos(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Conexão com o banco
        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()

        # Título
        tk.Label(self, text="Lista de Produtos", font=("Arial", 14, "bold")).pack(pady=10)

        # Treeview (Tabela)
        colunas = ("ID", "Nome", "Código", "Preço Compra", "Preço Venda", "Estoque")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=10)

        # Definindo cabeçalhos
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botão atualizar
        tk.Button(self, text="Atualizar Lista", command=self.carregar_produtos).pack(pady=5)

        # Carregar dados logo ao iniciar
        self.carregar_produtos()

    def carregar_produtos(self):
        # Limpa tabela antes de inserir novos dados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca os produtos no banco
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()

        if not produtos:
            messagebox.showinfo("Info", "Nenhum produto cadastrado ainda.")
        else:
            for p in produtos:
                self.tree.insert("", "end", values=p)
