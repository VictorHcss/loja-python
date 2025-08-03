import flet as ft
import random
import string


def finalizar(page, usuario_id, total_compra, itens_carrinho, callback_voltar):
    """Tela de finalização de compra"""
    page.clean()

    # Cores do tema
    cor_texto = ft.Colors.WHITE
    cor_destaque = "#4FC3F7"
    cor_sucesso = "#4CAF50"

    # Definir AppBar corretamente
    page.appbar = ft.AppBar(
        title=ft.Text("Pedido Realizado", color=cor_texto),
        bgcolor=cor_destaque,
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=cor_texto,
            on_click=lambda e: callback_voltar()
        )
    )

    # Gerar número do pedido
    numero_pedido = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8))

    sucesso_container = ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    name=ft.icons.CHECK_CIRCLE,
                    size=100,
                    color=cor_sucesso
                ),
                ft.Container(height=20),
                ft.Text(
                    "Pagamento Confirmado!",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=cor_texto,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=10),
                ft.Text(
                    f"Pedido #{numero_pedido}",
                    size=18,
                    color=cor_destaque,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=5),
                ft.Text(
                    f"Total: R$ {total_compra:.2f}".replace('.', ','),
                    size=18,
                    color=cor_texto,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=30),
                ft.Text(
                    "Obrigado por comprar na GeekHub!",
                    size=16,
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=40),
                ft.ElevatedButton(
                    "CONTINUAR COMPRANDO",
                    icon=ft.icons.SHOPPING_BAG,
                    bgcolor=cor_destaque,
                    color="#000000",
                    width=250,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e: callback_voltar()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        ),
        alignment=ft.alignment.center,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#0d0d0d", "#1a1a1a", "#0d0d0d"]
        )
    )

    page.add(sucesso_container)
    page.update()
