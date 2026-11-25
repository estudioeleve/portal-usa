#!/usr/bin/env python3
"""
Arte de notícia do Portal USA (feed 1080x1350) só com Python + Pillow.
Não precisa de navegador. Usa o logo oficial (identidade/portal-usa-logo-bandeira-3d.png), sem esticar.

Uso:
  python3 robo/arte_card.py "EDITORIA" "Título da notícia" "Fonte: Nome da fonte" saida.jpg [foto.jpg] ["Foto: crédito"]
Segue a moldura oficial do feed. FOTO OBRIGATÓRIA (regra do Israel, 25/11/2026): sem foto, o script recusa.
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
    lg = lg.resize((largura, alt), Image.LANCZOS)
    # tira o fundo azul do PNG (logo vai direto sobre a foto, como na moldura)
    fundo = lg.getpixel((2, 2))
    a = Image.new("L", lg.size)
    pa, pl = a.load(), lg.load()
    for y in range(lg.height):
        for x in range(lg.width):
            dd = max(abs(c - b) for c, b in zip(pl[x, y], fundo))
            pa[x, y] = max(0, min(255, int((dd - 12) * 255 / 50)))
    lg = lg.convert("RGBA")
    lg.putalpha(a)
    return lg


FORCAR = os.environ.get("FORCAR_TITULO") == "1"  # só para teste
TRACK = -0.035  # letras bem juntas, igual às molduras (letter-spacing -.035em)


def larg(texto, f):
    return sum(f.getlength(c) for c in texto) + TRACK * f.size * (len(texto) - 1)


def texto_junto(d, cx, cy, texto, f, cor):
    x = cx - larg(texto, f) / 2
    for c in texto:
        d.text((x, cy), c, font=f, fill=cor, anchor="lm")
        x += f.getlength(c) + TRACK * f.size


def quebrar_equilibrado(texto, f, larg_max, max_linhas=3):
    """Escolhe a quebra (até 3 linhas) com larguras o mais iguais possível (nada de palavra sozinha)."""
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
            custo = (max(ws) - min(ws)) * 3 + sum(abs(x - sum(ws) / len(ws)) for x in ws)
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


def bandeira_fundo():
    """Fundo padrão quando não há foto: bandeira dos EUA grande balançando, escurecida (mesma bandeira do logo)."""
    import math
    from PIL import ImageFilter, ImageEnhance
    fw, fh = 1500, 900
    tex = Image.new("RGB", (fw, fh), "white")
    g = ImageDraw.Draw(tex)
    for k in range(13):
        if k % 2 == 0:
            g.rectangle((0, k * fh / 13, fw, (k + 1) * fh / 13 + 1), fill=RED)
    cw, ch = fw * 0.4, fh * 7 / 13
    g.rectangle((0, 0, cw, ch), fill=(31, 74, 168))
    for r in range(9):
        nn = 5 if r % 2 else 6
        for k in range(nn):
            x = (k + (1 if r % 2 else 0.5)) * cw / 6.2 + cw * 0.02
            y = (r + 0.75) * ch / 9.6
            pts = []
            for q in range(10):
                a = -math.pi / 2 + q * math.pi / 5
                rr = ch * 0.018 if q % 2 else ch * 0.045
                pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
            g.polygon(pts, fill="white")
    out = Image.new("RGB", (fw, fh + 300), NAVY)
    sh = Image.new("L", out.size, 128)
    amp = fh * 0.08
    for x in range(fw):
        u = x / fw
        ph = u * 2.4 * math.pi + 0.6
        dy = math.sin(ph) * amp * (0.35 + 0.65 * u)
        out.paste(tex.crop((x, 0, x + 1, fh)), (x, int(150 + dy)))
        sh.paste(int(128 + 90 * math.cos(ph)), (x, 0, x + 1, out.height))
    luz = Image.merge("RGB", (sh, sh, sh))
    from PIL import ImageChops
    out = ImageChops.multiply(out, luz).point(lambda v: min(255, int(v * 1.6)))
    out = out.rotate(-8, resample=Image.BICUBIC, expand=False, fillcolor=NAVY)
    # preenche o quadro (corta, não estica)
    esc = max(W / out.width, H / out.height) * 1.15
    out = out.resize((int(out.width * esc), int(out.height * esc)), Image.LANCZOS)
    l = (out.width - W) // 2
    out = out.crop((l, 0, l + W, H)).filter(ImageFilter.GaussianBlur(3))
    return ImageEnhance.Brightness(out).enhance(0.55)


def foto_preenchida(caminho):
    """Foto ocupando o quadro todo, sem esticar (corta as sobras, centralizada)."""
    im = Image.open(caminho).convert("RGB")
    esc = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 3
    return im.crop((l, t, l + W, t + H))


def degrade(img):
    """Degradê do padrão: forte no rodapé, sumindo até o meio; sombra leve no topo para o logo."""
    ov = Image.new("RGBA", (W, H), NAVY + (0,))
    px = ov.load()
    for y in range(H):
        if y < 240:
            a = 0.8 * (1 - y / 240)
        elif y >= 675:
            f = (y - 675) / (H - 675)
            pts = [(0, 0), (0.30, 0.45), (0.65, 0.85), (0.92, 1.0), (1, 1)]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if x0 <= f <= x1:
                    a = y0 + (y1 - y0) * (f - x0) / (x1 - x0)
                    break
        else:
            a = 0
        for x in range(W):
            px[x, y] = NAVY + (int(255 * a),)
    return Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")


def montar(editoria, titulo, fonte_txt, saida, foto=None, credito=None):
    if not foto or not os.path.exists(foto) or not credito:
        sys.exit("SEM FOTO: post só com bandeira é proibido. Use robo/coletar.py e passe a foto e o crédito 'Foto: NOME / VEÍCULO'.")
    # MOLDURA OFICIAL DO FEED (molduras/portal-usa-moldura-feed.png / modelos/m_feed.html):
    # foto cheia em cima, logo no canto superior esquerdo, degradê no rodapé, chip vermelho,
    # título branco centralizado em até 3 linhas iguais, @portalusanews embaixo.
    img = foto_preenchida(foto) if foto else bandeira_fundo()
    img = degrade(img)
    d = ImageDraw.Draw(img)
    lg = logo_oficial(193)  # 30% menor (Israel, 25/11/2026)
    img.paste(lg, (80, 64), lg)
    if foto and credito:
        fcr = fonte("Poppins-Regular.ttf", 18)
        d.text((W - 24, 652), credito, font=fcr, fill=(225, 230, 240), anchor="rm")
    # título: até 3 linhas do MESMO tamanho (padrão aprovado pelo Israel)
    opcoes = []
    for tam in range(66, 46, -2):
        ft = fonte("Poppins-Bold.ttf", tam)
        ls = quebrar_equilibrado(titulo, ft, W - 180)
        if ls:
            ws = [larg(l, ft) for l in ls]
            opcoes.append((min(ws) / max(ws), tam, ft, ls))
    if not opcoes:
        raise SystemExit("Título longo demais para 3 linhas: encurte.")
    boas = [o for o in opcoes if o[0] >= 0.88]
    razao, tam, f, linhas = boas[0] if boas else max(opcoes, key=lambda o: (o[0], o[1]))
    if razao < 0.80 and not FORCAR:
        raise SystemExit(
            "Título desequilibrado (linhas: " + " | ".join(linhas) + "). "
            "Reescreva o título (mais curto ou com outras palavras) para as linhas ficarem do mesmo tamanho.")
    # chip da editoria (posição fixa da moldura)
    fc = fonte("Poppins-Bold.ttf", 28)
    ed = editoria.upper()
    tw = d.textlength(ed, font=fc)
    x0, y0 = (W - tw) / 2 - 20, 868
    d.rectangle((x0, y0, x0 + tw + 40, y0 + 62), fill=RED)
    d.text((W / 2, y0 + 31), ed, font=fc, fill="white", anchor="mm")
    alt_l = tam * 1.13
    y_tit = 952
    for i, l in enumerate(linhas):
        texto_junto(d, W / 2, y_tit + i * alt_l + alt_l / 2, l, f, "white")
    d.text((W / 2, H - 76), "@portalusanews", font=fonte("Poppins-Regular.ttf", 26), fill=SOFT, anchor="mm")
    img.save(saida, quality=93)
    print(saida)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 4:
        raise SystemExit(__doc__)
    montar(a[0], a[1], a[2], a[3], a[4] if len(a) > 4 else None, a[5] if len(a) > 5 else None)
