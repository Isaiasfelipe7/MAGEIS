import database

class Ativo:
    def __init__(self, id, nome, valor):
        self.__id = id
        self.__nome = nome
        self.__valor = valor

    def criar_tabela_ativo(self):
        cur = conec.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ativo (
                id_ativo INT PRIMARY KEY,
                nome VARCHAR(5) NOT NULL,
                valor NUMERIC(10,2) NOT NULL
            );
            """)
        conec.commit()

        print('\nTabela "ativo" criada com sucesso!')