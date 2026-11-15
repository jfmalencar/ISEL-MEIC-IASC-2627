import random

from estado import Estado


class EstadoBlackjack(Estado):
    def __init__(self, soma_jogador: int, carta_dealer: int, as_utilizavel: int):
        self.soma_jogador = soma_jogador
        self.carta_dealer = carta_dealer
        self.as_utilizavel = as_utilizavel

    def ao_tuplo(self):
        return (self.soma_jogador, self.carta_dealer, self.as_utilizavel)

    def __hash__(self):
        return hash(self.ao_tuplo())

    def __eq__(self, outro):
        return isinstance(outro, EstadoBlackjack) and self.ao_tuplo() == outro.ao_tuplo()

    def __str__(self):
        return f"(Soma={self.soma_jogador}, Dealer={self.carta_dealer}, ÁsUtil={self.as_utilizavel})"

    def __repr__(self):
        return str(self)


class AmbienteBlackjack52:
    """Ambiente Blackjack com um baralho físico de 52 cartas sem reposição."""

    def __init__(self):
        self.estado_atual = None
        self.mao_jogador = []
        self.mao_dealer = []
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        self._baralho = []

    def _novo_baralho(self) -> list[tuple[int, int]]:
        """Cria um baralho com 13 valores e 4 naipes."""
        return [
            (valor, naipe)
            for naipe in range(4)
            for valor in range(1, 14)
        ]

    def _comprar_carta(self) -> int:
        """Retira uma carta física do baralho e devolve o seu valor Blackjack."""
        if not self._baralho:
            raise RuntimeError("Não existem cartas suficientes no baralho.")

        valor, _ = self._baralho.pop()
        return min(valor, 10)

    def _avaliar_mao(self, mao: list[int]) -> tuple[int, int]:
        soma = sum(mao)
        as_utilizavel = 0
        if 1 in mao and soma + 10 <= 21:
            soma += 10
            as_utilizavel = 1
        return soma, as_utilizavel

    def _registar_resultado(self, recompensa: float) -> None:
        if recompensa > 0:
            self.vitorias += 1
        elif recompensa < 0:
            self.derrotas += 1
        else:
            self.empates += 1

    def reiniciar_estatisticas(self) -> None:
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

    def reiniciar(self) -> EstadoBlackjack:
        self._baralho = self._novo_baralho()
        random.shuffle(self._baralho)
        self.mao_jogador = [self._comprar_carta(), self._comprar_carta()]
        self.mao_dealer = [self._comprar_carta(), self._comprar_carta()]
        soma_j, as_util = self._avaliar_mao(self.mao_jogador)
        self.estado_atual = EstadoBlackjack(soma_j, self.mao_dealer[0], as_util)
        return self.estado_atual

    def accoes(self, estado: EstadoBlackjack) -> list:
        if estado is None or estado.soma_jogador > 21:
            return []
        return [0, 1]

    def passo(self, acao: int):
        if self.estado_atual is None:
            raise RuntimeError("O episódio ainda não foi iniciado.")
        if acao not in (0, 1):
            raise ValueError("A ação deve ser 0 (Stick) ou 1 (Hit).")
        if self.estado_atual.soma_jogador > 21:
            raise RuntimeError("O episódio já terminou.")

        if acao == 1:
            self.mao_jogador.append(self._comprar_carta())
            soma_j, as_util = self._avaliar_mao(self.mao_jogador)
            self.estado_atual = EstadoBlackjack(
                soma_j, self.estado_atual.carta_dealer, as_util
            )
            if soma_j > 21:
                self._registar_resultado(-1.0)
                return self.estado_atual, -1.0, True
            return self.estado_atual, 0.0, False

        soma_j, _ = self._avaliar_mao(self.mao_jogador)
        soma_d, _ = self._avaliar_mao(self.mao_dealer)
        jogador_blackjack = len(self.mao_jogador) == 2 and soma_j == 21
        dealer_blackjack = len(self.mao_dealer) == 2 and soma_d == 21
        if jogador_blackjack:
            recompensa = 0.0 if dealer_blackjack else 1.5
        elif dealer_blackjack:
            recompensa = -1.0
        else:
            while soma_d < 17:
                self.mao_dealer.append(self._comprar_carta())
                soma_d, _ = self._avaliar_mao(self.mao_dealer)
            recompensa = (
                1.0 if soma_d > 21 or soma_j > soma_d
                else -1.0 if soma_j < soma_d
                else 0.0
            )
        self._registar_resultado(recompensa)
        return self.estado_atual, recompensa, True

    @property
    def cartas_restantes(self) -> int:
        """Número de cartas físicas ainda disponíveis no episódio."""
        return len(self._baralho)
