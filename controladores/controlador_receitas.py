from telas.tela_abstrata import Tela
from controladores.controlador_abstrato import Controlador
from entidades.receita import Receita
from telas.tela_receita import TelaReceita



class ControladorReceitas(Controlador):
    def __init__(self, tela: TelaReceita, controlador_central: Controlador):
        super().__init__(TelaReceita())
        self.__receitas = {}
        self.__controlador_central = controlador_central

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.registra_receita, 2: self.altera_receita, 3: self.remove_receita, 4: self.lista_receitas, 5: self.pesquisa_por_ingrediente}
        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5:"Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Receitas ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def registra_receita(self):
        pass
    
    def inclui_ingrediente_receita(self):
        pass

    def remove_ingrediente_receita(self):
        pass

    def altera_receita(self):
        pass

    def pesquisa_por_ingrediente(self):
        codigo_ingrediente = self.tela.pesquisa_por_ingrediente()
        try:
            ingrediente = self.__controlador_central.controlador_ingredientes.ingredientes[codigo_ingrediente]
            receitas = []
            for codigo, receita in self.__receitas.values():
                try:
                    receita.ingredientes_receita[ingrediente]
                except KeyError:
                    pass
                else:
                    receitas.append(self.dados_receita(codigo))
            if receitas:
                for dados in receitas:
                    self.tela.mostra_receita(dados)
            else:
                self.tela.mensagem("Nenhum resultado encontrado")
        except KeyError:
            self.tela.mensagem_erro("Não existe ingrediente com este código")


