
class CamadaDeEntrada:
    # Dimensão de saída da camada de entrada
    d_s: int
    # Saída da camada de entrada
    y: list

    def __init__(self, d_s: int):
        """
        Inicia uma camada de entrada com a dimensão de saída d_s.
            - d_s: dimensão de saída da camada de entrada (número de neurónios na camada)
        """

        # A dimensão de saída deve pertencer a Z^+
        if d_s <= 0:
            raise ValueError("A dimensão de saída deve ser um inteiro positivo.")

        # Dimensão de saída
        self.d_s = d_s

        # Inicializar a saída da camada de entrada como uma lista de zeros com tamanho d_s
        self.y = [0] * d_s

    def propagar(self, x: list):
        """
        Propaga a entrada x através da camada de entrada, armazenando a saída na variável y.
            - x: vetor de entrada da camada de entrada (deve ter dimensão d_s)
            
            - retorna: saída da camada de entrada (y)
        """

        # A dimensão da entrada deve ser igual à dimensão de saída da camada de entrada
        if len(x) != self.d_s:
            raise ValueError(f"A dimensão do vetor de entrada deve ser {self.d_s}.")

        # Armazenar a entrada x como a saída da camada de entrada
        self.y = x

        # Retornar a saída da camada de entrada
        return self.y