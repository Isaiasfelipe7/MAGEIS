import psycopg2

def conectar():
    nome_bd = input('Nome do banco de dados: ')
    usuario = input('Usuário do banco de dados: ')
    senha = input('Informe a senha do usuário: ')
    host = input('Informe o host do banco de dados (geralmente é localhost): ')
    porta = input('Informe a porta do banco de dados (geralmente é 5432): ')

    try:
        conn = psycopg2.connect(
            dbname=nome_bd,
            user=usuario,
            password=senha,
            host=host,
            port=porta
        )
        return conn

    except psycopg2.Error as e:
        print('\nNão foi possível estabelecer a conexão com o banco de dados.')
        print(e)
        exit()

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
            id_ativo SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            qtd INTEGER NOT NULL,
            valor NUMERIC(10, 2) NOT NULL
        );
    """)

    print('\ntabela "ativos" criada')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transacoes(
            id_trans SERIAL PRIMARY KEY,
            data DATE NOT NULL,
            tipo TEXT NOT NULL,
            valor NUMERIC (10,2) NOT NULL,
            quantidade INTEGER NOT NULL,
            corretora TEXT NOT NULL,
            id_ativo INTEGER NOT NULL,
            FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo)
        );
    """)
    print('tabela "transacoes" criada')
    conn.commit()

class ativo:
    def __init__(self, id_ativo, qtd, nome, valor):
        self.__id_ativo = id_ativo
        self.__nome = nome
        self.__qtd = qtd
        self.__valor = valor

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO ativos (id_ativo,nome, qtd, valor) VALUES (%s,%s, %s, %s)", (self.__id_ativo,self.__nome, self.__qtd, self.__valor))
        conn.commit()

    @property
    def id_ativo(self):
        return self.__id_ativo

    @id_ativo.setter
    def id_ativo(self, id_ativo):
        self.__id_ativo = id_ativo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome
        cur = conn.cursor()
        cur.execute("UPDATE ativos SET nome=%s WHERE id_ativo=%s", (self.__nome, self.__id_ativo))
        conn.commit()

    @property
    def qtd(self):
        return self.__qtd

    @qtd.setter
    def qtd(self,qtd):
        self.__qtd = qtd
        cur = conn.cursor()
        cur.execute("UPDATE ativos SET qtd=%s WHERE id_ativo=%s", (self.__qtd, self.__id_ativo))
        conn.commit()

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = valor
        cur = conn.cursor()
        cur.execute("UPDATE ativos SET valor=%s WHERE id_ativo=%s", (self.__valor, self.__id_ativo))
        conn.commit()

    def cadastrar_ativo():
        cadastrar_ativo = ativo(id_ativo=int(input('Informe o ID do ativo: ')), qtd=int(input('Informe a quantidade do ativo: ')), nome=str(input('Informe o nome do ativo: ')), valor=float(input('Informe o valor do ativo: ')))

        print(f'\nAtivo cadastrado com sucesso!')

    def excluir_ativo():
        id_ativo = int(input('Informe o ID do ativo que deseja excluir: '))
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ativos WHERE id_ativo = %s", (id_ativo,))
        atv = cur.fetchone()
        if atv is None:
            print('\nAtivo não encontrado!')
        else:
            cur.execute("DELETE FROM ativos WHERE id_ativo = %s", (id_ativo,))
            conn.commit()
            print('\nO ativo informado foi excluído com sucesso!')

    def listar_ativos():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ativos")
        ativos = cur.fetchall()
        if not ativos:
            print('\nNão há nenhum ativo cadastrado!')
        else:
            print('\n==== = LISTA DE ATIVOS = ====')

            for ativo in ativos:
                print(f'\n{ativo[0]} - {ativo[1]}: {ativo[3]}BRL ({ativo[2]})')


    def __str__(self):
        return f'\n{self.__nome}: {self.__valor}BRL ({self.__qtd})'

class transacoes:
    def __init__(self,id_transacao,data,quantidade_trans,tipo,corretora,valor_trans,id_ativo):
        self.__id_transacao = id_transacao
        self.__data = data
        self.__tipo =  tipo
        self.__valor_trans = valor_trans
        self.__quantidade_trans = quantidade_trans
        self.__corretora = corretora
        self.__id_ativo = id_ativo
        
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO transacoes (id_trans, data, tipo, valor, quantidade, corretora,id_ativo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (self.__id_transacao,self.__data, self.__tipo, self.__valor_trans,self.__quantidade_trans,self.__corretora, self.__id_ativo))
        conn.commit()


    @property
    def id_transacao(self):
        return self.__id_transacao
    
    @id_transacao.setter
    def id_transacao(self,id_transacao):
        self.__id_transacao = id_transacao
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self,data):
        self.__data = data
    
    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self,tipo):
        self.__tipo = tipo
        cur = conn.cursor()
        cur.execute("UPDATE transacoes SET tipo=%s WHERE id_transacao=%s", (self.__tipo, self.__id_transacao))
        conn.commit()

    @property
    def valor(self):
        return self.__valor
    
    @valor.setter
    def valor(self,valor_trans):
        self.__valor_trans = valor_trans
        cur = conn.cursor()
        cur.execute("UPDATE transacoes SET valor=%s WHERE id_transacao=%s", (self.__valor_trans, self.__id_transacao))
        conn.commit()

    @property
    def quantidade_trans(self):
        return self.__quantidade_trans
    
    @quantidade_trans.setter
    def quantidade_trans(self,quantidade_trans):
        self.__quantidade_trans = quantidade_trans
        cur = conn.cursor()
        cur.execute("UPDATE transacoes SET quantidade=%s WHERE id_transacao=%s", (self.__quantidade_trans, self.__id_transacao))
        conn.commit()

    @property
    def corretora(self):
        return self.__corretora
    
    @corretora.setter
    def corretora(self,corretora):
        self.__corretora = corretora
        cur = conn.cursor()
        cur.execute("UPDATE transacoes SET corretora=%s WHERE id_transaco=%s", (self.__corretora, self.__id_transacao))
        conn.commit()

    @property
    def id_ativo(self):
        return self.__id_ativo

    @id_ativo.setter
    def id_ativo(self, id_ativo):
        self.__id_ativo = id_ativo

    def cadastrar_transacao():
        cadastrar = transacoes(id_transacao=int(input('Informe o ID da transação: ')),data=input('Informe a data da transação (aaaa-mm--dd): '), tipo=input('Informe o tipo da transação (compra ou venda): '), valor_trans=float(input('Informe o valor da transação: ')), quantidade_trans=int(input('Informe a quantidade negociada: ')), corretora=input('Informe o nome da corretora: '), id_ativo=int(input('Informe o ID do ativo negociado: ')))
        print('\nTransação cadastrada com sucesso!')

    def excluir_transacao():
        id_transacao = int(input('Informe o ID da transação que deseja excluir: '))
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transacoes WHERE id_trans = %s", (id_transacao,))
        trans = cur.fetchone()

        if trans is None:
            print('\nTransação não encontrada!')
        else:
            cur.execute("DELETE FROM transacoes WHERE id_trans = %s", (id_transacao,))
            conn.commit()
            print('\nA transação informada foi excluída com sucesso!')

    def listar_transacoes():
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transacoes")
        rows = cur.fetchall()
        
        if not rows:
            print('\nNão há transações cadastradas!')
        else:
            print('\n=== = LISTA DE TRANSAÇÕES = ===')

            for row in rows:
                cur.execute("SELECT nome FROM ativos WHERE id_ativos=%s", (row[6],))
                nome_ativo = cur.fetchone()[0]
                print(f'\n{row[0]} - {row[1]} - {row[2]} - {row[4]} unidades de {nome_ativo} na corretora {row[5]} por {row[3]}BRL cada.')
    

    def __str__(self):
        return f'Transação de id: {self.__id_transacao}, no dia de {self.__data}, no valor total de {self.__valor}, com um total de {self.__quantidade} ações, na corretora {self.__corretora}.'

def main():

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

if __name__ == '__main__':
    main()
    