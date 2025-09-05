def trocar_tela(container, tela_cls):
    # Remove widgets existentes
    for widget in container.winfo_children():
        widget.destroy()

    # Cria nova tela
    tela_cls(container).pack(fill="both", expand=True)
