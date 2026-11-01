import random
from estado import Estado
from memoria_aprendizagem import MemoriaDeAprendizagem

class SeleccaoAccaoEGreedy:
    def __init__(self, accoes_disponiveis: list, memoria: MemoriaDeAprendizagem, epsilon: float = 0.1):
        self.epsilon = epsilon
        self.accoes_disponiveis = accoes_disponiveis
        self.memoria = memoria

    def accao_sofrega(self, s: Estado):
        """
        Obter ação sôfrega (greedy): escolhe a ação que maximiza Q(s, a).
        Aplica shuffle nas ações para desempate aleatório entre valores Q iguais.
        """
        accoes = self.accoes_disponiveis.copy()
        random.shuffle(accoes)
        return max(accoes, key=lambda a: self.memoria.q(s, a))

    def accao_exploracao(self):
        """Obter ação de exploração: escolha uniforme entre ações disponíveis."""
        return random.choice(self.accoes_disponiveis)

    def seleccionar_accao(self, s: Estado):
        """Selecciona a ação combinando exploração e aproveitamento."""               
        if random.random() > self.epsilon:
            return self.accao_sofrega(s)
        else:
            return self.accao_exploracao()
        