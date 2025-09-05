def aplicar_mascara_cpf(event):
    texto = entry_cpf.get()
    # Remove tudo que não for dígito
    texto = "".join(filter(str.isdigit, texto))[:11]  # limita a 11 dígitos
    formatado = ""

    if len(texto) > 0:
        formatado = texto[:3]
    if len(texto) > 3:
        formatado += "." + texto[3:6]
    if len(texto) > 6:
        formatado += "." + texto[6:9]
    if len(texto) > 9:
        formatado += "-" + texto[9:11]

    # Evita loop de eventos apagando/reinserindo
    entry_cpf.delete(0, tk.END)
    entry_cpf.insert(0, formatado)

def aplicar_mascara_cnpj(event):
    texto = entry_cnpj.get()
    texto = "".join(filter(str.isdigit, texto))[:14]  # limita a 14 dígitos
    formatado = ""

    if len(texto) > 0:
        formatado = texto[:2]
    if len(texto) > 2:
        formatado += "." + texto[2:5]
    if len(texto) > 5:
        formatado += "." + texto[5:8]
    if len(texto) > 8:
        formatado += "/" + texto[8:12]
    if len(texto) > 12:
        formatado += "-" + texto[12:14]

    entry_cnpj.delete(0, tk.END)
    entry_cnpj.insert(0, formatado)
