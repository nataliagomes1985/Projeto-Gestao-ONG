import sqlite3
from datetime import datetime

# Conexão com o banco de dados
conexao = sqlite3.connect('gestao_financeira.db')
cursor = conexao.cursor()

# Criação das tabelas
def criar_tabelas():
    cursor.execute('''CREATE TABLE IF NOT EXISTS doadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        email TEXT,
        telefone TEXT,
        endereco TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        fornecedor TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS doacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL NOT NULL,
        item TEXT,
        data TEXT NOT NULL,
        doador_id INTEGER,
        FOREIGN KEY (doador_id) REFERENCES doadores (id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL, -- 'despesa' ou 'doacao'
        valor REAL NOT NULL,
        data TEXT NOT NULL
    )''')

    conexao.commit()

# Função para cadastrar um novo doador
def cadastrar_doador():
    print("Cadastro de Doador")
    
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")

    cursor.execute('''INSERT INTO doadores (nome, cpf, email, telefone, endereco)
                      VALUES (?, ?, ?, ?, ?)''', (nome, cpf, email, telefone, endereco))
    conexao.commit()

    print(f"\nDoador {nome} cadastrado com sucesso!\n")

# Função para registrar uma nova despesa
def registrar_despesa():
    print("Registro de Despesa")

    item = input("Item: ")
    quantidade = int(input("Quantidade: "))
    valor = float(input("Valor total: "))
    data = input("Data (YYYY-MM-DD): ")
    fornecedor = input("Fornecedor: ")

    cursor.execute('''INSERT INTO despesas (item, quantidade, valor, data, fornecedor)
                      VALUES (?, ?, ?, ?, ?)''', (item, quantidade, valor, data, fornecedor))
    cursor.execute('''INSERT INTO movimentacoes (tipo, valor, data)
                      VALUES ('despesa', ?, ?)''', (valor, data))
    conexao.commit()

    print(f"\nDespesa de {valor} registrada com sucesso!\n")

# Função para registrar uma nova doação
def registrar_doacao():
    print("Registro de Doação")

    valor = float(input("Valor da doação: "))
    item = input("Item da doação (se aplicável): ")
    data = input("Data (YYYY-MM-DD): ")
    doador_id = int(input("ID do doador: "))

    cursor.execute('''INSERT INTO doacoes (valor, item, data, doador_id)
                      VALUES (?, ?, ?, ?)''', (valor, item, data, doador_id))
    cursor.execute('''INSERT INTO movimentacoes (tipo, valor, data)
                      VALUES ('doacao', ?, ?)''', (valor, data))
    conexao.commit()

    print(f"\nDoação de {valor} registrada com sucesso!\n")

# Função para gerar um relatório baseado em um período
def gerar_relatorio():
    print("Gerar Relatório")

    data_inicio = input("Data de início (YYYY-MM-DD): ")
    data_fim = input("Data de fim (YYYY-MM-DD): ")

    print(f"\nMovimentações entre {data_inicio} e {data_fim}:\n")

    # Relatório de Doações
    cursor.execute('''SELECT d.nome, doa.valor, doa.item, doa.data 
                      FROM doacoes doa
                      JOIN doadores d ON doa.doador_id = d.id
                      WHERE doa.data BETWEEN ? AND ?''', (data_inicio, data_fim))
    doacoes = cursor.fetchall()

    if doacoes:
        print("Doações:")
        for doacao in doacoes:
            print(f"Doador: {doacao[0]}, Valor: {doacao[1]}, Item: {doacao[2]}, Data: {doacao[3]}")
    else:
        print("Nenhuma doação registrada no período.")
    
    # Relatório de Despesas
    cursor.execute('''SELECT item, quantidade, valor, data, fornecedor 
                      FROM despesas
                      WHERE data BETWEEN ? AND ?''', (data_inicio, data_fim))
    despesas = cursor.fetchall()

    if despesas:
        print("\nDespesas:")
        for despesa in despesas:
            print(f"Item: {despesa[0]}, Quantidade: {despesa[1]}, Valor: {despesa[2]}, Data: {despesa[3]}, Fornecedor: {despesa[4]}")
    else:
        print("Nenhuma despesa registrada no período.")

    # Valor total em caixa
    cursor.execute('''SELECT SUM(CASE WHEN tipo = 'doacao' THEN valor ELSE 0 END) - 
                             SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END) 
                      FROM movimentacoes
                      WHERE data BETWEEN ? AND ?''', (data_inicio, data_fim))
    saldo = cursor.fetchone()[0]
    
    print(f"\nValor em caixa no período: {saldo}\n")

# Menu principal
def menu():
    while True:
        print("1. Cadastrar Doador")
        print("2. Registrar Doação")
        print("3. Registrar Despesa")
        print("4. Gerar Relatório")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_doador()
        elif opcao == "2":
            registrar_doacao()
        elif opcao == "3":
            registrar_despesa()
        elif opcao == "4":
            gerar_relatorio()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

# Execução do sistema
if __name__ == "__main__":
    criar_tabelas()
    menu()
