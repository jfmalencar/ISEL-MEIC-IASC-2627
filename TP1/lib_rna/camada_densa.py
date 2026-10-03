from .funcao_ativacao import FuncaoAtivacao
from .neuronio import Neuronio

class CamadaDensa:
    # Dimensão de entrada da camada densa
    d_e: int
    # Dimensão de saída da camada densa
    d_s: int
    # Função de ativação da camada densa
    funcao_ativacao: FuncaoAtivacao
    # Neurónios da camada densa
    neuronios: list
    
    def __init__(self, d_e: int, d_s: int, phi: FuncaoAtivacao):
        """
        Inicia uma camada densa com a dimensão de entrada d_e, a dimensão de saída d_s e a função de ativação phi.
            - d_e: dimensão de entrada da camada densa (número de entradas)
            - d_s: dimensão de saída da camada densa (número de neurónios)
            - phi: função de ativação a ser utilizada por todos os neurónios da camada
        """

        # A dimensão de entrada e a dimensão de saída devem pertencer a Z^+
        if d_e <= 0:
            raise ValueError("A dimensão de entrada deve ser um inteiro positivo.")
        self.d_e = d_e

        # A dimensão de saída deve pertencer a Z^+
        if d_s <= 0:
            raise ValueError("A dimensão de saída deve ser um inteiro positivo.")
        self.d_s = d_s

        # A função de ativação deve ser uma instância da classe FuncaoAtivacao
        if not isinstance(phi, FuncaoAtivacao):
            raise ValueError("A função de ativação deve ser uma instância da classe FuncaoAtivacao.")

        # Inicializar a função de ativação
        self.funcao_ativacao = phi

        # Inicializar os neurónios da camada densa
        self.neuronios = [Neuronio(d_e, self.funcao_ativacao) for _ in range(d_s)]

    @property
    def y(self):
        """
        Propriedade que retorna a saída da camada densa, que é a saída de todos os neurónios da camada.
        """

        # Retornar a saída de todos os neurónios da camada densa
        return [neuronio.y for neuronio in self.neuronios]

    def propagar(self, x: list):
        """
        Propaga a entrada x através da camada densa, calculando a saída de cada neurónio.
            - x: vetor de entrada da camada densa

            - retorna: vetor de saída da camada densa
        """

        # A dimensão da entrada deve ser igual à dimensão de entrada da camada densa
        if len(x) != self.d_e:
            raise ValueError(f"A dimensão do vetor de entrada deve ser {self.d_e}.")

        # Propagar a entrada x através de todos os neurónios da camada densa
        y = [neuronio.propagar(x) for neuronio in self.neuronios]

        # Retornar a saída da camada densa
        return y

    # Parte 2 --------------------------------
    def adaptar (self, prop_err_saida: list, saida_camada_anterior: list, taxa_aprendizagem: float):
        """
        Adapta os pesos e o pendor de todos os neurónios da camada densa com base no vetor de erro de saída, na saída da camada anterior e na taxa de aprendizagem.
            - prop_err_saida: vetor de erro de saída da camada densa
            - saida_camada_anterior: vetor de saída da camada anterior
            - taxa_aprendizagem: taxa de aprendizagem a ser utilizada na adaptação dos pesos e do pendor
        """

        # A dimensão do vetor de erro de saída deve ser igual à dimensão de saída da camada densa
        if len(prop_err_saida) != len(self.neuronios):
            raise ValueError(f"A dimensão do vetor de erro de saída deve ser {len(self.neuronios)}.")

        # Adaptar os pesos e o pendor de todos os neurónios da camada densa
        for i, neuronio in enumerate(self.neuronios):
            neuronio.adaptar(prop_err_saida[i], saida_camada_anterior, taxa_aprendizagem)