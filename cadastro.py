import flet as ft
import time
from bdconfig import bdconfig, bd


def cadastro(page, callback_login):
    """Tela de cadastro de novos usuários"""
    page.clean()

    # Limpar AppBar anterior
    page.appbar = None

    parametro = bdconfig()
    page.bgcolor = "#0d0d0d"
    page.window_bgcolor = "#0d0d0d"
    page.padding = 0

    def fazer_cadastro(e):
        """Função para cadastrar novo usuário"""
        # Validar senhas
        if senha_input.value != confirmar_senha_input.value:
            mostrar_erro("As senhas não coincidem!")
            return

        # Validar campos obrigatórios
        if not nome_input.value or not email_input.value or not senha_input.value:
            mostrar_erro("Preencha todos os campos obrigatórios!")
            return

        # Validar email
        if "@" not in email_input.value:
            mostrar_erro("Digite um email válido!")
            return

        try:
            # Verificar se email já existe
            usuario_existente = bd.buscar_um(
                "SELECT * FROM usuario WHERE email = ?",
                (email_input.value,)
            )

            if usuario_existente:
                mostrar_erro("Este e-mail já está cadastrado!")
                return

            # Inserir novo usuário
            sucesso = bd.executar_query(
                'INSERT INTO usuario (nome, sobrenome, email, senha, telefone) VALUES (?, ?, ?, ?, ?)',
                (nome_input.value, s_nome_input.value, email_input.value,
                 senha_input.value, telefone_input.value)
            )

            if sucesso:
                # Mostrar sucesso
                page.clean()
                page.add(ft.Stack(
                    [
                        ft.Image(
                            src="./img/fundonew.jpg",
                            width=page.width,
                            height=page.height,
                            fit=ft.ImageFit.COVER,
                            opacity=0.8
                        ),
                        ft.Container(
                            ft.Text("Usuário cadastrado com sucesso!",
                                    color=ft.Colors.WHITE, size=20),
                            bgcolor=ft.colors.with_opacity(
                                0.8, ft.Colors.GREEN_400),
                            alignment=ft.alignment.center,
                            expand=True,
                            padding=20
                        )
                    ],
                    expand=True
                ))
                page.update()
                time.sleep(2)
                callback_login()
            else:
                mostrar_erro("Erro ao criar conta. Tente novamente.")

        except Exception as erro:
            mostrar_erro(f"Erro ao cadastrar: {str(erro)}")

    def mostrar_erro(mensagem):
        """Função para mostrar mensagens de erro"""
        page.snack_bar = ft.SnackBar(
            ft.Text(mensagem),
            bgcolor=ft.Colors.RED_400
        )
        page.snack_bar.open = True
        page.update()

    def criar_textfield(label, icon, password=False, obrigatorio=False):
        """Função para criar campos de texto padronizados"""
        label_text = f"{label} *" if obrigatorio else label
        return ft.TextField(
            label=label_text,
            border=ft.InputBorder.OUTLINE,
            width=400,
            password=password,
            can_reveal_password=password,
            prefix_icon=icon,
            border_color=parametro[2],
            focused_border_color=parametro[2],
            focused_color=parametro[2],
            cursor_color=parametro[2],
            label_style=ft.TextStyle(color=ft.Colors.PURPLE_100),
            bgcolor="#1a1a1a",
            color=ft.Colors.WHITE
        )

    # Campos do formulário
    nome_input = criar_textfield(
        "Nome", ft.icons.PERSON_OUTLINE, obrigatorio=True)
    s_nome_input = criar_textfield("Sobrenome", ft.icons.PERSON_OUTLINE)
    email_input = criar_textfield(
        "Email", ft.icons.EMAIL_OUTLINED, obrigatorio=True)
    telefone_input = criar_textfield("Telefone", ft.icons.PHONE_OUTLINED)
    senha_input = criar_textfield(
        "Senha", ft.icons.LOCK_OUTLINE, password=True, obrigatorio=True)
    confirmar_senha_input = criar_textfield(
        "Confirmar senha", ft.icons.LOCK_OUTLINE, password=True, obrigatorio=True)

    # Elementos da interface
    logo = ft.Image(src=parametro[0], width=200,
                    border_radius=30,
                    height=200, fit=ft.ImageFit.CONTAIN)

    titulo = ft.Text(
        "CADASTRO",
        size=29,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=parametro[2],
    )

    # Nota sobre campos obrigatórios
    nota_obrigatorio = ft.Text(
        "* Campos obrigatórios",
        size=12,
        color=ft.Colors.WHITE70,
        text_align=ft.TextAlign.CENTER
    )

    # Botão cadastrar
    botao_cadastrar = ft.ElevatedButton(
        "CADASTRAR",
        width=400,
        bgcolor=parametro[2],
        color=parametro[3],
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=fazer_cadastro
    )

    # Link voltar para login
    voltar_login = ft.TextButton(
        "Já tem uma conta? Faça login",
        style=ft.ButtonStyle(color=parametro[2]),
        on_click=lambda e: callback_login()
    )

    # Container do formulário
    conteudo = ft.Column(
        [
            ft.Container(content=logo, alignment=ft.alignment.center,
                         margin=ft.margin.only(bottom=10)),
            titulo,
            nome_input,
            s_nome_input,
            email_input,
            telefone_input,
            senha_input,
            confirmar_senha_input,
            nota_obrigatorio,
            ft.Container(height=10),
            botao_cadastrar,
            voltar_login,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

    fundo = ft.Container(
        content=conteudo,
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

    # Stack com imagem de fundo e formulário
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
