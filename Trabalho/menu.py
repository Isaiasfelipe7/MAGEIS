import db

while True:
    print('\n=== = MENU = ===')
    print('\n1 - Conectar database')
    print('2 - Criar tabelas / "Ativos" e "Transações"')
    print('3 - Cadastrar ativos')
    print('4 - Listar ativos')
    print('5 - Excluir ativo')
    print('6 - Realizar transação')
    print('7 - Listar transações')
    print('8 - Excluir transação')
    print('0 - Sair')
    
    op = input('\nEscolha uma opção: ')
    
    if op == '1':
        dbname = input('Nome database: ')
        user = input('Usuário: ')
        password = input('Senha do user: ')
        conn = db.GerenciarBanco(dbname, user, password)
        db.GerenciarBanco.conectar_database(conn)
        print('\nA conexão foi estabelecida com sucesso!')
        
    elif op == '2':
        conn = db.GerenciarBanco(dbname, user, password)
        db.GerenciarBanco.tabela_ativos(conn)
        db.GerenciarBanco.tabela_transacoes(conn)

    elif op == '3':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Ativo.cadastrar_ativos(conn)

    elif op == '4':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Ativo.listar_ativos(conn)
    
    elif op == '5':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Ativo.exluir_ativo(conn)

    elif op == '6':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Transacoes.realizar_transacao(conn)

    elif op == '7':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Transacoes.listar_transacoes(conn)

    elif op == '8':
        conn = db.GerenciarBanco(dbname, user, password)
        db.Transacoes.excluir_transacao(conn)

    elif op == '0':
        print('\nVocê saiu...')
        break
    else:
        print('\nOpção Inválida. Tente Novamente')
