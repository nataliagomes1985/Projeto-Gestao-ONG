# Projeto Gestão-ONG

Este projeto tem como objetivo fornecer uma solução simples para gerenciar as finanças de uma ONG, permitindo o cadastro de doadores, registro de doações e despesas, controle de movimentações financeiras e geração de relatórios. O sistema é executado via terminal e utiliza um banco de dados SQLite para armazenar as informações.

## Funcionalidades

1. **Cadastro de Doador**: Armazena informações como nome, CPF, e-mail, telefone e endereço dos doadores.
2. **Registro de Despesas**: Permite registrar despesas com detalhes como item, quantidade, valor, data e fornecedor.
3. **Registro de Doações**: Registra doações com valor, item doado, data e o doador que fez a doação.
4. **Gerenciamento Financeiro**: Controla o fluxo financeiro subtraindo o valor das despesas das doações registradas.
5. **Geração de Relatórios**: Gera relatórios financeiros com base em um período especificado pelo usuário, mostrando as doações, despesas e saldo de caixa no período.

## Tabelas no Banco de Dados

O sistema utiliza um banco de dados SQLite, com as seguintes tabelas:

- **doadores**: Armazena informações sobre os doadores.
- **despesas**: Armazena as despesas registradas.
- **doacoes**: Armazena as doações realizadas.
- **movimentacoes**: Armazena as movimentações financeiras (doações e despesas) para facilitar o cálculo do saldo.

## Requisitos

- **Python 3.x**
- **SQLite3** (integrado no Python)
  
## Instalação

1. Clone este repositório para sua máquina local:
   ```bash
   git clone https://github.com/seuusuario/Projeto-Gestao-ONG.git

