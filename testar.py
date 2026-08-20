"""
Testador por niveis da Atividade 1.   Uso:  python3 testar.py

Roda um nivel por vez e PARA no primeiro que falhar, com uma dica.
Resolva um nivel antes de olhar o proximo.
"""
import sys
from mini_base import analisar, ErroLexico
from afds import REGRAS, PALAVRAS, DESCARTAR

ERRO_ESPERADO = object()


def tokens(texto):
    return [(c, l) for c, l, _, _ in
            analisar(texto, REGRAS, PALAVRAS, DESCARTAR)][:-1]


NIVEIS = [
    ('0', 'identificadores e espacos (ja vem pronto)', [
        ('qtd',        [('ID', 'qtd')]),
        ('a b',        [('ID', 'a'), ('ID', 'b')]),
        ('_x1',        [('ID', '_x1')]),
     ], 'Se este nivel falhar, algo foi apagado do afd_id ou do afd_branco.'),

    ('1', 'literais inteiros', [
        ('42',         [('INTEIRO', '42')]),
        ('0',          [('INTEIRO', '0')]),
        ('7 13',       [('INTEIRO', '7'), ('INTEIRO', '13')]),
        ('9x',         [('INTEIRO', '9'), ('ID', 'x')]),
     ], 'afd_inteiro: um ou mais digitos. Dois estados bastam.\n'
        '  Repare no ultimo caso: "9x" da dois tokens, nao um erro.'),

    ('2', 'atribuicao e ponto e virgula', [
        ('=',          [('ATRIB', '=')]),
        (';',          [('PVIRG', ';')]),
        ('qtd = 42;',  [('ID', 'qtd'), ('ATRIB', '='),
                        ('INTEIRO', '42'), ('PVIRG', ';')]),
        ('==',         [('ATRIB', '='), ('ATRIB', '=')]),
        (';;',         [('PVIRG', ';'), ('PVIRG', ';')]),
     ], 'afd_atrib e afd_pvirg: dois estados cada, uma transicao cada.\n'
        '  Use os conjuntos IGUAL e PVIRG.\n'
        '  Cuidado com self-loop: o estado inicial nao pode ter uma\n'
        '  transicao de volta pra ele mesmo, senao "==" vira um token so.'),

    ('3', 'palavras reservadas de tipo', [
        ('inteiro',    [('TIPO', 'inteiro')]),
        ('real',       [('TIPO', 'real')]),
        ('logico',     [('TIPO', 'logico')]),
        ('inteirox',   [('ID', 'inteirox')]),
        ('int',        [('ID', 'int')]),
        ('inteiro qtd = 42;',
                       [('TIPO', 'inteiro'), ('ID', 'qtd'), ('ATRIB', '='),
                        ('INTEIRO', '42'), ('PVIRG', ';')]),
     ], 'Nao e um automato novo. Acrescente as tres palavras ao dicionario\n'
        '  PALAVRAS, mapeando cada uma para a categoria TIPO.\n'
        '  Repare que "inteirox" continua sendo ID: a palavra tem que casar inteira.'),

    ('4', 'literais reais', [
        ('7.5',        [('REAL', '7.5')]),
        ('0.0',        [('REAL', '0.0')]),
        ('6.25',       [('REAL', '6.25')]),
        ('42',         [('INTEIRO', '42')]),
        ('12.',        ERRO_ESPERADO),
        ('real media = 7.5;',
                       [('TIPO', 'real'), ('ID', 'media'), ('ATRIB', '='),
                        ('REAL', '7.5'), ('PVIRG', ';')]),
     ], 'afd_real: digitos, ponto, digitos. Precisa de quatro estados.\n'
        '  A pegadinha esta em "12.": qual estado NAO pode ser final?\n'
        '  Se voce marcou o estado logo depois do ponto como final,\n'
        '  o analisador aceita "12." como numero, e nao deveria.'),

    ('5', 'literais logicos', [
        ('verdadeiro', [('LOGICO', 'verdadeiro')]),
        ('falso',      [('LOGICO', 'falso')]),
        ('falsox',     [('ID', 'falsox')]),
        ('logico ok = verdadeiro;',
                       [('TIPO', 'logico'), ('ID', 'ok'), ('ATRIB', '='),
                        ('LOGICO', 'verdadeiro'), ('PVIRG', ';')]),
     ], 'Mesmo mecanismo do nivel 3: acrescente ao dicionario PALAVRAS,\n'
        '  agora mapeando para a categoria LOGICO.'),

    ('6', 'comentarios de linha', [
        ('// nada',    []),
        ('qtd // resto da linha',      [('ID', 'qtd')]),
        ('// um\nqtd', [('ID', 'qtd')]),
        ('/',          ERRO_ESPERADO),
     ], 'afd_comentario: duas barras, e depois tudo que nao for quebra de linha.\n'
        '  Tres estados. Use BARRA e SIGMA - {chr(10)}.\n'
        '  Comentario ja esta em DESCARTAR, entao ele nao aparece na saida.\n'
        '  Uma barra sozinha deve dar erro: divisao e assunto da atividade 2.'),

    ('7', 'integracao: bloco de declaracoes', [
        ('inteiro qtd = 2;\nreal media;\nlogico ok = falso;',
                       [('TIPO', 'inteiro'), ('ID', 'qtd'), ('ATRIB', '='),
                        ('INTEIRO', '2'), ('PVIRG', ';'),
                        ('TIPO', 'real'), ('ID', 'media'), ('PVIRG', ';'),
                        ('TIPO', 'logico'), ('ID', 'ok'), ('ATRIB', '='),
                        ('LOGICO', 'falso'), ('PVIRG', ';')]),
     ], 'Nada de novo para fazer. Se os niveis anteriores passaram, este passa.'),
]


def roda_nivel(casos):
    falhas = []
    for texto, esperado in casos:
        if esperado is ERRO_ESPERADO:
            try:
                obtido = tokens(texto)
                falhas.append((texto, 'erro lexico', obtido))
            except ErroLexico:
                pass
        else:
            try:
                obtido = tokens(texto)
            except ErroLexico as e:
                falhas.append((texto, esperado, f'erro lexico: {e}'))
                continue
            if obtido != esperado:
                falhas.append((texto, esperado, obtido))
    return falhas


def main():
    print()
    for num, titulo, casos, dica in NIVEIS:
        falhas = roda_nivel(casos)
        passou = len(casos) - len(falhas)
        marca = 'ok' if not falhas else 'FALHOU'
        print(f'  NIVEL {num}  {titulo:<42} {passou}/{len(casos)}  {marca}')
        if falhas:
            texto, esperado, obtido = falhas[0]
            print()
            print(f'    entrada:   {texto!r}')
            print(f'    esperado:  {esperado}')
            print(f'    obtido:    {obtido}')
            if len(falhas) > 1:
                print(f'    (e outros {len(falhas) - 1} caso(s) neste nivel)')
            print()
            print(f'    Dica: {dica}')
            print()
            print(f'  Pare aqui. Resolva o nivel {num} antes de seguir.')
            print()
            sys.exit(1)
    print()
    print('  Todos os niveis passaram. Rode agora:')
    print('      python3 lexico.py niveis/n7.mini')
    print()


if __name__ == '__main__':
    main()
