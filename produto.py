import flet as ft
from bdconfig import bdconfig, bd


def produtos(page, callback_login, usuario_id):
    """Tela de listagem de produtos"""
    page.clean()
    parametro = bdconfig()
    page.bgcolor = "#0d0d0d"
    page.window_bgcolor = "#0d0d0d"
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Definir AppBar corretamente
    page.appbar = ft.AppBar(
        title=ft.Row(
            [
                ft.Image(src="./img/imgnew.gif", width=40, height=40,
                         border_radius=30, fit=ft.ImageFit.CONTAIN),
                ft.Container(width=10),
                ft.Text(parametro[1], size=24,
                        weight=ft.FontWeight.BOLD, color=parametro[2]),
                ft.Container(width=20),
                ft.Text("Nossos Produtos", size=20, color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.with_opacity(0.8, "#121212"),
        toolbar_height=70
    )

    def buscar_produtos():
        """Buscar produtos do banco de dados"""
        try:
            produtos_db = bd.buscar_todos(
                'SELECT id, nome, descricao, preco, estoque, categoria, imagem FROM produto'
            )

            return [
                {
                    "id": p[0], "nome": p[1], "descricao": p[2], "preco": p[3],
                    "estoque": p[4], "categoria": p[5], "imagem": p[6]
                }
                for p in produtos_db
            ]
        except Exception as e:
            print(f"Erro ao buscar produtos: {str(e)}")
            return []

    def adicionar_ao_carrinho(produto_id):
        """Adicionar produto ao carrinho"""
        try:
            # Verificar se produto já está no carrinho
            existente = bd.buscar_um(
                "SELECT quantidade FROM carrinho WHERE usuario_id = ? AND produto_id = ?",
                (usuario_id, produto_id)
            )

            if existente:
                # Atualizar quantidade
                nova_qtd = existente[0] + 1
                bd.executar_query(
                    "UPDATE carrinho SET quantidade = ? WHERE usuario_id = ? AND produto_id = ?",
                    (nova_qtd, usuario_id, produto_id)
                )
            else:
                # Inserir novo item
                bd.executar_query(
                    "INSERT INTO carrinho (usuario_id, produto_id, quantidade) VALUES (?, ?, ?)",
                    (usuario_id, produto_id, 1)
                )

            page.snack_bar = ft.SnackBar(
                ft.Text("Produto adicionado ao carrinho!"),
                bgcolor=ft.Colors.GREEN
            )
            page.snack_bar.open = True
            page.update()

        except Exception as erro:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro: {erro}"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()

    def mostrar_detalhes(e):
        """Mostrar detalhes do produto"""
        produto_id = e.control.data

        try:
            produto = bd.buscar_um(
                'SELECT id, nome, descricao, preco, estoque, categoria, imagem FROM produto WHERE id = ?',
                (produto_id,)
            )

            if produto:
                from detalhe_produto import detalhe_produto
                produto_dict = {
                    "id": produto[0], "nome": produto[1], "descricao": produto[2],
                    "preco": produto[3], "estoque": produto[4], "categoria": produto[5], "imagem": produto[6]
                }
                detalhe_produto(
                    page,
                    produto_dict,
                    lambda: produtos(page, callback_login, usuario_id),
                    lambda p: adicionar_ao_carrinho(p["id"])
                )

        except Exception as e:
            print(f"Erro ao buscar produto: {e}")

    def ir_carrinho(e):
        """Ir para o carrinho"""
        from carrinho import carrinho
        carrinho(page, usuario_id, lambda: produtos(
            page, callback_login, usuario_id))

    # Buscar produtos
    produtos_lista = buscar_produtos()

    # Grid de produtos
    grid_produtos = ft.GridView(
        expand=True,
        max_extent=180,
        child_aspect_ratio=0.7,
        spacing=10,
        run_spacing=10,
        padding=15
    )

    # Adicionar produtos ao grid
    for produto in produtos_lista:
        preco_formatado = f"R$ {produto['preco']:.2f}".replace('.', ',')

        grid_produtos.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Image(
                                src=produto["imagem"],
                                width=130,
                                height=100,
                                fit=ft.ImageFit.COVER,
                                border_radius=8,
                                error_content=ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Icon(
                                                ft.icons.IMAGE_NOT_SUPPORTED,
                                                size=40,
                                                color=ft.Colors.WHITE70
                                            ),
                                            ft.Text(
                                                "Sem imagem",
                                                size=10,
                                                color=ft.Colors.WHITE70,
                                                text_align=ft.TextAlign.CENTER
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5
                                    ),
                                    alignment=ft.alignment.center
                                )
                            ),
                            width=130,
                            height=100,
                            bgcolor="#2a2a2a",
                            border_radius=8,
                            alignment=ft.alignment.center
                        ),
                        ft.Text(produto["nome"], size=12, weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=parametro[2], max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(produto["categoria"], size=10,
                                text_align=ft.TextAlign.CENTER, color=ft.Colors.WHITE70),
                        ft.Text(preco_formatado, size=14,
                                color=parametro[2], text_align=ft.TextAlign.CENTER,
                                weight=ft.FontWeight.BOLD),
                    ],
                    spacing=6,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=ft.colors.with_opacity(0.92, "#121212"),
                border_radius=10,
                padding=12,
                shadow=ft.BoxShadow(
                    blur_radius=4, color=ft.Colors.BLACK54, offset=ft.Offset(0, 2)),
                on_click=mostrar_detalhes,
                data=produto["id"],
                ink=True
            )
        )

    # Botões inferiores
    botao_voltar_login = ft.ElevatedButton(
        "Sair",
        width=200,
        height=40,
        bgcolor="#3A3A3A",
        color=ft.Colors.WHITE,
        on_click=lambda e: callback_login(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    botao_ver_carrinho = ft.ElevatedButton(
        "🛒 Carrinho",
        width=200,
        height=40,
        bgcolor=parametro[2],
        color=parametro[3],
        on_click=ir_carrinho,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    # Container principal
    conteudo_stack = ft.Stack(
        [
            ft.Image(src="./img/fundonew.jpg", width=page.width,
                     height=page.height, fit=ft.ImageFit.COVER, opacity=0.7),
            ft.Column(
                [
                    ft.Container(content=grid_produtos, expand=True),
                    ft.Container(
                        content=ft.Row([botao_voltar_login, botao_ver_carrinho],
                                       alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                        alignment=ft.alignment.center,
                        padding=10
                    )
                ],
                expand=True
            )
        ],
        expand=True
    )

    page.add(conteudo_stack)
    page.update()
