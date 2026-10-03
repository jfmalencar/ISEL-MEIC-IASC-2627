
from .camada_de_entrada import CamadaDeEntrada
from .camada_densa import CamadaDensa
from .funcao_ativacao import FuncaoAtivacao


class RedeNeuronal:
    # Camadas da rede neuronal
    camadas: list

    def __init__(self, forma: list, phi: FuncaoAtivacao):
        """
        Inicia uma rede neuronal com a forma especificada e a função de ativação phi.
            - forma: lista com a dimensão de cada camada da rede neuronal
            - phi: função de ativação a ser utilizada por todos os neurónios da rede
        """

        # Lista de camadas da rede neuronal
        camadas = []

        # Numero de camadas da rede neuronal
        N = len(forma)

        # Dimensão de saída da primeira camada (camada de entrada)
        d_s_1 = forma[0]

        # Inicializar a primeira camada como uma camada de entrada e adicioná-la à lista de camadas
        camada_1 = CamadaDeEntrada(d_s_1)
        camadas.append(camada_1)

        # Inicializar as camadas densas restantes e adicioná-las à lista de camadas
        for i in range(1, N):
            # Dimensão de entrada da camada densa
            d_e_n = forma[i - 1]
            # Dimensão de saída da camada densa
            d_s_n = forma[i]
            # Inicializar a camada densa e adicioná-la à lista de camadas
            camada_i = CamadaDensa(d_e_n, d_s_n, phi)
            camadas.append(camada_i)

        # Armazenar a lista de camadas
        self.camadas = camadas

    def prever(self, X: list):
        """
        Prevê as saídas da rede neuronal para as entradas X.
            - X: lista de amostras

            - retorna: lista de saídas previstas pela rede neuronal
        """

        # Propagar cada amostra de entrada X através da rede neuronal
        Y = [self.propagar(x) for x in X]

        # Retornar as saídas previstas
        return Y

    def propagar(self, x: list):
        """
        Propaga a entrada x através da rede neuronal.
            - x: lista com a entrada

            - retorna: saída da rede neuronal
        """

        # Inicializar a saída como a entrada da rede neuronal
        y = x

        # Propagar a entrada x através de todas as camadas da rede neuronal
        for camada in self.camadas:
            y = camada.propagar(y)

        # Retornar a saída da rede neuronal
        return y

    # Parte 2 --------------------------------
    @staticmethod
    def delta_saida(y_N: list, y: list):
        """
        Calcula a perda de saída da rede neuronal com base na saída prevista y_N e na saída desejada y.
            - y_N: vetor de treino de saída da rede neuronal
            - y: vetor de saida gerado pela rede neuronal

            - retorna: vetor de perda de saída da rede neuronal
        """
        return [y_N[i] - y[i] for i in range(len(y))]

    def retropropagar(self, delta_N: list, taxa_aprendizagem: float):
        """
        Retropropaga o erro de saída delta_N através da rede neuronal, adaptando os pesos e o pendor de cada camada com base na taxa de aprendizagem.
            - delta_N: vetor de erro de saída da rede neuronal
            - taxa_aprendizagem: taxa de aprendizagem a ser utilizada na adaptação dos pesos e do pendor
        """

        # Vetor de erro de saída da rede neuronal
        delta_n = delta_N

        for n in range(len(self.camadas) - 1, 0, -1):
            # Camada atual e camada anterior
            camada_atual = self.camadas[n]
            camada_anterior = self.camadas[n - 1]

            # Dimensão da saída da camada anterior
            d_anterior = len(camada_anterior.y)

            # Calcular o vetor de erro da camada anterior com base no vetor de erro da camada atual, nos pesos da camada atual e na derivada da saída da camada atual
            delta_anterior = [
                sum(
                    camada_atual.neuronios[j].pesos[i] * delta_n[j] * camada_atual.neuronios[j].derivada_y
                    for j in range(len(camada_atual.neuronios))
                )
                for i in range(d_anterior)
            ]

            # Adaptar os pesos e o viés da camada atual com base no vetor de erro da camada atual e na saída da camada anterior
            camada_atual.adaptar(delta_n, camada_anterior.y, taxa_aprendizagem)

            # Atualizar o vetor de erro da camada anterior para a próxima iteração
            delta_n = delta_anterior

    def adaptar(self, x: list, y: list, taxa_aprendizagem: float):
        """
        Adapta os pesos e o pendor da rede neuronal com base na entrada x, na saída desejada y e na taxa de aprendizagem.
            - x: vetor de treino de entrada da rede neuronal
            - y: vetor de treino de saída da rede neuronal
            - taxa_aprendizagem: taxa de aprendizagem a ser utilizada na adaptação dos pesos e do pendor

            - retorna: erro quadrático médio da rede neuronal
        """

        # Propagar a entrada x através da rede neuronal para obter a saída y_N
        y_N = self.propagar(x)

        # Calcular o vetor de erro de saída da rede neuronal com base na saída prevista y_N e na saída desejada y
        delta_N = self.delta_saida(y_N, y)

        # Retropropagar o erro de saída delta_N através da rede neuronal, adaptando os pesos e o pendor de cada camada com base na taxa de aprendizagem
        self.retropropagar(delta_N, taxa_aprendizagem)

        # Comprimento do vetor de erro de saída da rede neuronal
        # Prev: len(self.camadas) <= ERRO TODO
        K = len(delta_N)

        # Calcular o erro quadrático médio da rede neuronal com base no vetor de erro de saída delta_N
        mean_squared_error = sum(d ** 2 for d in delta_N) / K

        # Retornar o erro quadrático médio da rede neuronal
        return mean_squared_error

    def treinar(self, X: list, Y: list, n_epocas: int, erro_max: float, taxa_aprendizagem: float):
        """
        Treina a rede neuronal com base em um conjunto de dados de treino.
            - X: conjunto de entradas de treino da rede neuronal
            - Y: conjunto de saídas de treino da rede neuronal
            - n_epocas: número de épocas de treino
            - erro_max: erro máximo
            - taxa_aprendizagem: taxa de aprendizagem a ser utilizada na adaptação dos pesos e do pendor
        """

        # Treinar a rede neuronal por n_epocas ou até que o erro seja menor que erro_max
        for epoca in range(n_epocas):
            # Inicializar o erro total da época
            erro_epoca = 0

            # Para cada amostra de treino, adaptar os pesos e o pendor da rede neuronal e acumular o erro total
            for x, y in zip(X, Y):
                erro_entrada_x = self.adaptar(x, y, taxa_aprendizagem)
                erro_epoca = max(erro_epoca, erro_entrada_x)
            if epoca == 0:
                print(f"[{erro_epoca:.6f}, ", end="")
            elif epoca == n_epocas - 1:
                print(f"{erro_epoca:.6f}]")
            elif erro_epoca <= erro_max:
                print(f"{erro_epoca:.6f}]")
            else:
                print(f"{erro_epoca:.6f}, ", end="")
            # Se o erro médio for menor que o erro máximo, interromper o treino
            if erro_epoca <= erro_max:
                print(f"Numero de épocas: {epoca + 1}")
                break