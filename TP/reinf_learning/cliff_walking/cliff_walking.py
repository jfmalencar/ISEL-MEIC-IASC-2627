import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agente import Agente
from cliff_walking_ambiente import AmbienteCliffWalking
from q_learning import QLearning


SIMBOLOS = {
    0: "^",
    1: ">",
    2: "v",
    3: "<",
}


def executar_teste_cliff_walking() -> None:
    random.seed(42)
    ambiente = AmbienteCliffWalking(is_slippery=False)
    agente = Agente(accoes_disponiveis=[0, 1, 2, 3], valor_inicial=0.0, epsilon=0.1)
    q_learning = QLearning(
        memoria=agente.memoria,
        seleccao_accao=agente.seleccao_accao,
        alfa=0.1,
        gama=1.0,
    )

    num_episodios = 1000000
    recompensa_total = 0.0
    passos_totais = 0

    print(
        "--- A iniciar o treino do agente no Cliff Walking "
        f"({num_episodios} episódios) ---"
    )
    for _ in range(num_episodios):
        estado = ambiente.reiniciar()
        final = False

        while not final:
            agente.atualizar_accoes(ambiente.accoes(estado))
            acao = agente.seleccao_accao.seleccionar_accao(estado)
            novo_estado, recompensa, final, _ = ambiente.passo(acao)
            q_learning.aprender(estado, acao, recompensa, novo_estado, final=final)
            estado = novo_estado
            recompensa_total += recompensa
            passos_totais += 1

    print("Treino concluído!")
    print(f"Recompensa média por episódio: {recompensa_total / num_episodios:.2f}")
    print(f"Passos médios por episódio: {passos_totais / num_episodios:.2f}")
    print(f"Quedas no precipício: {ambiente.quedas_no_precipicio}")
    imprimir_politica(agente, ambiente)


def imprimir_politica(agente: Agente, ambiente: AmbienteCliffWalking) -> None:
    print("\n=== POLÍTICA APRENDIDA ===")
    for linha in range(ambiente.N_LINHAS):
        simbolos = []
        for coluna in range(ambiente.N_COLUNAS):
            estado = linha * ambiente.N_COLUNAS + coluna
            if estado == ambiente.INICIO:
                simbolos.append("S")
            elif estado in ambiente.PRECIPICIO:
                simbolos.append("C")
            elif estado == ambiente.OBJETIVO:
                simbolos.append("G")
            else:
                acao = agente.seleccao_accao.accao_sofrega(estado)
                simbolos.append(SIMBOLOS[acao])
        print(" ".join(simbolos))


if __name__ == "__main__":
    executar_teste_cliff_walking()
