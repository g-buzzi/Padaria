from telas.tela_venda import TelaVenda
from entidades.venda import Venda
from controladores.controlador_abstrato import Controlador
from entidades.item import Item
from entidades.funcionario import Funcionario
from entidades.cliente import Cliente
from entidades.produto import Produto


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
            venda = self.verifica_se_ja_existe_venda_com_codigo(dados_venda['codigo'])
            if isinstance(venda, Venda):
                self.tela.mensagem_erro('Já existe venda com esse código.')
                break
            else:
                
                funcionario = self.__controlador_central.controlador_funcionarios.verifica_se_ja_existe_funcionario_com_matricula(dados_venda['atendente'])
                if isinstance(funcionario, Funcionario):
                    dados_venda['atendente'] = funcionario
                else:
                    self.tela.mensagem_erro('Obrigatório informar um atendente.')
                
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
        if isinstance(cliente, Cliente):
            venda.data_entrega = dados_encomenda['data_entrega']
            venda.cliente = cliente
            venda.entregue = False
                          
            
    def solicita_itens(self, codigo):
        opcoes = {1: "Continuar cadastrando item", 0: "Concluir"}
        while True:
            venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
            
            dados_item = self.tela.solicita_item()
            produto = self.__controlador_central.controlador_produtos.seleciona_produto_por_codigo(dados_item['produto'])
            if isinstance(produto, Produto):
                venda.itens.append(Item(produto, dados_item['quantidade']))
            else:
                self.tela.mensagem_erro('Tente novamente, produto não encontrado.')
                break          
            
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
        if dados_venda['encomenda'] == 's':
            encomenda = True
        else:
            encomenda = False
            
        self.__vendas.append(Venda(
            dados_venda['codigo'],
            dados_venda['atendente'],
            encomenda
        ))
        self.tela.mensagem("Venda cadastrada com sucesso")
        
    def lista_vendas(self):
        self.tela.cabecalho('Lista Vendas')

        if len(self.__vendas) > 0:
            for venda in self.__vendas:
                self.lista_venda(venda)
        
        else:
            self.tela.mensagem_erro('Nenhuma venda encontrada.')
            
                
          
                
    def lista_venda(self, venda): 
        self.tela.cabecalho("Encomenda:" if venda.encomenda else "Venda:")
        
        if venda.encomenda == True:
            self.tela.mostra_dados_encomenda({
                'data_entrega': venda.data_entrega,
                'entregue': 'Sim' if venda.entregue else 'Não'
            })
        
                
        if venda.cliente or venda.encomenda == True:
            self.tela.mostra_cliente(
                venda.cliente.nome
            )
        
        self.tela.mostra_venda({
            'codigo': venda.codigo,
            'atendente': venda.atendente.nome,
            'encomenda': 'Sim' if venda.encomenda else 'Não'
        })
        
        self.tela.mostra_item(venda.itens)
        
        self.tela.mostra_valores({
            'preco_final': venda.preco_final,
            'desconto': venda.desconto,
        })
        
    def mostra_itens(self, itens: list[Item]):
        self.tela.cabecalho('Itens: ')
        for item in itens:
            self.tela.mostra_item({
                'produto': item.produto.nome,
                'quantidade': item.quantidade,
                'valor_unitario': item.produto.preco_venda
            })
            
    def lista_encomendas(self):
       
        if len(self.__vendas) > 0:
            for venda in self.__vendas:
                if venda.encomenda == True and venda.entregue == False:
                    self.lista_venda(venda)
                
        else:
            self.tela.mensagem_erro('Nenhuma venda encontrada.')
            
                
            
                        
    def lista_vendas_por_cliente(self):
        opcoes = {1: "Listar novamente", 0: "Voltar"}
        while True:
            cpf = self.tela.solicita_cpf_cliente()
            
            if len(self.__vendas) > 0:
                for venda in self.__vendas:
                    if venda.cliente and venda.cliente.cpf == cpf:
                        self.lista_venda(venda)
                    
            else:
                self.tela.mensagem_erro('Nenhuma venda encontrada.')
                break
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
       
            
    def lista_vendas_por_funcionario(self):
        opcoes = {1: "Listar novamente", 0: "Voltar"}
        while True:
            
            matricula = self.tela.solicita_matricula_funcionario()
            if len(self.__vendas) > 0:
                for venda in self.__vendas:
                    if venda.atendente and venda.atendente.matricula == matricula:
                        self.lista_venda(venda)
            else:
                self.tela.mensagem_erro('Nenhuma venda encontrada.')
                break
            
            opcao = self.tela.mostra_opcoes(opcoes)
            if opcao == 0:
                break
            
    
    def conclui_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Concluir encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        
        if isinstance(venda, Venda) and venda.encomenda == True:
            if venda.entregue == False:
                venda.entregue = True
                self.tela.mensagem("Encomenda concluída com sucesso.")
            else:
                self.tela.mensagem("Encomenda já entregue.")
        else:
            self.tela.mensagem_erro('Não existe encomenda com esse código.')
            
    def cancela_encomenda(self):
        codigo_venda = self.tela.solicita_codigo_venda('Cancelar encomenda')
        venda = self.verifica_se_ja_existe_venda_com_codigo(codigo_venda)
        
        if isinstance(venda, Venda) and venda.encomenda == True:
            if venda.entregue == False:
                self.__vendas.remove(venda)
                self.tela.mensagem("Encomenda cancelada com sucesso.")
            else:
                self.tela.mensagem("Encomenda não pode ser cancelada pois já foi entregue.")
        else:
            self.tela.mensagem_erro('Não existe encomenda com esse código.')
            
        
                 
    def seleciona_venda_por_codigo(self):
        
        codigo = self.tela.solicita_codigo_venda('Pesquisa Venda')
        if isinstance(codigo, int):        
            venda = self.verifica_se_ja_existe_venda_com_codigo(codigo)
            
            if isinstance(venda, Venda):
                self.lista_venda(venda)
            else:
                self.tela.mensagem_erro('Não existe venda ou código incorreto.')