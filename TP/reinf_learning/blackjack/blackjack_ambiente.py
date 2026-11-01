import random
from estado import Estado

class EstadoBlackjack(Estado):
    """
    Representação do Estado no Blackjack: (soma_jogador, carta_dealer, as_utilizavel)
    """
    def __init__(self, soma_jogador: int, carta_dealer: int, as_utilizavel: int):
        self.soma_jogador = soma_jogador      # 4..21
        self.carta_dealer = carta_dealer      # 1..10 (1 = Ás)
        self.as_utilizavel = as_utilizavel    # 0 ou 1

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

class AmbienteBlackjack:
    """
    Ambiente Blackjack segundo Sutton & Barto (Exemplo 5.1).
    Ações:
      0: Stick (Parar)
      1: Hit (Pedir Carta)
    """
    def __init__(self):
        self.estado_atual = None
        self.mao_jogador = []
        self.mao_dealer = []
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

    def reiniciar_estatisticas(self) -> None:
        """Repõe os contadores de resultados a zero."""
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

    def _registar_resultado(self, recompensa: float) -> None:
        """Regista o resultado terminal com base na recompensa final."""
        if recompensa > 0:
            self.vitorias += 1
        elif recompensa < 0:
            self.derrotas += 1
        else:
            self.empates += 1

    def _comprar_carta(self) -> int:
        """Sorteia uma carta do baralho infinito com reposição (figuras valem 10)."""
        carta = random.randint(1, 13)
        return min(carta, 10)

    def _avaliar_mao(self, mao: list[int]) -> tuple[int, int]:
        """Calcula a soma da mão e verifica se existe um Ás utilizável (como 11)."""
        soma = sum(mao)
        tem_as = 1 in mao
        as_utilizavel = 0

        if tem_as and soma + 10 <= 21:
            soma += 10
            as_utilizavel = 1

        return soma, as_utilizavel

    def reiniciar(self) -> EstadoBlackjack:
        """Inicia um novo episódio e distribui 2 cartas ao jogador e 2 ao dealer."""
        self.mao_jogador = [self._comprar_carta(), self._comprar_carta()]
        self.mao_dealer = [self._comprar_carta(), self._comprar_carta()]

        soma_j, as_util = self._avaliar_mao(self.mao_jogador)
        carta_visivel_dealer = self.mao_dealer[0]

        self.estado_atual = EstadoBlackjack(soma_j, carta_visivel_dealer, as_util)
        return self.estado_atual

    def accoes(self, estado: EstadoBlackjack) -> list:
        """Devolve as ações válidas se o jogador não tiver excedido 21."""
        if estado is None or estado.soma_jogador > 21:
            return []
        return [0, 1]

    def passo(self, acao: int):
        """
        Executa a ação selecionada pelo agente:
          - acao = 1 (Hit): Compra carta. Se > 21 -> Bust (r = -1.0, final = True).
          - acao = 0 (Stick): Dealer joga até soma >= 17 e determina o resultado final.
        """
        if self.estado_atual is None:
            raise RuntimeError("O episódio ainda não foi iniciado.")
        if acao not in (0, 1):
            raise ValueError("A ação deve ser 0 (Stick) ou 1 (Hit).")
        if self.estado_atual.soma_jogador > 21:
            raise RuntimeError("O episódio já terminou.")

        if acao == 1:  # Hit
            self.mao_jogador.append(self._comprar_carta())
            soma_j, as_util = self._avaliar_mao(self.mao_jogador)

            if soma_j > 21:  # Bust / Excedeu 21
                self.estado_atual = EstadoBlackjack(soma_j, self.estado_atual.carta_dealer, as_util)
                self._registar_resultado(-1.0)
                return self.estado_atual, -1.0, True
            else:
                self.estado_atual = EstadoBlackjack(soma_j, self.estado_atual.carta_dealer, as_util)
                return self.estado_atual, 0.0, False

        else:  # Stick (acao == 0)
            soma_j, _ = self._avaliar_mao(self.mao_jogador)
            soma_d, _ = self._avaliar_mao(self.mao_dealer)

            jogador_blackjack = len(self.mao_jogador) == 2 and soma_j == 21
            dealer_blackjack = len(self.mao_dealer) == 2 and soma_d == 21
            if jogador_blackjack:
                recompensa = 0.0 if dealer_blackjack else 1.5
                self._registar_resultado(recompensa)
                return self.estado_atual, recompensa, True
            if dealer_blackjack:
                self._registar_resultado(-1.0)
                return self.estado_atual, -1.0, True

            # Turno do dealer: compra cartas até atingir pelo menos 17
            while soma_d < 17:
                self.mao_dealer.append(self._comprar_carta())
                soma_d, _ = self._avaliar_mao(self.mao_dealer)

            # Comparação do resultado final
            if soma_d > 21 or soma_j > soma_d:
                recompensa = 1.0   # Vitória do jogador
            elif soma_j < soma_d:
                recompensa = -1.0  # Vitória do dealer
            else:
                recompensa = 0.0   # Empate

            self._registar_resultado(recompensa)
            return self.estado_atual, recompensa, True
