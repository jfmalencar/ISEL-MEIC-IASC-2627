# Aplicação de teste: Cliff Walking

[`cliff_walking.py`](./cliff_walking.py) treina um agente Q-learning para
atravessar uma grelha de 4 x 12, desde o início até ao objetivo, evitando o
precipício.

## Estados e ações

O ambiente [`cliff_walking_ambiente.py`](./cliff_walking_ambiente.py) usa a
posição codificada como:

```text
estado = linha * 12 + coluna
```

O estado inicial é `36` (`[3, 0]`) e o objetivo é `47` (`[3, 11]`).

| Ação | Movimento |
|---:|---|
| `0` | Cima |
| `1` | Direita |
| `2` | Baixo |
| `3` | Esquerda |

## Recompensas e transições

- Cada movimento normal produz `-1`.
- Entrar no precipício (`37..46`) produz `-100` e reposiciona o agente no
  estado inicial `36`.
- Entrar no objetivo `47` termina o episódio.
- A informação da transição inclui `{"p": 1.0}`.

`is_slippery=False` é o comportamento padrão. Quando ativado, a ação pode ser
substituída aleatoriamente por uma direção perpendicular ou pela direção
pretendida.

## Execução

No diretório `TP\reinf_learning`, executar:

```powershell
python cliff_walking.py
```

O programa treina durante 5000 episódios e apresenta a recompensa média, o
número médio de passos, as quedas no precipício e a política aprendida. Na
política impressa:

- `S` representa o início;
- `C` representa o precipício;
- `G` representa o objetivo;
- `^`, `>`, `v` e `<` representam cima, direita, baixo e esquerda.

