import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Vendas 0.1.0 - Menu Principal")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Menu superior
        self._criar_menu()

        # Frame principal (conteúdo dinâmico)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Status bar
        self.status = tk.StringVar()
        self.status.set("Pronto")
        self.status_bar = ttk.Label(self, textvariable=self.status, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # Exibe a tela inicial
        self.mostrar_tela_inicial()

    def _criar_menu(self):
        menubar = tk.Menu(self)

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menu_arquivo.add_command(label="Novo", command=lambda: self._mensagem("Novo arquivo"))
        menu_arquivo.add_command(label="Abrir", command=lambda: self._mensagem("Abrir arquivo"))
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self._sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def mostrar_tela_inicial(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Bem-vindo ao sistema!", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.container, text="Vendas", command=self.tela_vendas).pack(pady=10)
        ttk.Button(self.container, text="Produtos", command=self.tela_produtos).pack(pady=10)
        ttk.Button(self.container, text="Clientes", command=self.tela_clientes).pack(pady=10)
        ttk.Button(self.container, text="Relatórios", command=self.tela_relatorios).pack(pady=10)

    def tela_vendas(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Vendas", font=("Arial", 14)).pack(pady=20)

    def tela_produtos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Produtos", font=("Arial", 14)).pack(pady=20)

    def tela_clientes(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Clientes", font=("Arial", 14)).pack(pady=20)

    def tela_relatorios(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Relatórios", font=("Arial", 14)).pack(pady=20)

    def _mensagem(self, texto):
        self.status.set(texto)

    def _sobre(self):
        messagebox.showinfo("Sobre", "Este é um MVP de um sistema de gestão de loja. O projeto ainda está em fase de implementação, por isso algumas funcionalidades podem não estar disponíveis ou podem sofrer alterações nas próximas versões.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
