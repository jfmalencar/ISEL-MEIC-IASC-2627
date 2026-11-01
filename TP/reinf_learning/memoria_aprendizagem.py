from estado import Estado

class MemoriaDeAprendizagem:
    def __init__(self, valor_omissao: float = 0.0):
        self.valor_omissao = valor_omissao
        self.Q = {}         # Mapeamento (s, a) -> valor real

    def q(self, s: Estado, a) -> float:
        """Obter Q(s, a). Se não existir, retorna o valor de omissão."""
        return self.Q.get((s, a), self.valor_omissao)

    def actualizar(self, s: Estado, a, q_valor: float):
        """Atualizar a estimativa Q(s, a)"""
        self.Q[(s, a)] = q_valor
