import db

def menu():
    print('\n1 - Cadastrar')
    print('2 - Editar Transação')
    print('3 - Excluir Transação')
    print('4 - Detalhamento')
    print('5 - Historico de Transações')
    print('6 - ')


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
        db.detalhamento()
    elif op == '5':
        db.mostrar_historico()
    elif op == '6':
        pass
    else:
        print('Opção Inválida. Tente Novamente!')
