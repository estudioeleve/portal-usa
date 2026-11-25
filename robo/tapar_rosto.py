#!/usr/bin/env python3
"""
Tapa (desfoca forte) todos os rostos de uma foto. Proteção do imigrante: nunca mostrar rosto.

Uso:
  python3 robo/tapar_rosto.py entrada.jpg saida.jpg
Imprime quantos rostos tapou. Se tapar 0 e houver gente na foto, CONFIRA olhando a imagem:
nesse caso use outra foto ou tape à mão (ex.: --caixa x,y,largura,altura, pode repetir).
Dependência: pip install "opencv-python-headless<5" --break-system-packages
"""
import sys
import cv2


def main():
    args = sys.argv[1:]
    caixas_manuais = []
    while "--caixa" in args:
        i = args.index("--caixa")
        caixas_manuais.append(tuple(int(v) for v in args[i + 1].split(",")))
        del args[i:i + 2]
    entrada, saida = args[0], args[1]
    img = cv2.imread(entrada)
    if img is None:
        sys.exit(f"não abri a foto: {entrada}")
    cinza = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    caixas = list(caixas_manuais)
    for nome in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        det = cv2.CascadeClassifier(cv2.data.haarcascades + nome)
        for (x, y, w, h) in det.detectMultiScale(cinza, 1.1, 5, minSize=(24, 24)):
            caixas.append((x, y, w, h))
        if "profile" in nome:  # perfil virado para o outro lado
            espelho = cv2.flip(cinza, 1)
            W = cinza.shape[1]
            for (x, y, w, h) in det.detectMultiScale(espelho, 1.1, 5, minSize=(24, 24)):
                caixas.append((W - x - w, y, w, h))
    H, W = img.shape[:2]
    for (x, y, w, h) in caixas:
        # margem para cobrir cabelo/queixo
        mx, my = int(w * 0.25), int(h * 0.3)
        x0, y0 = max(0, x - mx), max(0, y - my)
        x1, y1 = min(W, x + w + mx), min(H, y + h + my)
        roi = img[y0:y1, x0:x1]
        k = max(31, (max(x1 - x0, y1 - y0) // 2) | 1)
        # pixeliza + desfoca: impossível reconhecer
        p = cv2.resize(roi, (8, 8), interpolation=cv2.INTER_LINEAR)
        p = cv2.resize(p, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST)
        img[y0:y1, x0:x1] = cv2.GaussianBlur(p, (k, k), 0)
    cv2.imwrite(saida, img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(f"rostos tapados: {len(caixas)}")


if __name__ == "__main__":
    main()
