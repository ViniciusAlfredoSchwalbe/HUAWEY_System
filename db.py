from mysql.connector import connect
from contextlib import contextmanager

parametros = dict(
    host="localhost",
    port=3306,
    user="root",
    password="senha123",
    database="huawey_db" 
)
@contextmanager
def nova_conexao():
    conexao = connect(**parametros)
    try:
        yield conexao
    finally:
        if(conexao and conexao.is_connected()):
            conexao.close()

