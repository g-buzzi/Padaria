from typing import List

from controladores.controlador_abstrato import Controlador
from telas.tela_funcionario import TelaFuncionario
from entidades.funcionario import Funcionario


class ControladorFuncionario(Controlador):

    def __init__(self):
        super().__init__(TelaFuncionario(self))
        self.__funcionarios: List[Funcionario] = []

    def abre_tela_inicial(self):
        switcher = {0: False, 1: self.cadastra_funcionario, 2: self.altera_funcionario, 3: self.remove_funcionario,
                    4: self.lista_funcionarios, 5: self.pesquisa_funcionario}

        opcoes = {1: "Cadastrar", 2: "Alterar", 3: "Remover", 4: "Listar", 5: "Pesquisar", 0: "Voltar"}
        while True:
            opcao = self.tela.mostra_opcoes(opcoes, "--------- Funcionários ---------")
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida:
                funcao_escolhida()
            else:
                break

    def cadastra_funcionario(self):
        # opcoes = {1: "Continuar cadastrando", 0: "Voltar"}

        dados_funcionario = self.tela.salva_funcionario('Cadastra')

        if len(self.__funcionarios) > 0:
            for funcionario in self.__funcionarios:
                if funcionario.matricula == dados_funcionario['matricula']:
                    self.tela.mensagem_erro('Já existe funcionário cadastrado com essa matrícula')

                else:
                    self.salva_dados_funcionario(dados_funcionario)

        else:
            self.salva_dados_funcionario(dados_funcionario)

    def salva_dados_funcionario(self, dados_funcionario):
        self.__funcionarios.append(Funcionario(
            dados_funcionario['matricula'],
            dados_funcionario['nome'],
            dados_funcionario['cpf'],
            dados_funcionario['telefone'],
            dados_funcionario['email'],
            dados_funcionario['salario']
        ))

    def lista_funcionarios(self):
        self.tela.adiciona_cabecalho('Lista Funcionários')

        for funcionario in self.__funcionarios:
            self.tela.lista_funcionario({
                'matricula': funcionario.matricula,
                'nome': funcionario.nome,
                'cpf': funcionario.cpf,
                'telefone': funcionario.telefone,
                'email': funcionario.email,
                'salario': funcionario.salario
            })

    def remove_funcionario(self):

        matricula = self.tela.solicita_matricula_funcionario('Remove')

        for funcionario in self.__funcionarios:
            if funcionario.matricula == matricula:
                self.__funcionarios.remove(funcionario)

    def pesquisa_funcionario(self):

        matricula = self.tela.solicita_matricula_funcionario('Pesquisa')

        for funcionario in self.__funcionarios:
            if funcionario.matricula == matricula:
                self.tela.lista_funcionario({
                    'matricula': funcionario.matricula,
                    'nome': funcionario.nome,
                    'cpf': funcionario.cpf,
                    'telefone': funcionario.telefone,
                    'email': funcionario.email,
                    'salario': funcionario.salario
                })

    def altera_funcionario(self):

        matricula = self.tela.solicita_matricula_funcionario('Altera')

        for funcionario in self.__funcionarios:
            if funcionario.matricula == matricula:

                dados_atualizados = self.tela.salva_funcionario()

                index = self.__funcionarios.index(funcionario)

                self.__funcionarios[index] = Funcionario(
                    dados_atualizados['matricula'],
                    dados_atualizados['nome'],
                    dados_atualizados['cpf'],
                    dados_atualizados['telefone'],
                    dados_atualizados['email'],
                    dados_atualizados['salario']
                )