import database

def menu():
    print('\n1 - Conectar database')
    print('2 - Criar tabela "ativo"')
    print('3 - Criar tabela "transacao"')
    print('4 - Cadastrar ativo')
    print('5 - Listar ativos')
    print('6 - Excluir ativo')


while True:
    menu()
    op = input('\nEscolha uma opção: ')

    if op == '1':
        dbname = input('Nome database: ')
        user = input('Usuário: ')
        password = input('Senha do user: ')
        host = input('Host: ')
        conn = database.Usuario(dbname, user, password, host)
        print('\nA Conexão foi estabelecida com sucesso!')
    elif op == '2':
        database.Usuario.criar_tabela_ativo(conn)
    elif op == '3':
        database.Usuario.criar_tabela_transacao(conn)
    elif op == '4':
        database.Ativo.cadastrar_ativo(conn)
    elif op == '5':
        database.Ativo.listar_ativos(conn)
    elif op == '6':
        database.Ativo.excluir_ativo(conn)
    else:
        print('\nOpção Inválida. Tente Novamente!')