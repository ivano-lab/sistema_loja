import os
import sqlite3
import utils

class Cliente:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.abspath(os.path.join(base_dir, '..', 'loja.db'))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def menu_cliente(self):
        while True:
            utils.print_linha()
            print("MÓDULO DE CLIENTES")
            utils.print_linha()
            print("1 - Listar clientes")
            print("2 - Cadastrar cliente")
            print("3 - Atualizar cliente")
            print("4 - Deletar cliente")
            print("0 - Voltar")
            print()
            opcao = input("Escolha: ")

            if opcao == "1":
                self.listar_clientes()

            elif opcao == "2":
                self.cadastrar_cliente()

            elif opcao == "3":
                self.atualizar_cliente()

            elif opcao == "4":
                self.deletar_cliente()

            elif opcao == "0":
                print("Saindo do módulo de Clientes...")
                break
            else:
                print("X Opção inválida.")

    def cadastrar_cliente(self):
        global data_nasc
        nome = input("Nome do cliente: ")
        cpf = None
        cnpj = None
        while True:
            tipo_cliente = input("Tipo de cliente (PF para pessoa física / PJ para pessoa jurídica): ").strip().upper()
            if tipo_cliente in ("PF", "PJ"):
                break
            print("Tipo cliente inválido. Digite PF ou PJ.")

        if tipo_cliente == "PF":
            cpf = utils.validar_cpf()
            cnpj = None
            data_nasc = input("Data de fundação da empresa (DD/MM/AAAA): ")

        else:
            cnpj = utils.validar_cnpj()
            cpf = None
            data_nasc = input("Data de nascimento do cliente (DD/MM/AAAA): ")

        self.cursor.execute(
            "INSERT INTO clientes (nome, tipo_cliente, cpf, cnpj, data_nascimento) VALUES (?, ?, ?, ?, ?)",
            (nome, tipo_cliente, cpf, cnpj, data_nasc)
        )
        self.conn.commit()
        print("\nCliente cadastrado com sucesso!")

    def listar_clientes(self):
        utils.print_linha()
        print("LISTAGEM DE CLIENTES")
        utils.print_linha()
        self.cursor.execute("SELECT * FROM clientes")
        clientes = self.cursor.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for c in clientes:
                print(
                    f"Cliente: {c[1]}")
                utils.underline()

    def deletar_cliente(self):
        id_delecao = input("Digite o ID do cliente a ser deletado: ")
        self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id_delecao,))
        if self.cursor.rowcount == 0:
            print("Nenhum cliente encontrado com este ID.")
        else:
            self.conn.commit()
            print("Cliente deletado com sucesso!")

    def atualizar_cliente(self):
        id_atualizacao = input("Digite o ID do cliente a ser atualizado: ")
        self.cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_atualizacao,))
        cliente = self.cursor.fetchone()

        if not cliente:
            print("Nenhum cliente encontrado com este ID.")
        else:
            self.conn.commit()
            print(f"Atualizando registro: {cliente[1]} | CPF: {cliente[2]}")
            novo_nome_cliente = input(f"Editar nome (ENTER para manter '{cliente[1]}'): ") or cliente[1]
            novo_cpf = input(f"Editar CPF (ENTER para manter '{cliente[2]}'): ") or cliente[2]
            nova_data_nasc = input(f"Editar data de nascimento (ENTER para manter '{cliente[3]}'): ") or cliente[3]

            self.cursor.execute("""
                UPDATE clientes
                SET nome = ?, cpf = ?, data_nascimento = ?
                WHERE id = ?
            """, (novo_nome_cliente, novo_cpf, nova_data_nasc, id_atualizacao))
            self.conn.commit()
            print("Cliente atualizado com sucesso!")

    def __del__(self):
        self.conn.close()
    