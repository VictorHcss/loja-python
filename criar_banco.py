from bdconfig import bd


def popular_banco():
    """Função para popular o banco com dados de teste"""
    print("🚀 Populando banco de dados GeekHub...")
    print("-" * 50)

    # Verificar se já existem parâmetros
    parametros_existentes = bd.buscar_um('SELECT COUNT(*) FROM parametro')
    if not parametros_existentes or parametros_existentes[0] == 0:
        bd.executar_query('''
            INSERT INTO parametro (logomarca, nome, bgcolor, color)
            VALUES (?, ?, ?, ?)
        ''', ("🎮", "GeekHub", "#4FC3F7", "#FFFFFF"))
        print("✅ Parâmetros do sistema criados")

    # Verificar se já existe usuário de teste
    usuario_existente = bd.buscar_um('SELECT COUNT(*) FROM usuario')
    if not usuario_existente or usuario_existente[0] == 0:
        bd.executar_query('''
            INSERT INTO usuario (nome, sobrenome, email, senha, telefone)
            VALUES (?, ?, ?, ?, ?)
        ''', ("Victor", "Silva", "victor@geekhub.com", "123456", "(11) 99999-9999"))
        print("✅ Usuário de teste criado: victor@geekhub.com / 123456")

    # Verificar se já existem produtos
    produtos_existentes = bd.buscar_um('SELECT COUNT(*) FROM produto')
    if not produtos_existentes or produtos_existentes[0] == 0:
        produtos = [
            # Periféricos
            ("Teclado Mecânico RGB", "Teclado mecânico gamer com switches blue e iluminação RGB",
             299.99, 15, "Periféricos", "🎮"),
            ("Mouse Gamer 12000 DPI", "Mouse gamer de alta precisão com 12000 DPI",
             159.99, 25, "Periféricos", "🖱️"),
            ("Mousepad XXL", "Mousepad gamer extra grande",
             79.99, 30, "Periféricos", "🎯"),

            # Áudio
            ("Headset Gamer 7.1", "Headset com som surround 7.1 virtual",
             249.99, 20, "Áudio", "🎧"),
            ("Caixa de Som RGB", "Caixa de som 2.1 com iluminação RGB",
             199.99, 12, "Áudio", "🔊"),

            # Monitores
            ("Monitor 24\" 144Hz", "Monitor gamer Full HD 144Hz",
             899.99, 8, "Monitores", "🖥️"),
            ("Monitor Ultrawide 34\"", "Monitor ultrawide QHD",
             1599.99, 5, "Monitores", "📺"),

            # Hardware
            ("Placa de Vídeo RTX 4060", "GPU NVIDIA GeForce RTX 4060 8GB",
             2299.99, 6, "Hardware", "💻"),
            ("Processador AMD Ryzen 7", "CPU AMD Ryzen 7 5700X",
             1199.99, 10, "Hardware", "⚡"),
            ("Memória RAM 16GB", "Kit 2x8GB DDR4 3200MHz RGB",
             399.99, 18, "Hardware", "💾"),

            # Jogos
            ("Cyberpunk 2077", "RPG futurístico em mundo aberto",
             149.99, 50, "Jogos", "🎮"),
            ("The Witcher 3", "RPG épico com mais de 100 horas",
             89.99, 35, "Jogos", "⚔️"),
            ("FIFA 24", "Simulador de futebol mais realista", 199.99, 40, "Jogos", "⚽"),

            # Móveis
            ("Cadeira Gamer Pro", "Cadeira ergonômica com apoio lombar",
             799.99, 12, "Móveis", "🪑"),
            ("Mesa Gamer RGB", "Mesa com iluminação RGB integrada",
             599.99, 8, "Móveis", "🏠"),

            # Acessórios
            ("Webcam 4K", "Webcam 4K para streaming", 299.99, 15, "Acessórios", "📹"),
            ("Controle Sem Fio", "Controle wireless com vibração",
             179.99, 22, "Acessórios", "🎮"),
        ]

        for produto in produtos:
            bd.executar_query('''
                INSERT INTO produto (nome, descricao, preco, estoque, categoria, imagem)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', produto)

        print(f"✅ {len(produtos)} produtos criados!")

    print("-" * 50)
    print("✅ Banco populado com sucesso!")
    print("\n📋 Credenciais de teste:")
    print("Email: victor@geekhub.com")
    print("Senha: 123456")


if __name__ == "__main__":
    popular_banco()
    print("\nPressione Enter para continuar...")
    input()
