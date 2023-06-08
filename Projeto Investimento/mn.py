import db

def menu():
    print('\n1 - Cadastrar')
    print('2 - Editar Transação')
    print('3 - Excluir Transação')
    print('4 - Historico de Transações')
    print('5 - Detalhar por Ativo')
    print('6 - Lucro por Ativo')
    print('7 - Lucro Total da Carteira')
    print('8 - Reiniciar Banco de Dados')
    print('0 - Sair')


while True:

    menu()

    op = input('\nEscolha uma opção: ')

    if op == '1':
        db.cadastrar_dados()
    elif op == '2':
        db.editar_transacao()
    elif op == '3':
        db.excluir_transacao()
    elif op == '4':
        db.mostrar_historico()
    elif op == '5':
        db.detalhamento()
    elif op == '6':
        db.lc_ativo()
    elif op == '7':
        db.lc_carteira()
    elif op == '8':
        db.reiniciar()
    elif op == '0':
        print('Volte logo!')
        break
    else:
        print('Opção Inválida. Tente Novamente!')