import flet as ft
from bdconfig import bdconfig, bd


def login(page, callback_produtos, callback_cadastro, callback_esqueci):
    page.clean()

    # Limpar AppBar anterior
    page.appbar = None

    parametro = bdconfig()
    page.bgcolor = "#0d0d0d"
    page.window_bgcolor = "#0d0d0d"
    page.padding = 0

    def verificar_login(e):
        email = email_input.value
        senha = senha_input.value
        if not email or not senha:
            mensagem_erro.value = "Por favor, preencha todos os campos"
            mensagem_erro.visible = True
            page.update()
            return
        try:
            usuario = bd.buscar_um(
                'SELECT * FROM usuario WHERE email = ? AND senha = ?',
                (email, senha)
            )
            if usuario:
                mensagem_erro.visible = False
                page.session.set("usuario_id", usuario[0])
                page.session.set("usuario_nome", usuario[1])
                callback_produtos()
            else:
                mensagem_erro.value = "Email ou senha incorretos"
                mensagem_erro.visible = True
                page.update()
        except Exception as e:
            mensagem_erro.value = f"Erro ao fazer login: {str(e)}"
            mensagem_erro.visible = True
            page.update()

    logo = ft.Image(
        src=parametro[0],
        width=200,
        height=200,
        border_radius=30,
        fit=ft.ImageFit.CONTAIN,
    )

    email_input = ft.TextField(
        label="Email",
        border=ft.InputBorder.OUTLINE,
        width=400,
        prefix_icon=ft.icons.EMAIL_OUTLINED,
        border_color=parametro[2],
        focused_border_color=parametro[2],
        focused_color=parametro[2],
        cursor_color=parametro[2],
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_100),
        bgcolor="#1a1a1a",
        color=ft.Colors.WHITE,
    )

    senha_input = ft.TextField(
        label="Senha",
        border=ft.InputBorder.OUTLINE,
        width=400,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.icons.LOCK_OUTLINE,
        border_color=parametro[2],
        focused_border_color=parametro[2],
        focused_color=parametro[2],
        cursor_color=parametro[2],
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_100),
        bgcolor="#1a1a1a",
        color=ft.Colors.WHITE,
    )

    mensagem_erro = ft.Text("", color=ft.Colors.RED_500, visible=False)

    esqueceu_senha = ft.TextButton(
        "Esqueceu a senha?",
        style=ft.ButtonStyle(color=ft.Colors.WHITE),
        on_click=lambda e: callback_esqueci()
    )

    botao_login = ft.ElevatedButton(
        "Entrar",
        width=400,
        bgcolor=parametro[2],
        color=parametro[3],
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=verificar_login
    )

    botao_criar = ft.ElevatedButton(
        "Criar Conta",
        width=400,
        bgcolor=parametro[2],
        color=parametro[3],
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=lambda e: callback_cadastro()
    )

    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=logo, alignment=ft.alignment.center,
                             margin=ft.margin.only(bottom=10)),
                ft.Container(height=10),
                ft.Text("LOGIN", size=29, weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER, color=parametro[2]),
                email_input,
                senha_input,
                mensagem_erro,
                ft.Container(content=esqueceu_senha,
                             alignment=ft.alignment.center_right, width=400),
                ft.Container(height=10),
                botao_login,
                botao_criar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.colors.with_opacity(0.7, "#121212"),
        border_radius=10,
        width=450,
        padding=20,
        alignment=ft.alignment.center,
    )

    imagem_fundo = ft.Image(
        src="./img/fundonew.jpg",
        width=page.width,
        height=page.height,
        fit=ft.ImageFit.COVER,
        opacity=0.8
    )

    page.add(
        ft.Stack(
            [
                imagem_fundo,
                ft.Container(content=formulario,
                             alignment=ft.alignment.center, expand=True)
            ],
            expand=True
        )
    )
    page.update()
