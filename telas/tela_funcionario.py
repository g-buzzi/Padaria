from telas.tela_abstrata import Tela


class TelaFuncionario(Tela):

   def __init__(self, controlador):
       super().__init__(controlador)

   def mostra_opcoes(self) -> int:

       while True:
           print("--------- Opções ---------")
           print("1: Cadastrar Funcionário")
           print("2: Alterar Funcionário")
           print("3: Remover Funcionário")
           print("4: Listar Funcionários")
           print("5: Pesquisar Funcionários")
           print("0: Voltar")
           print()
           opcao = self.le_num_inteiro(valores_validos = range(6))
           print()
           return opcao