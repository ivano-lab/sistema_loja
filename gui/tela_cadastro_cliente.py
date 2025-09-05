import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from navegacao import trocar_tela

class TelaCadastroCliente(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Conexão com o banco
        self.conn = sqlite3.connect("loja.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
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
        self.conn.commit()

        # --- Título ---
        tk.Label(self, text="Cadastro de Cliente", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Frame para campos de entrada ---
        self.frame_campos = tk.Frame(self)
        self.frame_campos.pack(pady=10)

        # Nome
        tk.Label(self.frame_campos, text="Nome").pack()
        self.entry_nome = tk.Entry(self.frame_campos)
        self.entry_nome.pack()

        # Tipo de cliente
        tk.Label(self.frame_campos, text="Tipo de Cliente").pack()
        self.tipo_cliente = ttk.Combobox(self.frame_campos, values=["PF", "PJ"], state="readonly")
        self.tipo_cliente.current(0)  # padrão PF
        self.tipo_cliente.pack()
        self.tipo_cliente.bind("<<ComboboxSelected>>", self.atualizar_campos)

        # CPF
        self.label_cpf = tk.Label(self.frame_campos, text="CPF")
        self.entry_cpf = tk.Entry(self.frame_campos)
        self.entry_cpf.bind("<KeyRelease>", self.aplicar_mascara_cpf)

        # CNPJ
        self.label_cnpj = tk.Label(self.frame_campos, text="CNPJ")
        self.entry_cnpj = tk.Entry(self.frame_campos)
        self.entry_cnpj.bind("<KeyRelease>", self.aplicar_mascara_cnpj)

        # Data de nascimento (sempre fica depois de CPF/CNPJ)
        self.label_data = tk.Label(self.frame_campos, text="Data de Nascimento")
        self.label_data.pack()
        self.entry_data_nasc = tk.Entry(self.frame_campos)
        self.entry_data_nasc.bind("<KeyRelease>", self.aplicar_mascara_data)
        self.entry_data_nasc.pack()

        # --- Botões ---
        tk.Button(self, text="Cadastrar", command=self.cadastrar_cliente).pack(pady=10)
        tk.Button(self, text="Voltar", command=self.voltar_tela_inicial).pack(pady=10)

        # Exibe inicialmente campo CPF
        self.atualizar_campos()

    def atualizar_campos(self, event=None):
        """Mostra CPF se PF, CNPJ se PJ (logo acima da Data de Nascimento)"""
        self.label_cpf.pack_forget()
        self.entry_cpf.pack_forget()
        self.label_cnpj.pack_forget()
        self.entry_cnpj.pack_forget()

        if self.tipo_cliente.get() == "PF":
            self.label_cpf.pack(before=self.label_data)
            self.entry_cpf.pack(before=self.label_data)
        else:
            self.label_cnpj.pack(before=self.label_data)
            self.entry_cnpj.pack(before=self.label_data)

    def aplicar_mascara_cpf(self, event):
        texto = self.entry_cpf.get()
        # Remove tudo que não for dígito
        texto = "".join(filter(str.isdigit, texto))[:11]  # limita a 11 dígitos
        formatado = ""

        if len(texto) > 0:
            formatado = texto[:3]
        if len(texto) > 3:
            formatado += "." + texto[3:6]
        if len(texto) > 6:
            formatado += "." + texto[6:9]
        if len(texto) > 9:
            formatado += "-" + texto[9:11]

        # Evita loop de eventos apagando/reinserindo
        self.entry_cpf.delete(0, tk.END)
        self.entry_cpf.insert(0, formatado)

    def aplicar_mascara_cnpj(self, event):
        texto = self.entry_cnpj.get()
        texto = "".join(filter(str.isdigit, texto))[:14]  # limita a 14 dígitos
        formatado = ""

        if len(texto) > 0:
            formatado = texto[:2]
        if len(texto) > 2:
            formatado += "." + texto[2:5]
        if len(texto) > 5:
            formatado += "." + texto[5:8]
        if len(texto) > 8:
            formatado += "/" + texto[8:12]
        if len(texto) > 12:
            formatado += "-" + texto[12:14]

        self.entry_cnpj.delete(0, tk.END)
        self.entry_cnpj.insert(0, formatado)

    def aplicar_mascara_data(self, event):
        texto = self.entry_data_nasc.get()
        texto = "".join(filter(str.isdigit, texto))[:8]  # apenas números, máximo 8 dígitos (ddmmyyyy)

        formatado = ""
        if len(texto) > 0:
            formatado = texto[:2]  # dd
        if len(texto) > 2:
            formatado += "/" + texto[2:4]  # /mm
        if len(texto) > 4:
            formatado += "/" + texto[4:8]  # /aaaa

        # Atualiza o campo com o texto formatado
        self.entry_data_nasc.delete(0, tk.END)
        self.entry_data_nasc.insert(0, formatado)

    def cadastrar_cliente(self):
        nome = self.entry_nome.get()
        tipo = self.tipo_cliente.get()
        cpf = self.entry_cpf.get() if tipo == "PF" else None
        cnpj = self.entry_cnpj.get() if tipo == "PJ" else None
        data_nasc = self.entry_data_nasc.get()


        # Validação básica
        if not nome or not tipo or (tipo == "PF" and not cpf) or (tipo == "PJ" and not cnpj):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        try:
            self.cursor.execute("""
                INSERT INTO clientes (nome, tipo_cliente, cpf, cnpj, data_nascimento)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, tipo, cpf, cnpj, data_nasc))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu: {e}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_cnpj.delete(0, tk.END)
        self.entry_data_nasc.delete(0, tk.END)
        self.tipo_cliente.current(0)
        self.atualizar_campos()

    def voltar_tela_inicial(self):
        from tela_inicial_cliente import TelaInicialCliente
        trocar_tela(self.master, TelaInicialCliente)
