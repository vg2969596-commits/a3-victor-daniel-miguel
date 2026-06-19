import sqlite3

def criar_banco():
    # Conecta ao arquivo do banco (se não existir, ele cria automaticamente)
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    
    # Criação da tabela de pets com os campos obrigatórios solicitados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especie TEXT NOT NULL,
        raca TEXT NOT NULL,
        idade INTEGER NOT NULL,
        nome_tutor TEXT NOT NULL
    )
    """)
    
    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados e tabela 'pets' inicializados com sucesso!")

if __name__ == "__main__":
    criar_banco()