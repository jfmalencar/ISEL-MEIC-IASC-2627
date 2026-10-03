from .funcao_ativacao import FuncaoAtivacao, FuncaoAtivacaoEnum
from .rede_neuronal import RedeNeuronal
import random

def normalizar_dados_input(x: list, nome_funcao_ativacao: str):
    """
    Normaliza os dados de entrada para o intervalo [-1, 1] se a função de ativação for TANH.
    Caso contrário, retorna os dados sem normalização.
    """
    if nome_funcao_ativacao.upper() == "TANH":
        # Normalizar os dados de entrada para o intervalo [-1, 1]
        x_normalized = [[(2 * val - 1) for val in sample] for sample in x]
        return x_normalized
    else:
        # Para outras funções de ativação, retornar os dados sem normalização
        return x

def main():
    """
    Função principal que testa a implementação da rede neuronal.
    
    Caso de estudo utilizado: Detecção de barras verticais em uma matriz 3x3.
    - Conjunto de Dados de Treino: 7 amostras (3 positivas e 4 negativas)
    
    Parâmetros da rede neuronal:
    - Arquitetura: 
        + 9 neurônios na camada de entrada;
        + 3 neurônios na camada oculta;
        + 1 neurônio na camada de saída.
    
    - Função de Ativação: Tangente Hiperbólica (TANH)
    - Número de Épocas: 1000
    - Erro Máximo: 0.05
    - Taxa de Aprendizagem: 0.2
    """

    # 1. Conjunto de Dados de Treino
    X_treino = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1],
    ]

    Y_treino = [ 
        [0], 
        [1], 
        [1], 
        [1], 
        [0], 
        [0], 
        [0],
    ]

    # 2. Conjunto de Dados de Teste
    X_teste = [
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0]
    ]

    Y_teste = [
        [1],
        [1],
        [1],
        [0],
        [0],
        [0],
        [1],
        [0],
        [0],
        [1],
        [0],
        [0]
    ]

    # 3. Configuração dos Hiperparâmetros
    # Exemplo de arquitetura: Entrada (9) -> Oculta (3) -> Saída (1)
    forma_rede = [9, 3, 1] 

    funcao_ativacao = FuncaoAtivacaoEnum.TANH
    phi = funcao_ativacao.value

    n_epocas = 1000
    erro_max = 0.05
    taxa_aprendizagem = 0.2

    # 4. Inicialização da Rede Neuronal
    print("--- Inicializando a Rede Neuronal ---")
    rede = RedeNeuronal(forma=forma_rede, phi=phi)

    X_treino = normalizar_dados_input(X_treino, funcao_ativacao.name)
    print(f"Dados de treino normalizados para a função de ativação {funcao_ativacao.name}:")
    for i, x in enumerate(X_treino):
        print(f"Amostra {i + 1}: {x}")

    Y_treino = normalizar_dados_input(Y_treino, funcao_ativacao.name)
    print(f"Dados de treino normalizados para a função de ativação {funcao_ativacao.name}:")
    for i, x in enumerate(Y_treino):
        print(f"Amostra {i + 1}: {x}")
            
    X_teste = normalizar_dados_input(X_teste, funcao_ativacao.name)
    print(f"Dados de teste normalizados para a função de ativação {funcao_ativacao.name}:")
    for i, x in enumerate(X_teste):
        print(f"Amostra {i + 1}: {x}")
            

    # 5. Treino da Rede Neuronal
    print(f"--- Treinando a rede por {n_epocas} épocas (ou até erro < {erro_max}) ---")
    rede.treinar(
        X=X_treino,
        Y=Y_treino,
        n_epocas=n_epocas,
        erro_max=erro_max,
        taxa_aprendizagem=taxa_aprendizagem
    )
    print("Treino concluído.\n")

    # 6. Avaliação e Previsão nos Dados de Teste
    print("--- Avaliação nos Dados de Teste ---")
    previsoes = rede.prever(X_teste)

    for i, (x_amostra, y_pred) in enumerate(zip(X_teste, previsoes)):
        # Arredondamento opcional para classe binária (0 ou 1)
        classe_prevista = [1 if val >= 0.0 else 0 for val in y_pred] if funcao_ativacao == FuncaoAtivacaoEnum.TANH else [1 if val >= 0.5 else 0 for val in y_pred]
        print(f"Amostra {i + 1}: {x_amostra}")
        print(f"  -> Saída Bruta: {y_pred}")
        print(f"  -> Classe Prevista: {classe_prevista} - Classe esperada: {Y_teste[i][0]}\n")


if __name__ == "__main__":
    main()