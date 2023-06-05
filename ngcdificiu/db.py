import psycopg2
import random
from tabulate import tabulate
from prettytable import PrettyTable

class investimentos:
    def __init__(self,ativo,quantidade, valor_unit, taxa_corretagem, tipo_transacao, valor_operacao=0.0,  b3=0.0, valor_total=0.0, preco_medio = 0, resultado = None, total_lc = 0):
        self.__codigo  = criar_cod()
        self.__ativo = ativo
        self.__quantidade = quantidade
        self.__valor_unit = valor_unit
        self.__taxa_corretagem = taxa_corretagem
        self.__tipo_transacao = tipo_transacao

        self.__b3 = b3
        self.__valor_operacao = valor_operacao
        self.__valor_total = valor_total
        self.__preco_medio = preco_medio
        self.__resultado = resultado
        self.__total_lc = total_lc


    @property
    def codigo(self):
        return self.__codigo
    @property
    def ativo(self):
        return self.__ativo
    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def valor_unit(self):
        return self.__valor_unit
    @property
    def taxa_corretagem(self):
        return self.__taxa_corretagem
    @property
    def tipo_transacao(self):
        return self.__tipo_transacao
    @property
    def b3(self):
        return self.__b3
    @property
    def valor_operacao(self):
        return self.__valor_operacao
    @property
    def valor_total(self):
        return self.__valor_total
    @property
    def preco_medio(self):
        return self.__preco_medio
    @property
    def resultado(self):
        return self.__resultado
    @property
    def total_lc(self):
        return self.__total_lc
    

    def calc(self):
        self.__valor_operacao = self.__valor_unit * self.__quantidade
        self.__b3 = self.__valor_operacao * 0.03 / 100
        self.__valor_total = self.__valor_operacao + self.__taxa_corretagem + self.__b3


    def salvarDados(self):
        conn = psycopg2.connect(database="sam", 
                                user="postgres", 
                                password="postgres", 
                                host="localhost", 
                                port="5432")
            
        cur = conn.cursor()
        cur.execute("INSERT INTO investimentos VALUES(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)", (self.__codigo,self.ativo,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao,  self.__b3, self.__valor_total, 0.0, self.__resultado, 0.0))
        conn.commit()
        cur.close()
        conn.close()
        


    def atualizarDados(self):     
        conn = psycopg2.connect(database="sam", 
                                user="postgres", 
                                password="postgres", 
                                host="localhost", 
                                port="5432")

        cur = conn.cursor()

        cur.execute('UPDATE investimentos SET quantidade = %s, valor_unit = %s, taxa_corretagem = %s, tipo_transacao = %s, valor_operacao = %s, b3 = %s, valor_total = %s, preco_medio = %s, resultado = %s, total_lc = %s WHERE codigo = %s', 
                    (self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao, self.__b3, self.__valor_total, self.__preco_medio, self.__resultado,self.__total_lc, self.__codigo))
        conn.commit()
        cur.close()
        conn.close()


    def precoMedio(self):
        conn = psycopg2.connect(database="sam", 
                                user="postgres", 
                                password="postgres", 
                                host="localhost", 
                                port="5432") 
        cur = conn.cursor()
        preco_medio = self.valor_total / self.quantidade
        cur.execute("UPDATE investimentos SET preco_medio = %s WHERE codigo = %s", (preco_medio, self.__codigo))
        conn.commit()
        conn.close()    
        cur.close()


    def lucro_prejuizo(self):
        conn = psycopg2.connect(database="sam", 
                                user="postgres", 
                                password="postgres", 
                                host="localhost", 
                                port="5432") 
        cur = conn.cursor()
        l_c = (self.__valor_unit - self.__preco_medio) * self.quantidade
        if l_c > 0: 
            rest = 'LUCRO'
        else:
            rest = 'PREJUIZO'
        
        cur.execute('UPDATE investimentos SET resultado = %s, total_lc = %s WHERE codigo = %s', (rest,l_c,self.__codigo))
        conn.commit()
        conn.close()
        cur.close()


def lc_ativo():
    conn = psycopg2.connect(database="sam", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", 
                            port="5432")
    cur = conn.cursor()
    ativo = input('Insira o nome do ativo: ')
    cur.execute('SELECT total_lc FROM investimentos WHERE ativo = %s', (ativo))
    conn.commit()
    res = cur.fetchall()
    for row in res:
        print(row)
    conn.close()
    cur.close()


def lc_carteira():
    conn = psycopg2.connect(database="sam", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", 
                            port="5432") 
    cur = conn.cursor()
    cur.execute('SELECT SUM(total_lc) as total_lucro FROM investimentos')
    conn.commit()
    res = cur.fetchall()
    print(res)
    conn.close()
    cur.close()


def criar_cod():
    cod = ''.join(random.choices('0123456789', k=5))
    return cod


def detalhamento():
    conn = psycopg2.connect(database="sam", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", 
                            port="5432")
    cur = conn.cursor()
    ativo = input('Insira o ativo da transação: ').upper()
    cur.execute("select * from investimentos where ativo = %s", (ativo,))
    res = cur.fetchall()
    for row in res:
        print(row)
    
    conn.close()
    cur.close()


def cadastrar_dados():
    ativo = input('Insira o nome do ativo: ').upper()
    quantidade = int(input('Insira a quantidade: '))
    valor_unit = float(input('Insira o valor unitário do ativo: '))
    taxa_corretagem = float(input('Insira a corretagem: '))
    tipo_op = input('Insira o tipo de transação: ').upper()[0]
    inv = investimentos(ativo, quantidade, valor_unit, taxa_corretagem, tipo_op)
    if tipo_op == 'C':
        inv.calc()
        inv.salvarDados()
        inv.precoMedio()
        print('Sucesso!')
    else:
        inv.calc()
        inv.precoMedio()
        inv.lucro_prejuizo()

def editar_transacao():
    conn = psycopg2.connect(
        database="sam",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    codigo = input('Insira o código da transação: ')

   
    cur.execute("SELECT * FROM investimentos WHERE codigo = %s", (codigo,))
    transaction = cur.fetchone()

    if transaction:
        
        print("\nDetalhes da transação:")
        print("Código:", transaction[0])
        print("Ativo:", transaction[1])
        print("Quantidade:", transaction[2])
        print("Valor Unitário:", transaction[3])
        print("Taxa de Corretagem:", transaction[4])
        print("Tipo de Transação:", transaction[5])

        
        quantidade = int(input('Insira a nova quantidade: '))
        valor_unit = float(input('Insira o novo valor unitário do ativo: '))
        taxa_corretagem = float(input('Insira a nova corretagem: '))

        
        cur.execute("""
            UPDATE investimentos
            SET quantidade = %s, valor_unit = %s, taxa_corretagem = %s
            WHERE codigo = %s
        """, (quantidade, valor_unit, taxa_corretagem, codigo))
        conn.commit()

        
        inv = investimentos(
            ativo=transaction[1],
            quantidade=quantidade,
            valor_unit=valor_unit,
            taxa_corretagem=taxa_corretagem,
            tipo_transacao=transaction[5],

        )
        inv.calc()
        inv.precoMedio()
        inv.lucro_prejuizo()
        inv.atualizarDados()
        
        cur.execute("""
            UPDATE investimentos
            SET valor_operacao = %s, b3 = %s, valor_total = %s, preco_medio = %s, resultado = %s, total_lc = %s
            WHERE codigo = %s
        """, (
            inv.valor_operacao, inv.b3, inv.valor_total,
            inv.preco_medio, inv.resultado, inv.total_lc,
            codigo
        ))
        conn.commit()


        print("Transação atualizada com sucesso.")
    else:
        print("Transação não encontrada.")

    conn.close()
    cur.close()



def excluir_transacao():
    conn = psycopg2.connect(
        database="sam",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    codigo = input('Insira o código da transação: ')

    cur.execute("SELECT * FROM investimentos WHERE codigo = %s", (codigo,))
    transactions = cur.fetchall()

    if transactions:
        print("Foram encontradas as seguintes transações com o código", codigo)
        for i, transaction in enumerate(transactions):
            print("Transação", i + 1)
            print("Código:", transaction[0])
            print("Ativo:", transaction[1])
            print("Quantidade:", transaction[2])
            print("Valor Unitário:", transaction[3])
            print("Taxa de Corretagem:", transaction[4])
            print("Tipo de Transação:", transaction[5])
            print("--------------------------------")

       
        while True:
            choice = input("Digite o número da transação que deseja excluir (ou '0' para cancelar): ")
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(transactions):
                    break
            print("Opção inválida. Tente novamente.")

        if choice != 0:
            transaction = transactions[choice - 1]

            print("Detalhes da transação selecionada:")
            print("Código:", transaction[0])
            print("Ativo:", transaction[1])
            print("Quantidade:", transaction[2])
            print("Valor Unitário:", transaction[3])
            print("Taxa de Corretagem:", transaction[4])
            print("Tipo de Transação:", transaction[5])

            
            confirm = input("Tem certeza que deseja excluir esta transação? (S/N): ")
            if confirm.upper() == "S":
                
                cur.execute("DELETE FROM investimentos WHERE codigo = %s", (transaction[0],))
                conn.commit()
                print("Transação excluída com sucesso.")
            else:
                print("Operação de exclusão cancelada.")
    else:
        print("Nenhuma transação encontrada com o código", codigo)

    conn.close()
    cur.close()

def listar_ativos():
    conn = psycopg2.connect(
        database="sam",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT ativo FROM investimentos")
    ativos = cur.fetchall()

    if ativos:
        print("Ativos disponíveis:")
        for ativo in ativos:
            print(ativo[0])
    else:
        print("Nenhum ativo encontrado.")

    conn.close()
    cur.close()

# Biblioteca -  pip install tabulate
def mostrar_historico():
    conn = psycopg2.connect(
        database="sam",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM investimentos ORDER BY codigo")
    transacoes = cur.fetchall()

    if transacoes:
        headers = [col[0] for col in cur.description]
        tabela_transacoes = []

        for transacao in transacoes:
            tabela_transacoes.append(list(transacao))

        print(tabulate(tabela_transacoes, headers=headers, tablefmt="fancy_grid"))
    else:
        print("Nenhuma transação encontrada.")

    conn.close()
    cur.close()

# Biblioteca - pip install prettytable
def mostrar_historico2():
    conn = psycopg2.connect(
        database="sam",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM investimentos ORDER BY codigo")
    transacoes = cur.fetchall()

    if transacoes:
        tabela = PrettyTable()
        tabela.field_names = [desc[0] for desc in cur.description]

        for transacao in transacoes:
            tabela.add_row(transacao)

        print(tabela)
    else:
        print("Nenhuma transação encontrada.")

    conn.close()
    cur.close()
