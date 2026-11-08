"""作品集區塊（中英日西共用）。圖片在 assets/portfolio/，新人都已同意公開（Zoe 2026-11-08）。"""
FILES = ["couple-portrait-western-wedding-dress-lift", "couple-portrait-kimono-furisode-wedding",
         "couple-portrait-wedding-dress-cats-balloons", "couple-portrait-chinese-wedding-dress-dog"]
SIZES = [(607, 808), (800, 800), (800, 800), (757, 1008)]
T = {
    "zh": ("Portfolio", "似顏繪作品", "西式婚紗、和服、中式禮服都能畫，也可以把毛小孩一起畫進來。以下作品都經過新人同意公開。",
           ["西式婚紗・抱起來的瞬間", "和服振袖・並肩坐著", "婚紗＋兩隻貓（加畫寵物）", "中式褂裙＋狗狗（加畫寵物）"],
           ["新人似顏繪：西式婚紗，新郎把新娘抱起來", "新人似顏繪：新郎穿紋付羽織袴、新娘穿紅色振袖並肩坐著", "新人似顏繪：婚紗與西裝，腳邊兩隻貓和一束氣球", "新人似顏繪：中式褂裙與立領禮服，中間一隻德國牧羊犬"], "關閉"),
    "en": ("Portfolio", "Couple portraits we’ve drawn", "Wedding gowns, kimono, Chinese wedding attire, and pets too. Shared with each couple’s permission.",
           ["Wedding dress, the lift", "Kimono, side by side", "Wedding dress with two cats (pet add-on)", "Chinese wedding attire with their dog (pet add-on)"],
           ["Hand-drawn couple portrait: groom lifting the bride in her wedding dress", "Hand-drawn couple portrait: couple in kimono and a red furisode sitting side by side", "Hand-drawn couple portrait: bride and groom with two cats and balloons", "Hand-drawn couple portrait: couple in Chinese wedding attire with a German Shepherd"], "Close"),
    "ja": ("Portfolio", "似顔絵の作品", "ウェディングドレス、着物、中国式の婚礼衣装、ペットも一緒に描けます。掲載はおふたりの了承を得ています。",
           ["ウェディングドレス・抱き上げポーズ", "振袖・並んで座って", "ドレス＋猫2匹（ペット追加）", "中国式婚礼衣装＋愛犬（ペット追加）"],
           ["ふたりの似顔絵：新郎が新婦を抱き上げるウェディングドレス姿", "ふたりの似顔絵：紋付袴と赤い振袖で並んで座るふたり", "ふたりの似顔絵：ドレスとタキシード、足元に猫2匹と風船", "ふたりの似顔絵：中国式の婚礼衣装とジャーマン・シェパード"], "閉じる"),
    "es": ("Portafolio", "Retratos que hemos dibujado", "Vestidos de novia, kimono, trajes de boda chinos y también mascotas. Compartidos con permiso de cada pareja.",
           ["Vestido de novia, el abrazo", "Kimono, lado a lado", "Vestido de novia con dos gatos (mascota extra)", "Traje de boda chino con su perro (mascota extra)"],
           ["Retrato de pareja dibujado a mano: el novio levanta a la novia", "Retrato de pareja dibujado a mano: pareja en kimono y furisode rojo sentados juntos", "Retrato de pareja dibujado a mano: novios con dos gatos y globos", "Retrato de pareja dibujado a mano: pareja con traje de boda chino y un pastor alemán"], "Cerrar"),
}
CSS = """
<style>
.folio-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; align-items: start; }
.folio-grid figure { margin: 0; background: #fff; padding: 10px 10px 12px; border-radius: 10px; box-shadow: 0 24px 40px -28px rgba(90, 34, 50, .45); cursor: zoom-in; transition: transform .5s cubic-bezier(.2,.7,.1,1); }
.folio-grid figure:nth-child(odd) { transform: rotate(-1deg); } .folio-grid figure:nth-child(even) { transform: rotate(1deg) translateY(14px); }
.folio-grid figure:hover { transform: rotate(0) translateY(-6px); }
.folio-grid img { width: 100%; height: auto; border-radius: 4px; }
.folio-grid figcaption { font-size: 14px; color: var(--muted); padding-top: 8px; text-align: center; line-height: 1.5; }
dialog.folio-zoom { border: 0; padding: 0; background: transparent; max-width: min(92vw, 640px); margin: auto; }
dialog.folio-zoom::backdrop { background: rgba(40, 12, 20, .82); }
dialog.folio-zoom img { max-height: 88vh; width: auto; max-width: 100%; margin: auto; border-radius: 6px; display: block; }
dialog.folio-zoom button { position: absolute; top: 10px; right: 10px; width: 44px; height: 44px; border-radius: 50%; border: 0; background: #fff; font-size: 18px; cursor: pointer; }
@media (max-width: 860px) { .folio-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; } }
</style>"""


def section(lang, no="", prefix="/"):
    k, h2, p, caps, alts, close = T[lang]
    figs = "\n".join(
        f'        <figure class="rv" style="--i:{i}" data-src="{prefix}assets/portfolio/{f}.webp"><img src="{prefix}assets/portfolio/{f}.webp" alt="{alts[i]}" width="{w}" height="{h}" loading="lazy"><figcaption>{caps[i]}</figcaption></figure>'
        for i, (f, (w, h)) in enumerate(zip(FILES, SIZES)))
    num = f'<span class="no">{no}</span>' if no else '<span class="no">✦</span>'
    return f"""
  <section id="portfolio" style="padding-top:0">
    <div class="wrap">
      <div class="chapter">{num}<div><span class="kicker">{k}</span><h2>{h2}</h2><p>{p}</p></div></div>
      <div class="folio-grid" id="folio">
{figs}
      </div>
    </div>
  </section>
<dialog class="folio-zoom" id="folio-zoom"><img alt=""><button type="button" aria-label="{close}">✕</button></dialog>
<script>
(() => {{ try {{
  const z = document.getElementById("folio-zoom"), g = document.getElementById("folio");
  g.addEventListener("click", (e) => {{ const f = e.target.closest("figure"); if (!f) return; const im = z.querySelector("img"); im.src = f.dataset.src; im.alt = f.querySelector("img").alt; z.showModal(); }});
  z.addEventListener("click", (e) => {{ if (e.target === z || e.target.tagName === "BUTTON") z.close(); }});
}} catch (err) {{}} }})();
</script>
"""
