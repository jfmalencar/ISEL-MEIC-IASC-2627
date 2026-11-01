import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from blackjack_ambiente import EstadoBlackjack
from blackjack_ambiente_52 import AmbienteBlackjack52
from agente import Agente
from q_learning import QLearning

def executar_teste_blackjack():
    random.seed(42)
    ambiente = AmbienteBlackjack52()
    agente = Agente(accoes_disponiveis=[0, 1], valor_inicial=0.0, epsilon=0.1)
    q_learning = QLearning(memoria=agente.memoria, seleccao_accao=agente.seleccao_accao, alfa=0.01, gama=1.0)

    num_episodios = 1000000
    recompensa_total = 0.0
    ambiente.reiniciar_estatisticas()

    print(f"--- A Iniciar o Treino do Agente no Blackjack ({num_episodios} episódios) ---")
    for ep in range(num_episodios):
        s = ambiente.reiniciar()
        final = False

        while not final:
            agente.atualizar_accoes(ambiente.accoes(s))
            a = agente.seleccao_accao.seleccionar_accao(s)
            s_linha, r, final = ambiente.passo(a)
            
            q_learning.aprender(s, a, r, s_linha, final=final)
            s = s_linha
            if final:
                recompensa_total += r

    print(f"Treino Concluído!")
    print(f"Recompensa Média por Episódio: {recompensa_total / num_episodios:.4f}")
    print("\n=== RESULTADOS ===")
    print(f"Vitórias: {ambiente.vitorias} ({ambiente.vitorias / num_episodios:.2%})")
    print(f"Derrotas: {ambiente.derrotas} ({ambiente.derrotas / num_episodios:.2%})")
    print(f"Empates: {ambiente.empates} ({ambiente.empates / num_episodios:.2%})")
    print(f"Total contabilizado: {ambiente.vitorias + ambiente.derrotas + ambiente.empates}")

    # Exibição da Matriz de Decisão Aprendida (Soma do Jogador x Carta Visível do Dealer)
    print("\n=== POLÍTICA APRENDIDA (Sem Ás Utilizável) ===")
    print("Soma J. | Dealer (1..10)  [0 = Stick (Parar), 1 = Hit (Pedir)]")
    print("-" * 60)
    for soma in range(12, 22):
        decisoes = [
            str(agente.seleccao_accao.accao_sofrega(EstadoBlackjack(soma, d, 0)))
            for d in range(1, 11)
        ]
        print(f"  {soma:2d}    | " + "  ".join(decisoes))

if __name__ == "__main__":
    executar_teste_blackjack()