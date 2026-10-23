from memoria_aprendizagem import MemoriaDeAprendizagem
from selecao_acao import SeleccaoAccaoEGreedy

class SARSA:
    def __init__(self, memoria: MemoriaDeAprendizagem, seleccao_accao: SeleccaoAccaoEGreedy, alpha: float = 0.1, gamma: float = 0.9):
        self.memoria = memoria
        self.politica = seleccao_accao
        self.alpha = alpha
        self.gamma = gamma

    def aprender(self, s: int, a, r: float, s_linha: int, a_linha):
        """
        Atualiza a estimativa Q(s, a) usando a regra de atualização SARSA:
        Q(s, a) <- Q(s, a) + alpha * (r + gamma * Q(s', a') - Q(s, a))
        """

        q_sa = self.memoria.q(s, a)
        q_slal = self.memoria.q(s_linha, a_linha)

        q_novo = q_sa + self.alpha * (r + self.gamma * q_slal - q_sa)
        self.memoria.actualizar(s, a, q_novo)

#--------------------------------------------------------------------------

def treinar_agente_sarsa(ambiente, sarsa: SARSA, num_episodios: int = 100):
    for episodio in range(num_episodios):
        # 1. Iniciar estado s
        s = ambiente.reiniciar()
        accoes_disponiveis = ambiente.accoes(s)

        # 2. Escolher a de acordo com s com base na política e-greedy
        a = sarsa.politica.seleccionar_accao(s, accoes_disponiveis)

        e_terminal = False
        while not e_terminal and a is not None:
            # 3. Executar ação a, observar r e s'
            s_linha, r, e_terminal = ambiente.passo(a)

            if not e_terminal:
                # 4. Escolher a' de acordo com s' com base na política e-greedy
                accoes_proximas = ambiente.accoes(s_linha)
                a_linha = sarsa.politica.accao_sofrega(s_linha, accoes_proximas)

                # 5. Passo de aprendizagem s -> a -> r -> s' -> a'
                sarsa.aprender(s, a, r, s_linha, a_linha)

                # 6. Atualizar s <- s', a <- a'
                s, a = s_linha, a_linha
            else:
                # Tratar passo de experiência final (estado terminal)
                sarsa.aprender(s, a, r, s_linha, a_linha=None)