import os
import sqlite3
import utils

class Produto:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.abspath(os.path.join(base_dir, '..', 'loja.db'))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def menu_produto(self):
        while True:
            utils.print_linha()
            print("MÓDULO DE PRODUTOS")
            utils.print_linha()
            print("1 - Listar produtos")
            print("2 - Cadastrar produto")
            print("3 - Atualizar produto")
            print("4 - Deletar produto")
            print("0 - Voltar")
            print()
            opcao = input("Escolha: ")

            if opcao == "1":
                self.listar_produto()
            elif opcao == "2":
                self.cadastrar_produto()
            elif opcao == "3":
                self.atualizar_produto()
            elif opcao == "4":
                self.deletar_produto()
            elif opcao == "0":
                print("Saindo do módulo de Produtos...")
                break
            else:
                print("X Opção inválida.")

    def cadastrar_produto(self):
        nome_produto = input("Nome do produto: ")
        codigo = input("Código do produto: ")
        preco_compra = utils.validar_preco("Preço de compra R$: ")
        preco_venda = utils.validar_preco("Preço de venda R$: ")
        quantidade = utils.validar_quantidade()

        self.cursor.execute(
            "INSERT INTO produtos (nome_produto, codigo, preco_compra, preco_venda, estoque) VALUES (?, ?, ?, ?, ?)",
            (nome_produto, codigo, preco_compra, preco_venda, quantidade)
        )
        self.conn.commit()
        print()
        print("Produto cadastrado com sucesso!")

    def listar_produto(self):
        utils.print_linha()
        print("LISTAGEM DE PRODUTOS")
        utils.print_linha()
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()
        if not produtos:
            print("Nenhum produto cadastrado.")
        else:
            for p in produtos:
                print(f"Nome: {p[1]} | Código: {p[2]} | Preço de compra: {utils.formatar_moeda(p[3])} | Preço de venda: {utils.formatar_moeda(p[4])} | Quantidade em estoque: {p[5]}")
                print()

    def deletar_produto(self):
        id_delecao = input("Digite o ID do produto a ser deletado: ")
        self.cursor.execute("DELETE FROM produtos WHERE id = ?", (id_delecao,))
        if self.cursor.rowcount == 0:
            print("Nenhum produto encontrado com este ID.")
        else:
            self.conn.commit()
            print("Produto deletado com sucesso!")

    def atualizar_produto(self):
        id_atualizacao = input("Digite o ID do produto a ser atualizado: ")
        self.cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_atualizacao,))
        produto = self.cursor.fetchone()

        if not produto:
            print("Nenhum produto encontrado com este ID.")
        else:
            self.conn.commit()
            print(f"Atualizando registro: {produto[1]} | Código: {produto[2]}")
            novo_nome_produto = input(f"Novo nome (ENTER para manter '{produto[1]}'): ") or produto[1]
            novo_codigo = input(f"Novo código (ENTER para manter '{produto[2]}'): ") or produto[2]
            novo_preco_compra = utils.validar_preco(f"Novo preço de compra (ENTER para manter '{produto[3]}'): ") or produto[3]
            novo_preco_venda = utils.validar_preco(f"Novo preço de venda (ENTER para manter '{produto[4]}'): ") or produto[4]
            nova_quantidade = utils.validar_quantidade(f"Nova quantidade (ENTER para manter '{produto[5]}'): ") or produto[5]

            self.cursor.execute("""
                UPDATE produtos
                SET nome_produto = ?, codigo = ?, preco_compra = ?, preco_venda = ?, estoque = ?
                WHERE id = ?
            """, (novo_nome_produto, novo_codigo, novo_preco_compra, novo_preco_venda, nova_quantidade, id_atualizacao))
            self.conn.commit()
            print("Produto atualizado com sucesso!")

    def __del__(self):
        self.conn.close()