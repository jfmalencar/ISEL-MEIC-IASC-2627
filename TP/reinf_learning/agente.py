from memoria_aprendizagem import MemoriaDeAprendizagem
from selecao_acao import SeleccaoAccaoEGreedy

class Agente:
    def __init__(self, accoes_disponiveis: list = None, valor_inicial: float = 0.0, epsilon: float = 0.1):
        self.accoes_disponiveis = accoes_disponiveis if accoes_disponiveis is not None else []
        self.memoria = MemoriaDeAprendizagem(valor_inicial)
        self.seleccao_accao = SeleccaoAccaoEGreedy(self.accoes_disponiveis, self.memoria, epsilon)

    def atualizar_accoes(self, accoes: list):
        """Atualiza a lista de ações disponíveis para o agente."""
        self.accoes_disponiveis = accoes
        self.seleccao_accao.accoes_disponiveis = accoes