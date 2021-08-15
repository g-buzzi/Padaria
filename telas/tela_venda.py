from telas.tela_abstrata import Tela

class TelaVenda(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        
    def recebe_dados_venda(self, mensagem: str = None):
        if mensagem:
            self.cabecalho(mensagem)

        return {
            'codigo': self.le_num_inteiro('Código: '),
            'atendente': self.le_num_inteiro('Matrícula do atendente: '),
            'encomenda': self.le_string('Encomenda (s/n): ')
        }
      
    def mostra_dados_encomenda(self, dados_encomenda):
        print(
            '\nData de entrega:', dados_encomenda['data_entrega'],
            '\nEntregue:', dados_encomenda['entregue']
        )
        
    def mostra_cliente(self, cliente):
        print(
            '\nCliente:', cliente,
            '\n'
        )
          
    def mostra_venda(self, dados_venda):
        
        print(
            
            '\nCódigo:', dados_venda['codigo'],
            '\nAtendente:', dados_venda['atendente'],
            '\nEncomenda:', dados_venda['encomenda'],
            '\n'
        )
        
    def mostra_item(self, itens):
        print('Itens:')
        for item in itens:
            print('Produto:', item.produto.nome.ljust(10), 'Quantidade:', item.quantidade.ljust(10), 'Valor unitário R$:', item.produto.preco_venda)
            
    def mostra_valores(self, dados_valores):
        print(
            '\nDesconto (%):', dados_valores['desconto'],
            '\nPreço final R$:', dados_valores['preco_final'],
            '\n--------------Fim da Venda-------------------'
        )
        
    def solicita_codigo_venda(self, mensagem: str):
        self.cabecalho(mensagem)
        return self.le_string('Código da venda: ')
    
    def solicita_item(self):
        self.cabecalho('Dados do item: ')
        
        return {
            'produto': self.le_num_inteiro('Código do produto: '),
            'quantidade': self.le_num_inteiro('Quantidade: ')
        }
        
    def solicita_dados_encomenda(self):
        self.cabecalho('Dados da encomenda: ')
        
        return {
            'data_entrega': self.le_string('Data de entrega: '),
            'cliente': self.le_string('Cpf do cliente: ')
        }
        
    def solicita_desconto(self):
        
        return self.le_num_inteiro('Desconto (%): ')