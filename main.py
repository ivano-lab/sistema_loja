from utils import *
from utils.produto import Produto

while True:
    utils.print_linha()
    print("SISTEMA DE GESTÃO DE LOJA (MVP)")
    utils.print_linha()
    print("1 - Produtos")
    print("2 - Vendas")
    print("3 - Clientes")
    print("0 - Sair")
    print()
    opcao = input("Escolha: ")

    if opcao == "1":
        produto = Produto()
        produto.menu_produto()

    elif opcao == "2":
        print("Implementando Menu Vendas")

    elif opcao == "3":
        print("Implementando Menu Clientes")

    elif opcao == "0":
        print("Saindo do Sistema...")
        break

    else:
        print("X  Opção Inválida.")
