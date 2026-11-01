from estado import Estado
from memoria_aprendizagem import MemoriaDeAprendizagem
from selecao_acao import SeleccaoAccaoEGreedy

class QLearning:
    def __init__(self, memoria: MemoriaDeAprendizagem, seleccao_accao: SeleccaoAccaoEGreedy, alfa: float = 0.1, gama: float = 0.9):
        self.mem_aprend = memoria
        self.sel_accao = seleccao_accao
        self.alpha = alfa
        self.gamma = gama

    def aprender(self, s: Estado, a, r: float, s_linha: Estado, a_linha = None, final: bool = False):
        """
        Atualiza a estimativa Q(s, a) usando a regra de atualização Q-learning:
        Q(s, a) <- Q(s, a) + alpha * (r + gamma * max_a' Q(s', a') - Q(s, a))
        """
        q_atual = self.mem_aprend.q(s, a)

        if final:
            retorno_esperado = r
        else:
            a_sofrega = self.sel_accao.accao_sofrega(s_linha)
            q_max = self.mem_aprend.q(s_linha, a_sofrega)
            retorno_esperado = r + self.gamma * q_max

        q_novo = q_atual + self.alpha * (retorno_esperado - q_atual)
        self.mem_aprend.actualizar(s, a, q_novo)