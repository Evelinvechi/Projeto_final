import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar_bd():

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="Evelin",
            password="Evelin",
            database="loja_pure"
        )
        print("Conexão estabelecida com sucesso!")
        return conexao
    except Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

def criar_tabelas(cursor):
   
    tabelas = {
        "produtos": (
            "CREATE TABLE IF NOT EXISTS produtos ("
            "id INT AUTO_INCREMENT PRIMARY KEY," 
            "nome VARCHAR(200) NOT NULL," 
            "descricao TEXT," 
            "preco DECIMAL(10, 2) NOT NULL," 
            "estoque INT NOT NULL," 
            "categoria VARCHAR(200)"
            ")"
        ),
        "clientes": (
            "CREATE TABLE IF NOT EXISTS clientes ("
            "id INT AUTO_INCREMENT PRIMARY KEY," 
            "nome VARCHAR(100) NOT NULL," 
            "email VARCHAR(100)," 
            "telefone VARCHAR(20)," 
            "endereco TEXT"
            ")"
        ),
        "pedidos": (
            "CREATE TABLE IF NOT EXISTS pedidos ("
            "id INT AUTO_INCREMENT PRIMARY KEY," 
            "cliente_id INT," 
            "produto_id INT," 
            "quantidade INT NOT NULL," 
            "total DECIMAL(10, 2) NOT NULL,"
            "data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP," 
            "FOREIGN KEY (cliente_id) REFERENCES clientes(id)," 
            "FOREIGN KEY (produto_id) REFERENCES produtos(id)"
            ")"
        )
    }

    for nome, sql in tabelas.items():
        try:
            cursor.execute(sql)
            print(f"Tabela '{nome}' criada ou já existente.")
        except Error as erro:
            print(f"Erro ao criar tabela {nome}: {erro}")

def adicionar_produto(cursor):
   
    try:
        nome = input("Nome do produto: ")
        descricao = input("Descrição: ")
        
        while True:
            try:
                preco = float(input("Preço: "))
                if preco > 0:
                    break
                print("O preço deve ser maior que zero.")
            except ValueError:
                print("Por favor, digite um número válido para o preço.")
        
        while True:
            try:
                estoque = int(input("Quantidade em estoque: "))
                if estoque >= 0:
                    break
                print("O estoque não pode ser negativo.")
            except ValueError:
                print("Por favor, digite um número inteiro válido para o estoque.")
        
        categoria = input("Categoria: ")

        cursor.execute(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (%s, %s, %s, %s, %s)",
            (nome, descricao, preco, estoque, categoria)
        )
        print("Produto adicionado com sucesso!")
    except Error as erro:
        print(f"Erro ao adicionar produto: {erro}")

def listar_produtos(cursor):
   
    try:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        
        print("\nLista de Produtos:")
        print("ID | Nome | Descrição | Preço | Estoque | Categoria")
        print("-" * 80)
        for produto in produtos:
            print(f"{produto[0]} | {produto[1]} | {produto[2][:30]}... | €{produto[3]:.2f} | {produto[4]} | {produto[5]}")
    except Error as erro:
        print(f"Erro ao listar produtos: {erro}")

def registrar_cliente(cursor):
  
    try:
        nome = input("Nome do cliente: ")
        email = input("E-mail: ")
        telefone = input("Telefone: ")
        endereco = input("Endereço: ")

        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone, endereco) VALUES (%s, %s, %s, %s)",
            (nome, email, telefone, endereco)
        )
        print("Cliente registrado com sucesso!")
    except Error as erro:
        print(f"Erro ao registrar cliente: {erro}")

def listar_clientes(cursor):
   
    try:
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        print("\nLista de Clientes:")
        print("ID | Nome | Email | Telefone | Endereço")
        print("-" * 80)
        for cliente in clientes:
            print(f"{cliente[0]} | {cliente[1]} | {cliente[2]} | {cliente[3]} | {cliente[4]}")
    except Error as erro:
        print(f"Erro ao listar clientes: {erro}")

def realizar_pedido(cursor, conexao):
   
    try:
        listar_clientes(cursor)
        cliente_id = int(input("ID do cliente: "))
        
        cursor.execute("SELECT id FROM clientes WHERE id = %s", (cliente_id,))
        if not cursor.fetchone():
            print("Cliente não encontrado.")
            return

        listar_produtos(cursor)
        produto_id = int(input("ID do produto: "))
        
        cursor.execute("SELECT preco, estoque FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()
        
        if not produto:
            print("Produto não encontrado.")
            return

        while True:
            try:
                quantidade = int(input("Quantidade: "))
                if quantidade > 0:
                    break
                print("A quantidade deve ser maior que zero.")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")

        if produto[1] >= quantidade:
            total = produto[0] * quantidade
            try:
                cursor.execute(
                    "INSERT INTO pedidos (cliente_id, produto_id, quantidade, total) VALUES (%s, %s, %s, %s)",
                    (cliente_id, produto_id, quantidade, total)
                )
                cursor.execute(
                    "UPDATE produtos SET estoque = estoque - %s WHERE id = %s",
                    (quantidade, produto_id)
                )
                conexao.commit()
                print(f"Pedido realizado com sucesso! Total: €{total:.2f}")
            except Error as erro:
                conexao.rollback()
                print(f"Erro ao realizar pedido: {erro}")
        else:
            print("Estoque insuficiente.")
    except ValueError:
        print("Por favor, digite números válidos para ID do cliente e produto.")
    except Error as erro:
        print(f"Erro ao processar pedido: {erro}")

def listar_pedidos(cursor):
   
    try:
        cursor.execute("""
            SELECT p.id, c.nome as cliente, pr.nome as produto, 
                   p.quantidade, p.total, p.data_pedido
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            JOIN produtos pr ON p.produto_id = pr.id
            ORDER BY p.data_pedido DESC
        """)
        pedidos = cursor.fetchall()
        if not pedidos:
            print("Nenhum pedido registrado.")
            return
        
        print("\nHistórico de Pedidos:")
        print("ID | Cliente | Produto | Quantidade | Total | Data")
        print("-" * 90)
        for pedido in pedidos:
            print(f"{pedido[0]} | {pedido[1]} | {pedido[2]} | {pedido[3]} | €{pedido[4]:.2f} | {pedido[5]}")
    except Error as erro:
        print(f"Erro ao listar pedidos: {erro}")

def menu():

    conexao = conectar_bd()
    if not conexao:
        return

    cursor = conexao.cursor()
    criar_tabelas(cursor)

    while True:
        print("\nMenu Principal:")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Registrar Cliente")
        print("4. Listar Clientes")
        print("5. Realizar Pedido")
        print("6. Listar Pedidos")
        print("7. Sair")

        opcao = input("\nEscolha uma opção: ")

        try:
            if opcao == "1":
                adicionar_produto(cursor)
            elif opcao == "2":
                listar_produtos(cursor)
            elif opcao == "3":
                registrar_cliente(cursor)
            elif opcao == "4":
                listar_clientes(cursor)
            elif opcao == "5":
                realizar_pedido(cursor, conexao)
            elif opcao == "6":
                listar_pedidos(cursor)
            elif opcao == "7":
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida. Tente novamente.")

            conexao.commit()
        except Error as erro:
            conexao.rollback()
            print(f"Erro na operação: {erro}")

    cursor.close()
    conexao.close()
    print("Obrigada por utilizar nosso programa de gerenciamento!")

if __name__ == "__main__":
    menu()