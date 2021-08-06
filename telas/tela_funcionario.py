from telas.tela_abstrata import Tela


class TelaFuncionario(Tela):

    def __init__(self, controlador):
        super().__init__(controlador)

    def salva_funcionario(self, acao_chave: str = None):
        if acao_chave:
            print('------- ' + acao_chave + ' Funcionário -------')

        return {
            'matricula': self.le_num_inteiro('Matrícula: '),
            'nome': self.le_string('Nome: '),
            'cpf': self.le_string('CPF: '),
            'telefone': self.le_num_inteiro('Telefone: '),
            'email': self.le_string('E-mail: '),
            'salario': self.le_num_fracionario('Salário: ')
        }

    def lista_funcionario(self, dados_funcionario):

        print(
            'Matrícula:', dados_funcionario['matricula'],
            '\nNome:', dados_funcionario['nome'],
            '\nCPF:', dados_funcionario['cpf'],
            '\nTelefone:', dados_funcionario['telefone'],
            '\nE-mail:', dados_funcionario['email'],
            '\nSalário:', dados_funcionario['salario'],
            '\n'
            '\n---------------------------------------'
            '\n'
        )

    def pesquisa_funcionario(self, acao_chave: str):
        print('------- ' + acao_chave + ' Funcionário -------')
        return self.le_num_inteiro('Matrícula: ')

