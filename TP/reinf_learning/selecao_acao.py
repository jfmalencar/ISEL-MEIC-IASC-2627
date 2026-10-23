import random
from memoria_aprendizagem import MemoriaDeAprendizagem

class SeleccaoAccaoEGreedy:
    def __init__(self, memoria: MemoriaDeAprendizagem, epsilon: float = 0.1):
        self.memoria = memoria
        self.epsilon = epsilon

    def accao_sofrega(self, s: int, accoes: list):
        """
        Obter ação sôfrega (greedy): escolhe a ação que maximiza Q(s, a).
        Aplica shuffle nas ações para desempate aleatório entre valores Q iguais.
        """
        accoes_shuffled = accoes.copy()
        random.shuffle(accoes_shuffled)
        return max(accoes_shuffled, key=lambda a: self.memoria.q(s, a))

    def accao_exploracao(self, accoes: list):
        """Obter ação de exploração: escolha uniforme entre ações disponíveis."""
        return random.choice(accoes)

    def seleccionar_accao(self, s: int, accoes: list):
        """Selecciona a ação combinando exploração e aproveitamento."""
        if not accoes:
            return None

        if random.random() > self.epsilon:
            return self.accao_sofrega(s, accoes)  # Aproveitar conhecimento
        else:
            return self.accao_exploracao(accoes)   # Explorar