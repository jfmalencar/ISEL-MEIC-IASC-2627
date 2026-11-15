from agente import Agente
from algoritmos._comum import TreinoBlackjack
from q_learning import QLearning


class TreinoQLearning(TreinoBlackjack):
    @property
    def nome(self) -> str:
        return "Q-Learning"

    def criar_algoritmo(self, agente: Agente, observador):
        return QLearning(
            agente.memoria,
            agente.seleccao_accao,
            alfa=self.configuracao.alfa,
            gama=self.configuracao.gama,
            observador=observador,
        )

    def executar_episodio(self, ambiente, agente: Agente, algoritmo) -> float:
        estado = ambiente.reiniciar()
        recompensa_total = 0.0
        final = False
        while not final:
            agente.atualizar_accoes(ambiente.accoes(estado))
            acao = agente.seleccao_accao.seleccionar_accao(estado)
            self.registar_acao(estado, acao)
            novo_estado, recompensa, final = ambiente.passo(acao)
            algoritmo.aprender(estado, acao, recompensa, novo_estado, final=final)
            estado = novo_estado
            recompensa_total += recompensa
        return recompensa_total
