from mysql.connector import connect

conexao = connect(
    
    host="localhost",
    port=3306,
    user="root",
    password="senha123"
)

cursor = conexao.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS Huawey_DB')