from telas.tela_venda import TelaVenda
from entidades.venda import Venda
from controladores.controlador_abstrato import Controlador
from entidades.item import Item


class ControladorVendas(Controlador):
    def __init__(self, controlador_central: Controlador):
        super().__init__(TelaVenda(self))
        self.__vendas: list[Venda] = []
        self.__controlador_central = controlador_central
        
    def abre_tela_inicial(self):
        switcher = {
            0: False, 
            1: self.cadastra_venda,
            2: False,
            3: False,
            4: self.lista_vendas,
            5: self.seleciona_venda_por_codigo}

        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Vendas ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break
            
    def cadastra_venda(self):
        opcoes = {1: "Continuar cadastrando", 0: "Voltar"}

        while True:
            dados_venda = self.tela.recebe_dados_venda('Cadastra Venda')
            resposta = self.verifica_se_ja_existe_venda_com_codigo(dados_venda['codigo'])
            if resposta:
                self.tela.mensagem_erro('Já existe venda com esse código.')
                break
            else:
                
                self.salva_dados_venda(dados_venda)
                
                self.solicita_itens(dados_venda['codigo'])
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    def solicita_itens(self, codigo):
        opcoes = {1: "Continuar cadastrando", 0: "Concluir"}
        while True:
            venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
            
            dados_item = self.tela.solicita_item()
            produto = self.__controlador_central.controlador_produtos.seleciona_produto_por_codigo(dados_item['produto'])
            venda.itens.append(Item(produto, dados_item['quantidade']))
            
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        
            
    def verifica_se_ja_existe_venda_com_codigo(self, codigo):
        for venda in self.__vendas:
            if codigo == venda.codigo:
                return venda                
        else:
            return None
        
    def salva_dados_venda(self, dados_venda):
        self.__vendas.append(Venda(
            dados_venda['codigo'],
            dados_venda['atendente'],
            dados_venda['encomenda']
        ))
        
    def lista_vendas(self):
        self.tela.cabecalho('Lista Vendas')

        for venda in self.__vendas:
            self.tela.mostra_venda({
                'codigo': venda.codigo,
                'atendente': venda.atendente,
                'encomenda': venda.encomenda,
                'itens': venda.itens,
                'preco_final': venda.preco_final,
                'desconto': venda.desconto,
                'cliente': venda.cliente,
                'data_entrega': venda.data_entrega,
                'entregue': venda.entregue
            })
            
    def seleciona_venda_por_codigo(self):
        
        codigo = self.tela.solicita_codigo_venda('Pesquisa Venda')

        for venda in self.__vendas:
            if venda.codigo == codigo:
                self.tela.mostra_venda({
                    'codigo': venda.codigo,
                    'atendente': venda.atendente,
                    'encomenda': venda.encomenda,
                    'itens': venda.itens,
                    'preco_final': venda.preco_final,
                    'desconto': venda.desconto,
                    'cliente': venda.cliente,
                    'data_entrega': venda.data_entrega,
                    'entregue': venda.entregue
                })