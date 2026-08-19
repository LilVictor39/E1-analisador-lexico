"""
Infraestrutura do analisador lexico.  NAO EDITE ESTE ARQUIVO.
Seu trabalho e no afds.py
"""
from automata.fa.dfa import DFA
import string

# ----------------------------------------------------------------------
# Conjuntos de simbolos, prontos para usar nas transicoes
# ----------------------------------------------------------------------
LETRAS  = set(string.ascii_letters)      # a..z  A..Z
DIGITOS = set(string.digits)             # 0..9
SUBLIN  = {'_'}
BRANCOS = set(' \t\r\n')
PONTO   = {'.'}
BARRA   = {'/'}
IGUAL   = {'='}
PVIRG   = {';'}
OUTROS  = set(string.punctuation) - SUBLIN - PONTO - BARRA - IGUAL - PVIRG

SIGMA = (LETRAS | DIGITOS | SUBLIN | BRANCOS | PONTO
         | BARRA | IGUAL | PVIRG | OUTROS)

ERRO = 'ERRO'      # estado absorvente de rejeicao, criado automaticamente


def de(conjunto, destino):
    """de(DIGITOS, 'n1')  ->  {'0':'n1', '1':'n1', ..., '9':'n1'}"""
    return {c: destino for c in conjunto}


def afd(estados, transicoes, inicial, finais):
    """
    Monta um AFD COMPLETO a partir de uma especificacao parcial.
    Todo par (estado, simbolo) que voce nao declarar vai para ERRO,
    e ERRO rejeita.
    """
    todos = set(estados) | {ERRO}
    tabela = {}
    for e in todos:
        linha = {c: ERRO for c in SIGMA}
        linha.update(transicoes.get(e, {}))
        tabela[e] = linha
    return DFA(states=todos, input_symbols=SIGMA, transitions=tabela,
               initial_state=inicial, final_states=set(finais))


def mais_longo(automato, texto, inicio):
    """Tamanho do MAIOR prefixo de texto[inicio:] aceito. Zero se nada casar."""
    estado = automato.initial_state
    melhor = 0
    for i in range(inicio, len(texto)):
        estado = automato.transitions[estado][texto[i]]
        if estado == ERRO:
            break
        if estado in automato.final_states:
            melhor = i - inicio + 1
    return melhor


class ErroLexico(Exception):
    pass


def analisar(texto, regras, palavras, descartar):
    """
    Duas regras de decisao:
      1. casamento mais longo
      2. prioridade pela ordem em `regras`, para empates de mesmo tamanho
    """
    tokens, pos, linha, coluna = [], 0, 1, 1
    while pos < len(texto):
        vencedora, tamanho = None, 0
        for nome, automato in regras:
            n = mais_longo(automato, texto, pos)
            if n > tamanho:            # ESTRITAMENTE maior: a ordem desempata
                vencedora, tamanho = nome, n
        if tamanho == 0:
            raise ErroLexico(
                f'[{linha}:{coluna}] caractere inesperado {texto[pos]!r}')
        lexema = texto[pos:pos + tamanho]
        # uma palavra reservada e um ID que esta na tabela de palavras
        if vencedora == 'ID' and lexema in palavras:
            vencedora = palavras[lexema]
        if vencedora not in descartar:
            tokens.append((vencedora, lexema, linha, coluna))
        quebras = lexema.count('\n')
        if quebras:
            linha += quebras
            coluna = tamanho - lexema.rfind('\n')
        else:
            coluna += tamanho
        pos += tamanho
    tokens.append(('EOF', '', linha, coluna))
    return tokens
