import random


class AmbienteCliffWalking:
    """Ambiente Cliff Walking numa grelha de 4 linhas por 12 colunas."""

    N_LINHAS = 4
    N_COLUNAS = 12
    INICIO = 36
    OBJETIVO = 47
    PRECIPICIO = frozenset(range(37, 47))
    ACCOES = (0, 1, 2, 3)

    def __init__(self, is_slippery: bool = False):
        self.is_slippery = is_slippery
        self.estado_atual = self.INICIO
        self.passos = 0
        self.quedas_no_precipicio = 0

    def reiniciar(self) -> int:
        """Reinicia o episódio e devolve a observação inicial."""
        self.estado_atual = self.INICIO
        self.passos = 0
        return self.estado_atual

    def reset(self) -> tuple[int, dict[str, float]]:
        """Alias compatível com a API habitual de ambientes."""
        return self.reiniciar(), {"p": 1.0}

    def accoes(self, estado: int) -> list[int]:
        """Devolve as quatro ações enquanto o episódio não terminou."""
        if estado == self.OBJETIVO:
            return []
        return list(self.ACCOES)

    def _movimento_efetivo(self, acao: int) -> int:
        if not self.is_slippery:
            return acao
        if acao == 0:
            return random.choice((0, 1, 3))
        if acao == 1:
            return random.choice((1, 0, 2))
        if acao == 2:
            return random.choice((2, 1, 3))
        return random.choice((3, 2, 0))

    def _nova_posicao(self, estado: int, acao: int) -> int:
        linha, coluna = divmod(estado, self.N_COLUNAS)
        if acao == 0:
            linha = max(0, linha - 1)
        elif acao == 1:
            coluna = min(self.N_COLUNAS - 1, coluna + 1)
        elif acao == 2:
            linha = min(self.N_LINHAS - 1, linha + 1)
        else:
            coluna = max(0, coluna - 1)
        return linha * self.N_COLUNAS + coluna

    def passo(self, acao: int) -> tuple[int, float, bool, dict[str, float]]:
        """Executa uma ação e devolve observação, recompensa, fim e informação."""
        if acao not in self.ACCOES:
            raise ValueError("A ação deve estar no intervalo 0..3.")
        if self.estado_atual == self.OBJETIVO:
            raise RuntimeError("O episódio já terminou.")

        acao_efetiva = self._movimento_efetivo(acao)
        nova_posicao = self._nova_posicao(self.estado_atual, acao_efetiva)
        self.passos += 1

        if nova_posicao in self.PRECIPICIO:
            self.estado_atual = self.INICIO
            self.quedas_no_precipicio += 1
            return self.estado_atual, -100.0, False, {"p": 1.0}

        self.estado_atual = nova_posicao
        terminou = nova_posicao == self.OBJETIVO
        return self.estado_atual, -1.0, terminou, {"p": 1.0}

    def step(self, acao: int) -> tuple[int, float, bool, dict[str, float]]:
        """Alias em inglês para executar uma transição."""
        return self.passo(acao)
