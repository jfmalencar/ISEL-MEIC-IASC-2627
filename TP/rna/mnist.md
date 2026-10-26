# Aplicação de teste com o dataset MNIST

O ficheiro `mnist.py` testa a implementação da classe `RedeNeuronal` usando o
dataset MNIST. O objetivo é treinar a rede para reconhecer imagens
manuscritas dos dígitos de `0` a `9` e avaliar o seu desempenho com imagens que
não foram usadas durante o treino.
A aplicação pode ser encontrada na diretoria **'/TP/rna/'** do repositório a seguir:
<https://github.com/jfmalencar/ISEL-MEIC-IASC-2627>

## Organização dos dados

O dataset MNIST é composto por quatro ficheiros em formato binário IDX:

- `train-images.idx3-ubyte`: imagens utilizadas no treino;
- `train-labels.idx1-ubyte`: rótulos das imagens de treino;
- `t10k-images.idx3-ubyte`: imagens utilizadas no teste;
- `t10k-labels.idx1-ubyte`: rótulos das imagens de teste.

Os ficheiros devem estar na pasta `mnist`, localizada junto do script
`mnist.py`. O script também aceita a organização alternativa em que cada
ficheiro está dentro de uma pasta com o mesmo nome.

Cada imagem MNIST tem `28 x 28` pixels. Os pixels são representados por valores
inteiros entre `0` e `255`, em que `0` representa preto e `255` representa
branco.

## Carregamento e preparação dos dados

### Imagens

A função `carregar_imagens` executa os seguintes passos:

1. Abre o ficheiro binário em modo de leitura;
2. Lê o cabeçalho IDX;
3. Confirma o *magic number* `2051`, que identifica ficheiros de imagens;
4. Obtém o número de imagens, linhas e colunas;
5. Lê a quantidade de imagens solicitada;
6. Transforma cada imagem numa lista com `784` valores;
7. Normaliza cada pixel através da expressão:

   ```text
   pixel_normalizado = pixel / 255.0
   ```

Depois da normalização, todos os valores de entrada estão no intervalo
`[0, 1]`.

### Rótulos

A função `carregar_rotulos` lê os rótulos correspondentes às imagens:

1. Abre o ficheiro binário;
2. Confirma o *magic number* `2049`, que identifica ficheiros de rótulos;
3. Lê um byte por cada rótulo;
4. Converte cada rótulo para um vetor *one-hot* com 10 posições.

Por exemplo, o dígito `3` é convertido para:

```text
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
```

O índice que contém `1` corresponde à classe correta.

## Arquitetura da rede neuronal

A rede é criada na função `main` com a seguinte forma:

```text
784 -> hidden_size -> 10
```

As camadas têm as seguintes funções:

- **Camada de entrada:** recebe os `784` pixels da imagem;
- **Camada oculta:** possui, por omissão, `32` neurónios;
- **Camada de saída:** possui `10` neurónios, um para cada dígito;
- **Função de ativação:** função sigmoide em todos os neurónios.

O maior valor produzido pelos 10 neurónios da camada de saída representa a
classe escolhida pela rede.

## Processo de treino

O treino é realizado pelo método `treinar` da classe `RedeNeuronal`.

Para cada época e para cada par de entrada e saída esperada, a rede:

1. Propaga os pixels da imagem pelas camadas;
2. Compara a saída obtida com o vetor *one-hot* esperado;
3. Calcula o erro de cada saída;
4. Propaga o erro para trás através da rede;
5. Atualiza os pesos e os pendores dos neurónios;
6. Considera o fator de momento na atualização dos parâmetros.

Este processo é uma aplicação de aprendizagem supervisionada com
retropropagação do erro.

O treino termina quando o número de épocas configurado é atingido. O script
usa `erro_max=0.0`, pelo que não interrompe antecipadamente devido ao erro
máximo da rede.

## Avaliação

Depois do treino, a função `avaliar` propaga as imagens do conjunto de teste
pela rede. Para cada imagem:

1. Obtém os 10 valores produzidos pela camada de saída;
2. Escolhe o índice com maior valor;
3. Compara a classe prevista com o rótulo esperado.

A precisão é calculada por:

```text
precisão = número de classificações corretas / número total de imagens
```

No final, a precisão é apresentada em percentagem:

```text
Precisão no conjunto de teste: 85.40%
```

## Execução

A partir da pasta `TP1\rna`, executar:

```powershell
python mnist.py
```

Por omissão, são usados:

- `1000` imagens para treino;
- `1000` imagens para teste;
- `5` épocas;
- taxa de aprendizagem `0.1`;
- momento `0.5`;
- `32` neurónios na camada oculta;
- semente aleatória `42`.

É possível alterar estes valores através dos argumentos da linha de comandos:

```powershell
python mnist.py `
    --train-size 5000 `
    --test-size 1000 `
    --epochs 10 `
    --learning-rate 0.1 `
    --momentum 0.5 `
    --hidden-size 64 `
    --seed 42
```

Os argumentos `--train-size`, `--test-size` e `--epochs` têm de ser positivos.
Reduzir o número de amostras ou de épocas permite testar rapidamente o
funcionamento da aplicação; aumentar esses valores pode melhorar a
aprendizagem, mas também aumenta o tempo de execução.

## Fluxo geral da aplicação

```text
Início
  |
  v
Ler argumentos e definir a semente aleatória
  |
  v
Localizar os ficheiros IDX do MNIST
  |
  v
Ler e normalizar as imagens
  |
  v
Ler e converter os rótulos para one-hot
  |
  v
Criar a RedeNeuronal
  |
  v
Treinar com retropropagação
  |
  v
Classificar as imagens de teste
  |
  v
Calcular e apresentar a precisão
  |
  v
Fim
```
