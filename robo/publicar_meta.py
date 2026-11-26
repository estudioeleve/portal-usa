#!/usr/bin/env python3
"""
Publica no Instagram do Portal USA pela API oficial da Meta (Instagram Graph API).
Sem custo. Sem biblioteca extra (só Python 3).

A chave NUNCA fica neste arquivo nem no repositório.
Ela fica no COFRE do Claude ("Network secrets" do ambiente, host graph.facebook.com, tipo Bearer).
O próprio Claude coloca a chave em cada chamada para graph.facebook.com — o robô nunca vê a chave.
  IG_USER_ID   = ID da conta do Instagram (@portalusanews), número que começa com 1784...
                 (não é segredo: pode ficar em "Environment variables" ou em robo/config.json)
  META_TOKEN   = só para teste fora do Claude (opcional)
  META_VERSAO  = opcional, versão da API (padrão v25.0)

Os arquivos precisam estar numa URL pública (ex.: raw.githubusercontent.com/...).

Uso:
  python3 publicar_meta.py foto     URL_IMAGEM            "legenda" [collab1,collab2]
  python3 publicar_meta.py carrossel URL1,URL2,URL3        "legenda" [collab1]
  python3 publicar_meta.py reels    URL_VIDEO [URL_CAPA]  "legenda" [collab1]
  python3 publicar_meta.py limite
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

TOKEN = os.environ.get("META_TOKEN", "")
IG = os.environ.get("IG_USER_ID", "")
if not IG:
    try:
        IG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))).get("ig_user_id", "")
    except Exception:
        IG = ""
VER = os.environ.get("META_VERSAO", "v25.0")
BASE = "https://graph.facebook.com/" + VER + "/"


def _req(metodo, caminho, dados=None):
    dados = dict(dados or {})
    if TOKEN:
        dados["access_token"] = TOKEN
    corpo = urllib.parse.urlencode(dados).encode()
    if metodo == "GET":
        url = BASE + caminho + "?" + corpo.decode()
        r = urllib.request.Request(url)
    else:
        r = urllib.request.Request(BASE + caminho, data=corpo, method="POST")
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        erro = e.read().decode()
        raise SystemExit("ERRO DA META: " + erro)


def _collab(lista):
    if not lista:
        return {}
    nomes = [n.strip().lstrip("@") for n in lista.split(",") if n.strip()][:3]
    return {"collaborators": json.dumps(nomes)}


def _esperar(container, limite_s=900):
    """Vídeo precisa terminar de processar antes de publicar."""
    ini = time.time()
    while time.time() - ini < limite_s:
        st = _req("GET", container, {"fields": "status_code,status"})
        cod = st.get("status_code")
        if cod == "FINISHED":
            return
        if cod in ("ERROR", "EXPIRED"):
            raise SystemExit("ERRO NO PROCESSAMENTO: " + json.dumps(st))
        time.sleep(10)
    raise SystemExit("Demorou demais para processar o vídeo.")


def _ja_publicado(legenda, horas=12):
    """Trava contra post duplicado: procura nos últimos posts um com a mesma legenda."""
    chave = " ".join((legenda or "").split())[:120]
    if not chave:
        return None
    try:
        d = _req("GET", IG + "/media", {"fields": "id,timestamp,caption,permalink", "limit": "30"})
    except SystemExit:
        return None
    agora = time.time()
    for m in d.get("data", []):
        try:
            t = time.mktime(time.strptime(m["timestamp"][:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone
        except Exception:
            t = agora
        if agora - t > horas * 3600:
            continue
        if " ".join((m.get("caption") or "").split())[:120] == chave:
            return m
    return None


INTERVALO_MIN_S = 600  # 10 min entre posts: evita o bloqueio anti-spam da Meta


def _esperar_intervalo():
    """Se o último post saiu há menos de 10 min, ESPERA (não desiste) até completar o intervalo."""
    try:
        d = _req("GET", IG + "/media", {"fields": "timestamp", "limit": "1"})
        ts = d["data"][0]["timestamp"][:19]
        t = time.mktime(time.strptime(ts, "%Y-%m-%dT%H:%M:%S")) - time.timezone
    except Exception:
        return
    falta = INTERVALO_MIN_S - (time.time() - t)
    if falta > 0:
        print(f"Aguardando {int(falta)} s para respeitar 10 min entre posts...", file=sys.stderr)
        time.sleep(falta)


def _parar_se_duplicado(legenda):
    m = _ja_publicado(legenda)
    if m:
        print(json.dumps({"ok": True, "ja_publicado": True, "media_id": m["id"], "link": m.get("permalink", "")}, ensure_ascii=False))
        raise SystemExit(0)


def _publicar(container, legenda=""):
    _parar_se_duplicado(legenda)
    _esperar_intervalo()
    ultimo = None
    for tentativa in range(5):
        try:
            r = _req("POST", IG + "/media_publish", {"creation_id": container})
            break
        except SystemExit as e:
            # A Meta às vezes devolve erro mas o post SAI. Confere antes de tentar de novo.
            ultimo = e
            time.sleep(30)
            _parar_se_duplicado(legenda)
            print(f"Erro da Meta (tentativa {tentativa + 1}/5); post não saiu, tentando de novo...", file=sys.stderr)
            time.sleep(60 * (tentativa + 1))
    else:
        raise ultimo
    mid = r["id"]
    link = _req("GET", mid, {"fields": "permalink"}).get("permalink", "")
    print(json.dumps({"ok": True, "media_id": mid, "link": link}, ensure_ascii=False))
    return mid


def foto(url, legenda, collab=""):
    _parar_se_duplicado(legenda)
    d = {"image_url": url, "caption": legenda}
    d.update(_collab(collab))
    c = _req("POST", IG + "/media", d)["id"]
    _esperar(c, 120)
    return _publicar(c, legenda)


def carrossel(urls, legenda, collab=""):
    _parar_se_duplicado(legenda)
    filhos = []
    for u in urls.split(",")[:10]:
        u = u.strip()
        if u.lower().split("?")[0].endswith((".mp4", ".mov")):
            c = _req("POST", IG + "/media", {"media_type": "VIDEO", "video_url": u, "is_carousel_item": "true"})["id"]
        else:
            c = _req("POST", IG + "/media", {"image_url": u, "is_carousel_item": "true"})["id"]
        _esperar(c)
        filhos.append(c)
    d = {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": legenda}
    d.update(_collab(collab))
    c = _req("POST", IG + "/media", d)["id"]
    _esperar(c, 300)
    return _publicar(c, legenda)


def reels(url, legenda, capa="", collab=""):
    _parar_se_duplicado(legenda)
    d = {"media_type": "REELS", "video_url": url, "caption": legenda, "share_to_feed": "true"}
    if capa:
        d["cover_url"] = capa
    d.update(_collab(collab))
    c = _req("POST", IG + "/media", d)["id"]
    _esperar(c)
    return _publicar(c, legenda)


def limite():
    r = _req("GET", IG + "/content_publishing_limit", {"fields": "quota_usage,config"})
    print(json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    if not IG:
        raise SystemExit("Falta o IG_USER_ID (variável de ambiente ou robo/config.json).")
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    tipo = a[0]
    if tipo == "foto":
        foto(a[1], a[2], a[3] if len(a) > 3 else "")
    elif tipo == "carrossel":
        carrossel(a[1], a[2], a[3] if len(a) > 3 else "")
    elif tipo == "reels":
        # reels URL_VIDEO [URL_CAPA] "legenda" [collab]
        if len(a) >= 4 and a[2].startswith("http"):
            reels(a[1], a[3], a[2], a[4] if len(a) > 4 else "")
        else:
            reels(a[1], a[2], "", a[3] if len(a) > 3 else "")
    elif tipo == "limite":
        limite()
    else:
        raise SystemExit(__doc__)
