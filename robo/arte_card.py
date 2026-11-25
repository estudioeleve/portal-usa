#!/usr/bin/env python3
"""
Arte de notícia do Portal USA (feed 1080x1350) só com Python + Pillow.
Não precisa de navegador. Usa o logo oficial (identidade/portal-usa-logo-bandeira-3d.png), sem esticar.

Uso:
  python3 robo/arte_card.py "EDITORIA" "Título da notícia" "Fonte: Nome da fonte" saida.jpg
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
NAVY = (11, 30, 74)
RED = (200, 32, 47)
SOFT = (201, 214, 242)
W, H = 1080, 1350
MARGEM = 100  # margem de segurança lateral


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(AQUI, "fontes", nome), tam)


def logo_oficial(largura):
    im = Image.open(os.path.join(RAIZ, "identidade", "portal-usa-logo-bandeira-3d.png")).convert("RGB")
    esq = im.crop((0, 0, im.width // 2, im.height))
    caixa = (118, 280, 689, 505)  # área do logo na metade azul
    lg = esq.crop(caixa)
    alt = round(lg.height * largura / lg.width)
    return lg.resize((largura, alt), Image.LANCZOS)


TRACK = -0.035  # letras bem juntas, igual às molduras (letter-spacing -.035em)


def larg(texto, f):
    return sum(f.getlength(c) for c in texto) + TRACK * f.size * (len(texto) - 1)


def texto_junto(d, cx, cy, texto, f, cor):
    x = cx - larg(texto, f) / 2
    for c in texto:
        d.text((x, cy), c, font=f, fill=cor, anchor="lm")
        x += f.getlength(c) + TRACK * f.size


def quebrar_equilibrado(texto, f, larg_max, max_linhas=4):
    """Escolhe a quebra de linhas com larguras mais parecidas (nada de palavra sozinha)."""
    pal = texto.split()
    w = lambda s: larg(s, f)
    melhor = None
    n = len(pal)

    def rec(i, linhas):
        nonlocal melhor
        if len(linhas) > max_linhas:
            return
        if i == n:
            ws = [w(l) for l in linhas]
            if max(ws) > larg_max:
                return
            custo = (max(ws) - min(ws)) + len(linhas) * 5
            if len(linhas) > 1 and min(len(l.split()) for l in linhas) < 2:
                custo += 10000
            if melhor is None or custo < melhor[0]:
                melhor = (custo, linhas)
            return
        for j in range(i + 1, n + 1):
            l = " ".join(pal[i:j])
            if w(l) > larg_max:
                break
            rec(j, linhas + [l])

    rec(0, [])
    return melhor[1] if melhor else None


def montar(editoria, titulo, fonte_txt, saida):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    lg = logo_oficial(520)
    img.paste(lg, ((W - lg.width) // 2, 150))
    # título: maior fonte que caiba em até 4 linhas equilibradas
    for tam in range(76, 46, -2):
        f = fonte("Poppins-Bold.ttf", tam)
        linhas = quebrar_equilibrado(titulo, f, W - 2 * MARGEM)
        if linhas:
            break
    if not linhas:
        raise SystemExit("Título longo demais: encurte.")
    alt_l = int(tam * 1.15)
    bloco = alt_l * len(linhas)
    y_tit = 840 - bloco // 2 + 40
    # chip da editoria
    fc = fonte("Poppins-Bold.ttf", 30)
    tw = d.textlength(editoria.upper(), font=fc)
    cx0 = (W - tw) / 2 - 22
    cy0 = y_tit - 92
    d.rectangle((cx0, cy0, cx0 + tw + 44, cy0 + 60), fill=RED)
    d.text((W / 2, cy0 + 30), editoria.upper(), font=fc, fill="white", anchor="mm")
    for i, l in enumerate(linhas):
        texto_junto(d, W / 2, y_tit + i * alt_l + alt_l / 2, l, f, "white")
    fr = fonte("Poppins-Regular.ttf", 26)
    if fonte_txt:
        d.text((W / 2, H - 140), fonte_txt, font=fr, fill=SOFT, anchor="mm")
    d.text((W / 2, H - 90), "@portalusanews", font=fonte("Poppins-Regular.ttf", 28), fill=SOFT, anchor="mm")
    img.save(saida, quality=93)
    print(saida)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4:
        raise SystemExit(__doc__)
    montar(a[0], a[1], a[2], a[3])
