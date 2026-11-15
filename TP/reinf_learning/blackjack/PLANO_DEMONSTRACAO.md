# Planeamento da demonstração de aprendizagem por reforço

## 1. Objetivo da demonstração

A demonstração pretende comparar Q-Learning, SARSA, Dyna-Q e QME num ambiente
de Blackjack com um baralho físico de 52 cartas, sem reposição dentro de cada
episódio.

As conclusões devem responder a quatro questões:

1. Qual algoritmo aprende uma política com melhor desempenho?
2. Qual algoritmo aprende mais rapidamente?
3. Qual algoritmo apresenta menor variabilidade entre sementes?
4. Qual é o custo adicional das simulações e da memória de experiências?

Não deve ser assumido à partida que um algoritmo é superior. As conclusões
devem ser baseadas nas métricas exportadas e em experiências repetidas.

## 2. Preparação

Executar os comandos a partir da pasta `blackjack`:

```powershell
cd TP\reinf_learning\blackjack
```

Confirmar que a aplicação inicia e que apresenta as quatro opções de treino:

```powershell
python blackjack.py --episodios 10 --avaliacao 10 --saida resultados\teste
```

O programa pede uma opção:

```text
1 - Q-Learning
2 - SARSA
3 - Dyna-Q
4 - QME
```

Os resultados são guardados na pasta indicada por `--saida`.

## 3. Experiência base

A primeira experiência deve usar os mesmos parâmetros para os quatro
algoritmos:

| Parâmetro | Valor |
|---|---:|
| Episódios de treino | 100 000 |
| Episódios de avaliação | 10 000 |
| Sementes | 10 |
| `alfa` | 0.01 |
| `gama` | 1.0 |
| `epsilon` | 0.1 |
| `num_simulacoes` | 5 |
| `dim_max` | 10 000 |

Para cada algoritmo, executar a aplicação e escolher a opção correspondente.
Os comandos seguintes mostram a execução não interativa da escolha do método:

```powershell
"1" | python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados\q_learning

"2" | python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados\sarsa

"3" | python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados\dyna_q

"4" | python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados\qme
```

Cada pasta deve conter `episodios.csv`, `atualizacoes_q.csv`,
`execucoes.csv` e `configuracoes.json`.

## 4. Experiências sobre os parâmetros

### 4.1 Taxa de aprendizagem

Repetir a experiência base com:

```text
alfa = 0.001, 0.01, 0.1
```

Objetivo: verificar se uma taxa maior acelera a aprendizagem, mas aumenta a
variabilidade ou impede a estabilização da política.

Manter constantes todos os restantes parâmetros e usar as mesmas sementes.

### 4.2 Fator de desconto

Repetir com:

```text
gama = 0.0, 0.5, 1.0
```

Objetivo: estudar a importância atribuída a recompensas futuras. No Blackjack,
`gama = 1.0` considera integralmente o resultado terminal, enquanto valores
menores reduzem a influência de recompensas futuras.

### 4.3 Exploração

Repetir com:

```text
epsilon = 0.0, 0.1, 0.3
```

Objetivo: comparar exploração e aproveitamento. `epsilon = 0.0` pode produzir
uma política pouco explorada; `epsilon = 0.3` pode aprender mais lentamente,
mas visitar mais estados.

A comparação final deve usar sempre a avaliação com `epsilon = 0`, para não
confundir exploração com qualidade da política.

### 4.4 Planeamento em Dyna-Q e QME

Para Dyna-Q e QME, variar:

```text
num_simulacoes = 0, 1, 5, 20
```

Objetivo: medir o ganho de desempenho produzido pelo planeamento e o custo
computacional adicional.

Para QME, variar também:

```text
dim_max = 100, 1000, 10000
```

Objetivo: verificar se uma memória maior melhora a diversidade das
experiências e o desempenho da política.

## 5. Análise dos dados

### Passo 1 — Validar a execução

Verificar em `execucoes.csv`:

- se todas as execuções têm a mesma configuração prevista;
- se existem 10 sementes por configuração;
- se o número de episódios coincide com o esperado;
- se treino e avaliação estão separados;
- se não existem execuções incompletas.

### Passo 2 — Comparar o desempenho final

Usar os episódios com `fase = avaliacao` e calcular, por algoritmo e semente:

- recompensa média;
- taxa de vitória;
- taxa de derrota;
- taxa de empate;
- desvio-padrão;
- intervalo de confiança.

A métrica principal deve ser a recompensa média de avaliação, porque considera
também Blackjack natural `+1.5`, derrotas `-1.0` e empates `0.0`.

### Passo 3 — Comparar a velocidade de aprendizagem

Nos episódios de treino:

1. calcular a média móvel da recompensa;
2. calcular a média móvel da taxa de vitória;
3. comparar o número de episódios necessário para atingir um limiar comum;
4. observar se a curva estabiliza ou continua muito variável.

Um algoritmo pode ter uma recompensa final semelhante a outro, mas atingir esse
resultado com muito menos episódios.

### Passo 4 — Analisar a estabilidade

Usar `atualizacoes_q.csv` e `episodios.csv` para observar:

- evolução de `q_delta_medio`;
- evolução de `td_error_medio`;
- alterações na política;
- dispersão dos resultados entre sementes.

Valores Q mais estáveis não garantem uma política melhor, mas ajudam a
identificar convergência ou instabilidade do treino.

### Passo 5 — Analisar o custo computacional

Comparar em `execucoes.csv`:

- duração total do treino;
- duração total da avaliação;
- número de atualizações Q;
- número de atualizações simuladas;
- tamanho do modelo Dyna-Q;
- ocupação da memória do QME.

O ganho de uma técnica de planeamento deve ser comparado com o seu custo.

### Passo 6 — Analisar parâmetros específicos

Para Dyna-Q e QME, produzir gráficos de:

- recompensa média em função de `num_simulacoes`;
- tempo de execução em função de `num_simulacoes`;
- recompensa média em função de `dim_max`;
- ocupação da memória ao longo do treino.

As sementes devem ser mantidas iguais entre configurações para reduzir o efeito
da aleatoriedade.

## 6. Gráficos recomendados

Para o relatório, incluir pelo menos:

1. recompensa média móvel por episódio;
2. taxa de vitória na avaliação por algoritmo;
3. boxplot da recompensa entre sementes;
4. recompensa média versus tempo de execução;
5. `q_delta_medio` ao longo do treino;
6. efeito de `num_simulacoes` em Dyna-Q e QME;
7. efeito de `dim_max` no QME.

As curvas de treino devem mostrar média e uma faixa de variação entre sementes,
em vez de apenas uma execução individual.

## 7. Estrutura das conclusões

As conclusões do relatório devem seguir esta estrutura:

### Desempenho

Indicar qual algoritmo obteve a maior recompensa média de avaliação e se a
diferença foi consistente entre sementes.

### Velocidade

Indicar qual algoritmo atingiu primeiro um desempenho estável e quantos
episódios foram necessários.

### Robustez

Comparar o desvio-padrão e o intervalo de confiança. Uma média superior com
grande variabilidade deve ser apresentada com cautela.

### Custo

Relacionar o desempenho com o tempo de execução, o número de atualizações e a
memória utilizada. Dyna-Q ou QME só devem ser considerados vantajosos se o
ganho justificar o custo adicional.

### Limitações

Registar limitações como:

- ambiente simplificado;
- espaço de estados discreto;
- recompensas esparsas;
- número finito de sementes;
- dependência dos resultados em relação aos hiperparâmetros;
- ausência de garantia de optimalidade da política aprendida.

Uma conclusão válida deve indicar também quando não existe diferença
estatisticamente clara entre dois algoritmos.

## 8. Reprodutibilidade

Guardar juntamente com os gráficos e tabelas:

- `configuracoes.json`;
- os três ficheiros CSV;
- versão do código;
- data da execução;
- versão do Python;
- comando utilizado;
- sementes usadas.

Assim, os resultados apresentados no relatório podem ser reproduzidos e
auditados posteriormente.

## Comandos para execução no Windows

Os comandos PowerShell para executar todas as experiências estão em
[`COMANDOS_EXPERIENCIAS.txt`](./COMANDOS_EXPERIENCIAS.txt). Copie e execute
cada linha individualmente a partir da pasta `blackjack`.
