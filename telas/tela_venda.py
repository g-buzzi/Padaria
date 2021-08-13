from telas.tela_abstrata import Tela

class TelaVenda(Tela):
    def __init__(self, controlador):
        super().__init__(controlador)
        
    def recebe_dados_venda(self, mensagem: str = None):
        if mensagem:
            self.cabecalho(mensagem)

        return {
            'codigo': self.le_num_inteiro('Código: '),
            'atendente': self.le_string('Atendente: '),
            'encomenda': self.le_string('Encomenda (s/n): ')
        }
        
    def mostra_venda(self, dados_venda):
        
        print(
            'Código:', dados_venda['codigo'],
            '\nAtendente:', dados_venda['atendente'],
            '\nEncomenda:', dados_venda['encomenda'],
            '\nItens:', dados_venda['itens'],
            '\nPreço final:', dados_venda['preco_final'],
            '\nDesconto:', dados_venda['desconto'],
            '\nCliente:', dados_venda['cliente'],
            '\nData entrega:', dados_venda['data_entrega'],
            '\nEntregue:', dados_venda['entregue'],
            '\n'
            '\n---------------------------------------'
            '\n'
        )
        
    def solicita_codigo_venda(self, mensagem: str):
        self.cabecalho(mensagem)
        return self.le_string('Código da venda: ')
    
    def solicita_item(self):
        self.cabecalho('Dados do item')
        
        return {
            'produto': self.le_num_inteiro('Código do produto: '),
            'quantidade': self.le_num_inteiro('Quantidade: ')
        }
        