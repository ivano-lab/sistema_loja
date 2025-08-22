import os
import sqlite3
import utils

class Venda:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.abspath(os.path.join(base_dir, '..', 'loja.db'))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def nova_venda(self):
        pass

    def menu_venda(self):
        while True:
            utils.print_linha()
            print("MÓDULO DE VENDAS")
            utils.print_linha()
            print("1 - Listar vendas")
            print("2 - Efetuar venda")
            print("3 - Atualizar venda")
            print("4 - Deletar venda")
            print("0 - Voltar")
            print()
            opcao = input("Escolha: ")

            if opcao == "1":
                pass
            elif opcao == "2":
                pass
            elif opcao == "3":
                pass
            elif opcao == "4":
                pass
            elif opcao == "0":
                print("Saindo do módulo de Clientes...")
                break
            else:
                print("X Opção inválida.")

