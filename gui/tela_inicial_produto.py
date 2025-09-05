import tkinter as tk
from navegacao import trocar_tela
from tela_cadastro_produto import TelaCadastroProduto
from tela_listagem_produto import TelaListagemProdutos

class TelaInicialProduto(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tk.Label(self, text="Módulo de Produtos", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Produto", width=25,
                  command=lambda: trocar_tela(self.master, TelaCadastroProduto)).pack(pady=5)

        tk.Button(self, text="Listar Produtos", width=25,
                  command=lambda: trocar_tela(self.master, TelaListagemProdutos)).pack(pady=5)

        tk.Button(self, text="Voltar",
                  command=self.voltar_tela_inicial).pack(pady=10)

    def voltar_tela_inicial(self):
        from tela_inicial import TelaInicial
        trocar_tela(self.master, TelaInicial)

        #tk.Button(self, text="Sair", width=25, command=self.master.quit).pack(pady=20)
