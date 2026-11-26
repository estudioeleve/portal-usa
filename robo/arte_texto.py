#!/usr/bin/env python3
"""
Tela de TEXTO do carrossel do Portal USA (feed 1080x1350), na identidade oficial.
Fundo azul-marinho, logo oficial no canto, chip vermelho, título curto, texto com marcadores,
número da tela e @portalusanews. Margem lateral igual à do título padrão (127 px).

Uso:
  python3 robo/arte_texto.py "CHIP" "Título da tela" "Texto|• item 1|• item 2" saida.jpg "2/5"
  - Separe parágrafos/itens com |. Item que começa com "• " vira marcador vermelho.
  - Trechos entre *asteriscos* saem em negrito.
O texto tem que caber: se passar do espaço, o script recusa (resuma mais).
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
import arte_card as base

W, H = 1080, 1350
M = 127
NAVY, NAVY2, RED = (11, 30, 74), (19, 47, 110), (200, 32, 47)
SOFT = (201, 214, 242)


def f(nome, tam):
    return ImageFont.truetype(os.path.join(base.AQUI, "fontes", nome), tam)


def fundo():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = tuple(int(NAVY2[i] * (1 - t) + NAVY[i] * t) for i in range(3))
        d.line((0, y, W, y), fill=c)
    return img


def palavras_ricas(texto):
    """Quebra em (palavra, negrito). *trecho em negrito* pode ter várias palavras."""
    out, dentro = [], False
    for p in texto.split():
        comeca = p.startswith("*")
        termina = p.rstrip(".,;:!?)").endswith("*") and len(p.strip("*.,;:!?)")) > 0
        neg = dentro or comeca
        if comeca and not termina:
            dentro = True
        if termina:
            dentro = False
        if p.strip("*"):
            out.append((p.replace("*", ""), neg))
    return out


def montar(chip, titulo, corpo, saida, pag):
    img = fundo()
    d = ImageDraw.Draw(img)
    lg = base.logo_oficial(193)
    img.paste(lg, (80, 64), lg)
    d.text((W - 80, 112), pag, font=f("Poppins-Regular.ttf", 28), fill=SOFT, anchor="rm")
    y = 250
    fc = f("Poppins-Bold.ttf", 28)
    tw = d.textlength(chip.upper(), font=fc)
    d.rectangle((M, y, M + tw + 40, y + 62), fill=RED)
    d.text((M + 20, y + 31), chip.upper(), font=fc, fill="white", anchor="lm")
    y += 100
    ft = f("Poppins-Bold.ttf", 58)
    for linha in quebrar([(w, True) for w in titulo.split()], ft, ft, W - 2 * M):
        d.text((M, y), " ".join(w for w, _ in linha), font=ft, fill="white")
        y += 70
    y += 30
    tam = 38
    fr, fb = f("Poppins-Regular.ttf", tam), f("Poppins-Bold.ttf", tam)
    for par in corpo.split("|"):
        par = par.strip()
        marc = par.startswith("• ")
        if marc:
            par = par[2:]
        x0 = M + (44 if marc else 0)
        linhas = quebrar(palavras_ricas(par), fr, fb, W - M - x0)
        for i, linha in enumerate(linhas):
            if marc and i == 0:
                d.rectangle((M + 4, y + 20, M + 20, y + 36), fill=RED)
            x = x0
            for w, b in linha:
                fo = fb if b else fr
                d.text((x, y), w, font=fo, fill="white" if b else (232, 237, 247))
                x += d.textlength(w + " ", font=fo)
            y += int(tam * 1.42)
        y += 26
    if y > H - 150:
        raise SystemExit(f"TEXTO NÃO CABE na tela ({saida}): resuma mais.")
    d.line((M, H - 120, W - M, H - 120), fill=(60, 84, 140), width=2)
    d.text((W / 2, H - 76), "@portalusanews", font=f("Poppins-Regular.ttf", 26), fill=SOFT, anchor="mm")
    img.save(saida, quality=93)
    print(saida)


def quebrar(pals, fr, fb, larg_max):
    linhas, atual, wcur = [], [], 0
    for w, b in pals:
        fo = fb if b else fr
        lw = fo.getlength(w + " ")
        if atual and wcur + fo.getlength(w) > larg_max:
            linhas.append(atual)
            atual, wcur = [], 0
        atual.append((w, b))
        wcur += lw
    if atual:
        linhas.append(atual)
    return linhas


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 5:
        raise SystemExit(__doc__)
    montar(*a[:5])
