"""Executa o analisador lexico sobre um arquivo. Uso: python3 lexico.py arquivo"""
import sys
from mini_base import analisar, ErroLexico
from afds import REGRAS, PALAVRAS, DESCARTAR

arquivo = sys.argv[1] if len(sys.argv) > 1 else 'niveis/n7.mini'
with open(arquivo, encoding='utf-8') as f:
    texto = f.read()
try:
    for cat, lex, l, c in analisar(texto, REGRAS, PALAVRAS, DESCARTAR):
        print(f'{l:>3}:{c:<3} {cat:<12} {lex!r}')
except ErroLexico as e:
    print(f'erro lexico: {e}')
    sys.exit(1)
