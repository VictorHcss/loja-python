import flet as ft


def detalhe_produto(page, produto, callback_voltar, callback_adicionar_ao_carrinho):
    page.clean()

    # Definir AppBar corretamente
    page.appbar = ft.AppBar(
        title=ft.Text("Detalhes do Produto", color=ft.Colors.WHITE),
        bgcolor="#4FC3F7",
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=lambda e: callback_voltar()
        )
    )

    preco_formatado = f"R$ {produto['preco']:.2f}".replace(".", ",")

    imagem = ft.Image(
        src=produto["imagem"],
        width=250,
        height=200,
        fit=ft.ImageFit.COVER,
        border_radius=15
    )

    detalhes = ft.Column(
        [
            imagem,
            ft.Text(produto["nome"], size=24, weight="bold",
                    color="white", text_align="center"),
            ft.Text(preco_formatado, size=22, weight="bold",
                    color="#4FC3F7", text_align="center"),
            ft.Text(f"Categoria: {produto['categoria']}", color="white"),
            ft.Text(f"Estoque: {produto['estoque']} unidades",
                    color=ft.Colors.GREEN_400 if produto["estoque"] > 0 else ft.Colors.RED_400),
            ft.Text("Descrição:", size=16, weight="bold", color="white"),
            ft.Text(produto["descricao"], color=ft.Colors.WHITE70),
            ft.Container(height=20),
            ft.ElevatedButton(
                "🛒 ADICIONAR AO CARRINHO",
                bgcolor="#4FC3F7",
                color="black",
                width=250,
                disabled=produto["estoque"] == 0,
                on_click=lambda e: callback_adicionar_ao_carrinho(produto)
            ),
            ft.OutlinedButton(
                "⬅️ VOLTAR",
                width=250,
                on_click=lambda e: callback_voltar()
            )
        ],
        spacing=10,
        horizontal_alignment="center",
        scroll=ft.ScrollMode.AUTO
    )

    container = ft.Container(
        content=detalhes,
        expand=True,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#0d0d0d", "#1a1a1a", "#0d0d0d"]
        )
    )

    page.add(container)
    page.update()
