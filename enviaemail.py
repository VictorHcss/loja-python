import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_email(recipient_email, nova_senha):
    try:
        remetente = "contato@curtaaulacurta.com.br"  # ideal: vir da tabela parametro
        senha = "Senac123**"
        servidor_smtp = "mail.curtaaulacurta.com.br"
        porta = 587

        mensagem = MIMEMultipart()
        mensagem["From"] = remetente
        mensagem["To"] = recipient_email
        mensagem["Subject"] = "Recuperação de Senha - GeekHub"
        corpo = f"Sua nova senha temporária é: {nova_senha}\n\nAltere-a após o login."
        mensagem.attach(MIMEText(corpo, "plain"))

        with smtplib.SMTP(servidor_smtp, porta) as servidor:
            servidor.ehlo()
            if servidor.has_extn("STARTTLS"):
                servidor.starttls()
                servidor.ehlo()

            servidor.login(remetente, senha)
            servidor.sendmail(remetente, recipient_email, mensagem.as_string())

        return True

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False
