import flet as ft
import asyncio
from login import login
from esqueci import esqueci
from produto import produtos
from cadastro import cadastro
from bdconfig import bdconfig


async def main(page: ft.Page):
    page.title = "GeekHub"
    page.bgcolor = "#0d0d0d"
    page.window.width = 560
    page.window.height = 800
    page.window.center()
    page.padding = 0

    parametro = bdconfig()
    COR_PRIMARIA = parametro[2]
    COR_FUNDO = "#0d0d0d"
    COR_TEXTO = "#FFFFFF"

    def abre_login(e=None):
        login(page, abre_produtos, abre_cadastro, abre_esqueci)

    def abre_produtos(e=None):
        usuario_id = page.session.get("usuario_id")
        produtos(page, abre_login, usuario_id)

    def abre_cadastro(e=None):
        cadastro(page, abre_login)

    def abre_esqueci(e=None):
        esqueci(page, abre_login)

    logo_container = ft.Container(
        content=ft.Image(
            src='assets/img/logo.jpg',
            width=200,
            height=200,
            border_radius=50,
            fit=ft.ImageFit.CONTAIN
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(
            1000, ft.AnimationCurve.EASE_OUT)
    )

    titulo_container = ft.Container(
        content=ft.Text(
            "GeekHub",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=COR_PRIMARIA,
            text_align=ft.TextAlign.CENTER
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(800, ft.AnimationCurve.EASE_OUT)
    )

    subtitulo_container = ft.Container(
        content=ft.Text(
            "Sua loja gamer completa",
            size=16,
            color=COR_TEXTO,
            text_align=ft.TextAlign.CENTER,
            opacity=0.8
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(600, ft.AnimationCurve.EASE_OUT)
    )

    progress_container = ft.Container(
        content=ft.ProgressBar(
            width=300, color=COR_PRIMARIA, bgcolor="#2a2a2a", value=0),
        opacity=0,
        animate_opacity=ft.animation.Animation(400, ft.AnimationCurve.EASE_OUT)
    )

    progress_text = ft.Container(
        content=ft.Text(
            "Iniciando...",
            size=12,
            color=COR_TEXTO,
            text_align=ft.TextAlign.CENTER,
            opacity=0.7
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(400, ft.AnimationCurve.EASE_OUT)
    )

    dots_container = ft.Container(
        content=ft.Row(
            [
                ft.Container(width=8, height=8, bgcolor=COR_PRIMARIA,
                             border_radius=4, opacity=0.3)
                for _ in range(3)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        ),
        opacity=0,
        animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

    splash_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=100),
                logo_container,
                ft.Container(height=30),
                titulo_container,
                ft.Container(height=15),
                subtitulo_container,
                ft.Container(height=80),
                progress_container,
                ft.Container(height=15),
                progress_text,
                ft.Container(height=25),
                dots_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        width=page.width,
        height=page.height,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[COR_FUNDO, "#1a1a1a", COR_FUNDO]
        )
    )

    page.add(splash_container)
    page.update()

    messages = [
        "Iniciando sistema...",
        "Carregando produtos...",
        "Configurando banco...",
        "Preparando interface...",
        "Quase pronto...",
        "Bem-vindo ao GeekHub!"
    ]

    await asyncio.sleep(0.5)
    logo_container.opacity = 1
    page.update()

    await asyncio.sleep(0.4)
    titulo_container.opacity = 1
    page.update()

    await asyncio.sleep(0.3)
    subtitulo_container.opacity = 1
    page.update()

    await asyncio.sleep(0.4)
    progress_container.opacity = 1
    progress_text.opacity = 1
    dots_container.opacity = 1
    page.update()

    for i in range(101):
        progress_container.content.value = i / 100
        if i < len(messages) * 17:
            msg_index = min(i // 17, len(messages) - 1)
            progress_text.content.value = messages[msg_index]
        dot_index = (i // 8) % 3
        for j, dot in enumerate(dots_container.content.controls):
            dot.opacity = 1.0 if j == dot_index else 0.3
        page.update()
        await asyncio.sleep(0.04)

    await asyncio.sleep(0.8)
    for element in [logo_container, titulo_container, subtitulo_container, progress_container, progress_text, dots_container]:
        element.opacity = 0
    page.update()

    await asyncio.sleep(1)
    page.clean()
    abre_login()

if __name__ == "__main__":
    ft.app(target=main)
