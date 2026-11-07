/* Arte para Story do Instagram (1080x1920) no visual do Radar Criminal.
   Uso: RadarStory.abrir({ kicker, tribunal, orgao, impacto, titulo, processo, imagem, chamada }) */
(() => {
  const W = 1080, H = 1920;
  const C = { bg: "#F3F1EE", card: "#FFFFFF", ink: "#1D1D1F", muted: "#6E6E73", hair: "#E6E3DF", wine: "#6B2430", gold: "#A27A3E",
    favor: "#1B7F4B", favorBg: "#E7F4EC", contra: "#C0392B", contraBg: "#FBEAE7" };
  const ROT = { favoravel: "Favorável à defesa", desfavoravel: "Desfavorável à defesa", neutro: "Informativo" };
  const F = '"Figtree", -apple-system, "Segoe UI", Roboto, Arial, sans-serif';
  const S = '"Source Serif 4", Georgia, serif';

  const img = src => new Promise(ok => { if (!src) return ok(null); const i = new Image(); i.onload = () => ok(i); i.onerror = () => ok(null); i.src = src; });
  function rr(x, y, w, h, r, ctx) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function linhas(ctx, txt, max, limite) {
    const out = []; let l = "";
    for (const p of String(txt || "").split(/\s+/)) { const t = l ? l + " " + p : p; if (ctx.measureText(t).width > max && l) { out.push(l); l = p; } else l = t; }
    if (l) out.push(l);
    if (out.length > limite) { out.length = limite; let u = out[limite - 1]; while (ctx.measureText(u + "…").width > max && u.includes(" ")) u = u.slice(0, u.lastIndexOf(" ")); out[limite - 1] = u + "…"; }
    return out;
  }

  async function desenhar(d) {
    try { await Promise.all(["800 66px Figtree", "700 40px Figtree", "500 30px Figtree", "600 34px 'Source Serif 4'"].map(f => document.fonts.load(f))); } catch (e) {}
    const [logo, capa] = await Promise.all([img(d.logo || "logo-mark.png"), img(d.imagem)]);
    const cv = document.createElement("canvas"); cv.width = W; cv.height = H;
    const ctx = cv.getContext("2d");
    ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);

    // topo: marca
    let y = 110;
    if (logo) { const lh = 64, lw = logo.width * lh / logo.height; ctx.drawImage(logo, 80, y - 50, lw, lh); ctx.font = `700 46px ${F}`; ctx.fillStyle = C.ink; ctx.fillText("Radar Criminal", 80 + lw + 22, y); }
    else { ctx.font = `700 46px ${F}`; ctx.fillStyle = C.ink; ctx.fillText("Radar Criminal", 80, y); }

    // medidas (o cartão se ajusta ao conteúdo)
    const cx = 64, cw = W - 128, px = cx + 64, pw = cw - 128;
    const ih = capa ? Math.round(cw * 9 / 16) : 300;
    const tf = capa ? 64 : 74, tlh = Math.round(tf * 1.25);
    ctx.font = `800 ${tf}px ${F}`; const tl = linhas(ctx, d.titulo, pw, capa ? 6 : 8);
    ctx.font = `500 30px ${F}`; const pl = d.processo ? linhas(ctx, d.processo, pw, capa ? 2 : 5) : [];
    const temSelo = !!(d.impacto && ROT[d.impacto]);
    const ch = ih + 70 + (temSelo ? 92 : 0) + (temSelo ? 64 : 96) + tl.length * tlh + (pl.length ? 30 + pl.length * 44 : 0) + 60;
    const cy = Math.max(170, Math.round(170 + (1450 - ch) / 2));

    ctx.save(); ctx.shadowColor = "rgba(0,0,0,0.08)"; ctx.shadowBlur = 40; ctx.shadowOffsetY = 12; rr(cx, cy, cw, ch, 44, ctx); ctx.fillStyle = C.card; ctx.fill(); ctx.restore();
    ctx.save(); rr(cx, cy, cw, ch, 44, ctx); ctx.clip();
    if (capa) {
      const r = Math.max(cw / capa.width, ih / capa.height), sw = cw / r, sh = ih / r;
      ctx.drawImage(capa, (capa.width - sw) / 2, (capa.height - sh) / 2, sw, sh, cx, cy, cw, ih);
    } else {
      const g = ctx.createLinearGradient(cx, cy, cx + cw, cy + ih); g.addColorStop(0, C.wine); g.addColorStop(1, "#3E1219");
      ctx.fillStyle = g; ctx.fillRect(cx, cy, cw, ih);
      ctx.fillStyle = "rgba(255,255,255,0.92)"; ctx.font = `italic 600 64px ${S}`; ctx.fillText(d.kicker || "Artigo", cx + 64, cy + ih - 80);
    }
    ctx.restore();

    y = cy + ih + 70;
    ctx.font = `700 34px ${F}`; ctx.fillStyle = C.wine;
    const meta = [d.tribunal, d.orgao].filter(Boolean).join(" · ") || "Artigo do Radar Criminal";
    ctx.fillText(linhas(ctx, meta, pw, 1)[0] || "", px, y);
    if (temSelo) {
      y += 34; ctx.font = `700 30px ${F}`; const t = ROT[d.impacto], tw = ctx.measureText(t).width;
      const bg = d.impacto === "favoravel" ? C.favorBg : d.impacto === "desfavoravel" ? C.contraBg : "#EFEDEA";
      const fg = d.impacto === "favoravel" ? C.favor : d.impacto === "desfavoravel" ? C.contra : C.muted;
      rr(px, y, tw + 48, 58, 29, ctx); ctx.fillStyle = bg; ctx.fill(); ctx.fillStyle = fg; ctx.fillText(t, px + 24, y + 40); y += 58;
    }
    y += temSelo ? 64 : 96; ctx.font = `800 ${tf}px ${F}`; ctx.fillStyle = C.ink;
    tl.forEach((l, i) => ctx.fillText(l, px, y + i * tlh)); y += (tl.length - 1) * tlh;
    if (pl.length) { y += 30 + 44; ctx.font = `500 30px ${F}`; ctx.fillStyle = C.muted; pl.forEach((l, i) => ctx.fillText(l, px, y + i * 44)); }

    // chamada
    const by = H - 220;
    ctx.font = `500 34px ${F}`; ctx.fillStyle = C.muted; ctx.textAlign = "center";
    ctx.fillText(d.chamada || "Leia a ementa e a fonte oficial em", W / 2, by);
    ctx.font = `800 46px ${F}`; ctx.fillStyle = C.wine; ctx.fillText("talynefigueiredo.github.io", W / 2, by + 64);
    ctx.font = `500 26px ${F}`; ctx.fillStyle = C.muted; ctx.fillText("Conteúdo informativo. Não é consultoria jurídica.", W / 2, H - 70);
    ctx.textAlign = "left";
    return cv;
  }

  function modal() {
    let m = document.getElementById("storyModal");
    if (m) return m;
    m = document.createElement("div"); m.id = "storyModal"; m.className = "story-modal"; m.hidden = true;
    m.innerHTML = `<div class="sm-box" role="dialog" aria-modal="true" aria-labelledby="smT">
      <button class="sm-x" type="button" aria-label="Fechar">×</button>
      <h3 id="smT">Compartilhar no Story</h3>
      <div class="sm-prev"><img alt="Prévia da arte para o Story"></div>
      <div class="sm-acts"><button class="sm-share" type="button">Compartilhar no Instagram</button><a class="sm-dl" download="radar-criminal-story.png">Baixar imagem</a></div>
      <p class="sm-tip">No celular, toque em <b>Compartilhar no Instagram</b> e escolha <b>Instagram › Story</b>. No computador, baixe a imagem e publique pelo app.</p>
    </div>`;
    document.body.appendChild(m);
    const fechar = () => { m.hidden = true; document.body.style.overflow = ""; };
    m.addEventListener("click", e => { if (e.target === m || e.target.closest(".sm-x")) fechar(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && !m.hidden) fechar(); });
    return m;
  }

  async function abrir(d) {
    const m = modal(), im = m.querySelector(".sm-prev img"), dl = m.querySelector(".sm-dl"), sh = m.querySelector(".sm-share"), tip = m.querySelector(".sm-tip");
    im.removeAttribute("src"); m.hidden = false; document.body.style.overflow = "hidden"; sh.disabled = true; sh.textContent = "Gerando arte…";
    const cv = await desenhar(d);
    const blob = await new Promise(ok => cv.toBlob(ok, "image/png"));
    const url = URL.createObjectURL(blob); im.src = url; dl.href = url;
    const file = new File([blob], "radar-criminal-story.png", { type: "image/png" });
    const pode = !!(navigator.canShare && navigator.canShare({ files: [file] }));
    sh.hidden = !pode; sh.disabled = false; sh.textContent = "Compartilhar no Instagram";
    tip.hidden = false;
    sh.onclick = async () => { try { await navigator.share({ files: [file] }); } catch (e) { if (e && e.name !== "AbortError") dl.click(); } };
  }

  window.RadarStory = { abrir, desenhar };
})();
