from utils import *
from utils.produto import Produto
from utils.cliente import Cliente
from utils.venda import Venda


while True:
    utils.print_linha()
    print("SISTEMA DE GESTÃO DE LOJA (MVP)")
    utils.print_linha()
    print("1 - Produtos")
    print("2 - Vendas")
    print("3 - Clientes")
    print("0 - Sair")
    print("9 - Resetar banco")
    print()
    opcao = input("Escolha: ")

    if opcao == "1":
        produto = Produto()
        produto.menu_produto()

    elif opcao == "2":
        venda = Venda()
        venda.menu_venda()

    elif opcao == "3":
        cliente = Cliente()
        cliente.menu_cliente()

    elif opcao == "0":
        print("Saindo do Sistema...")
        break
    elif opcao =="9":
        print("Resetando Banco")
        utils.reseta_banco()
        break

    else:
        print("X  Opção Inválida.")
