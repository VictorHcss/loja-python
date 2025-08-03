import flet as ft
import random
import string
from bdconfig import bdconfig, bd
from enviaemail import enviar_email


def esqueci(page, voltar_login):
    """Tela de recuperação de senha"""
    page.clean()

    # Limpar AppBar anterior
    page.appbar = None

    parametro = bdconfig()
    page.bgcolor = "#0d0d0d"
    page.window_bgcolor = "#0d0d0d"
    page.padding = 0

    def gerar_senha_temporaria():
        """Gerar senha temporária de 8 caracteres"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def enviar_nova_senha(e):
        """Função para enviar nova senha"""
        email_usuario = campo_email.value.strip()

        # Validações
        if not email_usuario or "@" not in email_usuario:
            mensagem_status.value = "Digite um email válido!"
            mensagem_status.color = "red"
            page.update()
            return

        try:
            # Verificar se email existe
            usuario = bd.buscar_um(
                "SELECT * FROM usuario WHERE email = ?",
                (email_usuario,)
            )

            if not usuario:
                # Por segurança, não revelar se o email existe ou não
                mensagem_status.value = "Se o email estiver cadastrado, você receberá instruções."
                mensagem_status.color = "green"
                page.update()
                return

            # Gerar nova senha
            senha_temporaria = gerar_senha_temporaria()

            # Atualizar senha no banco
            sucesso = bd.executar_query(
                "UPDATE usuario SET senha = ? WHERE email = ?",
                (senha_temporaria, email_usuario)
            )

            if sucesso:
                # Tentar enviar email
                try:
                    sucesso_email = enviar_email(
                        email_usuario, senha_temporaria)

                    if sucesso_email:
                        mensagem_status.value = f"Nova senha enviada para {email_usuario}!"
                        mensagem_status.color = "green"
                    else:
                        # Se falhar o email, mostrar a senha na tela
                        mensagem_status.value = f"Sua nova senha temporária é: {senha_temporaria}"
                        mensagem_status.color = "green"

                except Exception:
                    # Fallback: mostrar senha na tela
                    mensagem_status.value = f"Sua nova senha temporária é: {senha_temporaria}"
                    mensagem_status.color = "green"

                page.update()

                # Aguardar e voltar para login
                page.run_task(voltar_apos_sucesso)
            else:
                mensagem_status.value = "Erro ao gerar nova senha. Tente novamente."
                mensagem_status.color = "red"
                page.update()

        except Exception as erro:
            mensagem_status.value = f"Erro: {erro}"
            mensagem_status.color = "red"
            page.update()

    async def voltar_apos_sucesso():
        """Aguardar e voltar para login"""
        import asyncio
        await asyncio.sleep(4)
        voltar_login()

    # Elementos da interface
    titulo = ft.Text("Recuperar Senha",
                     size=30,
                     color=parametro[2],
                     weight=ft.FontWeight.BOLD,
                     text_align=ft.TextAlign.CENTER)

    aviso = ft.Text("Digite seu email para receber a nova senha temporária",
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER)

    campo_email = ft.TextField(
        label="Seu email",
        width=400,
        border=ft.InputBorder.OUTLINE,
        prefix_icon=ft.icons.EMAIL_OUTLINED,
        border_color=parametro[2],
        focused_border_color=parametro[2],
        focused_color=parametro[2],
        cursor_color=parametro[2],
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_100),
        bgcolor="#1a1a1a",
        color=ft.Colors.WHITE
    )

    mensagem_status = ft.Text("", color="red")

    botao_enviar = ft.ElevatedButton(
        "Enviar Nova Senha",
        on_click=enviar_nova_senha,
        width=400,
        bgcolor=parametro[2],
        color=parametro[3],
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

    botao_voltar = ft.TextButton(
        "Voltar para o Login",
        on_click=lambda e: voltar_login(),
        style=ft.ButtonStyle(color=parametro[2])
    )

    logo = ft.Image(
        src=parametro[0],
        width=200,
        height=200,
        border_radius=30,
        fit=ft.ImageFit.CONTAIN
    )

    # Container do formulário
    fundo = ft.Container(
        content=ft.Column(
            [
                ft.Container(content=logo, alignment=ft.alignment.center,
                             margin=ft.margin.only(bottom=10)),
                titulo,
                aviso,
                campo_email,
                botao_enviar,
                mensagem_status,
                botao_voltar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        bgcolor=ft.colors.with_opacity(0.9, "#121212"),
        border_radius=10,
        width=450,
        padding=20,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=0.2,
            blur_radius=6,
            color=ft.Colors.GREY,
            offset=ft.Offset(0, 0.1),
        )
    )

    # Stack com imagem de fundo
    stack = ft.Stack(
        [
            ft.Image(
                src="./img/fundonew.jpg",
                width=page.width,
                height=page.height,
                fit=ft.ImageFit.COVER,
                opacity=0.8
            ),
            ft.Container(
                content=fundo,
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        expand=True
    )

    page.add(stack)
    page.update()
