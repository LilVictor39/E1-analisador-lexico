# E1 — Analisador léxico

**Individual · entrega no encontro 8**

---

## O que você vai construir

Um programa que lê isto:

```
inteiro qtd = 42;
```

E devolve isto:

```
TIPO      'inteiro'
IDENT     'qtd'
ATRIB     '='
INTEIRO   '42'
PVIRG     ';'
```

Isso é a **primeira fase de um compilador**: transformar texto solto numa sequência de
tokens identificados.

---

## O que já está pronto, e o que é seu

Toda a lógica de decisão já está escrita: ler o arquivo, aplicar o casamento mais
longo, resolver prioridade entre padrões, reportar erro com linha e coluna.

**Seu trabalho é um só: definir os autômatos.**

Você desenha o autômato no papel, como fez na oficina, e depois escreve aquele desenho
em Python. Só isso.

---

## Um exemplo completo, do papel ao teste

Vamos fazer juntos o autômato do **literal inteiro**, que é o nível 1.

### Passo 1 · O que a máquina precisa lembrar

*Um inteiro é um ou mais dígitos.*

Então a máquina precisa lembrar apenas: **já vi pelo menos um dígito?**

Duas respostas, dois estados.

### Passo 2 · O desenho

```
                dígito
    ──▶ ( n0 ) ────────▶ (( n1 ))
                             ↺ dígito
```

`n0` é o inicial. `n1` é de aceitação, porque chegando ali você já viu um dígito. E
`n1` tem laço, porque mais dígitos continuam valendo.

### Passo 3 · O desenho virando código

Cada peça do desenho vira uma linha:

```python
afd_inteiro = afd(
    estados=['n0', 'n1'],                   # os dois círculos
    transicoes={
        'n0': de(DIGITOS, 'n1'),            # a flecha de n0 para n1
        'n1': de(DIGITOS, 'n1'),            # o laço em n1
    },
    inicial='n0',                           # a flecha que vem do nada
    finais=['n1'],                          # o círculo duplo
)
```

**Compare com o desenho.** Cada linha do código é um elemento do desenho, na mesma
ordem: os estados, as flechas, o inicial, os finais.

### Passo 4 · Testar

```bash
python3 testar.py
```

```
  NIVEL 0  identificadores e espacos      3/3  ok
  NIVEL 1  literais inteiros              4/4  ok
  NIVEL 2  atribuicao e ponto e virgula   0/3  FALHOU
```

Passou. O testador avançou sozinho para o próximo nível.

---

## As duas ferramentas que você vai usar

### `afd(...)` — monta o autômato

Recebe quatro coisas, que são exatamente as quatro do seu desenho:

| parâmetro | é |
|---|---|
| `estados` | a lista dos círculos |
| `transicoes` | as flechas |
| `inicial` | onde começa |
| `finais` | quais têm círculo duplo |

**E ele completa o autômato para você.** Todo par estado-símbolo que você não declarar
vai para um estado de erro, que rejeita. Você não precisa desenhar o estado de erro:
ele é acrescentado automaticamente.

### `de(...)` — atalho para muitas flechas

Desenhar uma flecha para cada dígito daria dez linhas. `de` faz de uma vez:

```python
de(DIGITOS, 'n1')
# vira {'0':'n1', '1':'n1', '2':'n1', ..., '9':'n1'}
```

**Conjuntos já prontos:**

`LETRAS` · `DIGITOS` · `SUBLIN` · `BRANCOS` · `PONTO` · `BARRA` · `IGUAL` · `PVIRG` · `SIGMA`

Combine com `|` para unir e `-` para tirar:

```python
de(LETRAS | DIGITOS, 'i1')     # letras e dígitos
de(SIGMA - {'\n'}, 'c1')       # qualquer coisa menos quebra de linha
```

---

## Os oito níveis

Trabalhe **em ordem**, de cima para baixo no arquivo `afds.py`.

| nível | o que passa a funcionar | o que você escreve |
|---|---|---|
| 0 | `qtd` | nada, já vem pronto |
| 1 | `42` | o autômato do inteiro |
| 2 | `qtd = 42;` | atribuição e ponto e vírgula |
| 3 | `inteiro qtd = 42;` | as palavras reservadas de tipo |
| 4 | `real media = 7.5;` | o autômato do real |
| 5 | `logico ok = verdadeiro;` | mais palavras reservadas |
| 6 | `// comentário` | o autômato do comentário |
| 7 | um arquivo completo | nada, é a recompensa |

**O nível 0 já vem resolvido.** Leia o código dele com atenção antes de começar: são os
seus dois modelos, o identificador e o espaço em branco.

---

## Como trabalhar

**Rode o testador a cada mudança.**

```bash
python3 testar.py
```

Ele para no primeiro nível que falha, mostra o que era esperado, o que saiu, e dá uma
dica.

```
  NIVEL 4  literais reais                 0/4  FALHOU

    entrada:   '7.5'
    esperado:  [('REAL', '7.5')]
    obtido:    [('INTEIRO', '7'), erro lexico: [1:2] caractere inesperado '.']

    Dica: afd_real: digitos, ponto, digitos. O estado DEPOIS do ponto
          nao pode ser final, senao '12.' passa.
```

**E veja o analisador rodando de verdade** a qualquer momento:

```bash
python3 lexico.py niveis/n3.mini
```

---

## Preparação

```bash
pip install automata-lib
```

Opcional, só se quiser gerar os desenhos automaticamente:

```bash
pip install pygraphviz coloraide
```

---

## Duas armadilhas anunciadas

**Nível 4, o número real.** O estado logo depois do ponto **não pode ser de
aceitação**. Se for, `12.` passa como número válido. É exatamente a armadilha que
vocês resolveram no papel na oficina.

**Nível 6, o comentário.** Ele vai até o fim da linha, então a quebra de linha não faz
parte dele. `SIGMA - {'\n'}` é o seu amigo.

---

## O que entregar

**1. O arquivo `afds.py`** com os oito níveis passando.

**2. Um relatório de duas páginas**, com:

- Um **desenho** de cada autômato que você escreveu, feito à mão ou em ferramenta
- Para cada um: **o que cada estado lembra**, em português
- Quantos estados você usou, e por que esse número
- O nível que te deu mais trabalho, e o que estava errado na sua primeira tentativa

---

## Como será avaliado

| | peso |
|---|---|
| os oito níveis passando | 40% |
| os desenhos, corretos e correspondendo ao código | 25% |
| a explicação do que cada estado lembra | 25% |
| o relato do erro que você cometeu e corrigiu | 10% |

Os últimos 10% são de graça e quase ninguém pega: basta contar honestamente onde você
travou. Errar e consertar é o trabalho.

---

## Se travar

**O testador não roda.** Confira se instalou `automata-lib` e se está na pasta certa.

**Um nível passa e o seguinte quebra o anterior.** Provavelmente você marcou um estado
como final que não deveria ser, e agora um padrão está roubando o casamento de outro.

**Não sei quantos estados usar.** Volte ao papel e responda a pergunta da oficina: o
que cada estado precisa lembrar? A quantidade de respostas distintas é a quantidade de
estados.

**Estado sobrando não é erro.** Se o seu autômato funciona com um estado a mais que o
do colega, está certo do mesmo jeito.
