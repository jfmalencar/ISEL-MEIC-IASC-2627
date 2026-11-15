from estado import Estado
from memoria_experiencia import MemoriaExperiencia
from memoria_aprendizagem import MemoriaDeAprendizagem
from q_learning import QLearning
from selecao_acao import SeleccaoAccaoEGreedy


class QME(QLearning):
    def __init__(
        self,
        memoria: MemoriaDeAprendizagem,
        seleccao_accao: SeleccaoAccaoEGreedy,
        alfa: float,
        gama: float,
        num_sim: int,
        dim_max: int,
        observador=None,
    ):
        super().__init__(memoria, seleccao_accao, alfa, gama, observador)
        self.num_sim = num_sim
        self.memoria_experiencia = MemoriaExperiencia(dim_max)

    def aprender(
        self,
        s: Estado,
        a,
        r: float,
        s_linha: Estado,
        a_linha=None,
        final: bool = False,
    ):
        super().aprender(s, a, r, s_linha, a_linha, final)
        self.memoria_experiencia.actualizar((s, a, r, s_linha))
        self.simular()

    def simular(self):
        amostras = self.memoria_experiencia.amostrar(self.num_sim)
        for s, a, r, s_linha in amostras:
            super().aprender(s, a, r, s_linha, simulada=True)
