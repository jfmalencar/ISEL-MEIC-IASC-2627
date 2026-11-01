# Implementação da aprendizagem por reforço

Este diretório contém uma implementação simples de aprendizagem por reforço
tabular. O agente interage com um ambiente, escolhe ações, recebe
recompensas e atualiza os valores estimados das decisões.

## Arquitetura

O fluxo principal é:

1. O ambiente fornece o estado atual.
2. O agente disponibiliza esse estado ao seletor de ação.
3. O seletor escolhe uma ação usando exploração e aproveitamento.
4. O ambiente executa a ação e devolve `(estado seguinte, recompensa, final)`.
5. O algoritmo de aprendizagem atualiza a memória Q.
6. O ciclo repete-se até ao fim do episódio.

### Estado

`estado.py` fornece a classe `Estado`. Cada estado tem um identificador
(`id_estado`) e é hashable, podendo ser usado como parte da chave de um
dicionário.

### Agente

`Agente` (`agente.py`) agrega:

- a lista de ações disponíveis;
- uma instância de `MemoriaDeAprendizagem`;
- uma instância de `SeleccaoAccaoEGreedy`.

Quando `atualizar_accoes` é chamado, a lista é atualizada tanto no agente como
no seletor. Assim, o seletor trabalha sempre com as ações válidas do estado
atual.

## Memória de aprendizagem

`MemoriaDeAprendizagem` mantém uma tabela Q num dicionário:

```text
Q[(estado, ação)] = valor estimado
```

Se um par estado-ação ainda não existir, `q` devolve `valor_omissao`, que por
defeito é `0.0`. O método `actualizar` grava uma nova estimativa.

Os objetos usados como estado devem implementar igualdade e hash consistentes;
por isso `Estado` pode ser usado diretamente como parte da chave.

## Seleção de ação: ε-greedy

`SeleccaoAccaoEGreedy` equilibra:

- **aproveitamento**: escolhe a ação com maior valor Q;
- **exploração**: escolhe aleatoriamente uma ação disponível.

Com probabilidade `epsilon`, é feita exploração. Caso contrário, é escolhida a
ação sôfrega. Quando há empate entre ações com o mesmo valor Q, as ações são
baralhadas antes de aplicar `max`, produzindo um desempate aleatório.

Para a aplicação de Blackjack:

```text
0 = Stick (parar)
1 = Hit (pedir carta)
```

## Algoritmos

### Q-learning

Implementado em `q_learning.py`. É um método *off-policy*: o alvo usa a melhor
ação estimada no estado seguinte, independentemente da ação que será escolhida
pela política de exploração.

Para uma transição não terminal:

```text
Q(s,a) <- Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
```

Em estados terminais, não é acrescentado valor futuro:

```text
Q(s,a) <- Q(s,a) + α [r - Q(s,a)]
```

Parâmetros:

- `alfa` (`α`): taxa de aprendizagem;
- `gama` (`γ`): fator de desconto;
- `final`: indica se a transição termina o episódio.

### SARSA

Implementado em `sarsa.py`. É um método *on-policy*: o alvo usa a ação
efetivamente escolhida no estado seguinte.

```text
Q(s,a) <- Q(s,a) + α [r + γ Q(s',a') - Q(s,a)]
```

Se a transição for terminal ou `a_linha` for `None`, o alvo é apenas `r`.

### Dyna-Q

Implementado em `dyna_q.py`. Dyna-Q combina:

1. uma atualização Q-learning usando a experiência real;
2. o registo da transição no `ModeloTR`;
3. várias atualizações simuladas a partir de transições guardadas.

`ModeloTR` mantém:

```text
T[(s,a)] = s'
R[(s,a)] = r
```

Cada simulação escolhe aleatoriamente uma transição conhecida e reaplica a
atualização de Q-learning. O número de simulações por experiência é definido
por `n_simulacoes`.

## Exemplo de ciclo de aprendizagem

Um ciclo genérico com Q-learning tem a seguinte forma:

```python
estado = ambiente.reiniciar()
final = False

while not final:
    agente.atualizar_accoes(ambiente.accoes(estado))
    acao = agente.seleccao_accao.seleccionar_accao(estado)
    novo_estado, recompensa, final = ambiente.passo(acao)
    q_learning.aprender(estado, acao, recompensa, novo_estado, final=final)
    estado = novo_estado
```

O mesmo padrão pode ser usado com `SARSA` ou `DynaQ`, respeitando os
argumentos adicionais exigidos pelo algoritmo.

