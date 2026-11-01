from estado import Estado
from memoria_aprendizagem import MemoriaDeAprendizagem
from selecao_acao import SeleccaoAccaoEGreedy

class SARSA:
    def __init__(self, memoria: MemoriaDeAprendizagem, seleccao_accao: SeleccaoAccaoEGreedy, alfa: float = 0.1, gama: float = 0.9):
        self.mem_aprend = memoria
        self.sel_accao = seleccao_accao
        self.alpha = alfa
        self.gamma = gama

    def aprender(self, s: Estado, a, r: float, s_linha: Estado, a_linha, final: bool = False):
        """
        Atualiza a estimativa Q(s, a) usando a regra de atualização SARSA:
        Q(s, a) <- Q(s, a) + alpha * (r + gamma * Q(s', a') - Q(s, a))
        """
        if final or a_linha is None:
            J = r
        else:
            J = r + self.gamma * self.mem_aprend.q(s_linha, a_linha)

        q_atual = self.mem_aprend.q(s, a)
        q_novo = q_atual + self.alpha * (J - q_atual)
        
        self.mem_aprend.actualizar(s, a, q_novo)
