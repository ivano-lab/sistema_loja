import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TelaListagemProdutos2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Conexão com o banco
        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()

        tk.Label(self, text="Lista de Produtos", font=("Arial", 14, "bold")).pack(pady=10)

        colunas = ("ID", "Nome", "Código", "Preço Compra", "Preço Venda", "Estoque")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=10)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões de ação
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Editar Selecionado", command=self.editar_produto).grid(row=0, column=0, padx=5)
        tk.Button(frame_botoes, text="Excluir Selecionado", command=self.excluir_produto).grid(row=0, column=1, padx=5)
        tk.Button(frame_botoes, text="Atualizar Lista", command=self.carregar_produtos).grid(row=0, column=2, padx=5)

        self.carregar_produtos()

    def carregar_produtos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM produtos")
        for p in self.cursor.fetchall():
            self.tree.insert("", "end", values=p)

    def excluir_produto(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return

        produto = self.tree.item(item_selecionado)["values"]
        produto_id = produto[0]

        confirm = messagebox.askyesno("Confirmação", f"Deseja excluir o produto '{produto[1]}'?")
        if confirm:
            self.cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    def editar_produto(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return

        produto = self.tree.item(item_selecionado)["values"]
        produto_id, nome, codigo, preco_compra, preco_venda, estoque = produto

        # Abre janela de edição
        janela = tk.Toplevel(self)
        janela.title("Editar Produto")

        tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(janela)
        entry_nome.insert(0, nome)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(janela, text="Código:").grid(row=1, column=0, padx=5, pady=5)
        entry_codigo = tk.Entry(janela)
        entry_codigo.insert(0, codigo)
        entry_codigo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(janela, text="Preço Compra:").grid(row=2, column=0, padx=5, pady=5)
        entry_pc = tk.Entry(janela)
        entry_pc.insert(0, preco_compra)
        entry_pc.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(janela, text="Preço Venda:").grid(row=3, column=0, padx=5, pady=5)
        entry_pv = tk.Entry(janela)
        entry_pv.insert(0, preco_venda)
        entry_pv.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(janela, text="Estoque:").grid(row=4, column=0, padx=5, pady=5)
        entry_estoque = tk.Entry(janela)
        entry_estoque.insert(0, estoque)
        entry_estoque.grid(row=4, column=1, padx=5, pady=5)

        def salvar_edicao():
            novo_nome = entry_nome.get()
            novo_codigo = entry_codigo.get()
            novo_pc = float(entry_pc.get())
            novo_pv = float(entry_pv.get())
            novo_estoque = int(entry_estoque.get())

            self.cursor.execute("""
                UPDATE produtos
                SET nome_produto=?, codigo=?, preco_compra=?, preco_venda=?, estoque=?
                WHERE id=?
            """, (novo_nome, novo_codigo, novo_pc, novo_pv, novo_estoque, produto_id))
            self.conn.commit()
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            janela.destroy()

        tk.Button(janela, text="Salvar", command=salvar_edicao).grid(row=5, column=0, columnspan=2, pady=10)
