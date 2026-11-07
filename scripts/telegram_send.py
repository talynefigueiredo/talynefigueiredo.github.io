"""Envia ao canal do Telegram as decisões novas do posts.json (uma mensagem com foto por decisão).
Roda no GitHub Actions. Precisa de TELEGRAM_BOT_TOKEN (secret) e TELEGRAM_CHAT_ID (variável, ex.: @radarcriminal).
Controle do que já foi enviado: telegram-enviados.json."""
import json, os, sys, time, html, urllib.request, urllib.parse, uuid

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
BASE = "https://talynefigueiredo.github.io"
MAX = 6
EMO = {"favoravel": "🟢 Favorável à defesa", "desfavoravel": "🔴 Desfavorável à defesa", "neutro": "⚪ Sem impacto definido"}

if not TOKEN or not CHAT:
    print("TELEGRAM_BOT_TOKEN ou TELEGRAM_CHAT_ID não configurados; nada a fazer."); sys.exit(0)

posts = json.load(open("posts.json", encoding="utf-8"))["posts"]
ctl_path = "telegram-enviados.json"
ctl = json.load(open(ctl_path, encoding="utf-8")) if os.path.exists(ctl_path) else {"enviados": []}
feitos = set(ctl["enviados"])
novos = [p for p in posts if p["id"] not in feitos]
novos.sort(key=lambda p: p["data"])  # do mais antigo para o mais recente
pular = novos[:-MAX] if len(novos) > MAX else []
novos = novos[-MAX:]

def api(metodo, campos, arquivo=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{metodo}"
    if arquivo:
        b = uuid.uuid4().hex
        corpo = b""
        for k, v in campos.items():
            corpo += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        nome, dados = arquivo
        corpo += f'--{b}\r\nContent-Disposition: form-data; name="photo"; filename="{nome}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode() + dados + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request(url, data=corpo, headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(campos).encode())
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    if not res.get("ok"):
        raise RuntimeError(res)
    return res

enviados = []
for p in novos:
    titulo = html.escape(p["titulo"])
    legenda = (f"<b>{titulo}</b>\n\n{EMO.get(p.get('impacto'), '')} · {html.escape(p['tribunal'])} – {html.escape(p.get('orgao', ''))}\n\n"
               f"📄 <a href=\"{BASE}/p/{p['id']}.html\">Ler a ementa no Radar Criminal</a>\n"
               f"🏛️ <a href=\"{html.escape(p['fonteUrl'])}\">Fonte oficial</a>\n\n"
               f"<i>Conteúdo informativo. Imagem ilustrativa (IA).</i>")
    campos = {"chat_id": CHAT, "caption": legenda, "parse_mode": "HTML"}
    img = p.get("imagem")
    try:
        if img and os.path.exists(img):
            api("sendPhoto", campos, (os.path.basename(img), open(img, "rb").read()))
        else:
            api("sendMessage", {"chat_id": CHAT, "text": legenda, "parse_mode": "HTML", "disable_web_page_preview": "false"})
        enviados.append(p["id"]); print("enviado:", p["id"])
    except Exception as e:
        print("falhou:", p["id"], e); break
    time.sleep(3)

ctl["enviados"] = list(feitos | set(enviados) | {p["id"] for p in pular})
ctl["atualizadoEm"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
json.dump(ctl, open(ctl_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(enviados)} enviados; {len(pular)} antigos marcados sem envio.")
if novos and not enviados: sys.exit(1)
