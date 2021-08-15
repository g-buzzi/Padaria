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
            2: self.lista_encomendas,
            3: self.lista_vendas_por_cliente,
            4: self.lista_vendas_por_funcionario,
            5: self.lista_vendas,
            6: self.conclui_encomenda,
            7: self.cancela_encomenda,
            8: self.seleciona_venda_por_codigo}

        opcoes = {
            1: "Cadastrar Venda", 
            2: "Listar Encomendas", 
            3: "Listar Vendas por Cliente", 
            4: 'Listar Vendas por Atendente', 
            5: "Listar Vendas", 
            6: 'Concluir Encomenda', 
            7: 'Cancelar Encomenda',
            8: "Pesquisar Venda", 
            0: "Voltar"
        }
        
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Vendas ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break
            
    def cadastra_venda(self):
        opcoes = {1: "Continuar cadastrando venda", 0: "Voltar"}

        while True:
            dados_venda = self.tela.recebe_dados_venda('Cadastra Venda')
            resposta = self.verifica_se_ja_existe_venda_com_codigo(dados_venda['codigo'])
            if resposta:
                self.tela.mensagem_erro('Já existe venda com esse código.')
                break
            else:
                
                funcionario = self.__controlador_central.controlador_funcionarios.verifica_se_ja_existe_funcionario_com_matricula(dados_venda['atendente'])
                dados_venda['atendente'] = funcionario
                
                self.salva_dados_venda(dados_venda)
                
                
                if dados_venda['encomenda'] == 's':
                    self.solicita_dados_encomenda(dados_venda['codigo'])
                    
                self.solicita_itens(dados_venda['codigo'])
                
                self.solicita_desconto(dados_venda['codigo'])
                
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        
            
    def solicita_desconto(self, codigo_venda):
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        
        desconto = self.tela.solicita_desconto()
        venda.desconto = desconto
                    
    
    def solicita_dados_encomenda(self, codigo):
        
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
        
        dados_encomenda = self.tela.solicita_dados_encomenda()
        cliente = self.__controlador_central.controlador_clientes.verifica_se_ja_existe_cliente_com_cpf(dados_encomenda['cliente'])
        if cliente != None:
            venda.data_entrega = dados_encomenda['data_entrega']
            venda.cliente = cliente
            venda.entregue = False
                          
            
    def solicita_itens(self, codigo):
        opcoes = {1: "Continuar cadastrando item", 0: "Concluir"}
        while True:
            venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
            
            dados_item = self.tela.solicita_item()
            produto = self.__controlador_central.controlador_produtos.seleciona_produto_por_codigo(dados_item['produto'])
            venda.itens.append(Item(produto, dados_item['quantidade']))            
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
        
            
    def verifica_se_ja_existe_venda_com_codigo(self, codigo) -> Venda:
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
            self.lista_venda()
                
    def lista_venda(self, venda): 
        if venda.encomenda == 's':
                self.tela.mostra_dados_encomenda({
                    'data_entrega': venda.data_entrega,
                    'entregue': venda.entregue
                })
                
        if venda.cliente or venda.encomenda == 's':
            self.tela.mostra_cliente({
                'cliente': venda.cliente.nome
            })
        
        self.tela.mostra_venda({
            'codigo': venda.codigo,
            'atendente': venda.atendente.nome,
            'encomenda': venda.encomenda
        })
        
        self.tela.mostra_item(venda.itens)
        
        self.tela.mostra_valores({
            'preco_final': venda.preco_final,
            'desconto': venda.desconto,
        })
            
    def lista_encomendas(self):
        for venda in self.__vendas:
            if venda.encomenda == 's' and venda.entregue == False:
                self.lista_venda(venda)
                
    def lista_vendas_por_cliente(self):
        cpf = self.tela.solicita_cpf_cliente
        
        for venda in self.__vendas:
            if venda.cliente.cpf == cpf:
                self.lista_venda(venda)
                
            else:
                self.tela.mensagem_erro('Não existe nenhuma venda para esse cliente informado.')
        else:
            self.tela.mensagem_erro('Não existem vendas cadastradas. Cadastre uma primeiro.')
            
    def lista_vendas_por_funcionario(self):
        matricula = self.tela.solicita_matricula_funcionario
        
        for venda in self.__vendas:
            if venda.atendente.matricula == matricula:
                self.lista_venda(venda)
                
            else:
                self.tela.mensagem_erro('Não existe nenhuma venda realizada por esse funcionário.')
        else:
            self.tela.mensagem_erro('Não existem vendas cadastradas. Cadastre uma primeiro.')
            
    
    def conclui_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Concluir encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        
        if isinstance(venda, Venda) and venda.encomenda == 's':
            venda.entregue = True
        else:
            self.tela.mensagem_erro('Não existe encomenda ou código incorreto.')
            
    def cancela_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Cancelar encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        
        if isinstance(venda, Venda) and venda.encomenda == 's':
            self.__vendas.remove(venda)
        else:
            self.tela.mensagem_erro('Não existe encomenda ou código incorreto.')
            
        
                 
    def seleciona_venda_por_codigo(self):
        
        codigo = self.tela.solicita_codigo_venda('Pesquisa Venda')
        venda = verifica_se_ja_existe_venda_com_codigo(codigo)
        
        if isinstance(venda, Venda):
            self.lista_venda(venda)
        else:
            self.tela.mensagem_erro('Não existe venda ou código incorreto.')