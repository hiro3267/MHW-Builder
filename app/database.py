import sqlite3
from pathlib import Path

# Caminho para o arquivo builds.db na raiz do projeto
DB_PATH = Path(__file__).resolve().parent.parent / "builds.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                dados TEXT NOT NULL,
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
