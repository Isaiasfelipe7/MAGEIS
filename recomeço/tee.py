import psycopg2

class Ativo:
    def __init__(self, quantidade, valor, nome):
        self.quantidade = quantidade
        self.valor = valor
        self.nome = nome

    def preco_medio(self):
        return self.valor / self.quantidade if self.quantidade != 0 else 0

    def lucro_prejuizo(self, valor_atual):
        resultado = (valor_atual - self.preco_medio()) * self.quantidade
        if resultado > 0:
            return 'Lucro'
        elif resultado < 0:
            return 'Prejuízo'
        else:
            return 'Sem lucro/prejuízo'

    def salvar_no_banco(self):
        conn = psycopg2.connect(host='seu_host',
                                port='sua_porta',
                                database='seu_banco_de_dados',
                                user='seu_usuario',
                                password='sua_senha')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ativo (quantidade, valor, nome) VALUES (%s, %s, %s)',
                       (self.quantidade, self.valor, self.nome))
        conn.commit()
        conn.close()


class Transacao:
    def __init__(self, quantidade, valor, compra_venda, corretagem, operacao, taxa_b3):
        self.quantidade = quantidade
        self.valor = valor
        self.compra_venda = compra_venda
        self.corretagem = corretagem
        self.operacao = operacao
        self.taxa_b3 = taxa_b3

    def total(self):
        return (self.valor * self.quantidade) + self.corretagem + self.taxa_b3

    def salvar_no_banco(self):
        conn = psycopg2.connect(host='seu_host',
                                port='sua_porta',
                                database='seu_banco_de_dados',
                                user='seu_usuario',
                                password='sua_senha')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transacao (quantidade, valor, compra_venda, corretagem, operacao, taxa_b3) '
                       'VALUES (%s, %s, %s, %s, %s, %s)',
                       (self.quantidade, self.valor, self.compra_venda, self.corretagem, self.operacao, self.taxa_b3))
        conn.commit()
        conn.close()


# Exemplo de uso das classes
ativo1 = Ativo(100, 1500, 'Empresa A')
ativo1.salvar_no_banco()

transacao1 = Transacao(50, 2000, 'Compra', 10, 'Ação', 5)
transacao1.salvar_no_banco()

# Calcular o preço médio e verificar lucro/prejuízo de um ativo específico
conn = psycopg2.connect(host='seu_host',
                        port='sua_porta',
                        database='seu_banco_de_dados',
                        user='seu_usuario',
                        password='sua_senha')
cursor = conn.cursor()
cursor.execute('SELECT SUM(quantidade * valor) / SUM(quantidade) FROM transacao WHERE nome = %s', (ativo1.nome,))
resultado = cursor.fetchone()
valor_atual = 1800  # Valor atual do ativo (exemplo)
ativo1.valor = valor_atual

if resultado:
    preco_medio = resultado[0]
    print(f"Preço médio do ativo {ativo1.nome}: R${preco_medio:.2f}")
    print(f"Resultado: {ativo1.lucro_prejuizo(valor_atual)}")
else:
    print("Não há transações para este ativo.")

conn.close()
