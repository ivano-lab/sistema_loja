import os
import sqlite3
import utils
from datetime import datetime

class Venda:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.abspath(os.path.join(base_dir, '..', 'loja.db'))

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

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
                self.relatorio_vendas()
            elif opcao == "2":
                self.nova_venda()
            elif opcao == "3":
                pass
            elif opcao == "4":
                pass
            elif opcao == "0":
                print("Saindo do módulo de Clientes...")
                break
            else:
                print("X Opção inválida.")

    def relatorio_vendas(self):
        while True:
            utils.print_linha()
            print("RELATÓRIO DE VENDAS")
            utils.print_linha()
            self.cursor.execute("SELECT * FROM vendas")
            vendas = self.cursor.fetchall()
            if not vendas:
                print("Nenhuma venda cadastrada.")
            else:
                for venda in vendas:
                    print(f"ID: {venda[0]}, ID Cliente: {venda[1]}, DATA VENDA: {venda[2]}, "
                          f"FORMA PAGAMENTO: {venda[3]}, VALOR TOTAL: {venda[4]}")

                    utils.underline()
            print("Opções:")
            print("1 - Ver relatório detalhado de uma venda")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "0":
                print("Saindo do módulo de Relatório...")
                break
            elif opcao == "1":
                id_venda = input("Digite o ID da venda para ver detalhes: ")
                if id_venda.isdigit():
                    from utils.relatorio import Relatorio
                    relatorio = Relatorio(self.db_path)
                    relatorio.relatorio_detalhado(int(id_venda))
                else:
                    print("ID inválido!")
            else:
                print("Opção inválida.")

    def nova_venda(self):
        utils.print_linha()
        print("Nova Venda")
        utils.print_linha()

        # Seleciona cliente
        self.cursor.execute("SELECT id, nome FROM clientes")
        clientes = self.cursor.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado. Cadastre um cliente antes.")
            return

        for c in clientes:
            print(f"{c[0]} - {c[1]}")
        cliente_id = int(input("Digite o ID do cliente: "))

        # Forma de pagamento
        forma_pagamento = input("Forma de pagamento (Dinheiro/Cartão/Pix): ")

        itens = []
        total = 0

        while True:
            # Seleciona produto
            self.cursor.execute("SELECT id, nome_produto, preco_venda, estoque FROM produtos")
            produtos = self.cursor.fetchall()
            if not produtos:
                print("Nenhum produto cadastrado.")
                return

            for p in produtos:
                print(f"{p[0]} - {p[1]} | Preço: {utils.formatar_moeda(p[2])} | Estoque: {p[3]}")
            produto_id = int(input("Digite o ID do produto (0 para finalizar): "))
            if produto_id == 0:
                break

            quantidade = int(input("Quantidade: "))
            self.cursor.execute("SELECT nome_produto, preco_venda, estoque FROM produtos WHERE id=?", (produto_id,))
            produto = self.cursor.fetchone()

            if not produto:
                print("Produto inválido.")
                continue

            nome, preco, estoque = produto
            if quantidade > estoque:
                print("Estoque insuficiente!")
                continue

            subtotal = preco * quantidade
            itens.append((produto_id, quantidade, preco, subtotal))
            total += subtotal

            # Atualiza estoque
            novo_estoque = estoque - quantidade
            self.cursor.execute("UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, produto_id))
            self.conn.commit()

            print(f"Adicionado {quantidade}x {nome} - Subtotal: {utils.formatar_moeda(subtotal)}")

        if not itens:
            print("Venda cancelada (nenhum item adicionado).")
            return

        # Salva a venda
        data_venda = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO vendas (cliente_id, data, forma_pagamento, valor_total) VALUES (?, ?, ?, ?)",
            (cliente_id, data_venda, forma_pagamento, total)
        )
        venda_id = self.cursor.lastrowid

        for produto_id, quantidade, preco, subtotal in itens:
            self.cursor.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (venda_id, produto_id, quantidade, preco, subtotal))

        self.conn.commit()
        print(f"Venda registrada com sucesso! Total: {utils.formatar_moeda(total)}")

    def __del__(self):
        self.conn.close()
