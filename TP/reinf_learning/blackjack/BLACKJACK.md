# Aplicação de teste: Blackjack

[`blackjack.py`](./blackjack.py) é o ponto de entrada da aplicação de teste.
Antes do treino, apresenta as opções Q-Learning, SARSA, Dyna-Q e QME. O
resultado inclui a recompensa média, as estatísticas dos episódios e a
política aprendida.

Cada algoritmo tem a sua implementação de treino em
[`algoritmos/`](./algoritmos/):

- [`q_learning/treino.py`](./algoritmos/q_learning/treino.py): Q-Learning;
- [`sarsa/treino.py`](./algoritmos/sarsa/treino.py): SARSA;
- [`dyna_q/treino.py`](./algoritmos/dyna_q/treino.py): Dyna-Q;
- [`qme/treino.py`](./algoritmos/qme/treino.py): Q-Learning com memória de
  experiências.

As quatro implementações herdam de `TreinoBlackjack`, a classe abstrata que
define o ciclo comum de treino.

## Regras do ambiente

O treino usa exclusivamente
[`ambiente/blackjack_ambiente_52.py`](./ambiente/blackjack_ambiente_52.py),
com um baralho físico de 52 cartas e sem reposição. O baralho é recriado e
baralhado no início de cada episódio; cada carta retirada é removida e não
pode voltar a ser sorteada nesse episódio.

Cartas de figura valem `10`, cartas numéricas mantêm o seu valor e o ás vale
`1` ou `11`.

O ás é considerado utilizável como `11` sempre que isso não fizer a soma
ultrapassar `21`. Caso contrário, é contado como `1`.

No início de cada episódio:

- o jogador recebe duas cartas;
- o dealer recebe duas cartas;
- apenas a primeira carta do dealer é observada pelo agente.

## Observação e ações

`EstadoBlackjack` representa a observação como:

```text
(soma_jogador, carta_dealer, as_utilizavel)
```

Os componentes são inteiros:

- `soma_jogador`: soma atual da mão do jogador;
- `carta_dealer`: carta visível do dealer, entre `1` e `10`;
- `as_utilizavel`: `1` se a mão usa um ás como `11`, caso contrário `0`.

As ações válidas são:

| Ação | Significado |
|---:|---|
| `0` | Stick: parar de pedir cartas |
| `1` | Hit: pedir uma carta |

Enquanto o jogador não ultrapassar `21`, `accoes` devolve `[0, 1]`. Depois de
um estado bust, não há ações válidas.

## Transições e recompensas

### Hit

Ao escolher `1`, o jogador recebe uma carta:

- se a soma ultrapassar `21`, o episódio termina com recompensa `-1.0`;
- caso contrário, a recompensa é `0.0` e o episódio continua.

### Stick

Ao escolher `0`, o dealer revela a carta escondida e compra cartas até obter
uma soma de pelo menos `17`. Depois:

- jogador vence: `+1.0`;
- jogador perde: `-1.0`;
- empate: `0.0`.

Um Blackjack natural corresponde a uma mão inicial de duas cartas com soma
`21`:

- jogador com Blackjack e dealer sem Blackjack: `+1.5`;
- ambos com Blackjack: `0.0`;
- dealer com Blackjack e jogador sem Blackjack: `-1.0`.

## Execução do treino

O ponto de entrada é:

```powershell
python blackjack.py --episodios 100000
```

As métricas podem ser configuradas e exportadas para uma pasta:

```powershell
python blackjack.py --episodios 100000 --avaliacao 10000 `
    --sementes 10 --saida resultados
```

O treino usa `epsilon` para exploração. A avaliação é executada depois do
treino com `epsilon = 0`, sem alterar a memória Q.

O programa:

1. fixa a semente aleatória em `42`;
2. pergunta qual dos quatro algoritmos deve ser usado;
3. cria o ambiente e um agente com as ações `[0, 1]`;
4. executa o número de episódios indicado;
5. imprime a recompensa média por episódio;
6. imprime as estatísticas e a política sôfrega aprendida.

O número de episódios é opcional e tem o valor predefinido `100000`.

Os parâmetros usados no treino são:

```text
epsilon = 0.1
alfa = 0.01
gama = 1.0
```

Durante cada episódio terminal, o ambiente atualiza os contadores
`vitorias`, `derrotas` e `empates`. Uma recompensa positiva, incluindo o
Blackjack natural `+1.5`, conta como vitória; uma recompensa negativa conta
como derrota; e uma recompensa `0.0` conta como empate. A aplicação apresenta
as quantidades e percentagens no final do treino. Os contadores podem ser
reiniciados explicitamente com `ambiente.reiniciar_estatisticas()`.

## Política apresentada

No final, a aplicação percorre somas do jogador entre `12` e `21` e cartas do
dealer entre `1` e `10`. Para cada combinação, consulta a ação sôfrega da
memória Q, assumindo `as_utilizavel = 0`.

A saída tem o formato:

```text
Soma J. | Dealer (1..10)  [0 = Stick (Parar), 1 = Hit (Pedir)]
```

Esta tabela mostra a decisão atualmente preferida pelo agente, não uma
garantia de uma política ótima. A qualidade depende do número de episódios,
da taxa de aprendizagem, de `epsilon` e da aleatoriedade das cartas.

Para a descrição completa dos ficheiros exportados e da metodologia de análise,
consultar [`METRICAS.md`](./METRICAS.md).

## Métricas exportadas

Cada execução produz, na pasta indicada por `--saida`:

| Ficheiro | Conteúdo |
|---|---|
| `episodios.csv` | Recompensa, resultado, ações, estados, duração e métricas Q por episódio |
| `atualizacoes_q.csv` | Variação Q, erro temporal e indicação de atualização simulada |
| `execucoes.csv` | Parâmetros, recompensas, estatísticas e tempos agregados por execução |
| `configuracoes.json` | Configuração completa de cada execução |

Os episódios têm uma coluna `fase` com os valores `treino` ou `avaliacao`.
As métricas específicas incluem o tamanho do modelo do Dyna-Q, a ocupação da
memória de experiências do QME, o número de simulações e o número de
atualizações Q reais e simuladas. Os CSV podem ser carregados diretamente com
`pandas`.

## Relação com a implementação

Os principais ficheiros são:

| Ficheiro | Responsabilidade |
|---|---|
| `blackjack.py` | Seleção do algoritmo, execução e apresentação dos resultados |
| `ambiente/blackjack_ambiente_52.py` | Estado, baralho físico, regras, transições e recompensas |
| `algoritmos/_comum.py` | Classe abstrata e apresentação dos resultados |
| `algoritmos/q_learning/treino.py` | Treino Q-Learning |
| `algoritmos/sarsa/treino.py` | Treino SARSA |
| `algoritmos/dyna_q/treino.py` | Treino Dyna-Q |
| `algoritmos/qme/treino.py` | Treino QME |
| `agente.py` | Associação entre memória e seletor de ações |
| `selecao_acao.py` | Política ε-greedy |
| `memoria_aprendizagem.py` | Tabela Q |
| `q_learning.py` | Atualização Q-learning |
| `sarsa.py` | Atualização SARSA |
| `dyna_q.py` | Atualização Dyna-Q |
| `qme.py` | Atualização QME e memória de experiências |

Para usar a variante sem reposição:

```python
from ambiente.blackjack_ambiente_52 import AmbienteBlackjack52

ambiente = AmbienteBlackjack52()
estado = ambiente.reiniciar()
print(ambiente.cartas_restantes)  # 48 após as quatro cartas iniciais
```
