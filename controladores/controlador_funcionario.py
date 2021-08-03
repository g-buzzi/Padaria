from controladores.controlador_abstrato import Controlador
from telas.tela_funcionario import TelaFuncionario


class ControladorFuncionario(Controlador):

   def __init__(self):
       super().__init__(TelaFuncionario(self))

   def abre_tela_inicial(self):
       pass