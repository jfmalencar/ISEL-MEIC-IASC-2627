from agente import Agente
from algoritmos._comum import TreinoBlackjack
from sarsa import SARSA


class TreinoSARSA(TreinoBlackjack):
    @property
    def nome(self) -> str:
        return "SARSA"

    def criar_algoritmo(self, agente: Agente, observador):
        return SARSA(
            agente.memoria,
            agente.seleccao_accao,
            alfa=self.configuracao.alfa,
            gama=self.configuracao.gama,
            observador=observador,
        )

    def executar_episodio(self, ambiente, agente: Agente, algoritmo) -> float:
        estado = ambiente.reiniciar()
        agente.atualizar_accoes(ambiente.accoes(estado))
        acao = agente.seleccao_accao.seleccionar_accao(estado)
        self.registar_acao(estado, acao)
        recompensa_total = 0.0
        final = False

        while not final:
            novo_estado, recompensa, final = ambiente.passo(acao)
            recompensa_total += recompensa
            if final:
                proxima_acao = None
            else:
                agente.atualizar_accoes(ambiente.accoes(novo_estado))
                proxima_acao = agente.seleccao_accao.seleccionar_accao(novo_estado)
                self.registar_acao(novo_estado, proxima_acao)
            algoritmo.aprender(
                estado, acao, recompensa, novo_estado, proxima_acao, final
            )
            estado, acao = novo_estado, proxima_acao
        return recompensa_total
