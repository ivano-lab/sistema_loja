import re
import locale
import sqlite3

conn = sqlite3.connect('loja.db')
cursor = conn.cursor()

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

def formatar_moeda(valor: float) -> str:
    return locale.currency(valor, grouping=True)

def print_linha():
    print("=" * 40)

def underline():
    print("_" * 40)

def validar_preco(texto_prompt):
    while True:
        valor = input(texto_prompt)
        try:
            preco = float(valor)
            if preco < 0:
                print("Preço não pode ser negativo. Tente novamente.")
                continue
            return preco
        except ValueError:
            print("Valor inválido. Digite um número válido (ex: 12.50).")

def validar_quantidade(texto_prompt="Quandidade: "):
    while True:
        entrada = input(texto_prompt)
        try:
            quantidade = float(entrada)
            if quantidade < 0:
                print("Quantidade não pode ser negativa. Tente novamente.")
                continue
            return quantidade
        except ValueError:
            print("Quantidade inválida. Digite um número válido (ex: 5, 100, 3500).")


def validar_digito_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(digit) * factor for digit, factor in zip(cpf[:9], range(10, 1, -1)))
    dig1 = (soma * 10 % 11) % 10

    soma = sum(int(digit) * factor for digit, factor in zip(cpf[:10], range(11, 1, -1)))
    dig2 = (soma * 10 % 11) % 10

    return cpf[-2:] == f"{dig1}{dig2}"

def validar_cpf():
    while True:
        cpf = input("CPF do cliente: ")
        if validar_digito_cpf(cpf):
            return cpf
        else:
            print("CPF Inválido. Tente novamente.")

def validar_digito_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj_puro, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj_puro, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    dig1 = calcular_digito(cnpj[:12], pesos1)
    dig2 = calcular_digito(cnpj[:12] + dig1, pesos2)

    return cnpj[-2:] == dig1 + dig2

def validar_cnpj():
    while True:
        cnpj = input("CNPJ do cliente: ")
        if validar_digito_cnpj(cnpj):
            return cnpj
        else:
            print("CNPJ Inválido. Tente novamente.")



def reseta_banco():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()

    for tabela in tabelas:
        nome_tabela = tabela[0]
        if nome_tabela == 'sqlite_sequence':
            continue
        cursor.execute(f"DROP TABLE IF EXISTS {nome_tabela}")

    conn.commit()
    conn.close()