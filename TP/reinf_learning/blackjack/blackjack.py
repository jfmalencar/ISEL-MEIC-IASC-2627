import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algoritmos._comum import TreinoBlackjack, apresentar_resultados
from algoritmos.dyna_q.treino import TreinoDynaQ
from algoritmos.q_learning.treino import TreinoQLearning
from algoritmos.qme.treino import TreinoQME
from algoritmos.sarsa.treino import TreinoSARSA
from metricas import ConfiguracaoTreino, exportar_resultados


OPCOES_TREINO = {
    "1": TreinoQLearning,
    "2": TreinoSARSA,
    "3": TreinoDynaQ,
    "4": TreinoQME,
}


def selecionar_treino() -> TreinoBlackjack:
    print("=== Blackjack: seleção do método de treino ===")
    print("1 - Q-Learning")
    print("2 - SARSA")
    print("3 - Dyna-Q")
    print("4 - QME")

    while True:
        opcao = input("Escolha o método de treino: ").strip()
        classe_treino = OPCOES_TREINO.get(opcao)
        if classe_treino is not None:
            return classe_treino
        print("Opção inválida. Escolha um método entre 1 e 4.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodios", type=int, default=100_000)
    parser.add_argument("--avaliacao", type=int, default=1_000)
    parser.add_argument("--sementes", type=int, default=1)
    parser.add_argument("--alfa", type=float, default=0.01)
    parser.add_argument("--gama", type=float, default=1.0)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--num-simulacoes", type=int, default=5)
    parser.add_argument("--dim-max", type=int, default=10_000)
    parser.add_argument("--saida", default="resultados")
    args = parser.parse_args()

    classe_treino = selecionar_treino()
    if args.sementes <= 0:
        parser.error("--sementes deve ser maior que zero")

    nome_algoritmo = classe_treino(1).nome
    resultados = []
    for indice in range(args.sementes):
        semente = 42 + indice
        random.seed(semente)
        configuracao = ConfiguracaoTreino(
            algoritmo=nome_algoritmo,
            num_episodios=args.episodios,
            num_avaliacao=args.avaliacao,
            alfa=args.alfa,
            gama=args.gama,
            epsilon=args.epsilon,
            num_simulacoes=args.num_simulacoes,
            dim_max=args.dim_max,
            semente=semente,
            run_id=f"{nome_algoritmo}_{semente}",
        )
        treino = classe_treino(configuracao)
        print(
            f"\nA iniciar o treino {treino.nome} "
            f"(execução {indice + 1}/{args.sementes})..."
        )
        resultado = treino.treinar()
        apresentar_resultados(resultado)
        resultados.append(resultado)

    exportar_resultados(resultados, args.saida)
    print(f"\nMétricas exportadas para: {args.saida}")


if __name__ == "__main__":
    main()
