class MemoriaDeAprendizagem:
    def __init__(self, valor_omissao: float = 0.0):
        self.valor_omissao = valor_omissao
        self.Q = {}         # Mapeamento (s, a) -> valor real
        self.estados = set() # Conjunto de estados observados

    def q(self, s, a) -> float:
        """Obter Q(s, a). Se não existir, retorna o valor de omissão."""
        return self.Q.get((s, a), self.valor_omissao)

    def actualizar(self, s, a, q_valor: float):
        """Atualizar a estimativa Q(s, a) e registar o estado s."""
        self.estados.add(s)
        self.Q[(s, a)] = q_valor

    def obter_estados(self) -> set:
        """Devolve o conjunto de estados conhecidos."""
        return self.estados