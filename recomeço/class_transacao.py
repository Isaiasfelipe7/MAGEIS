import database

class Transacao:
    def __init__(self, id_transacao, tipo, qtd, corretagem, operacao, taxa_b3, total, preco_medio, resultado):
        self.__id_transacao = id_transacao
        self.__tipo = tipo
        self.__qtd = qtd
        self.__corretagem = corretagem
        self.__operacao = operacao
        self.__taxa_b3 = taxa_b3
        self.__total = total
        self.__preco_medio = preco_medio
        self.__resultado = resultado

    def criar_tabela_transacao(self):
        insert = database.Usuario.conectar_database()
        pass