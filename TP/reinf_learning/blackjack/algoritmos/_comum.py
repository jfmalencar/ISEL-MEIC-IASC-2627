from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from agente import Agente
from ambiente.blackjack_ambiente_52 import AmbienteBlackjack52, EstadoBlackjack
from metricas import ConfiguracaoTreino, MetricasTreino


@dataclass
class ResultadoTreino:
    configuracao: ConfiguracaoTreino
    agente: Agente
    ambiente: AmbienteBlackjack52
    ambiente_avaliacao: AmbienteBlackjack52
    metricas: MetricasTreino
    recompensa_treino: float
    recompensa_avaliacao: float

    @property
    def vitorias_avaliacao(self) -> int:
        return self.ambiente_avaliacao.vitorias

    @property
    def derrotas_avaliacao(self) -> int:
        return self.ambiente_avaliacao.derrotas

    @property
    def empates_avaliacao(self) -> int:
        return self.ambiente_avaliacao.empates


class TreinoBlackjack(ABC):
    def __init__(self, configuracao: ConfiguracaoTreino | int):
        if isinstance(configuracao, int):
            configuracao = ConfiguracaoTreino(
                algoritmo=self.nome, num_episodios=configuracao
            )
        self.configuracao = configuracao
        self.metricas = MetricasTreino(configuracao)

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome apresentado ao utilizador."""

    @abstractmethod
    def criar_algoritmo(self, agente: Agente, observador):
        """Cria o algoritmo de aprendizagem usado pelo treino."""

    @abstractmethod
    def executar_episodio(self, ambiente, agente: Agente, algoritmo) -> float:
        """Executa um episódio e devolve a recompensa acumulada."""

    def registar_acao(self, estado, acao: int) -> None:
        self.metricas.registar_acao(estado, acao)

    def treinar(self) -> ResultadoTreino:
        ambiente = AmbienteBlackjack52()
        agente = Agente(
            accoes_disponiveis=[0, 1],
            valor_inicial=0.0,
            epsilon=self.configuracao.epsilon,
        )
        algoritmo = self.criar_algoritmo(
            agente, self.metricas.registar_actualizacao
        )

        recompensa_treino = 0.0
        for episodio in range(1, self.configuracao.num_episodios + 1):
            self.metricas.iniciar_episodio(episodio, "treino")
            recompensa = self.executar_episodio(ambiente, agente, algoritmo)
            self.metricas.finalizar_episodio(recompensa, ambiente, algoritmo)
            recompensa_treino += recompensa

        ambiente_avaliacao = AmbienteBlackjack52()
        recompensa_avaliacao = self._avaliar(
            ambiente_avaliacao, agente, algoritmo
        )
        return ResultadoTreino(
            self.configuracao,
            agente,
            ambiente,
            ambiente_avaliacao,
            self.metricas,
            recompensa_treino,
            recompensa_avaliacao,
        )

    def _avaliar(self, ambiente, agente, algoritmo) -> float:
        epsilon_anterior = agente.seleccao_accao.epsilon
        agente.seleccao_accao.epsilon = 0.0
        recompensa_total = 0.0
        try:
            for episodio in range(1, self.configuracao.num_avaliacao + 1):
                self.metricas.iniciar_episodio(episodio, "avaliacao")
                estado = ambiente.reiniciar()
                final = False
                recompensa = 0.0
                while not final:
                    agente.atualizar_accoes(ambiente.accoes(estado))
                    acao = agente.seleccao_accao.accao_sofrega(estado)
                    self.registar_acao(estado, acao)
                    estado, recompensa, final = ambiente.passo(acao)
                self.metricas.finalizar_episodio(recompensa, ambiente, algoritmo)
                recompensa_total += recompensa
        finally:
            agente.seleccao_accao.epsilon = epsilon_anterior
        return recompensa_total


def apresentar_resultados(resultado: ResultadoTreino) -> None:
    config = resultado.configuracao
    ambiente = resultado.ambiente_avaliacao
    episodios = config.num_avaliacao
    print(f"\n=== RESULTADOS: {config.algoritmo} ===")
    print(f"Episódios de treino: {config.num_episodios}")
    print(f"Recompensa média de treino: {resultado.recompensa_treino / config.num_episodios:.4f}")
    if episodios:
        print(f"Recompensa média de avaliação: {resultado.recompensa_avaliacao / episodios:.4f}")
        print(f"Vitórias na avaliação: {ambiente.vitorias} ({ambiente.vitorias / episodios:.2%})")
        print(f"Derrotas na avaliação: {ambiente.derrotas} ({ambiente.derrotas / episodios:.2%})")
        print(f"Empates na avaliação: {ambiente.empates} ({ambiente.empates / episodios:.2%})")

    print("\n=== POLÍTICA APRENDIDA (Sem Ás Utilizável) ===")
    print("Soma J. | Dealer (1..10)  [0 = Stick, 1 = Hit]")
    print("-" * 60)
    for soma in range(12, 22):
        decisoes = [
            str(resultado.agente.seleccao_accao.accao_sofrega(
                EstadoBlackjack(soma, dealer, 0)
            ))
            for dealer in range(1, 11)
        ]
        print(f"  {soma:2d}    | " + "  ".join(decisoes))
