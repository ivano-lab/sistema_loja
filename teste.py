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
                      f"FORMA PAGAMENTO: {venda[3]}, VALOR TOTAL: {utils.formatar_moeda(venda[4])}")
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
                self.relatorio_detalhado(int(id_venda))
            else:
                print("ID inválido!")
        else:
            print("Opção inválida.")

def relatorio_detalhado(self, id_venda):
    utils.print_linha()
    print(f"DETALHES DA VENDA {id_venda}")
    utils.print_linha()

    self.cursor.execute("""
        SELECT p.nome_produto, i.quantidade, i.preco_unitario, i.subtotal
        FROM itens_venda i
        JOIN produtos p ON i.produto_id = p.id
        WHERE i.venda_id = ?
    """, (id_venda,))
    itens = self.cursor.fetchall()

    if not itens:
        print("Nenhum item encontrado para esta venda.")
    else:
        for item in itens:
            print(f"Produto: {item[0]} | Quantidade: {item[1]} | "
                  f"Preço Unitário: {utils.formatar_moeda(item[2])} | "
                  f"Subtotal: {utils.formatar_moeda(item[3])}")
    utils.underline()
