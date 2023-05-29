import psycopg2

class GerenciarBanco:
    def __init__(self, dbname, user, password, port=5432, host='raja.db.elephantsql.com'):
        self.dbname = dbname
        self.__user = user
        self.__password = password
        self.__port = port
        self.host = host
        
    def conectar_database(self):
        try:
            conec = psycopg2.connect(
                dbname=self.dbname,
                user=self.__user,
                password=self.__password,
                port=self.__port,
                host=self.host
            )
            
            return conec
        
        except psycopg2.Error as e:
            print('\nNão foi possível estabelecer a conexão com o banco de dados.')
            print(e)
            exit()

    def tabela_ativos(self):
        insert = GerenciarBanco(self.dbname, self.__user, self.__password)
        conec = GerenciarBanco.conectar_database(insert)
        cur = conec.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ativos (
                id_ativo INT PRIMARY KEY,
                nome TEXT NOT NULL,
                qtd INT NOT NULL,
                valor NUMERIC(10,2) NOT NULL
            );
        """)
        conec.commit()
        
        print('\nTabela "ativos" criada com sucesso!')

    def tabela_transacoes(self):
        insert = GerenciarBanco(self.dbname, self.__user, self.__password)
        conec = GerenciarBanco.conectar_database(insert)
        cur = conec.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transacoes(
                id INT PRIMARY KEY,
                data DATE NOT NULL,
                tipo TEXT NOT NULL,
                valor NUMERIC(10,2) NOT NULL,
                qtd INT NOT NULL,
                corretora TEXT NOT NULL,
                id_ativo INT NOT NULL,
                FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo)
            );
        """)
        conec.commit()

        print('\nTabela "transacoes" criada com sucesso')
    
    def dbname(self):
        return self.dbname
    
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
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, valor):
        print('\nSem permissão!')

    def host(self):
        return self.host
        
class Ativo:
    def __init__(self, id, nome, qtd, valor):
        self.__id = id
        self.nome = nome
        self.qtd = qtd
        self.valor = valor

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self):
        print('\nPrimary key')

    def nome(self):
        return self.nome

    def qtd(self):
        return self.qtd
    
    def valor(self):
        return self.valor

    def cadastrar_ativos(self):
        self.__id = int(input('ID ativo: '))
        self.nome = str(input('Nome do ativo: '))
        self.qtd = int(input('Quantidade: '))
        self.valor = float(input('Valor do ativo: '))

        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('INSERT INTO ativos (id_ativo,nome, qtd, valor) VALUES (%s,%s, %s, %s)', (self.__id,self.nome, self.qtd, self.valor))
        conec.commit()

        print(f'\nAtivo: {self.nome} cadastrado com sucesso!')

    def listar_ativos(self):
        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('SELECT * FROM ativos')
        ativo = cur.fetchall()
        if not ativo:
            print('\nNão hã nenhum ativo cadastrado!')
        else:
            print('\n==== = LISTA DE ATIVOS = ====')
            for act in ativo:
                print(f'\n{act[0]} - {act[1]}: {act[3]}BRL ({act[2]})')
    
    def exluir_ativo(self):
        id = int(input('Informe o ID do ativo que deseja excluir: '))
        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('SELECT * FROM ativos WHERE id_ativo = %s', (id,))
        ativo = cur.fetchone()
        if ativo is None:
            print('\nO ID do ativo informado não foi encontrado!')
        else:
            cur.execute('DELETE FROM ativos WHERE id_ativo = %s', (id,))
            conec.commit()
            print(f'\nO Ativo com o ID informado, foi exluído com sucesso!')
        
class Transacoes:
    def __init__(self, id, data, tipo, valor, qtd, corretora, id_ativo):
        self.__id = id
        self.data = data
        self.tipo = tipo
        self.valor = valor
        self.qtd = qtd
        self.corretora = corretora
        self.__id_ativo = id_ativo

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, valor):
        print('\nPrimary key')

    @property
    def id_ativo(self):
        return self.__id_ativo
    
    @id_ativo.setter
    def id_ativo(self, valor):
        print('\nSem permissão!')

    def data(self):
        return self.data
    
    def tipo(self):
        return self.tipo
    
    def valor(self):
        return self.valor
    
    def qtd(self):
        return self.qtd
    
    def corretora(self):
        return self.corretora
    
    def realizar_transacao(self):
        self.__id = int(input('Informe o ID da transação: '))
        self.data = input('Data da transação (AAAA-MM-DD): ')
        self.tipo = str(input('Tipo da transação (compra/venda): '))
        self.valor = float(input('Valor da transação: '))
        self.qtd = int(input('Quantidade negociada: '))
        self.corretora = str(input('Nome da corretora: '))
        self.__id_ativo = int(input('Informe o ID do ativo negociado: '))

        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('INSERT INTO transacoes (id, data, tipo, valor, qtd, corretora, id_ativo) VALUES (%s, %s, %s, %s, %s, %s, %s)', (self.__id, self.data, self.tipo, self.valor, self.qtd, self.corretora, self.__id_ativo))
        conec.commit()
        print('\nTransação realizada com sucesso!')

    def listar_transacoes(self):
        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('SELECT * FROM transacoes')
        transacao = cur.fetchall()

        if not transacao:
            print('\nNão há nenhma transação realizada!')
        else:
            print('\n==== = LISTA DE TRANSAÇÕES = ====')
            for trans in transacao:
                cur.execute('SELECT nome FROM ativos WHERE id_ativo=%s', (trans[6],))
                nome_ativo = cur.fetchone()[0]
                print(f'\n{trans[0]} - {trans[1]} - {trans[2]} - {trans[4]} unidades de {nome_ativo} na corretora {trans[5]} por {trans[3]}BRL cada.')

    def excluir_transacao(self):
        self.__id = int(input('ID da transação que deseja excluir: '))
        conec = GerenciarBanco.conectar_database(self)
        cur = conec.cursor()
        cur.execute('SELECT * FROM transacoes WHERE id = %s', (self.__id,))
        transacao = cur.fetchone()

        if transacao is None:
            print('\nTransação não encontrada!')
        else:
            cur.execute('DELETE FROM transacoes WHERE id = %s', (self.__id,))
            conec.commit()
            print(f'\nA transação com o ID - {self.__id}, foi excluída com sucesso!')
