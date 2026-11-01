class Ambiente1DTeste:
    def __init__(self):
        # Conjunto de Estados S = {0, 1, 2, 3, 4, 5, 6}
        self.estados = list(range(0, 8))
        self.estado_inicial = 3
        self.estado_atual = self.estado_inicial

    def reiniciar(self) -> int:
        """Reinicia o ambiente para o estado inicial no início de um episódio."""
        self.estado_atual = self.estado_inicial
        return self.estado_atual

    def accoes(self, s: int) -> list:
        """Retorna o conjunto de ações A(s) válidas no estado s."""
        if s in (0, 6):  # Estados terminais não têm ações
            return []
        return ["esquerda", "direita"]

    def passo(self, a: str):
        """
        Executa a ação a no ambiente e retorna (s_linha, r, e_terminal).
        Transições e Recompensas R(s, a, s'):
          - Movimento para a posição 6 -> Ganho (+1), terminal
          - Movimento para a posição 0 -> Perda (-1), terminal
          - Outras posições -> Recompensa 0, não terminal
        """
        s = self.estado_atual

        if a == "esquerda":
            s_linha = max(0, s - 1)
        elif a == "direita":
            s_linha = min(6, s + 1)
        else:
            s_linha = s

        self.estado_atual = s_linha

        # Definição de Recompensa e Estado Terminal
        if s_linha == 6:
            r = 1.0
            e_terminal = True
        elif s_linha == 0:
            r = -1.0
            e_terminal = True
        else:
            r = 0.0
            e_terminal = False

        return s_linha, r, e_terminal