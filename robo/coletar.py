#!/usr/bin/env python3
"""
Pega a foto principal (og:image) da matéria da fonte e o crédito da foto (figcaption).

Uso:
  python3 robo/coletar.py LINK_DA_MATERIA            # começa nova coleta
  python3 robo/coletar.py OUTRO_LINK --anexar        # acrescenta outra foto do mesmo fato

Grava em dados/feed/fotos/:
  - AAAAMMDD-HHMMSS-<site>.jpg   (foto já aparada pelo aparar.py)
  - coleta.json                  (lista: link, site, foto, credito, credito_legenda, largura, altura)

Erro de rede (403, bloqueado, sem conexão) → sai com código 2 e a mensagem "ERRO DE REDE".
Nesse caso o robô PARA e avisa o Israel (não tenta outro caminho).
Depois de coletar, o robô TEM que abrir e olhar a foto antes de usar.
Deps: pip install requests trafilatura beautifulsoup4 ftfy pillow --break-system-packages
"""
import io, json, os, re, sys, time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image

try:
    import ftfy
    conserta = ftfy.fix_text
except ImportError:
    conserta = lambda t: t

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from aparar import aparar  # noqa: E402

RAIZ = os.path.dirname(AQUI)
PASTA = os.path.join(RAIZ, "dados", "feed", "fotos")
INDICE = os.path.join(PASTA, "coleta.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"}
CA = "/root/.ccr/ca-bundle.crt"


def erro_rede(msg):
    print(f"ERRO DE REDE: {msg}")
    print("Tente a foto em outra matéria do mesmo fato (--anexar). Regra do Israel: quando der erro, resolva e poste.")
    sys.exit(2)


def baixar(url):
    try:
        r = requests.get(url, headers=UA, timeout=30, verify=CA if os.path.exists(CA) else True)
    except requests.RequestException as e:
        erro_rede(f"{urlparse(url).netloc} bloqueado ou fora do ar ({e.__class__.__name__})")
    if r.status_code in (401, 403, 407, 451) or r.status_code >= 500:
        erro_rede(f"{urlparse(url).netloc} respondeu {r.status_code}")
    r.raise_for_status()
    return r


def meta(soup, *nomes):
    for n in nomes:
        t = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n})
        if t and t.get("content"):
            return t["content"].strip()
    return ""


def credito_figcaption(soup, foto_url):
    """Procura o crédito na legenda da foto principal (figcaption) ou em campos de crédito."""
    nome_foto = os.path.basename(urlparse(foto_url).path).split(".")[0][:20]
    figuras = soup.find_all("figure")
    alvo = None
    for f in figuras:
        img = f.find("img")
        src = (img.get("src") or img.get("data-src") or "") if img else ""
        if nome_foto and nome_foto in src:
            alvo = f
            break
    if alvo is None and figuras:
        alvo = figuras[0]
    legenda = ""
    if alvo is not None:
        cap = alvo.find("figcaption")
        if cap:
            legenda = conserta(" ".join(cap.get_text(" ").split()))
    if not legenda:
        c = soup.find(class_=re.compile(r"(credit|credito|caption|legenda)", re.I))
        if c:
            legenda = conserta(" ".join(c.get_text(" ").split()))
    nome = ""
    m0 = re.search(r"([A-Z][\w.'-]+(?: [A-Z][\w.'-]+){1,3})\s*/\s*(?:[\w ]*Photo|AP|Reuters|Getty Images|AFP|EFE|Staff)\b", legenda)
    if m0:
        return legenda[:300], m0.group(1).strip()
    m = re.search(r"(?:foto|photo|crédito|credit|imagem|image)\s*[:/-]?\s*(?:by\s+)?([^|()\n]{2,80})", legenda, re.I)
    if m:
        nome = m.group(1).strip(" .-–—")
    elif re.search(r"(AP|Reuters|Getty|AFP|EFE)\b", legenda):
        nome = re.search(r"([\w .'-]*(AP|Reuters|Getty Images|AFP|EFE)[\w .'-]*)", legenda).group(1).strip()
    return legenda[:300], nome


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    anexar = "--anexar" in sys.argv
    if not args:
        print(__doc__)
        sys.exit(1)
    link = args[0]
    os.makedirs(PASTA, exist_ok=True)

    r = baixar(link)
    r.encoding = r.apparent_encoding or r.encoding
    soup = BeautifulSoup(r.text, "html.parser")
    foto = meta(soup, "og:image:secure_url", "og:image", "twitter:image", "twitter:image:src")
    if not foto:
        print("SEM FOTO: a matéria não tem og:image. Procure outra matéria do mesmo fato (--anexar).")
        sys.exit(3)
    foto = urljoin(link, foto)
    veiculo = meta(soup, "og:site_name") or urlparse(link).netloc.replace("www.", "")
    titulo = conserta(meta(soup, "og:title") or (soup.title.get_text() if soup.title else ""))

    ri = baixar(foto)
    try:
        im = Image.open(io.BytesIO(ri.content))
        im.load()
    except Exception:
        print("SEM FOTO: o arquivo da og:image não é uma imagem válida.")
        sys.exit(3)
    im = aparar(im)
    site = re.sub(r"[^a-z0-9]+", "-", urlparse(link).netloc.replace("www.", "").lower()).strip("-")
    nome = time.strftime("%Y%m%d-%H%M%S", time.gmtime()) + f"-{site}.jpg"
    caminho = os.path.join(PASTA, nome)
    im.save(caminho, quality=95)

    legenda, autor = credito_figcaption(soup, foto)
    credito = f"Foto: {autor} / {veiculo}" if autor else f"Foto: reprodução / {veiculo}"
    item = {"link": link, "titulo": titulo, "veiculo": veiculo, "foto": os.path.relpath(caminho, RAIZ),
            "og_image": foto, "credito": credito, "credito_legenda": legenda,
            "largura": im.width, "altura": im.height}

    lista = []
    if anexar and os.path.exists(INDICE):
        try:
            lista = json.load(open(INDICE, encoding="utf-8"))
        except Exception:
            lista = []
    lista.append(item)
    json.dump(lista, open(INDICE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(json.dumps(item, ensure_ascii=False, indent=1))
    if im.width < 900 or im.height < 600:
        print("ATENÇÃO: resolução baixa — provavelmente não serve. Procure outra matéria (--anexar).")
    print("Agora ABRA e OLHE a foto antes de usar (fato certo, nítida, assunto no centro, sem logo, sem rosto de imigrante).")


if __name__ == "__main__":
    main()
