"""Treino da RedeNeuronal com o dataset MNIST em formato IDX.

Exemplo:
    python mnist.py --train-size 1000 --test-size 1000 --epochs 5

Os ficheiros MNIST devem estar na pasta ``mnist`` junto deste script.
"""

from __future__ import annotations

import argparse
import random
import struct
from pathlib import Path

from TP.rna.funcao_ativacao import FuncaoAtivacaoEnum
from TP.rna.rede_neuronal import RedeNeuronal


def _localizar_ficheiro(pasta: Path, nomes: tuple[str, ...]) -> Path:
    """Encontra um ficheiro IDX, incluindo a estrutura alternativa existente."""
    # Tentar primeiro os nomes convencionais dos ficheiros descarregados do MNIST.
    for nome in nomes:
        ficheiro = pasta / nome
        if ficheiro.is_file():
            return ficheiro

        # Aceitar também a estrutura de diretórios alternativa presente no projeto.
        ficheiro_alternativo = pasta / nome.replace(".", "-") / nome.replace(".", "-")
        if ficheiro_alternativo.is_file():
            return ficheiro_alternativo

    # Interromper a execução explicitamente quando os dados não estão disponíveis.
    nomes_procurados = ", ".join(nomes)
    raise FileNotFoundError(f"Não foi possível encontrar: {nomes_procurados}")


def carregar_imagens(ficheiro: Path, limite: int | None = None) -> list[list[float]]:
    """Lê imagens IDX e normaliza cada pixel para o intervalo [0, 1]."""
    with ficheiro.open("rb") as stream:
        # O cabeçalho IDX contém o identificador do formato e as dimensões do dataset.
        magic, numero_imagens, numero_linhas, numero_colunas = struct.unpack(
            ">IIII", stream.read(16)
        )
        if magic != 2051:
            raise ValueError(f"Magic number inválido para imagens MNIST: {magic}")

        # Ler apenas a quantidade solicitada permite executar experiências menores.
        quantidade = numero_imagens if limite is None else min(limite, numero_imagens)
        tamanho = numero_linhas * numero_colunas
        dados = stream.read(quantidade * tamanho)
        if len(dados) != quantidade * tamanho:
            raise ValueError("O ficheiro de imagens MNIST está incompleto.")

    # Cada imagem é transformada num vetor e cada pixel é escalado de [0, 255] para [0, 1].
    return [
        [pixel / 255.0 for pixel in dados[inicio : inicio + tamanho]]
        for inicio in range(0, len(dados), tamanho)
    ]


def carregar_rotulos(
    ficheiro: Path, limite: int | None = None
) -> list[list[float]]:
    """Lê rótulos IDX e converte-os em vetores one-hot."""
    with ficheiro.open("rb") as stream:
        # O cabeçalho dos rótulos IDX contém o identificador do formato e o número de exemplos.
        magic, numero_rotulos = struct.unpack(">II", stream.read(8))
        if magic != 2049:
            raise ValueError(f"Magic number inválido para rótulos MNIST: {magic}")

        # Cada rótulo ocupa exatamente um byte.
        quantidade = numero_rotulos if limite is None else min(limite, numero_rotulos)
        dados = stream.read(quantidade)
        if len(dados) != quantidade:
            raise ValueError("O ficheiro de rótulos MNIST está incompleto.")

    # Converter, por exemplo, o rótulo 3 em [0, 0, 0, 1, 0, ..., 0].
    return [[1.0 if classe == rotulo else 0.0 for classe in range(10)] for rotulo in dados]


def classe_prevista(saida: list[float]) -> int:
    """Obtém a classe correspondente ao maior valor da saída da rede."""
    # A saída com maior ativação representa a classe escolhida pela rede neuronal.
    return max(range(len(saida)), key=saida.__getitem__)


def avaliar(rede: RedeNeuronal, X: list[list[float]], Y: list[list[float]]) -> float:
    """Calcula a precisão da rede num conjunto de amostras."""
    # Propagar todas as imagens e comparar a classe prevista com a classe esperada.
    previsoes = rede.prever(X)
    acertos = sum(
        classe_prevista(previsao) == classe_prevista(rotulo)
        for previsao, rotulo in zip(previsoes, Y)
    )
    # A precisão é a proporção de classificações corretas.
    return acertos / len(Y) if Y else 0.0


def main() -> None:
    # Definir os hiperparâmetros através da linha de comandos para permitir experiências diferentes.
    parser = argparse.ArgumentParser(description="Testar RedeNeuronal com MNIST.")
    parser.add_argument("--train-size", type=int, default=1000)
    parser.add_argument("--test-size", type=int, default=1000)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--momentum", type=float, default=0.5)
    parser.add_argument("--hidden-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.train_size <= 0 or args.test_size <= 0 or args.epochs <= 0:
        parser.error("train-size, test-size e epochs devem ser positivos.")

    # Fixar a semente torna a inicialização aleatória da rede reproduzível.
    random.seed(args.seed)
    pasta_mnist = Path(__file__).with_name("mnist")

    # Localizar os quatro ficheiros necessários: imagens e rótulos de treino e de teste.
    imagens_treino = _localizar_ficheiro(
        pasta_mnist, ("train-images.idx3-ubyte", "train-images-idx3-ubyte")
    )
    rotulos_treino = _localizar_ficheiro(
        pasta_mnist, ("train-labels.idx1-ubyte", "train-labels-idx1-ubyte")
    )
    imagens_teste = _localizar_ficheiro(
        pasta_mnist, ("t10k-images.idx3-ubyte", "t10k-images-idx3-ubyte")
    )
    rotulos_teste = _localizar_ficheiro(
        pasta_mnist, ("t10k-labels.idx1-ubyte", "t10k-labels-idx1-ubyte")
    )

    # Carregar e preparar os dados antes de iniciar a aprendizagem.
    X_treino = carregar_imagens(imagens_treino, args.train_size)
    Y_treino = carregar_rotulos(rotulos_treino, args.train_size)
    X_teste = carregar_imagens(imagens_teste, args.test_size)
    Y_teste = carregar_rotulos(rotulos_teste, args.test_size)

    if len(X_treino) != len(Y_treino) or len(X_teste) != len(Y_teste):
        raise ValueError("O número de imagens e rótulos não coincide.")

    # Arquitetura: 784 entradas (28x28 pixels), camada oculta e 10 saídas (dígitos 0 a 9).
    # A função sigmoide produz valores contínuos adequados à codificação one-hot dos rótulos.
    rede = RedeNeuronal(
        forma=[28 * 28, args.hidden_size, 10],
        phi=FuncaoAtivacaoEnum.SIGMOID.value,
    )
    print(
        f"Treino MNIST: {len(X_treino)} amostras, "
        f"teste: {len(X_teste)} amostras, épocas: {args.epochs}"
    )

    # Treinar com retropropagação: em cada amostra, a rede calcula o erro,
    # propaga-o para trás e atualiza pesos e pendores.
    rede.treinar(
        X=X_treino,
        Y=Y_treino,
        n_epocas=args.epochs,
        erro_max=0.0,
        taxa_aprendizagem=args.learning_rate,
        momento=args.momentum,
    )

    # Avaliar com dados que não foram usados durante o treino.
    precisao = avaliar(rede, X_teste, Y_teste)
    print(f"Precisão no conjunto de teste: {precisao:.2%}")


if __name__ == "__main__":
    main()
