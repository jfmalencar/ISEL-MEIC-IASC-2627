import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agente import Agente
from blackjack_ambiente import EstadoBlackjack
from blackjack_ambiente_52 import AmbienteBlackjack52
from sarsa import SARSA


def executar_teste_blackjack_sarsa() -> None:
    random.seed(42)
    ambiente = AmbienteBlackjack52()
    agente = Agente(accoes_disponiveis=[0, 1], valor_inicial=0.0, epsilon=0.1)
    sarsa = SARSA(
        memoria=agente.memoria,
        seleccao_accao=agente.seleccao_accao,
        alfa=0.01,
        gama=1.0,
    )

    num_episodios = 1000000
    recompensa_total = 0.0
    ambiente.reiniciar_estatisticas()

    print(
        "--- A iniciar o treino SARSA do agente no Blackjack "
        f"({num_episodios} episódios) ---"
    )
    for _ in range(num_episodios):
        estado = ambiente.reiniciar()
        agente.atualizar_accoes(ambiente.accoes(estado))
        acao = agente.seleccao_accao.seleccionar_accao(estado)
        final = False

        while not final:
            novo_estado, recompensa, final = ambiente.passo(acao)
            recompensa_total += recompensa
            agente.atualizar_accoes(ambiente.accoes(novo_estado))

            if final:
                proxima_acao = None
            else:
                proxima_acao = agente.seleccao_accao.seleccionar_accao(novo_estado)

            sarsa.aprender(
                estado,
                acao,
                recompensa,
                novo_estado,
                a_linha=proxima_acao,
                final=final,
            )
            estado = novo_estado
            acao = proxima_acao

    print("Treino SARSA concluído!")
    print(f"Recompensa média por episódio: {recompensa_total / num_episodios:.4f}")
    print("\n=== RESULTADOS ===")
    print(f"Vitórias: {ambiente.vitorias} ({ambiente.vitorias / num_episodios:.2%})")
    print(f"Derrotas: {ambiente.derrotas} ({ambiente.derrotas / num_episodios:.2%})")
    print(f"Empates: {ambiente.empates} ({ambiente.empates / num_episodios:.2%})")
    print(f"Total contabilizado: {ambiente.vitorias + ambiente.derrotas + ambiente.empates}")
    imprimir_politica(agente)


def imprimir_politica(agente: Agente) -> None:
    print("\n=== POLÍTICA SARSA APRENDIDA (Sem Ás Utilizável) ===")
    print("Soma J. | Dealer (1..10)  [0 = Stick (Parar), 1 = Hit (Pedir)]")
    print("-" * 60)
    for soma in range(12, 22):
        decisoes = [
            str(agente.seleccao_accao.accao_sofrega(EstadoBlackjack(soma, dealer, 0)))
            for dealer in range(1, 11)
        ]
        print(f"  {soma:2d}    | " + "  ".join(decisoes))


if __name__ == "__main__":
    executar_teste_blackjack_sarsa()
