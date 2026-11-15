# Loja Python

**GeekHub**: loja virtual desktop desenvolvida em Python com **Flet**, com banco de dados SQLite e envio de e-mails.

## Funcionalidades

- **Cadastro e login** de usuários.
- **"Esqueci minha senha":** gera uma nova senha e envia por e-mail.
- **Catálogo de produtos** com página de detalhes.
- **Carrinho de compras** e finalização do pedido.

## Tecnologias

Python · Flet · SQLite · smtplib

## Estrutura

```text
loja-python/
├── main.py             # Inicia o aplicativo e a navegação
├── criar_banco.py      # Popula o banco com dados de teste
├── bdconfig.py         # Acesso ao banco
├── login.py / cadastro.py / esqueci.py
├── produto.py / detalhe_produto.py
├── carrinho.py / finalizar.py
└── enviaemail.py       # Envio de e-mails
```

## Como executar

```bash
pip install flet
python criar_banco.py   # dados de teste (usuário: victor@geekhub.com / 123456)
python main.py
```

Para o envio de e-mails funcionar, configure o remetente e o servidor SMTP em `enviaemail.py`.

---

Um dos meus primeiros projetos em Python, desenvolvido por [Victor Henrique](https://github.com/VictorHcss).
