import tkinter as tk
from tkinter import messagebox
import sqlite3


# --- Configuração inicial do banco ---
def inicializar_banco():
    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# --- Função para salvar no banco ---
def salvar_produto():
    nome = entry_nome.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()

    if not nome or not preco or not quantidade:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    try:
        preco = float(preco)
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser número decimal e quantidade um inteiro.")
        return

    conn = sqlite3.connect("loja.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
                   (nome, preco, quantidade))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)


# --- Interface Tkinter ---
inicializar_banco()
root = tk.Tk()
root.title("Cadastro de Produtos - MVP")
root.geometry("400x250")

# Labels e Entrys
tk.Label(root, text="Nome do Produto:").pack(pady=5)
entry_nome = tk.Entry(root, width=40)
entry_nome.pack()

tk.Label(root, text="Preço (R$):").pack(pady=5)
entry_preco = tk.Entry(root, width=40)
entry_preco.pack()

tk.Label(root, text="Quantidade:").pack(pady=5)
entry_quantidade = tk.Entry(root, width=40)
entry_quantidade.pack()

# Botão salvar
tk.Button(root, text="Salvar Produto", command=salvar_produto, bg="green", fg="white").pack(pady=15)

root.mainloop()
