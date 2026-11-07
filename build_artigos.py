"""Gera artigos/<id>.html a partir de artigos.json (mesmo visual do site, com Open Graph e botão de Story).
Uso: python3 build_artigos.py"""
import json, html, os

BASE = "https://talynefigueiredo.github.io"
e = lambda s: html.escape(str(s or ""), quote=True)
posts = {p["id"]: p for p in json.load(open("posts.json", encoding="utf-8"))["posts"]}
dados = json.load(open("artigos.json", encoding="utf-8"))
os.makedirs("artigos", exist_ok=True)

CSS = """
:root{--bg:#FBFBFD;--bg-alt:#F3F1EE;--card:#fff;--ink:#1D1D1F;--muted:#6E6E73;--hair:#E6E3DF;--wine:#6B2430;--gold:#A27A3E;--favor:#1B7F4B;--favor-bg:#E7F4EC;--contra:#C0392B;--contra-bg:#FBEAE7;
--font:"Figtree",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;--font-text:"Source Serif 4",Georgia,serif;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--wine);text-underline-offset:3px}.wrap{max-width:760px;margin:0 auto;padding:0 20px}
.nav{position:sticky;top:0;z-index:30;background:rgba(251,251,253,.85);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.06)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;height:58px;max-width:1080px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700}.brand img{height:28px;width:auto}
.nav a.back{font-size:14.5px;font-weight:600;text-decoration:none}
header.art{padding:48px 0 8px}.k{font-size:13px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:.06em}
h1{font-size:clamp(30px,5vw,44px);line-height:1.15;letter-spacing:-.02em;margin:10px 0 14px;text-wrap:balance}
.sub{font-size:19px;color:var(--muted);margin:0 0 14px}.info{font-size:14.5px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}
.acts{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 8px}
.act{border:none;background:#F2F0ED;font-weight:600;font-size:14px;padding:8px 14px;border-radius:999px;cursor:pointer;text-decoration:none;color:var(--ink);display:inline-flex;align-items:center;gap:6px;font-family:inherit}
.act.zap{background:#E7F7EE;color:#11804A}.act.ig{background:linear-gradient(135deg,#FDE9E4,#F6E3F0);color:#8A2A5B}
article{font-family:var(--font-text);font-size:19px;line-height:1.7;padding:12px 0 24px}
article h2{font-family:var(--font);font-size:24px;letter-spacing:-.015em;margin:38px 0 10px;line-height:1.25}
article p{margin:0 0 18px}article ul{margin:0 0 20px;padding-left:22px}article li{margin:0 0 10px}
blockquote{margin:22px 0;padding:18px 22px;background:var(--card);border-left:4px solid var(--wine);border-radius:0 16px 16px 0;box-shadow:0 1px 2px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.04)}
blockquote p{margin:0 0 10px;white-space:pre-line}blockquote cite{display:block;font-family:var(--font);font-style:normal;font-size:14px;color:var(--muted)}
h2.fav{color:var(--favor)}h2.des{color:var(--contra)}
.rel{background:var(--bg-alt);padding:40px 0 56px;margin-top:24px}.rel h2{font-size:22px;margin:0 0 16px}
.rel a.c{display:block;background:var(--card);border-radius:18px;padding:16px 18px;margin:0 0 10px;text-decoration:none;color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.04)}
.rel a.c small{display:block;color:var(--muted);font-size:13.5px;margin-bottom:2px}.rel a.c b{font-weight:700;line-height:1.35}
.b{font-size:12px;font-weight:700;padding:2px 9px;border-radius:999px;margin-left:6px}.b.favoravel{background:var(--favor-bg);color:var(--favor)}.b.desfavoravel{background:var(--contra-bg);color:var(--contra)}.b.neutro{background:#EFEDEA;color:var(--muted)}
footer{padding:30px 0 50px;font-size:13.5px;color:var(--muted)}footer p{margin:0 0 8px}
.story-modal{position:fixed;inset:0;z-index:60;background:rgba(20,16,17,.55);display:flex;align-items:center;justify-content:center;padding:16px}.story-modal[hidden]{display:none}
.sm-box{position:relative;background:#fff;border-radius:22px;padding:22px 22px 18px;width:min(420px,100%);max-height:calc(100vh - 32px);overflow:auto;text-align:center;font-family:var(--font)}
.sm-box h3{font-size:19px;margin:0 0 14px}.sm-x{position:absolute;top:10px;right:12px;border:none;background:none;font-size:28px;line-height:1;cursor:pointer;color:var(--muted)}
.sm-prev{background:#F3F1EE;border-radius:14px;aspect-ratio:9/16;max-height:56vh;margin:0 auto 16px;overflow:hidden;display:flex;align-items:center;justify-content:center}.sm-prev img{height:100%;width:auto}
.sm-acts{display:flex;flex-direction:column;gap:10px}.sm-share,.sm-dl{border:none;border-radius:999px;padding:13px 18px;font-weight:700;font-size:16px;cursor:pointer;text-decoration:none;font-family:inherit}
.sm-share{background:linear-gradient(90deg,#F58529,#DD2A7B 55%,#8134AF);color:#fff}.sm-share[hidden]{display:none}.sm-dl{background:#F2F0ED;color:var(--ink)}.sm-tip{font-size:13.5px;color:var(--muted);margin:12px 0 0;line-height:1.45}
@media (max-width:640px){article{font-size:18px}header.art{padding-top:32px}}
"""

ROT = {"favoravel": "Favorável", "desfavoravel": "Desfavorável", "neutro": "Informativo"}

def bloco(b):
    if "h" in b:
        t = b["h"]; cls = ' class="fav"' if "favorece" in t else (' class="des"' if "desfavorece" in t else "")
        return f"<h2{cls}>{e(t)}</h2>"
    if "p" in b:  # texto próprio; aceita <b>
        return f"<p>{b['p']}</p>"
    if "ul" in b:
        return "<ul>" + "".join(f"<li>{i}</li>" for i in b["ul"]) + "</ul>"
    if "quote" in b:
        return f'<blockquote><p>{e(b["quote"])}</p><cite><a href="{e(b["url"])}" target="_blank" rel="noopener">{e(b["fonte"])} ↗</a></cite></blockquote>'
    return ""

def data_br(iso):
    a, m, d = iso.split("-"); return f"{int(d)}/{int(m)}/{a}"

vivos = set()
for a in dados["artigos"]:
    aid = a["id"]; vivos.add(aid + ".html"); url = f"{BASE}/artigos/{aid}.html"
    rel = "".join(
        f'<a class="c" href="../#p-{e(p["id"])}"><small>{e(p["tribunal"])} · {e(p["orgao"])}<span class="b {e(p["impacto"])}">{ROT.get(p["impacto"], "")}</span></small><b>{e(p["titulo"])}</b></a>'
        for p in (posts.get(i) for i in a.get("decisoes", [])) if p)
    zap = "https://api.whatsapp.com/send?text=" + html.escape(__import__("urllib.parse").parse.quote(f"*{a['titulo']}*\n{url}"), quote=True)
    story = json.dumps({"kicker": a["area"], "titulo": a["titulo"], "processo": a["resumo"], "chamada": "Leia o artigo completo em", "logo": "../logo-mark.png"}, ensure_ascii=False)
    doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(a["titulo"])} · Radar Criminal</title>
<meta name="description" content="{e(a["resumo"])}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Radar Criminal">
<meta property="og:title" content="{e(a["titulo"])}"><meta property="og:description" content="{e(a["resumo"])}">
<meta property="og:image" content="{BASE}/brand/logo-grupo-640.jpg"><meta property="og:url" content="{url}">
<link rel="canonical" href="{url}"><link rel="icon" href="../brand/logo-grupo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script src="../story.js" defer></script>
</head><body>
<header class="nav"><div class="wrap"><a class="brand" href="../"><img src="../logo-mark.png" alt="" width="54" height="28">Radar Criminal</a><a class="back" href="../#artigos">‹ Todos os artigos</a></div></header>
<div class="wrap">
<header class="art"><span class="k">{e(a["area"])}</span><h1>{e(a["titulo"])}</h1><p class="sub">{e(a["resumo"])}</p>
<div class="info"><span>Por Talyne Figueiredo</span><span>·</span><span>{data_br(a["data"])}</span><span>·</span><span>{e(a.get("leitura", ""))} de leitura</span></div>
<div class="acts"><a class="act zap" href="{zap}" target="_blank" rel="noopener">WhatsApp</a><button class="act" type="button" id="cp">Copiar link</button><button class="act ig" type="button" id="st">Story</button></div></header>
<article>{"".join(bloco(b) for b in a["blocos"])}</article>
</div>
{f'<section class="rel"><div class="wrap"><h2>Decisões citadas no Radar</h2>{rel}</div></section>' if rel else ""}
<footer><div class="wrap"><p>Conteúdo informativo e educacional; não constitui consultoria jurídica. As ementas citadas são reproduzidas das fontes oficiais indicadas; leia sempre o inteiro teor antes de citar.</p><p><a href="../">Radar Criminal</a> · <a href="https://t.me/radarcriminal" target="_blank" rel="noopener">Canal no Telegram</a> · <a href="https://chat.whatsapp.com/HPqADdmWNigGoGLBU06pu4" target="_blank" rel="noopener">Grupo no WhatsApp</a></p></div></footer>
<script>
const ST = {story};
document.getElementById("st").onclick = () => window.RadarStory && RadarStory.abrir(ST);
document.getElementById("cp").onclick = async e => {{ try {{ await navigator.clipboard.writeText("{url}"); e.target.textContent = "Link copiado"; }} catch (x) {{ e.target.textContent = "{url}"; }} }};
</script>
</body></html>"""
    open(f"artigos/{aid}.html", "w", encoding="utf-8").write(doc)

for f in os.listdir("artigos"):
    if f.endswith(".html") and f not in vivos: os.remove(os.path.join("artigos", f))
print(len(vivos), "artigos gerados")
