import psycopg2
import random 
from datetime import datetime
from tabulate import tabulate


class investimentos:
    def __init__(self,data,ativo,quantidade, valor_unit, taxa_corretagem, tipo_transacao, valor_operacao=0.0,  b3=0.0, valor_total=0.0, preco_medio = 0, resultado = '', total_lc = 0):
        self.__data = data
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
    def data(self):
        return self.__data
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
    

    def compra(self):
        self.__valor_operacao = self.__valor_unit * self.__quantidade
        self.__b3 = round(self.__valor_operacao * 0.03 / 100, 2)
        self.__valor_total = round(self.__valor_operacao + self.__taxa_corretagem + self.__b3, 2)



    def venda(self):
        self.__valor_operacao = self.__valor_unit * self.__quantidade
        self.__b3 = round(self.__valor_operacao * 0.03 / 100, 2)
        self.__valor_total = round(self.__valor_operacao - self.__taxa_corretagem - self.__b3, 2)
       


    def salvarDados(self):
        conn = psycopg2.connect(
            database="yynfswhx",
            user="yynfswhx",
            password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
            host="silly.db.elephantsql.com",
            port="5432"
        )
            
        cur = conn.cursor()
        cur.execute("INSERT INTO investimentos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)", (self.__data,self.__codigo,self.ativo,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao,  self.__b3, self.__valor_total, 0.0, self.__resultado, 0.0))
        conn.commit()
        cur.close()
        conn.close()
        


    def atualizarDados(self,codigo):     
        conn = psycopg2.connect(
            database="yynfswhx",
            user="yynfswhx",
            password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
            host="silly.db.elephantsql.com",
            port="5432"
        )

        cur = conn.cursor()

        cur.execute('UPDATE investimentos SET data = %s, ativo = %s, quantidade = %s, valor_unit = %s, taxa_corretagem = %s, tipo_transacao = %s, valor_operacao = %s WHERE codigo = %s', (self.__data,self.__ativo,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao,codigo))
        conn.commit()
        cur.close()
        conn.close()


    def precoMedio(self):
        conn = psycopg2.connect(
            database="yynfswhx",
            user="yynfswhx",
            password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
            host="silly.db.elephantsql.com",
            port="5432"
        ) 
        cur = conn.cursor()
        cur.execute('SELECT ativo, COUNT(*) as aparições from investimentos where ativo = %s GROUP BY ativo', (self.__ativo,))
        res = cur.fetchone()
        ap = res[1]
        if ap == 1:
            preco_medio = round(self.valor_total / self.quantidade, 2)
            cur.execute("UPDATE investimentos SET preco_medio = %s WHERE codigo = %s", (preco_medio, self.__codigo))
            conn.commit()
        elif ap > 1:
            cur.execute("SELECT (SELECT SUM(valor_total) FROM investimentos where ativo = %s and tipo_transacao = 'C'),(SELECT SUM(quantidade)FROM investimentos where ativo = %s and tipo_transacao = 'C'),(SELECT SUM(quantidade) FROM investimentos where ativo = %s and tipo_transacao = 'V') FROM investimentos where ativo = %s", (self.__ativo, self.__ativo,self.__ativo,self.__ativo))
            res_2 = cur.fetchone()
            vt = res_2[0]
            qtd_c = res_2[1] if res_2[1] is not None else 0
            qtd_v = res_2[2] if res_2[2] is not None else 0
            preco_medio = round(vt/(qtd_c-qtd_v), 2)
            cur.execute("UPDATE investimentos SET preco_medio = %s WHERE codigo = %s", (preco_medio, self.__codigo))
            conn.commit()
        conn.close()    
        cur.close()



    def lucro_prejuizo(self):

        conn = psycopg2.connect(
                database="yynfswhx",
                user="yynfswhx",
                password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
                host="silly.db.elephantsql.com",
                port="5432"
        ) 
        cur = conn.cursor()
        cur.execute("SELECT preco_medio FROM investimentos WHERE data = (SELECT MAX(data) FROM investimentos WHERE tipo_transacao = 'C' and ativo = %s)", (self.__ativo,))
        pm = cur.fetchone()[0]
        print(pm)
        l_c = round(((self.__valor_unit - pm) * self.quantidade) - (self.__taxa_corretagem + self.__b3),2)
        if l_c > 0: 
            rest = 'LUCRO'
        else:
            rest = 'PREJUIZO'
        
        cur.execute('UPDATE investimentos SET preco_medio = %s, resultado = %s, total_lc = %s WHERE codigo = %s', (pm,rest, l_c, self.__codigo))
        conn.commit()
        conn.close()
        cur.close()



def lc_ativo():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute('SELECT ativo, SUM(total_lc) as LucroTotal FROM investimentos GROUP BY ativo')
    res = cur.fetchall()

    table_data = [["Ativo", "Lucro Total"]]
    for row in res:
        table_data.append([row[0], row[1]])

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    conn.close()
    cur.close()



def lc_carteira():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute('SELECT SUM(total_lc) as LucroTotal FROM investimentos')
    res = cur.fetchone()

    lucro_total_carteira = res[0]
    table_data = [["Lucro Total"], [lucro_total_carteira]]

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    conn.close()
    cur.close()


def criar_cod():
    cod = ''.join(random.choices('0123456789', k=5))
    return cod




def detalhamento():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()
    ativo = input('Insira o ativo da transação: ').upper()
    cur.execute("select * from investimentos where ativo = %s", (ativo,))
    res = cur.fetchall()

    table_data = [["Data", "Código", "Ativo", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo de Transação", "Valor Operação", "B3", "Valor Total", "Preço Médio", "Resultado", "Total LC"]]
    for row in res:
        table_data.append(list(row))

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    conn.close()
    cur.close()



def rec_date():
    data_str = input("Digite a data no formato dd/mm/aaaa: ")
    data = datetime.strptime(data_str, "%d/%m/%Y")
    return data


def cadastrar_dados():
    data = rec_date().date()
    ativo = input('Insira o nome do ativo: ').upper()
    quantidade = int(input('Insira a quantidade: '))
    valor_unit = float(input('Insira o valor unitário do ativo: '))
    taxa_corretagem = float(input('Insira a corretagem: '))
    tipo_op = input('Insira o tipo de transação: ').upper()[0]
    inv = investimentos(data, ativo, quantidade, valor_unit, taxa_corretagem, tipo_op)
    if tipo_op == 'C':
        inv.compra()
        inv.salvarDados()
        inv.precoMedio()
    if tipo_op == 'V':
        inv.venda()
        inv.salvarDados()
        inv.lucro_prejuizo()


    table_data = [
        ["Data", "Código", "Ativo", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo de Transação"],
        [str(inv.data), inv.codigo, inv.ativo, inv.quantidade, inv.valor_unit, inv.taxa_corretagem, inv.tipo_transacao]
    ]
    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print('Cadastro ralizado com sucesso!')
    print(table)


def editar_transacao():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()
    codigo = input('Insira o código da transação a ser editada: ')
    cur.execute("SELECT * FROM investimentos WHERE codigo = %s", (codigo,))
    res = cur.fetchall()

    if len(res) == 0:
        print("Nenhuma transação encontrada com o código fornecido.")
        return

    table_data = [["Data", "Código", "Ativo", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo de Transação", "Valor Operação", "B3", "Valor Total", "Preço Médio", "Resultado", "Total LC"]]
    for row in res:
        table_data.append(list(row))

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    # Solicitar a edição dos valores da transação
    data = rec_date()
    ativo = input('Insira o novo ativo: ').upper()
    quantidade = int(input('Insira a nova quantidade: '))
    valor_unitario = float(input('Insira o novo valor unitário: '))
    taxa_corretagem = float(input('Insira a nova taxa de corretagem: '))

    inv = investimentos(
        data=data,
        ativo=ativo,
        quantidade=quantidade,
        valor_unit=valor_unitario,
        taxa_corretagem=taxa_corretagem,
        tipo_transacao= 'C',
    )

    inv.compra()
    inv.atualizarDados(codigo)
    inv.precoMedio()
    
    print("\nTransação atualizada com sucesso!")

    conn.close()
    cur.close()


def excluir_transacao():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()
    codigo = input('Insira o código da transação a ser excluída: ')
    cur.execute("SELECT * FROM investimentos WHERE codigo = %s", (codigo,))
    res = cur.fetchall()

    if len(res) == 0:
        print("Nenhuma transação encontrada com o código fornecido.")
        return

    table_data = [["Data", "Código", "Ativo", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo de Transação", "Valor Operação", "B3", "Valor Total", "Preço Médio", "Resultado", "Total LC"]]
    for row in res:
        table_data.append(list(row))

    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)

    confirmacao = input("Tem certeza de que deseja excluir esta transação? (S/N): ")
    if confirmacao.lower() == "s":
        cur.execute("DELETE FROM investimentos WHERE codigo = %s", (codigo,))
        conn.commit()
        print("Transação excluída com sucesso.")
    else:
        print("Exclusão cancelada.")

        conn.close()
        cur.close()

# Biblioteca -  pip install tabulate
def mostrar_historico():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
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
        print("\nNenhuma transação encontrada.")

    conn.close()
    cur.close()



def reiniciar():
    conn = psycopg2.connect(
        database="yynfswhx",
        user="yynfswhx",
        password="fkDkWLY0e2WVbNOtBN4HPMktb94_sK0X",
        host="silly.db.elephantsql.com",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute('DELETE from investimentos')
    conn.commit()
    conn.close()
    cur.close()