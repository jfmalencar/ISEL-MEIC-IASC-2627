import random

from .funcao_ativacao import FuncaoAtivacao

class Neuronio:
    # Dimensão da entrada do neurónio
    d: int
    # Função de ativação do neurónio
    funcao_ativacao: FuncaoAtivacao
    # Pesos das entradas do neurónio
    pesos: list
    # Pendor (bias) do neurónio
    pendor: float
    # Soma ponderada das entradas e pesos com o pendor
    h: float
    # Saída do neurónio após a aplicação da função de ativação
    y: float
    # Derivada da saída do neurónio
    derivada_y: float
    
    def __init__(self, d: int, phi: FuncaoAtivacao):
        """
        Inicia um Neurónio com a dimensão de entrada e a função de ativação.
            - d: dimensão da entrada (número de entradas do neurónio)
            - phi: função de ativação a ser utilizada pelo neurónio
        
        Os pesos e o pendor são inicializados aleatoriamente entre -1 e 1.
        A saída do neurónio (y) e a soma ponderada das entradas e pesos com o pendor (h) são inicializadas como 0.

        # Parte 2 --------------------------------
        A derivada da saída (derivada_y) também é inicializada como 0
        """

        # A dimensão da entrada deve pertencer a Z^+
        if d <= 0:
            raise ValueError("D deve ser um inteiro positivo.")

        # A função de ativação deve ser uma instância da classe FuncaoAtivacao
        if not isinstance(phi, FuncaoAtivacao):
            raise ValueError("A função de ativação deve ser uma instância da classe FuncaoAtivacao.")

        # Dimensão da entrada
        self.d = d

        # Função de ativação
        self.funcao_ativacao = phi
        
        # Pesos iniciais aleatórios entre -1 e 1
        self.pesos = [random.uniform(-1, 1) for _ in range(d)]
        
        # Pendor inicial aleatório entre -1 e 1
        self.pendor = random.uniform(-1, 1)
        
        # Soma ponderada das entradas e pesos com o pendor
        self.h = 0
        
        # Saída do neurónio após a aplicação da função de ativação
        self.y = 0

        # Parte 2 --------------------------------
        # Derivada da saída
        self.derivada_y = 0
        # ----------------------------------------
        

    def propagar(self, x: list):
        """
        Propaga a entrada x através do neurónio, calculando a soma ponderada das entradas 
        e pesos com o pendor (h) e aplicando a função de ativação para obter a saída (y).
            - x: vetor de entrada do neurónio (deve ter dimensão d)
            - retorna: saída do neurónio após a aplicação da função de ativação

        # Parte 2 --------------------------------
        A derivada da saída (derivada_y) também é calculada e armazenada.
        """

        # A dimensão da entrada deve ser igual à dimensão do neurónio
        if len(x) != self.d:
            raise ValueError(f"A dimensão do vetor de entrada deve ser {self.d}.")

        # Calcular a soma ponderada das entradas e pesos com o pendor
        self.h = sum(self.pesos[i] * x[i] for i in range(self.d)) + self.pendor

        # Atualizar a saída do neurónio após a aplicação da função phi
        self.y = self.funcao_ativacao.phi(self.h)

        # Parte 2 --------------------------------
        # Atualizar a derivada da saída do neurónio após a aplicação da derivada da função phi
        self.derivada_y = self.funcao_ativacao.derivada_phi(self.h)
        # ----------------------------------------

        # Retornar a saída do neurónio
        return self.y

    # Parte 2 --------------------------------
    def adaptar(self, propag_erro_saida: float, saida_camada_anterior: list, taxa_aprendizagem: float):
        """
        Adapta os pesos e o pendor do neurónio com base no erro de saída, na saída da camada anterior e na taxa de aprendizagem.
            - propag_erro_saida: componente de propagação do erro de saída do neurónio
            - saida_camada_anterior: vetor de saída da camada anterior (n-1)
            - taxa_aprendizagem: taxa de aprendizagem
        """

        # A dimensão da saída da camada anterior deve ser igual à dimensão do neurónio
        if len(saida_camada_anterior) != self.d:
            raise ValueError(f"A dimensão do vetor de saída da camada anterior deve ser {self.d}.")

        # Calcular o fator escalar: (-taxa_aprendizagem) * derivada_y * propag_erro_saida
        fator_escalar = (-taxa_aprendizagem) * self.derivada_y * propag_erro_saida

        # Calcular a variação dos pesos com base no fator escalar e na saída da camada anterior
        var_pesos = [fator_escalar * saida_camada_anterior[i] for i in range(self.d)]

        # Atualizar os pesos do neurónio com base no fator escalar e na saída da camada anterior
        self.pesos = [self.pesos[i] + var_pesos[i] for i in range(self.d)]

        # Atualizar o pendor do neurónio com base no fator escalar e no erro de saída
        self.pendor = self.pendor + fator_escalar