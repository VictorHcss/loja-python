import sqlite3
import os


def bdconfig():
    """Função para buscar parâmetros do sistema"""
    try:
        # Criar pasta assets se não existir
        if not os.path.exists('assets'):
            os.makedirs('assets')

        conexao = sqlite3.connect('assets/geekhub.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM parametro')
        parametro = cursor.fetchone()
        conexao.close()

        if parametro:
            return parametro
        else:
            # Retornar valores padrão se não encontrar
            return ("./img/logo.jpg", "GeekHub", "#4FC3F7", "#FFFFFF")
    except Exception as e:
        print(f"Erro ao buscar parâmetros: {e}")
        # Retornar valores padrão em caso de erro
        return ("./img/logo.jpg", "GeekHub", "#4FC3F7", "#FFFFFF")


class bd:
    """Classe para gerenciar conexões com o banco de dados"""

    @staticmethod
    def conectar():
        """Conecta ao banco de dados"""
        if not os.path.exists('assets'):
            os.makedirs('assets')
        return sqlite3.connect('assets/geekhub.db')

    @staticmethod
    def executar_query(query, parametros=None):
        """Executa uma query no banco"""
        try:
            conexao = bd.conectar()
            cursor = conexao.cursor()

            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)

            conexao.commit()
            conexao.close()
            return True
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return False

    @staticmethod
    def buscar_um(query, parametros=None):
        """Busca um registro no banco"""
        try:
            conexao = bd.conectar()
            cursor = conexao.cursor()

            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)

            resultado = cursor.fetchone()
            conexao.close()
            return resultado
        except Exception as e:
            print(f"Erro ao buscar registro: {e}")
            return None

    @staticmethod
    def buscar_todos(query, parametros=None):
        """Busca todos os registros no banco"""
        try:
            conexao = bd.conectar()
            cursor = conexao.cursor()

            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)

            resultado = cursor.fetchall()
            conexao.close()
            return resultado
        except Exception as e:
            print(f"Erro ao buscar registros: {e}")
            return []
