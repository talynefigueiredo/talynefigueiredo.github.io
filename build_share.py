"""Gera p/<id>.html para cada post (redireciona por JavaScript, não por meta refresh, para os robôs do WhatsApp lerem a imagem desta página): página leve com Open Graph (imagem, manchete e
descrição) para o link aparecer como card de notícia no WhatsApp; o visitante é levado
direto ao post no site. Uso: python3 build_share.py"""
import json, html, os
BASE = "https://talynefigueiredo.github.io"
ROT = {"favoravel": "Favorável à defesa", "desfavoravel": "Desfavorável à defesa", "neutro": "Sem impacto definido"}
d = json.load(open("posts.json", encoding="utf-8"))
os.makedirs("p", exist_ok=True)
vivos = set()
for p in d["posts"]:
    pid = p["id"]; vivos.add(pid + ".html")
    t = html.escape(p["titulo"], quote=True)
    desc = html.escape(f'{ROT.get(p.get("impacto"), "")} · {p.get("orgao", "")} · Leia a íntegra na fonte oficial.', quote=True)
    img = f'{BASE}/{p["imagem"]}' if p.get("imagem") else f"{BASE}/brand/logo-grupo-640.jpg"
    alvo = f"{BASE}/#p-{pid}"
    open(f"p/{pid}.html", "w", encoding="utf-8").write(f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>{t} · Radar Criminal</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Radar Criminal">
<meta property="og:title" content="{t}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}"><meta property="og:image:width" content="600"><meta property="og:image:height" content="338">
<meta property="og:url" content="{BASE}/p/{pid}.html"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{BASE}/p/{pid}.html"><script>location.replace("{alvo}")</script>
</head><body><p><a href="{alvo}">{t}</a></p></body></html>''')
for f in os.listdir("p"):
    if f not in vivos: os.remove(os.path.join("p", f))
print(len(vivos), "páginas de compartilhamento")
