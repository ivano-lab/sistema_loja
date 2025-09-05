def trocar_tela(container, tela_cls):
    """
    Remove todos os widgets do container e carrega uma nova tela.
    :param container: Frame ou janela principal onde as telas serão exibidas
    :param tela_cls: Classe da tela que será exibida
    """
    for widget in container.winfo_children():
        widget.destroy()

    tela_cls(container).pack(fill="both", expand=True)
