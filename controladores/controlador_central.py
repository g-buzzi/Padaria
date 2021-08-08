from controladores.controlador_abstrato import Controlador
from telas.tela_central import TelaCentral
from controladores.controlador_ingredientes import ControladorIngredientes
from controladores.controlador_receitas import ControladorReceitas

class ControladorCentral(Controlador):

    def __init__(self):
        super().__init__(TelaCentral(self))
        self.__controladores = {0: False, 1: ControladorIngredientes(self), 2: ControladorReceitas(self)}

    def abre_tela_inicial(self):
        opcoes = {1: "Ingredientes", 2: "Receitas", 0: "Sair"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "-------- Tela Inicial --------")
            controlador = self.__controladores[opcao]

            if controlador is False:
                break
            else:
                controlador.inicia()

    @property
    def controlador_ingredientes(self):
        return self.__controladores[1]
    
    @property
    def controlador_receitas(self):
        return self.__controladores[2]

