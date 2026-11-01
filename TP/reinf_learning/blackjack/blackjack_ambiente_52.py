import random

from blackjack_ambiente import AmbienteBlackjack, EstadoBlackjack


class AmbienteBlackjack52(AmbienteBlackjack):
    """Ambiente Blackjack com um baralho físico de 52 cartas sem reposição."""

    def __init__(self):
        super().__init__()
        self._baralho = []

    def _novo_baralho(self) -> list[tuple[int, int]]:
        """Cria um baralho com 13 valores e 4 naipes."""
        return [
            (valor, naipe)
            for naipe in range(4)
            for valor in range(1, 14)
        ]

    def _comprar_carta(self) -> int:
        """Retira uma carta do baralho e devolve o seu valor Blackjack."""
        if not self._baralho:
            raise RuntimeError("Não existem cartas suficientes no baralho.")

        valor, _ = self._baralho.pop()
        return min(valor, 10)

    def reiniciar(self) -> EstadoBlackjack:
        """Reinicia o baralho e começa um novo episódio."""
        self._baralho = self._novo_baralho()
        random.shuffle(self._baralho)
        return super().reiniciar()

    @property
    def cartas_restantes(self) -> int:
        """Número de cartas físicas ainda disponíveis no episódio."""
        return len(self._baralho)
