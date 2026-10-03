from enum import Enum
import math
from typing import Callable

class FuncaoAtivacao:
    # Função de ativação Phi
    phi: Callable[[float], float]
    # Derivada da função de ativação Phi
    derivada_phi: Callable[[float], float]

    def __init__(self, ativar: Callable[[float], float], derivada: Callable[[float], float]):
        """
        Inicia uma função de ativação com a função especificada e sua derivada.
            - ativar: função de ativação a ser utilizada
            - derivada: derivada da função de ativação a ser utilizada
        """

        # A função de ativação e sua derivada devem ser funções chamáveis (callable)
        if not callable(ativar):
            raise TypeError("A função de ativação deve ser uma função.")
        if not callable(derivada):
            raise TypeError("A derivada da função de ativação deve ser uma função.")

        # Inicializar a função de ativação e sua derivada
        self.phi = ativar
        self.derivada_phi = derivada

class FuncaoAtivacaoEnum(Enum):
    """
    Enumeração das funções de ativação disponíveis.
    """
    TANH = FuncaoAtivacao(
        ativar = lambda x: (math.tanh(x)),
        derivada = lambda x: (1 - math.tanh(x) ** 2)
    )

    SIGMOID = FuncaoAtivacao(
        ativar = lambda x: (1 / (1 + math.exp(-x))),
        derivada = lambda x: (1 / (1 + math.exp(-x))) * (1 - (1 / (1 + math.exp(-x))))
    )