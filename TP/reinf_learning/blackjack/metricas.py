from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConfiguracaoTreino:
    algoritmo: str
    num_episodios: int = 100_000
    num_avaliacao: int = 1_000
    alfa: float = 0.01
    gama: float = 1.0
    epsilon: float = 0.1
    num_simulacoes: int = 5
    dim_max: int = 10_000
    semente: int = 42
    run_id: str = ""

    def __post_init__(self):
        if self.num_episodios <= 0:
            raise ValueError("num_episodios deve ser maior que zero")
        if self.num_avaliacao < 0:
            raise ValueError("num_avaliacao não pode ser negativo")
        if not 0 <= self.alfa <= 1:
            raise ValueError("alfa deve estar entre zero e um")
        if not 0 <= self.gama <= 1:
            raise ValueError("gama deve estar entre zero e um")
        if not 0 <= self.epsilon <= 1:
            raise ValueError("epsilon deve estar entre zero e um")
        if self.num_simulacoes < 0 or self.dim_max <= 0:
            raise ValueError("Os parâmetros de simulação devem ser válidos")


class MetricasTreino:
    def __init__(self, configuracao: ConfiguracaoTreino):
        self.configuracao = configuracao
        self.episodios = []
        self.atualizacoes = []
        self._episodio_atual = None
        self._inicio_episodio = 0.0
        self._estados = set()
        self._acoes = 0
        self._hits = 0
        self._sticks = 0
        self._q_deltas = []
        self._td_erros = []
        self._atualizacoes_simuladas = 0
        self._recompensas_acumuladas = {"treino": 0.0, "avaliacao": 0.0}

    def iniciar_episodio(self, episodio: int, fase: str) -> None:
        self._episodio_atual = episodio
        self._fase_atual = fase
        self._inicio_episodio = time.perf_counter()
        self._estados = set()
        self._acoes = 0
        self._hits = 0
        self._sticks = 0
        self._q_deltas = []
        self._td_erros = []
        self._atualizacoes_simuladas = 0

    def registar_acao(self, estado, acao: int) -> None:
        self._estados.add(estado)
        self._acoes += 1
        if acao == 1:
            self._hits += 1
        elif acao == 0:
            self._sticks += 1

    def registar_actualizacao(
        self, q_delta: float, td_error: float, simulada: bool = False
    ) -> None:
        if self._episodio_atual is None:
            return
        self._q_deltas.append(abs(q_delta))
        self._td_erros.append(abs(td_error))
        if simulada:
            self._atualizacoes_simuladas += 1
        self.atualizacoes.append(
            {
                "run_id": self.configuracao.run_id,
                "algoritmo": self.configuracao.algoritmo,
                "semente": self.configuracao.semente,
                "fase": self._fase_atual,
                "episodio": self._episodio_atual,
                "q_delta": q_delta,
                "td_error": td_error,
                "simulada": simulada,
            }
        )

    def finalizar_episodio(
        self,
        recompensa: float,
        ambiente,
        algoritmo,
    ) -> None:
        if recompensa > 0:
            resultado = "vitoria"
        elif recompensa < 0:
            resultado = "derrota"
        else:
            resultado = "empate"
        self._recompensas_acumuladas[self._fase_atual] += recompensa

        q_values = getattr(algoritmo.mem_aprend, "Q", {})
        modelo = getattr(algoritmo, "modelo", None)
        memoria = getattr(algoritmo, "memoria_experiencia", None)
        self.episodios.append(
            {
                "run_id": self.configuracao.run_id,
                "algoritmo": self.configuracao.algoritmo,
                "semente": self.configuracao.semente,
                "fase": self._fase_atual,
                "episodio": self._episodio_atual,
                "recompensa": recompensa,
                "recompensa_acumulada": self._recompensas_acumuladas[self._fase_atual],
                "resultado": resultado,
                "num_acoes": self._acoes,
                "num_hits": self._hits,
                "num_sticks": self._sticks,
                "duracao_segundos": time.perf_counter() - self._inicio_episodio,
                "estados_visitados": len(self._estados),
                "q_tamanho": len(q_values),
                "q_delta_medio": _media(self._q_deltas),
                "td_error_medio": _media(self._td_erros),
                "atualizacoes_q": len(self._q_deltas),
                "atualizacoes_simuladas": self._atualizacoes_simuladas,
                "modelo_tamanho": len(modelo.T) if modelo is not None else 0,
                "memoria_experiencia": (
                    len(memoria.memoria) if memoria is not None else 0
                ),
                "cartas_restantes": ambiente.cartas_restantes,
            }
        )
        self._episodio_atual = None


def _media(valores):
    return sum(valores) / len(valores) if valores else 0.0


def exportar_resultados(resultados, pasta_saida: str) -> None:
    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)
    episodios = [linha for resultado in resultados for linha in resultado.metricas.episodios]
    atualizacoes = [
        linha for resultado in resultados for linha in resultado.metricas.atualizacoes
    ]
    execucoes = [
        {
            **asdict(resultado.configuracao),
            "recompensa_treino": resultado.recompensa_treino,
            "recompensa_avaliacao": resultado.recompensa_avaliacao,
            "duracao_treino_segundos": sum(
                linha["duracao_segundos"]
                for linha in resultado.metricas.episodios
                if linha["fase"] == "treino"
            ),
            "duracao_avaliacao_segundos": sum(
                linha["duracao_segundos"]
                for linha in resultado.metricas.episodios
                if linha["fase"] == "avaliacao"
            ),
            "vitorias_treino": resultado.ambiente.vitorias,
            "derrotas_treino": resultado.ambiente.derrotas,
            "empates_treino": resultado.ambiente.empates,
            "vitorias_avaliacao": resultado.vitorias_avaliacao,
            "derrotas_avaliacao": resultado.derrotas_avaliacao,
            "empates_avaliacao": resultado.empates_avaliacao,
        }
        for resultado in resultados
    ]
    _escrever_csv(pasta / "episodios.csv", episodios)
    _escrever_csv(pasta / "atualizacoes_q.csv", atualizacoes)
    _escrever_csv(pasta / "execucoes.csv", execucoes)
    (pasta / "configuracoes.json").write_text(
        json.dumps([asdict(resultado.configuracao) for resultado in resultados], indent=2),
        encoding="utf-8",
    )


def _escrever_csv(caminho: Path, linhas: list[dict]) -> None:
    if not linhas:
        caminho.write_text("", encoding="utf-8")
        return
    campos = list(dict.fromkeys(campo for linha in linhas for campo in linha))
    with caminho.open("w", newline="", encoding="utf-8") as ficheiro:
        escritor = csv.DictWriter(ficheiro, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)
