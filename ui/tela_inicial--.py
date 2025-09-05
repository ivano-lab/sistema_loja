import tkinter as tk
from tkinter import ttk

class SistemaVendas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas - Menu Principal")
        self.root.geometry("400x300")

        titulo = ttk.Label(root, text="Menu Principal", font=("Arial", 16))
        titulo.pack(pady=20)

        # Botões para módulos
        ttk.Button(root, text="Vendas", command=self.abrir_vendas).pack(pady=5)
        ttk.Button(root, text="Produtos", command=self.abrir_produtos).pack(pady=5)
        ttk.Button(root, text="Clientes", command=self.abrir_clientes).pack(pady=5)
        ttk.Button(root, text="Relatórios", command=self.abrir_relatorios).pack(pady=5)
        ttk.Button(root, text="Sair", command=root.quit).pack(pady=20)

    def abrir_vendas(self):
        self.nova_janela("Módulo de Vendas")

    def abrir_produtos(self):
        self.nova_janela("Módulo de Produtos")

    def abrir_clientes(self):
        self.nova_janela("Módulo de Clientes")

    def abrir_relatorios(self):
        self.nova_janela("Módulo de Relatórios")

    def nova_janela(self, titulo):
        janela = tk.Toplevel(self.root)
        janela.title(titulo)
        janela.geometry("400x300")
        ttk.Label(janela, text=titulo, font=("Arial", 14)).pack(pady=20)
        ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVendas(root)
    root.mainloop()
