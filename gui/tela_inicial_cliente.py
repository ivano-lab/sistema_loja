import tkinter as tk

from gui.tela_listagem_clientes import TelaListagemCliente
from navegacao import trocar_tela
from tela_cadastro_cliente import TelaCadastroCliente

class TelaInicialCliente(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        tk.Label(self, text="Módulo de Clientes", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Button(self, text="Cadastrar Cliente", width=25,
                  command=lambda: trocar_tela(self.master, TelaCadastroCliente)).pack(pady=5)

        tk.Button(self, text="Listar Clientes", width=25,
                  command=lambda: trocar_tela(self.master, TelaListagemCliente)).pack(pady=5)

        tk.Button(self, text="Voltar",
                  command=self.voltar_tela_inicial).pack(pady=10)

    def voltar_tela_inicial(self):
        from tela_inicial import TelaInicial
        trocar_tela(self.master, TelaInicial)

        #tk.Button(self, text="Sair", width=25, command=self.master.quit).pack(pady=20)
