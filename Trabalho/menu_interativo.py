while True:

    print('\n=== = Menu = ===')
    print('\n1 - Conectar database')
    print('2 - Criar tabelas "ativos" e "transacoes"')
    print('3 - Cadastrar ativo')
    print('4 - Excluir ativo')
    print('5 - Listar ativos')
    print('6 - Cadastrar transação')
    print('7 - Excluir transação')
    print('8 - Listar transações')
    print('0 - Sair')

    op = input('\nEscolha uma opção: ')
    
    if op == '1':
        conectar()
        print('\nConexão estabelecida com sucesso!')
    elif op == '2':
        criar_tabelas()
    elif op == '3':
        ativo.cadastrar_ativo()
    elif op == '4':
        ativo.excluir_ativo()
    elif op == '5':
        ativo.listar_ativos()
    elif op == '6':
        transacoes.cadastrar_transacao()
    elif op == '7':
        transacoes.excluir_transacao()
    elif op == '8':
        transacoes.listar_transacoes()
    elif op == '0':
        print('\nVocê saiu do menu...')
        break
    else:
        print('\nOpção Inválida. Tente Novamente!')
