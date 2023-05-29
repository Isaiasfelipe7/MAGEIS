import psycopg2

class Usuario:
    def __init__(self, dbname, user, password, host, port=5432):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    @property
    def dbname(self):
        return self.__dbname
    @dbname.setter
    def dbname(self, valor):
        print('\nSem permissão!')
    
    @property
    def user(self):
        return self.__user
    @user.setter
    def user(self, valor):
        print('\nSem permissão!')
    
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, valor):
        print('\nSem permissão!')
    
    @property
    def host(self):
        return self.__host
    @host.setter
    def host(self, valor):
        print('\nSem permissão!')
    
    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, valor):
        print('\nSem permissão!')

    def conectar_database(self):
        try:
            conec = psycopg2.connect(
                dbname=self.__dbname,
                user=self.__user,
                password=self.__password,
                host=self.__host,
                port=self.__port
            )
            return conec
        except psycopg2.Error as e:
            print('\nNão foi possivel estabelecer a conexão com o banco de dados.')
            print(e)
            exit()

    def criar_tabela_ativo(self):
        insert = Usuario(self.__dbname, self.__user, self.__password, self.__host, self.__port)
        conec = Usuario.conectar_database(insert)
        cur = conec.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ativo (
                id_ativo INT PRIMARY KEY,
                nome VARCHAR(5) NOT NULL,
                valor FLOAT NOT NULL
            );
            """)
        conec.commit()
        conec.close()

        print('\nTabela "ativo" criada com sucesso!')

    def criar_tabela_transacao(self):
        insert = Usuario(self.__dbname, self.__user, self.__password, self.__host, self.__port)
        conec = Usuario.conectar_database(insert)
        cur = conec.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transacao (
                id_transacao INT PRIMARY KEY,
                tipo VARCHAR(1) NOT NULL,
                qtd INT NOT NULL,
                corretagem FLOAT NOT NULL,
                operacao FLOAT NOT NULL,
                taxa_b3 FLOAT NOT NULL,
                total FLOAT NOT NULL,
                preco_medio FLOAT NOT NULL,
                resultado VARCHAR(1) NOT NULL,
                id_ativo INT NOT NULL,
                FOREIGN KEY (id_ativo) REFERENCES ativo(id_ativo)
            );
            """)
        conec.commit()
        conec.close()

        print('Tabela "transacao" criada com sucesso!')

class Ativo:
    def __init__(self, id, nome, valor):
        self.__id = id
        self.__nome = nome
        self.__valor = valor
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, valor):
        print('\nSem permissão!')

    @property
    def nome(self):
        return self.__nome
    
    @property
    def valor(self):
        return self.__valor
    
    
    def cadastrar_ativo(self):
        self.__id = int(input('ID do ativo: '))
        self.__nome = input('Nome do ativo: ')
        self.__valor = input('Valor do ativo: ')
        
        conec = Usuario.conectar_database(self)
        cur = conec.cursor()
        cur.execute("INSERT INTO ativo (id_ativo, nome, valor) VALUES (%s, %s, %s)", (self.__id, self.__nome, self.__valor))
        conec.commit()
        conec.close()

        print(f'\nAtivo: ID - {self.__id}, Nome - {self.__nome}, Valor - R${self.__valor}\nCadastrado com sucesso!')
    
    def listar_ativos(self):
        conec = Usuario.conectar_database(self)
        cur = conec.cursor()
        cur.execute("SELECT * FROM ativo")
        ativo = cur.fetchall()
        if not ativo:
            print('\nNão há nenhum ativo cadastrado!')
        else:
            print('\n| Lista de Ativos |')
            for act in ativo:
                print(f'\n{act[0]} - {act[1]} - R${act[2]}')

    def excluir_ativo(self):
        self.__id = int(input('Informe o ID do ativo que deseja excluir: '))
        
        conec = Usuario.conectar_database(self)
        cur = conec.cursor()
        cur.execute("SELECT * FROM ativo WHERE id_ativo = %s", (self.__id,))

        ativo = cur.fetchone()
        if ativo is None:
            print(f'\nO ativo com o ID {self.__id} não foi encontrado!')
        else:
            cur.execute("DELETE FROM ativo WHERE id_ativo = %s", (self.__id,))
            conec.commit()
            conec.close()
            print(f'\nO ativo com o ID {self.__id}, foi excluído com sucesso!')

class Transacao:
    def __init__(self, id_transacao, tipo, qtd, corretagem, operacao, taxa_b3):
        self.__id_transacao = id_transacao
        self.__tipo = tipo
        self.__qtd = qtd
        self.__corretagem = corretagem
        self.__operacao = operacao
        self.__taxa_b3 = taxa_b3