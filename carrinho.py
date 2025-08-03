import flet as ft
from bdconfig import bd


def carrinho(page, usuario_id, callback_voltar=None):
    """Tela do carrinho de compras"""
    page.clean()

    # Cores do tema
    cor_texto = ft.Colors.WHITE
    cor_destaque = "#4FC3F7"
    cor_secundaria = "#1a1a1a"

    # Definir AppBar corretamente
    page.appbar = ft.AppBar(
        title=ft.Text("Carrinho", color=cor_texto),
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=cor_texto,
            on_click=lambda e: callback_voltar() if callback_voltar else None
        ),
        bgcolor=cor_destaque
    )

    def buscar_itens_carrinho():
        """Buscar itens do carrinho"""
        try:
            itens = bd.buscar_todos('''
                SELECT c.id, c.produto_id, c.quantidade, p.nome, p.preco, p.imagem, p.estoque
                FROM carrinho c
                JOIN produto p ON c.produto_id = p.id
                WHERE c.usuario_id = ?
            ''', (usuario_id,))

            return [
                {
                    "id": item[0],
                    "produto_id": item[1],
                    "quantidade": item[2],
                    "nome": item[3],
                    "preco": item[4],
                    "imagem": item[5],
                    "estoque": item[6]
                }
                for item in itens
            ]
        except Exception as e:
            print(f"Erro ao buscar carrinho: {e}")
            return []

    def atualizar_quantidade(produto_id, nova_quantidade):
        """Atualizar quantidade do produto"""
        try:
            if nova_quantidade <= 0:
                bd.executar_query(
                    "DELETE FROM carrinho WHERE usuario_id = ? AND produto_id = ?",
                    (usuario_id, produto_id)
                )
            else:
                bd.executar_query(
                    "UPDATE carrinho SET quantidade = ? WHERE usuario_id = ? AND produto_id = ?",
                    (nova_quantidade, usuario_id, produto_id)
                )

            # Recarregar carrinho
            carrinho(page, usuario_id, callback_voltar)

        except Exception as e:
            print(f"Erro ao atualizar quantidade: {e}")

    def remover_item(produto_id):
        """Remover item do carrinho"""
        atualizar_quantidade(produto_id, 0)

    def limpar_carrinho():
        """Limpar todo o carrinho"""
        try:
            bd.executar_query(
                "DELETE FROM carrinho WHERE usuario_id = ?", (usuario_id,))
            carrinho(page, usuario_id, callback_voltar)
        except Exception as e:
            print(f"Erro ao limpar carrinho: {e}")

    def finalizar_compra(e):
        """Finalizar compra"""
        try:
            itens = buscar_itens_carrinho()
            if not itens:
                return

            # Registrar a compra no banco de dados
            for item in itens:
                bd.executar_query(
                    "INSERT INTO pedidos (usuario_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                    (usuario_id, item["produto_id"],
                     item["quantidade"], item["preco"])
                )

            # Limpar carrinho
            bd.executar_query(
                "DELETE FROM carrinho WHERE usuario_id = ?", (usuario_id,))

            # Mostrar tela de sucesso
            from finalizar import finalizar
            total = sum(item["preco"] * item["quantidade"] for item in itens)
            finalizar(page, usuario_id, total, itens, callback_voltar)

        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro ao finalizar compra: {str(e)}"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()

    # Buscar itens
    itens_carrinho = buscar_itens_carrinho()

    # Lista de itens
    lista_itens = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
    total_compra = 0

    if itens_carrinho:
        for item in itens_carrinho:
            subtotal = item["preco"] * item["quantidade"]
            total_compra += subtotal

            # Card do item
            card_item = ft.Container(
                content=ft.Row(
                    [
                        # Imagem do produto
                        ft.Container(
                            content=ft.Image(
                                src=item["imagem"],
                                width=60,
                                height=60,
                                fit=ft.ImageFit.COVER,
                                border_radius=8,
                                error_content=ft.Container(
                                    content=ft.Icon(
                                        ft.icons.IMAGE_NOT_SUPPORTED,
                                        size=30,
                                        color=ft.Colors.WHITE70
                                    ),
                                    alignment=ft.alignment.center
                                )
                            ),
                            width=60,
                            height=60,
                            bgcolor="#2a2a2a",
                            border_radius=8,
                            alignment=ft.alignment.center
                        ),
                        # Informações
                        ft.Column(
                            [
                                ft.Text(
                                    item["nome"],
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=cor_texto,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    f"R$ {item['preco']:.2f}".replace(
                                        '.', ','),
                                    size=12,
                                    color=cor_destaque
                                )
                            ],
                            spacing=5,
                            expand=True
                        ),
                        # Controles de quantidade
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.icons.REMOVE,
                                    icon_color=cor_texto,
                                    icon_size=20,
                                    tooltip="Diminuir",
                                    on_click=lambda e, pid=item["produto_id"], qtd=item["quantidade"]:
                                        atualizar_quantidade(pid, qtd - 1)
                                ),
                                ft.Text(
                                    str(item["quantidade"]),
                                    size=16,
                                    color=cor_texto,
                                    text_align=ft.TextAlign.CENTER,
                                    width=30
                                ),
                                ft.IconButton(
                                    icon=ft.icons.ADD,
                                    icon_color=cor_texto,
                                    icon_size=20,
                                    tooltip="Aumentar",
                                    on_click=lambda e, pid=item["produto_id"], qtd=item["quantidade"]:
                                        atualizar_quantidade(pid, qtd + 1)
                                )
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        # Subtotal
                        ft.Text(
                            f"R$ {subtotal:.2f}".replace('.', ','),
                            size=14,
                            color=cor_destaque,
                            width=80,
                            text_align=ft.TextAlign.RIGHT,
                            weight=ft.FontWeight.BOLD
                        ),
                        # Botão remover
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.Colors.RED_400,
                            tooltip="Remover",
                            on_click=lambda e, pid=item["produto_id"]: remover_item(
                                pid)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                bgcolor="#2a2a2a",
                border_radius=10,
                padding=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=5,
                    color=ft.colors.with_opacity(0.2, "#000000"),
                    offset=ft.Offset(0, 2)
                )
            )

            lista_itens.controls.append(card_item)

        # Total
        total_container = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "Total:",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=cor_texto
                    ),
                    ft.Text(
                        f"R$ {total_compra:.2f}".replace('.', ','),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=cor_destaque
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor="#2a2a2a",
            padding=20,
            border_radius=10,
            margin=ft.margin.only(top=20)
        )

        # Botões de ação
        botoes_acao = ft.Row(
            [
                ft.ElevatedButton(
                    "Limpar Carrinho",
                    bgcolor="#3A3A3A",
                    color=cor_texto,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda e: limpar_carrinho()
                ),
                ft.ElevatedButton(
                    "Finalizar Compra",
                    bgcolor=cor_destaque,
                    color="#000000",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=finalizar_compra
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=20
        )

        conteudo_carrinho = ft.Column(
            [
                lista_itens,
                total_container,
                ft.Container(height=20),
                botoes_acao
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

    else:
        # Carrinho vazio
        conteudo_carrinho = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.SHOPPING_CART_OUTLINED,
                        size=80,
                        color=ft.Colors.WHITE70
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        "Seu carrinho está vazio",
                        size=20,
                        color=ft.Colors.WHITE70,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=30),
                    ft.ElevatedButton(
                        "CONTINUAR COMPRANDO",
                        icon=ft.icons.SHOPPING_BAG,
                        bgcolor=cor_destaque,
                        color="#000000",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=lambda e: callback_voltar() if callback_voltar else None
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    # Container principal
    container_principal = ft.Container(
        content=conteudo_carrinho,
        expand=True,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#0d0d0d", "#1a1a1a", "#0d0d0d"]
        )
    )

    page.add(container_principal)
    page.update()
