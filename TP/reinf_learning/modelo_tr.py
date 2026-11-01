import random
from estado import Estado

class ModeloTR:
    """
    Modelo do mundo para ambientes deterministas, responsável por guardar o
    modelo de transição T(s, a) = s_linha e de recompensa R(s, a) = r.
    """
    def __init__(self):
        self.T = {}  # Mapeamento (s, a) -> s_linha
        self.R = {}  # Mapeamento (s, a) -> r

    def actualizar(self, s: Estado, a, s_linha: Estado, r: float):
        """Atualiza o modelo de transição e recompensa."""
        self.T[(s, a)] = s_linha
        self.R[(s, a)] = r

    def amostrar(self):
        if not self.T:
            return None
        s, a = random.choice(list(self.T.keys()))
        s_linha = self.T[(s, a)]
        r = self.R[(s, a)]
        return s, a, r, s_linha