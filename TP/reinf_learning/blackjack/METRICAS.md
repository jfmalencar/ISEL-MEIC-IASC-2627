# Métricas do treino

## Objetivo

A aplicação exporta dados estruturados para permitir a comparação dos
algoritmos Q-Learning, SARSA, Dyna-Q e QME através de métodos de ciência de
dados. O treino e a avaliação são registados separadamente.

## Execução

```powershell
python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados
```

Depois de escolher o algoritmo, são criadas quatro saídas na pasta indicada:

| Ficheiro | Unidade | Utilização |
|---|---|---|
| `episodios.csv` | Uma linha por episódio | Evolução da aprendizagem e desempenho |
| `atualizacoes_q.csv` | Uma linha por atualização Q | Erro temporal e estabilidade dos valores Q |
| `execucoes.csv` | Uma linha por execução/semente | Comparação agregada dos experimentos |
| `configuracoes.json` | Uma entrada por execução | Reprodutibilidade dos parâmetros |

O identificador `run_id` distingue execuções feitas com sementes diferentes.

## Parâmetros

Os parâmetros usados são guardados em `execucoes.csv` e
`configuracoes.json`:

| Parâmetro | Significado |
|---|---|
| `num_episodios` | Número de episódios de aprendizagem |
| `num_avaliacao` | Número de episódios após o treino |
| `alfa` | Taxa de aprendizagem |
| `gama` | Fator de desconto |
| `epsilon` | Probabilidade de exploração durante o treino |
| `num_simulacoes` | Simulações por experiência em Dyna-Q/QME |
| `dim_max` | Capacidade da memória de experiências do QME |
| `semente` | Semente usada para tornar a execução reprodutível |

A avaliação usa `epsilon = 0` e não altera a tabela Q. Assim, mede a política
aprendida sem misturar exploração com desempenho.

## `episodios.csv`

Colunas principais:

| Coluna | Descrição |
|---|---|
| `fase` | `treino` ou `avaliacao` |
| `episodio` | Número do episódio dentro da fase |
| `recompensa` | Recompensa terminal do episódio |
| `recompensa_acumulada` | Soma das recompensas na fase |
| `resultado` | `vitoria`, `derrota` ou `empate` |
| `num_acoes` | Número total de ações |
| `num_hits` / `num_sticks` | Contagem de cada ação |
| `duracao_segundos` | Duração do episódio |
| `estados_visitados` | Estados distintos visitados |
| `q_tamanho` | Número de pares estado-ação conhecidos |
| `q_delta_medio` | Média de `|Q_novo - Q_antigo|` |
| `td_error_medio` | Média do erro temporal absoluto |
| `atualizacoes_q` | Atualizações Q no episódio |
| `atualizacoes_simuladas` | Atualizações provenientes de planeamento |
| `modelo_tamanho` | Transições conhecidas pelo Dyna-Q |
| `memoria_experiencia` | Experiências armazenadas pelo QME |

## `atualizacoes_q.csv`

Cada linha representa uma atualização da tabela Q:

- `q_delta`: alteração assinada do valor Q;
- `td_error`: diferença entre o alvo e o valor Q anterior;
- `simulada`: indica se a atualização veio de uma experiência simulada;
- `fase` e `episodio`: permitem relacionar a atualização com o episódio.

Valores decrescentes de `q_delta` e `td_error` podem indicar estabilização,
mas não substituem a avaliação de desempenho.

## `execucoes.csv`

Este ficheiro permite comparar diretamente as execuções:

- recompensa total e média de treino;
- recompensa total de avaliação;
- vitórias, derrotas e empates;
- duração agregada do treino e da avaliação;
- todos os hiperparâmetros usados.

Para comparações entre algoritmos, devem ser mantidos constantes o número de
episódios, as sementes, `alfa`, `gama` e `epsilon`. Os parâmetros específicos
de Dyna-Q e QME devem ser estudados em experiências próprias.

## Exemplo de análise com pandas

```python
import pandas as pd

episodios = pd.read_csv("resultados/episodios.csv")
execucoes = pd.read_csv("resultados/execucoes.csv")

treino = episodios[episodios["fase"] == "treino"].copy()
treino["recompensa_media"] = (
    treino.groupby(["run_id"])["recompensa"]
    .transform(lambda serie: serie.rolling(1000, min_periods=1).mean())
)

avaliacao = episodios[episodios["fase"] == "avaliacao"]
resumo = (
    avaliacao.groupby("algoritmo")
    .agg(
        recompensa_media=("recompensa", "mean"),
        taxa_vitoria=("resultado", lambda serie: (serie == "vitoria").mean()),
        taxa_derrota=("resultado", lambda serie: (serie == "derrota").mean()),
    )
)
print(resumo)
```

## Recomendações experimentais

1. Usar pelo menos 10 sementes por configuração.
2. Separar sempre treino e avaliação.
3. Apresentar média e desvio-padrão entre sementes.
4. Usar gráficos de recompensa média móvel e taxa de vitória.
5. Comparar também tempo de execução e número de atualizações.
6. Variar `num_simulacoes` e `dim_max` separadamente.
7. Guardar a configuração juntamente com todos os resultados.
