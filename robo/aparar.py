#!/usr/bin/env python3
"""
Corta as bordas lisas (faixas brancas/pretas/de cor única) de uma foto.

Uso:
  python3 robo/aparar.py entrada.jpg [saida.jpg]
Sem saída, sobrescreve a entrada.
"""
import sys
from PIL import Image, ImageChops


def aparar(im, tolerancia=18, minimo=0.6):
    """Remove bordas de cor única. Não corta mais que (1 - minimo) de cada lado."""
    im = im.convert("RGB")
    w, h = im.size
    for i in range(4):
        w, h = im.size
        canto = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)][i]
        fundo = Image.new("RGB", im.size, im.getpixel(canto))
        dif = ImageChops.difference(im, fundo).convert("L").point(lambda v: 255 if v > tolerancia else 0)
        caixa = dif.getbbox()
        if not caixa:
            continue
        x0, y0, x1, y1 = caixa
        if (x1 - x0) >= w * minimo and (y1 - y0) >= h * minimo and (x1 - x0, y1 - y0) != (w, h):
            im = im.crop(caixa)
    return im


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ent = sys.argv[1]
    sai = sys.argv[2] if len(sys.argv) > 2 else ent
    im = aparar(Image.open(ent))
    im.save(sai, quality=95)
    print(f"aparada: {sai} ({im.width}x{im.height})")


if __name__ == "__main__":
    main()
