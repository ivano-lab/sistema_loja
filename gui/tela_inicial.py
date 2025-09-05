import tkinter as tk
from navegacao import trocar_tela
#from tela_cadastro_produto import TelaCadastroProduto
#from tela_listagem_produto import TelaListagemProdutos
from tela_inicial_produto import TelaInicialProduto
from tela_inicial_venda import TelaInicialVenda
from tela_inicial_cliente import TelaInicialCliente

class TelaInicial(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tk.Label(self, text="Bem-vindo ao Sistema!", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Módulo de Vendas", width=25,
                  command=lambda: trocar_tela(self.master, TelaInicialVenda)).pack(pady=5)

        tk.Button(self, text="Módulo de Produtos", width=25,
                  command=lambda: trocar_tela(self.master, TelaInicialProduto)).pack(pady=5)

        tk.Button(self, text="Módulo de Clientes", width=25,
                  command=lambda: trocar_tela(self.master, TelaInicialCliente)).pack(pady=5)

        tk.Button(self, text="Sair", width=25, command=self.master.quit).pack(pady=20)
