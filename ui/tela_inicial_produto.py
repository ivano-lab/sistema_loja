import tkinter as tk
from tkinter import ttk, messagebox
from tela_cadastro_produto import TelaCadastroProduto
from tela_listagem_produto import TelaListagemProdutos
from tela_listagem_produtoV2 import TelaListagemProdutos2

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Módulo de Produtos")
        self.geometry("1000x800")
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

        ttk.Label(self.container, text="Módulo de Produtos", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.container, text="Listar Produtos", command=self.tela_listagem_produtos).pack(pady=10)
        ttk.Button(self.container, text="Cadastrar Produtos", command=self.tela_cadastro_produtos).pack(pady=10)
        #ttk.Button(self.container, text="Editar Produtos", command=self.tela_edicao_produtos).pack(pady=10)
        #ttk.Button(self.container, text="Excluir Produtos", command=self.tela_exclusao_produtos).pack(pady=10)

    def tela_listagem_produtos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame_listagem = TelaListagemProdutos2(self.container)
        frame_listagem.pack(fill="both", expand=True)

    def tela_cadastro_produtos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        frame_cadastro = TelaCadastroProduto(self.container)
        frame_cadastro.pack(fill="both", expand=True)

    def tela_edicao_produtos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Edição de Produtos", font=("Arial", 14)).pack(pady=20)

    def tela_exclusao_produtos(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        ttk.Label(self.container, text="Exclusão de Produtos", font=("Arial", 14)).pack(pady=20)

    def _mensagem(self, texto):
        self.status.set(texto)

    def _sobre(self):
        messagebox.showinfo("Sobre", "Este é um MVP de um sistema de gestão de loja. O projeto ainda está em fase de implementação, por isso algumas funcionalidades podem não estar disponíveis ou podem sofrer alterações nas próximas versões.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
