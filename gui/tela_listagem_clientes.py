import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from navegacao import trocar_tela
from tela_inicial_produto import TelaInicialProduto


class TelaListagemCliente(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()

        tk.Label(self, text="Listagem de Clientes", font=("Arial", 14, "bold")).pack(pady=10)

        # Treeview para exibir clientes
        colunas = ("id", "nome", "tipo_cliente", "cpf", "cnpj", "data_nascimento")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")

        # Cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo_cliente", text="Tipo")
        self.tree.heading("cpf", text="CPF")
        self.tree.heading("cnpj", text="CNPJ")
        self.tree.heading("data_nascimento", text="Data Nasc.")

        # Ajuste de largura
        self.tree.column("id", width=40)
        self.tree.column("nome", width=150)
        self.tree.column("tipo_cliente", width=60)
        self.tree.column("cpf", width=100)
        self.tree.column("cnpj", width=120)
        self.tree.column("data_nascimento", width=100)

        self.tree.pack(pady=10, fill="both", expand=True)

        # Botões de ação
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Editar", command=self.editar_cliente).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.excluir_cliente).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Voltar", command=self.voltar_tela_inicial).grid(row=0, column=2, padx=5)

        # Carrega clientes no início
        self.carregar_clientes()

    def carregar_clientes(self):
        """Carrega clientes do banco no Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM clientes")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def excluir_cliente(self):
        """Exclui cliente selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return

        item = self.tree.item(selecionado)
        cliente_id = item["values"][0]

        confirmar = messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?")
        if confirmar:
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            self.conn.commit()
            self.carregar_clientes()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")


    def editar_cliente(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return

        cliente = self.tree.item(selecionado)["values"]
        cliente_id, nome, tipo_cliente, cpf, cnpj, data_nasc = cliente

        # Abre janela de edição
        janela = tk.Toplevel(self)
        janela.title("Editar Cliente")

        tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(janela)
        entry_nome.insert(0, nome)
        entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(janela, text="Tipo de Cliente:").grid(row=1, column=0, padx=5, pady=5)
        combo_tipo = ttk.Combobox(janela, values=["PF", "PJ"], state="readonly")
        combo_tipo.set(tipo_cliente)
        combo_tipo.grid(row=1, column=1, padx=5, pady=5)

        # CPF e CNPJ (serão mostrados condicionalmente)
        label_cpf = tk.Label(janela, text="CPF:")
        entry_cpf = tk.Entry(janela)
        if cpf:
            entry_cpf.insert(0, cpf)

        label_cnpj = tk.Label(janela, text="CNPJ:")
        entry_cnpj = tk.Entry(janela)
        if cnpj:
            entry_cnpj.insert(0, cnpj)

        tk.Label(janela, text="Data de Nascimento:").grid(row=4, column=0, padx=5, pady=5)
        entry_data_nasc = tk.Entry(janela)
        if data_nasc:
            entry_data_nasc.insert(0, data_nasc)
        entry_data_nasc.grid(row=4, column=1, padx=5, pady=5)

        # Função para atualizar campos dinamicamente
        def atualizar_campos(event=None):
            label_cpf.grid_forget()
            entry_cpf.grid_forget()
            label_cnpj.grid_forget()
            entry_cnpj.grid_forget()

            if combo_tipo.get() == "PF":
                label_cpf.grid(row=2, column=0, padx=5, pady=5)
                entry_cpf.grid(row=2, column=1, padx=5, pady=5)
            else:
                label_cnpj.grid(row=3, column=0, padx=5, pady=5)
                entry_cnpj.grid(row=3, column=1, padx=5, pady=5)

        combo_tipo.bind("<<ComboboxSelected>>", atualizar_campos)
        atualizar_campos()  # mostra o campo correto na abertura

        def salvar_edicao():
            novo_nome = entry_nome.get()
            novo_tipo = combo_tipo.get()
            novo_cpf = entry_cpf.get() if novo_tipo == "PF" else None
            novo_cnpj = entry_cnpj.get() if novo_tipo == "PJ" else None
            nova_data = entry_data_nasc.get()

            if not novo_nome or not novo_tipo or (novo_tipo == "PF" and not novo_cpf) or (
                    novo_tipo == "PJ" and not novo_cnpj):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return

            self.cursor.execute("""
                UPDATE clientes
                SET nome=?, tipo_cliente=?, cpf=?, cnpj=?, data_nascimento=?
                WHERE id=?
            """, (novo_nome, novo_tipo, novo_cpf, novo_cnpj, nova_data, cliente_id))
            self.conn.commit()
            self.carregar_clientes()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            janela.destroy()

        tk.Button(janela, text="Salvar", command=salvar_edicao).grid(row=5, column=0, columnspan=2, pady=10)

    def voltar_tela_inicial(self):
            trocar_tela(self.master, TelaInicialProduto)
