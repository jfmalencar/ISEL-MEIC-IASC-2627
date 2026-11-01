# Aplicação de teste: Blackjack

[`blackjack.py`](./blackjack.py) executa um agente Q-learning num ambiente de Blackjack
inspirado no Exemplo 5.1 de Sutton e Barto.

[`blackjack_sarsa.py`](./blackjack_sarsa.py) fornece uma aplicação
alternativa que usa o algoritmo SARSA com o mesmo ambiente de baralho físico.

## Regras do ambiente

O jogo usa um baralho infinito, isto é, cada carta é sorteada com reposição.
Cartas de figura valem `10`, cartas numéricas mantêm o seu valor e o ás vale
`1` ou `11`.

Existe também uma variante em
[`blackjack_ambiente_52.py`](./blackjack_ambiente_52.py), com um baralho físico
de 52 cartas e sem reposição. Essa variante expõe
`AmbienteBlackjack52`, mantendo a mesma API do ambiente original. O baralho é
recriado e baralhado no início de cada episódio; cada carta retirada é
removida e não pode voltar a ser sorteada nesse episódio.

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
python blackjack.py
```

Para executar a versão SARSA:

```powershell
python blackjack_sarsa.py
```

O programa:

1. fixa a semente aleatória em `42`;
2. cria o ambiente;
3. cria um agente com as ações `[0, 1]`;
4. cria um objeto `QLearning`;
5. executa `100000` episódios;
6. imprime a recompensa média por episódio;
7. imprime a política sôfrega aprendida para estados sem ás utilizável.

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

## Relação com a implementação

Os principais ficheiros são:

| Ficheiro | Responsabilidade |
|---|---|
| `blackjack_ambiente.py` | Estado, baralho, regras, transições e recompensas |
| `blackjack.py` | Ciclo de treino e apresentação da política |
| `blackjack_sarsa.py` | Ciclo de treino SARSA e apresentação da política |
| `agente.py` | Associação entre memória e seletor de ações |
| `selecao_acao.py` | Política ε-greedy |
| `memoria_aprendizagem.py` | Tabela Q |
| `q_learning.py` | Atualização Q-learning |
| `blackjack_ambiente_52.py` | Variante com baralho físico de 52 cartas |

Para usar a variante sem reposição:

```python
from blackjack_ambiente_52 import AmbienteBlackjack52

ambiente = AmbienteBlackjack52()
estado = ambiente.reiniciar()
print(ambiente.cartas_restantes)  # 48 após as quatro cartas iniciais
```
