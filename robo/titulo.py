#!/usr/bin/env python3
"""
PADRÃO ÚNICO DO TÍTULO — feed E Reels (regra do Israel, 26/11/2026).
Modelo aprovado: post do xerife de Frederick (26/11/2026):
  "Xerife aliado do ICE há 18 / anos em Maryland perde / a eleição para democrata"

- SEMPRE 3 linhas, com o mesmo tanto de texto em cada uma (nada de linha cheia e linha curtinha).
- SEMPRE o mesmo tamanho de letra: Poppins Bold 66 px (em arte de 1080 de largura). Nunca diminuir nem aumentar.
- Distância da lateral: a linha mais larga pode ter no máximo 825 px (cerca de 127 px de margem de cada lado).
  Esse é o LIMITE: nunca chegar mais perto da borda que isso.
- No máximo 74 caracteres contando espaços (o tanto do título do xerife). Mínimo 60, para não ficar "fechadinho".
Se o título não couber nesse padrão, o script RECUSA: reescreva o título e rode de novo.

Uso (conferir um título antes de fazer a arte ou o Reels):
  python3 robo/titulo.py "Título da notícia"
  python3 robo/titulo.py "Título da notícia" --html    # devolve as 3 linhas com <br> para o HTML do Reels
"""
import os, sys
from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
TAM = 66              # tamanho fixo da letra (px)
LARG_MAX = 826        # largura máxima da linha (px) = a linha mais larga do título modelo -> margem mínima ~127 px de cada lado
MAX_CHARS = 74        # máximo de caracteres, contando espaços
MIN_CHARS = 60        # mínimo, para as 3 linhas não ficarem curtinhas
LARG_MIN = 700        # a linha mais larga tem que passar disso (senão fica fechadinho)
EQUILIBRIO = 0.88     # linha mais curta >= 88% da mais longa
TRACK = -0.035        # espaçamento entre letras (igual à arte e ao CSS: letter-spacing -.035em)
ENTRELINHA = 1.13


def fonte():
    return ImageFont.truetype(os.path.join(AQUI, "fontes", "Poppins-Bold.ttf"), TAM)


def larg(texto, f=None):
    f = f or fonte()
    return sum(f.getlength(c) for c in texto) + TRACK * f.size * (len(texto) - 1)


def tres_linhas(titulo):
    """Devolve (linhas, larguras) ou levanta SystemExit explicando o que corrigir."""
    titulo = " ".join(titulo.split())
    n = len(titulo)
    if n > MAX_CHARS:
        raise SystemExit(f"TÍTULO LONGO: {n} caracteres (máximo {MAX_CHARS}, contando espaços). Encurte.")
    if n < MIN_CHARS:
        raise SystemExit(f"TÍTULO CURTO: {n} caracteres (mínimo {MIN_CHARS}). Precisa encher 3 linhas iguais: acrescente informação.")
    f = fonte()
    pal = titulo.split()
    melhor = None
    for i in range(1, len(pal) - 1):
        for j in range(i + 1, len(pal)):
            ls = [" ".join(pal[:i]), " ".join(pal[i:j]), " ".join(pal[j:])]
            if min(len(l.split()) for l in ls) < 2:
                continue
            ws = [larg(l, f) for l in ls]
            if max(ws) > LARG_MAX:
                continue
            custo = max(ws) - min(ws)
            if melhor is None or custo < melhor[0]:
                melhor = (custo, ls, ws)
    if not melhor:
        raise SystemExit("TÍTULO NÃO CABE em 3 linhas no tamanho padrão sem passar do limite da lateral. Reescreva.")
    _, ls, ws = melhor
    if min(ws) / max(ws) < EQUILIBRIO:
        raise SystemExit("TÍTULO DESEQUILIBRADO (" + " | ".join(ls) + "). Reescreva para as 3 linhas ficarem do mesmo tamanho.")
    if max(ws) < LARG_MIN:
        raise SystemExit("TÍTULO FECHADINHO (" + " | ".join(ls) + "). Use palavras maiores ou mais informação.")
    return ls, ws


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        raise SystemExit(__doc__)
    ls, ws = tres_linhas(a[0])
    if "--html" in sys.argv:
        print("<br>".join(ls))
    else:
        for l, w in zip(ls, ws):
            print(f"{w:6.0f} px | {l}")
        print(f"OK: {len(' '.join(a[0].split()))} caracteres, 3 linhas, letra {TAM}, margem mínima {(1080 - max(ws)) / 2:.0f} px")
