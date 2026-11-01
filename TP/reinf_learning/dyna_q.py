from modelo_tr import ModeloTR
from q_learning import QLearning
from estado import Estado
from selecao_acao import SeleccaoAccaoEGreedy
from memoria_aprendizagem import MemoriaDeAprendizagem

class DynaQ(QLearning):
    """
    Algoritmo Dyna-Q que herda de QLearning.
    Combina a aprendizagem direta a partir do ambiente real com o planeamento por simulação interna
    a partir do modelo do mundo (ModeloTR).
    """
    def __init__(self, memoria: MemoriaDeAprendizagem, seleccao_accao: SeleccaoAccaoEGreedy, alfa: float = 0.1, gama: float = 0.9, n_simulacoes: int = 5):
        super().__init__(memoria, seleccao_accao, alfa, gama)
        self.n_simulacoes = n_simulacoes
        self.modelo = ModeloTR()  # Modelo do mundo para simulações internas

    def aprender(self, s: Estado, a, r: float, s_linha: Estado, a_linha = None, final: bool = False):
        """
        Passo de aprendizagem Dyna-Q:
        1. Aprendizagem direta: Atualiza Q(s, a) via Q-learning com a experiência real.
        2. Atualização do modelo: Regista a transição observada.
        3. Planeamento: Executa simulações internas.
        """
        # Aprendizagem direta
        super().aprender(s, a, r, s_linha, a_linha, final)

        # Atualizar o modelo do mundo com a experiência real
        self.modelo.actualizar(s, a, r, s_linha)

        # Planeamento por simulação interna
        self.simular()

    def simular(self):
        """
        Realiza 'n_simulacoes' iterações de aprendizagem simulada,
        amostrando experiências passadas a partir do modelo do mundo.
        """
        for _ in range(self.n_simulacoes):
            amostra = self.modelo.amostrar()
            if amostra is not None:
                s_sim, a_sim, r_sim, s_linha_sim = amostra
                super().aprender(s_sim, a_sim, r_sim, s_linha_sim)