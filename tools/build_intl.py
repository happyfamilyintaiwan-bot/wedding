"""產生海外版介紹頁（/en/、/ja/、/es/）。
版面與 CSS 沿用中文版 index.html（提案 1），文字與價格在 intl_strings.py。
用法：python3 tools/build_intl.py          → 輸出到 _proposals/intl/<lang>/（本機預覽）
      python3 tools/build_intl.py --live   → 輸出到 <lang>/（上線用）
"""
import json, os, re, sys
from intl_strings import S, PRICES, MAIL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "--live" in sys.argv
BASE = "https://wedding.knittinghiyori.com"
LANGS = ["en", "ja", "es"]
LANG_NAMES = [("zh", "中文", "/"), ("en", "EN", "/en/"), ("ja", "日本語", "/ja/"), ("es", "ES", "/es/")]


class Keep(dict):
    """沒有對應的 {name} 這類欄位保留原樣（給 JS 之後替換）"""
    def __missing__(self, k):
        return "{" + k + "}"


def fmt(x):
    if isinstance(x, str):
        return x.format_map(Keep(mail=MAIL, **PRICES))
    if isinstance(x, (list, tuple)):
        return type(x)(fmt(i) for i in x)
    return x


def strip_tags(h):
    return re.sub(r"<[^>]+>", "", h)


zh = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
STYLE = re.search(r"<style>.*?</style>", zh, re.S).group(0)
TRACK = zh[zh.index("<script>\n/* 點擊追蹤"):zh.index("</body>")]

EXTRA_CSS = """
<style>
:root { --serif: SERIF; --sans: SANS; }
.langs { display: flex; gap: 4px; font-size: 13px; }
.nav .langs a { display: inline-block !important; }
.langs a { text-decoration: none; padding: 4px 8px; border-radius: 999px; color: var(--muted); }
.langs a[aria-current] { background: var(--blush); color: var(--wine); font-weight: 700; }
.pay-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
.pay-card { background: var(--cream); border: 1px solid var(--wine); border-radius: 22px; padding: 28px 30px; }
.pay-card h3 { font-family: var(--latin); font-size: 30px; color: var(--wine); font-weight: 500; }
.pay-card p { color: var(--muted); margin-top: 8px; }
.sample-note { text-align: center; color: var(--muted); font-size: 14px; margin-top: 70px; }
.hero h1 { letter-spacing: .02em; }
@media (max-width: 760px) { .pay-grid { grid-template-columns: 1fr; } .langs a { padding: 4px 6px; } }
@media (max-width: 420px) { .top .pill { display: none; } }
@media (max-width: 600px) { .row { grid-template-columns: 1fr; gap: 6px; } .row h3 { flex-wrap: wrap; row-gap: 4px; } .row .p { font-size: 32px; } .row .p s { font-size: .55em; color: var(--muted); } }
</style>"""

JS = r"""
<script>
(() => {
  const T = __T__, P = __P__;
  const $ = (id) => document.getElementById(id);
  const usd = (n) => "US$" + n.toLocaleString("en-US");
  const val = (id) => ($(id) ? $(id).value.trim() : "");
  const pick = (name) => (document.querySelector(`input[name=${name}]:checked`) || {}).value || "";
  let pets = 0, months = 0;
  function update() {
    const pkg = pick("pkg");
    $("style-more").hidden = pkg !== "bundle";
    const items = [[pkg === "bundle" ? T.ln_bundle : T.ln_portrait, pkg === "bundle" ? P.bundle_launch : P.portrait]];
    if (pets) items.push([`${T.ln_pet} ×${pets}`, pets * P.pet]);
    if (pkg === "bundle" && months) items.push([`${T.ln_month} ×${months}`, months * P.month]);
    const days = val("need") ? Math.ceil((new Date(val("need")) - new Date()) / 864e5) : 99;
    const rush = days < 28, base = items.reduce((a, [, p]) => a + p, 0);
    if (rush) items.push([`${T.ln_rush} (${P.rush_pct}%)`, Math.round(base * P.rush_pct / 100)]);
    const total = items.reduce((a, [, p]) => a + p, 0);
    $("sum").textContent = usd(total);
    $("lines").innerHTML = items.map(([n, p]) => `<li><span>${n}</span><span>${usd(p)}</span></li>`).join("");
    $("rush-note").textContent = rush ? T.q_rush_on : T.q_rush;
    const u = (s) => s || T.m_unset;
    const L = [T.m_head, "", `${T.m_name}: ${u(val("who"))}`, `${T.m_mail}: ${u(val("mail"))}`, `${T.m_names}: ${u(val("n1"))} & ${u(val("n2"))}`,
      `${T.m_country}: ${u(val("country"))}`, `${T.m_wd}: ${u(val("wd"))}`, `${T.m_need}: ${u(val("need"))}`, "", T.m_items];
    items.forEach(([n, p]) => L.push(`✔ ${n}  ${usd(p)}`));
    if (pkg === "bundle") L.push(`${T.m_style}: ${pick("style")}`);
    L.push(`${T.m_pay}: ${pick("pay")}`, "", `${T.m_total}: ${usd(total)}`, "");
    if (val("memo")) L.push(`${T.m_memo}: ${val("memo")}`, "");
    L.push(T.m_photo, "", T.m_agree);
    const text = L.join("\n");
    $("msg").value = text;
    const subject = T.m_subject.replace("{name}", u(val("who"))).replace("{date}", u(val("wd"))).replace("{total}", usd(total));
    $("mailto").href = `mailto:${T.mail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(text)}`;
  }
  document.querySelectorAll("[data-step]").forEach((b) => b.addEventListener("click", () => {
    const k = b.dataset.k, d = +b.dataset.step;
    if (k === "pets") { pets = Math.max(0, Math.min(6, pets + d)); $("pets").textContent = pets; }
    else { months = Math.max(0, Math.min(12, months + d)); $("months").textContent = months; }
    update();
  }));
  $("q").addEventListener("input", update); $("q").addEventListener("change", update);
  $("copy").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText($("msg").value); } catch { $("msg").select(); document.execCommand("copy"); }
    $("copied").hidden = false; setTimeout(() => { $("copied").hidden = true; }, 1800);
  });
  update();
  if (new URLSearchParams(location.search).has("still")) document.documentElement.classList.add("still");
  document.querySelectorAll("[data-split]").forEach((el) => {
    const walk = (node) => [...node.childNodes].forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        (n.textContent.match(/[A-Za-zÀ-ÿ’'.,¿?¡!]+|\s+|./gu) || []).forEach((ch) => {
          if (/^\s+$/.test(ch)) { frag.appendChild(document.createTextNode(" ")); return; }
          const w = document.createElement("span"); w.className = "w"; const s = document.createElement("span"); s.textContent = ch; w.appendChild(s); frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else walk(n);
    });
    walk(el); el.querySelectorAll(".w > span").forEach((s, i) => s.style.setProperty("--i", i));
  });
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: .12 });
  document.querySelectorAll(".rv, [data-split]").forEach((el) => io.observe(el));
  const fit = () => document.querySelectorAll(".device iframe").forEach((f) => { const w = f.parentElement.clientWidth; f.style.transform = `scale(${w / 375})`; f.style.height = `${f.parentElement.clientHeight / (w / 375)}px`; });
  const lio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.src = e.target.dataset.src; lio.unobserve(e.target); } }), { rootMargin: "300px" });
  document.querySelectorAll(".device iframe").forEach((f) => lio.observe(f));
  fit(); addEventListener("resize", fit);
})();
</script>
"""


CUR = ' aria-current="page"'


def build(lang):
    t = {k: fmt(v) for k, v in S[lang].items()}
    url = f"{BASE}/{lang}/"
    alts = "\n".join(f'<link rel="alternate" hreflang="{"zh-Hant" if c == "zh" else c}" href="{BASE}{p}">' for c, _, p in LANG_NAMES) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}/">'
    faq_ld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": t["og_title"], "description": t["desc"], "url": url, "areaServed": "Worldwide",
         "provider": {"@type": "Organization", "name": "編織日和 Knitting Hiyori", "url": "https://knittinghiyori.com/", "email": MAIL},
         "offers": [
             {"@type": "Offer", "name": strip_tags(t["rows"][0][1]), "price": str(PRICES["bundle_launch"]), "priceCurrency": "USD"},
             {"@type": "Offer", "name": strip_tags(t["rows"][1][1]), "price": str(PRICES["portrait"]), "priceCurrency": "USD"},
             {"@type": "Offer", "name": strip_tags(t["rows"][2][1]), "price": str(PRICES["pet"]), "priceCurrency": "USD"}]},
        {"@type": "FAQPage", "mainEntity": faq_ld}]}
    langs = "".join(f'<a href="{p}" hreflang="{"zh-Hant" if c == "zh" else c}"{CUR if c == lang else ""} data-cta="lang_switch" data-cta-type="wedding">{n}</a>' for c, n, p in LANG_NAMES)
    rows = "\n".join(f'        <div class="row rv"><span class="n">{n}</span><h3>{h}<small>{sm}</small></h3><span class="p">{p}</span><p>{d}</p></div>' for n, h, sm, p, d in t["rows"])
    ticks = "".join(f"<li>{a}<b>{b}</b></li>" for a, b in t["ticks"])
    phones = "\n".join(f'        <article class="ph rv" style="--i:{i}"><div class="device"><div class="screen"><iframe data-src="/{k.lower()}/?embed&lang={lang}" title="{k} {h}" loading="lazy" tabindex="-1"></iframe></div></div><h3><span>{k}</span>{h}</h3><p>{d}</p><a href="/{k.lower()}/?lang={lang}" target="_blank" rel="noopener" data-cta="style_{k.lower()}" data-cta-type="wedding">{t["see"]}</a></article>' for i, (k, h, d) in enumerate(t["styles"]))
    steps = "\n".join(f'        <li class="rv" style="--i:{i}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(t["steps"]))
    pays = "".join(f'<article class="pay-card rv" style="--i:{i}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(t["pay"]))
    faq = "\n".join(f"        <details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
    marquee = "".join(f"{t['marquee'][i]}<i>{t['marquee'][i + 1]}</i>" for i in range(0, len(t["marquee"]), 2))
    styles_radio = "".join(f'<label><input type="radio" name="style" value="{k} {h}"{" checked" if k == "A" else ""}><span>{k}・{h}</span></label>' for k, h, _ in t["styles"])
    js_t = {k: t[k] for k in ["ln_bundle", "ln_portrait", "ln_pet", "ln_month", "ln_rush", "q_rush", "q_rush_on", "m_head", "m_name", "m_mail", "m_names", "m_country", "m_wd", "m_need", "m_items", "m_style", "m_color", "m_total", "m_memo", "m_photo", "m_agree", "m_subject", "m_unset", "m_pay"]}
    js_t["mail"] = MAIL
    js = JS.replace("__T__", json.dumps(js_t, ensure_ascii=False)).replace("__P__", json.dumps(PRICES))
    robots = "noindex, nofollow" if not LIVE else "index, follow, max-image-preview:large"
    html = f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url}">
{alts}
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Knitting Hiyori">
<meta property="og:title" content="{t['og_title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/og.jpg">
<link rel="icon" href="/icons/favicon.ico?v=2" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png?v=2">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t['fonts']}&display=swap" rel="stylesheet">
{STYLE}{EXTRA_CSS.replace('SERIF', t['serif']).replace('SANS', t['sans'])}
<!-- wedding 子網域：不放 Travelpayouts、不放 Google 廣告（core §1） -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZQZHTYTRMQ"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag("js",new Date());
gtag("set",{{content_group:"wedding",page_lang:"{t['page_lang']}",page_title:"喜帖|似顏繪喜帖|結婚書約與電子喜帖報價"}});
gtag("config","G-ZQZHTYTRMQ",/[?]hy_debug=1/.test(location.search)?{{cookie_domain:".knittinghiyori.com",debug_mode:true}}:{{cookie_domain:".knittinghiyori.com"}});
</script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<meta name="spec-version" content="core-v1.9">
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="kh-brand" href="{url}" data-google-vignette="false" data-cta="brand_hub" data-cta-type="wedding"><img src="/icons/logo-knitting-120.webp" width="40" height="40" alt="">Knitting Hiyori<span class="site"> · {t['site']}</span></a>
    <nav class="nav" aria-label="{t['lang_label']}"><a href="#menu">{t['nav'][0]}</a><a href="#web">{t['nav'][1]}</a><a href="#pay">{t['nav'][2]}</a><a href="#faq">{t['nav'][3]}</a><span class="langs">{langs}</span><a class="pill" href="#quote" data-cta="hero_quote" data-cta-type="wedding">{t['nav_cta']} <span class="arr">→</span></a></nav>
  </div>
</header>

<main>
  <section class="hero wrap" style="padding-top:28px">
    <div class="l"><p class="big split" data-split>Drawn</p></div>
    <div class="arch-wrap" style="position:relative">
      <div class="arch rv" style="--i:2"><span class="sun"></span><img src="/assets/couple-kimono.webp" alt="{strip_tags(t['og_title'])}" width="766" height="1500"></div>
      <svg class="badge" viewBox="0 0 132 132" aria-hidden="true"><defs><path id="circ" d="M66 66m-50 0a50 50 0 1 1 100 0a50 50 0 1 1 -100 0"/></defs><circle class="core" cx="66" cy="66" r="5"/><text><textPath href="#circ">Illustrated Wedding · Knitting Hiyori ·</textPath></text></svg>
    </div>
    <div class="r"><p class="big split" data-split><em>in love</em></p></div>
    <span class="vert">{t['vert']}</span>
    <div class="hero-copy">
      <h1 class="rv" style="--i:3">{t['h1']}</h1>
      <div class="meta rv" style="--i:4">
        <p>{t['lead']}</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="pill" href="#quote" data-cta="hero_quote" data-cta-type="wedding">{t['cta1']} <span class="arr">→</span></a><a class="pill ghost" href="#menu" data-cta="hero_price" data-cta-type="wedding">{t['cta2']}</a></div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true"><div class="track"><span>{marquee}</span><span>{marquee}</span></div></div>

  <section id="menu">
    <div class="wrap">
      <div class="chapter"><span class="no">01</span><div><span class="kicker">{t['menu_kicker']}</span><h2 class="split" data-split>{t['menu_h2']}</h2><p>{t['menu_p']}</p></div></div>
      <div class="menu">
{rows}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap duo">
      <div class="frame rv"><img src="/assets/couple-kimono.webp" alt="" width="766" height="1500" loading="lazy"></div>
      <div class="rv" style="--i:1">
        <span class="kicker">{t['duo_kicker']}</span>
        <p class="quote-big" style="margin-top:14px">{t['duo_say']}</p>
        <ul class="ticks">{ticks}</ul>
      </div>
    </div>
  </section>

  <section id="web" style="background:var(--blush)">
    <div class="wrap">
      <div class="chapter"><span class="no">02</span><div><span class="kicker">{t['web_kicker']}</span><h2 class="split" data-split>{t['web_h2']}</h2><p>{t['web_p']}</p></div></div>
      <div class="phones">
{phones}
      </div>
      <div class="web-foot rv" style="margin-top:40px">
        <div><span class="kicker">{t['web_price_k']}</span><p class="p">US${PRICES['bundle_launch']}</p></div>
        <ul>{''.join(f'<li>{r}</li>' for r in t['web_rules'])}</ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="chapter"><span class="no">03</span><div><span class="kicker">{t['how_kicker']}</span><h2 class="split" data-split>{t['how_h2']}</h2><p>{t['how_p']}</p></div></div>
      <ol class="flow">
{steps}
      </ol>
      <div class="promise rv">
        <div><h3>{t['rush_h']}</h3><p>{t['rush_p']}</p></div>
        <div><h3>{t['share_h']}</h3><p>{t['share_p']}</p></div>
      </div>
    </div>
  </section>

  <section id="pay" style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">04</span><div><span class="kicker">{t['pay_kicker']}</span><h2 class="split" data-split>{t['pay_h2']}</h2><p>{t['pay_p']}</p></div></div>
      <div class="pay-grid">{pays}</div>
      <p class="note" style="margin-top:16px">{t['pay_note']}</p>
    </div>
  </section>

  <section class="quote" id="quote">
    <div class="wrap">
      <div class="chapter"><span class="no">05</span><div><span class="kicker">{t['q_kicker']}</span><h2 class="split" data-split>{t['q_h2']}</h2><p>{t['q_p']}</p></div></div>
      <div class="q-grid">
        <form class="q" id="q" onsubmit="return false">
          <fieldset>
            <legend><i>i.</i>{t['q_pkg']}</legend>
            <label class="opt"><input type="radio" name="pkg" value="bundle" checked> {t['q_bundle']}<span class="p">US${PRICES['bundle_launch']}</span></label>
            <label class="opt"><input type="radio" name="pkg" value="portrait"> {t['q_portrait']}<span class="p">US${PRICES['portrait']}</span></label>
            <div class="opt locked">{t['q_pets']}<span class="p"><span class="stepper"><button type="button" data-k="pets" data-step="-1" aria-label="−">−</button><output id="pets">0</output><button type="button" data-k="pets" data-step="1" aria-label="+">＋</button></span></span></div>
            <div class="sub-opts" id="style-more">
              <div class="field"><span>{t['q_style']}</span><div class="pills">{styles_radio}</div></div>
              <div class="field"><span>{t['q_months']}</span><span class="stepper" style="width:max-content"><button type="button" data-k="months" data-step="-1" aria-label="−">−</button><output id="months">0</output><button type="button" data-k="months" data-step="1" aria-label="+">＋</button></span></div>
            </div>
          </fieldset>
          <fieldset>
            <legend><i>ii.</i>{t['q_you']}</legend>
            <div class="row2"><div class="field"><label for="who">{t['q_name']}</label><input type="text" id="who" maxlength="40"></div><div class="field"><label for="mail">{t['q_mail']}</label><input type="email" id="mail"></div></div>
            <div class="row2"><div class="field"><label for="n1">{t['q_n1']}</label><input type="text" id="n1" maxlength="40"></div><div class="field"><label for="n2">{t['q_n2']}</label><input type="text" id="n2" maxlength="40"></div></div>
            <div class="row2"><div class="field"><label for="country">{t['q_country']}</label><input type="text" id="country" maxlength="40"></div><div class="field"><span>{t['pay_pick']}</span><div class="pills"><label><input type="radio" name="pay" value="Wise" checked><span>Wise</span></label><label><input type="radio" name="pay" value="PayPal"><span>PayPal</span></label></div></div></div>
            <div class="row2"><div class="field"><label for="wd">{t['q_wd']}</label><input type="date" id="wd"></div><div class="field"><label for="need">{t['q_need']}</label><input type="date" id="need"><span class="note" id="rush-note">{t['q_rush']}</span></div></div>
            <div class="field"><label for="memo">{t['q_memo']}</label><textarea id="memo" placeholder="{t['q_memo_ph']}"></textarea></div>
          </fieldset>
        </form>
        <aside class="receipt" aria-live="polite">
          <small>{t['est']}</small>
          <span class="total" id="sum">US${PRICES['bundle_launch']}</span>
          <ul id="lines"></ul>
          <label for="msg" style="display:block;margin-top:16px;font-weight:700;font-size:14.5px">{t['msg_label']}</label>
          <textarea id="msg" spellcheck="false"></textarea>
          <div class="acts"><button class="pill ghost" type="button" id="copy" data-cta="quote_copy" data-cta-type="other">{t['copy']}</button><a class="pill" id="mailto" data-cta="quote_email" data-cta-type="other">{t['send']} <span class="arr">→</span></a></div>
          <p class="note" style="margin-top:12px">{t['send_note']}<span class="copied" id="copied" hidden>　{t['copied']}</span></p>
        </aside>
      </div>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <div class="chapter"><span class="no">06</span><div><span class="kicker">{t['faq_kicker']}</span><h2 class="split" data-split>{t['faq_h2']}</h2></div></div>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>
</main>

<footer class="end">
  <div class="wrap">
    <p class="huge split" data-split>{t['end_h']}</p>
    <p>{t['end_p']}</p>
    <a class="pill" href="#quote" data-cta="hero_quote" data-cta-type="wedding">{t['end_cta']} <span class="arr">→</span></a>
    <small><a href="https://knittinghiyori.com/">編織日和 Knitting Hiyori</a> · <span class="langs" style="display:inline-flex">{langs}</span></small>
    <p class="kh-legal" style="font-size:13px;color:#c9a7ae;margin:8px 0 0">{t['legal']} <a href="https://knittinghiyori.com/privacy-policy/">{t['privacy']}</a></p>
  </div>
</footer>
{js}{TRACK}</body>
</html>
"""
    out = os.path.join(ROOT, lang) if LIVE else os.path.join(ROOT, "_proposals", "intl", lang)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    return out


for l in LANGS:
    print(build(l))
