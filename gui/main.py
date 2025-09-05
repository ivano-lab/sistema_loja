import tkinter as tk
#from tela_inicial_produto import TelaInicialProduto
from tela_inicial import TelaInicial

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão Comercial - MVP")
    root.geometry("1000x800")

    #TelaInicialProduto(root).pack(fill="both", expand=True)

    TelaInicial(root).pack(fill="both", expand=True)

    root.mainloop()
