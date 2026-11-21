#!/usr/bin/env python3
"""中文分頁產生器（2026-11-21）：似顏繪、結婚書約、電子喜帖、關於我們、部落格。

版面、CSS、品牌列、頁尾都沿用中文版 index.html，改樣式只改 index.html，再跑一次：
    python3 tools/build_pages.py
會做三件事：
1. 更新 index.html 頁首的分頁選單（<!--HY-NAV--> 與 <!--HY-NAV-M--> 之間）
2. 產生 caricature/ marriage-certificate/ web-invitation/ about/ blog/ 的 index.html
3. 更新 sitemap.xml 的中文分頁（英日西三頁保持原樣）
估價工具只在首頁；分頁的估價按鈕連 /?sy=…#quote 或 /?web=…#quote，首頁會帶入方案。
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://wedding.knittinghiyori.com"
SPEC = "core-v1.11"
TODAY = "2026-11-21"

PAGES = [  # (網址, 選單文字)
    ("/caricature/", "似顏繪"),
    ("/marriage-certificate/", "結婚書約"),
    ("/web-invitation/", "電子喜帖"),
    ("/about/", "關於我們"),
    ("/blog/", "部落格"),
]

idx_path = os.path.join(ROOT, "index.html")
zh = open(idx_path, encoding="utf-8").read()


def nav(cur):
    here = ' aria-current="page"'
    links = "".join(f'<a href="{u}"{here if u == cur else ""}>{t}</a>' for u, t in PAGES)
    langs = ""
    if cur == "/":
        langs = ('<span class="langs"><a href="/" hreflang="zh-Hant" aria-current="page" data-cta="lang_switch" data-cta-type="wedding">中文</a>'
                 '<a href="/en/" hreflang="en" data-cta="lang_switch" data-cta-type="wedding">EN</a>'
                 '<a href="/ja/" hreflang="ja" data-cta="lang_switch" data-cta-type="wedding">日本語</a>'
                 '<a href="/es/" hreflang="es" data-cta="lang_switch" data-cta-type="wedding">ES</a></span>')
    quote = "#quote" if cur == "/" else "/#quote"
    desk = (f'<nav class="nav" aria-label="網站選單">{links}{langs}'
            f'<a class="pill" href="{quote}" data-cta="hero_quote" data-cta-type="wedding">估價 <span class="arr">→</span></a></nav>')
    mob = f'<nav class="pages-m" aria-label="網站選單（手機）">{links}</nav>'
    return desk, mob


def put_nav(doc, cur):
    desk, mob = nav(cur)
    doc = re.sub(r"<!--HY-NAV-->(.*?<!--/HY-NAV-->)?", lambda m: f"<!--HY-NAV-->{desk}<!--/HY-NAV-->", doc, count=1, flags=re.S)
    doc = re.sub(r"<!--HY-NAV-M-->(.*?<!--/HY-NAV-M-->)?", lambda m: f"<!--HY-NAV-M-->{mob}<!--/HY-NAV-M-->", doc, count=1, flags=re.S)
    return doc


# 1. 首頁選單
zh = put_nav(zh, "/")
open(idx_path, "w", encoding="utf-8").write(zh)

# 共用零件（從首頁取）
styles = "\n".join(re.findall(r"<style>.*?</style>", zh.split("</head>")[0], flags=re.S))
icons_fonts = zh[zh.index('<link rel="icon"'):zh.index("<style>")].strip()
header = zh[zh.index('<header class="top">'):zh.index("</header>") + 9]
footer = zh[zh.index('<footer class="end">'):zh.index("</footer>") + 9].replace('href="#quote"', 'href="/#quote"')
track = re.search(r"<script>\s*/\* 點擊追蹤.*?</script>", zh, flags=re.S).group(0)
TPL = re.search(r"const TPL = (\[.*?\]);", zh, flags=re.S).group(1)

ANIM = """<script>
(() => {
  if (new URLSearchParams(location.search).has("still")) document.documentElement.classList.add("still");
  const zoom = document.getElementById("zoom");
  const reel = document.getElementById("reel");
  if (reel) reel.innerHTML = HY_TPL.map(([f, name], i) => `<figure data-src="/assets/shoyaku/${f}.webp"><img src="/assets/shoyaku/${f}.webp" alt="結婚書約模板 ${i + 1}：${name}" loading="lazy" width="900" height="1273"><figcaption><span>${name}</span><b>No.${i + 1}</b></figcaption></figure>`).join("");
  document.querySelectorAll("#reel, #folio").forEach((g) => g.addEventListener("click", (e) => { const f = e.target.closest("figure"); if (!f || !zoom) return; const im = zoom.querySelector("img"); im.src = f.dataset.src; im.alt = f.querySelector("img").alt; zoom.showModal(); }));
  if (zoom) zoom.addEventListener("click", (e) => { if (e.target === zoom || e.target.tagName === "BUTTON") zoom.close(); });
  document.querySelectorAll("[data-split]").forEach((el) => {
    const walk = (node) => [...node.childNodes].forEach((n) => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        (n.textContent.match(/[A-Za-z’'.,]+|\\s+|./gu) || []).forEach((ch) => {
          if (/^\\s+$/.test(ch)) { frag.appendChild(document.createTextNode(" ")); return; }
          const w = document.createElement("span"); w.className = "w"; const s = document.createElement("span"); s.textContent = ch; w.appendChild(s); frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else walk(n);
    });
    walk(el);
    el.querySelectorAll(".w > span").forEach((s, i) => s.style.setProperty("--i", i));
  });
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: .12 });
  document.querySelectorAll(".rv, [data-split]").forEach((el) => io.observe(el));
  const fit = () => document.querySelectorAll(".device iframe").forEach((f) => { const w = f.parentElement.clientWidth; f.style.transform = `scale(${w / 375})`; f.style.height = `${f.parentElement.clientHeight / (w / 375)}px`; });
  const lio = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { const f = e.target; f.src = f.dataset.src; lio.unobserve(f); } }), { rootMargin: "300px" });
  document.querySelectorAll(".device iframe").forEach((f) => lio.observe(f));
  fit(); addEventListener("resize", fit);
})();
</script>"""

PAGE_CSS = """<style>
/* 分頁共用（build_pages.py） */
.page-hero { padding: 56px 0 24px; }
.page-hero .crumb { font-size: 13.5px; color: var(--muted); }
.page-hero .crumb a { color: var(--muted); }
.page-hero h1 { font-family: var(--serif); font-weight: 900; font-size: clamp(30px, 5vw, 54px); line-height: 1.25; color: var(--wine); margin: 14px 0 16px; }
.page-hero .lead { max-width: 720px; font-size: 17px; color: var(--ink); }
.page-hero .acts { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }
.prose { max-width: 760px; }
.prose h2 { font-family: var(--serif); color: var(--wine); font-size: clamp(22px, 3vw, 30px); margin: 8px 0 12px; }
.prose h3 { font-family: var(--serif); color: var(--wine); font-size: 19px; margin: 22px 0 6px; }
.prose p, .prose li { margin-bottom: 10px; }
.prose ul { padding-left: 1.2em; }
.law { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 18px; }
.law > div { background: var(--cream); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; }
.law b { display: block; font-family: var(--serif); color: var(--wine); font-size: 18px; margin-bottom: 4px; }
.note-box { margin-top: 18px; font-size: 14.5px; color: var(--muted); }
.draft { background: #fff3cd; border: 1px dashed #b8860b; padding: 10px 14px; border-radius: 10px; font-size: 14px; color: #6b4e00; }
@media (max-width: 700px) { .law { grid-template-columns: 1fr; } .page-hero { padding-top: 32px; } }
</style>"""


def faq_html(qa):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in qa) + "</div>"


def faq_ld(qa):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in qa]}


def crumbs_ld(url, name):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "似顏繪喜帖", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + url}]}


def page(url, name, title, desc, ga_title, body, ld=(), robots="index, follow, max-image-preview:large", extra_js=""):
    graph = {"@context": "https://schema.org", "@graph": [crumbs_ld(url, name), *ld]}
    head = f"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="編織日和">
<meta property="og:title" content="{html.escape(title.rsplit('｜', 1)[0])}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og.jpg">
<meta name="robots" content="{robots}">
{icons_fonts}
{styles}
{PAGE_CSS}
<!-- wedding 子網域：不放 Travelpayouts、不放 Google 廣告（core §1） -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZQZHTYTRMQ"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag("js",new Date());
gtag("set",{{content_group:"wedding",page_lang:"zh-Hant",page_title:"{ga_title}"}});
gtag("config","G-ZQZHTYTRMQ",/[?]hy_debug=1/.test(location.search)?{{cookie_domain:".knittinghiyori.com",debug_mode:true}}:{{cookie_domain:".knittinghiyori.com"}});
</script>
<script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=1)}
</script>
<meta name="spec-version" content="{SPEC}">
</head>
<body>
"""
    body = re.sub(r'<span class="no">\d\d</span>', '<span class="no">✦</span>', body)
    doc = head + put_nav(header, url) + "\n\n<main>\n" + body + "\n</main>\n\n" + footer + \
        '\n\n<dialog class="zoom" id="zoom"><img alt=""><button type="button" aria-label="關閉">✕</button></dialog>\n' + \
        f"<script>const HY_TPL = {TPL};</script>\n{ANIM}\n{extra_js}{track}\n</body>\n</html>\n"
    out = os.path.join(ROOT, url.strip("/"))
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(doc)
    return url, robots.startswith("index")


def hero(crumb, h1, lead, acts):
    return f"""  <section class="page-hero">
    <div class="wrap">
      <p class="crumb"><a href="/">似顏繪喜帖</a> › {crumb}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="acts">{acts}</div>
    </div>
  </section>"""


def offer(name, price, desc):
    return {"@type": "Offer", "name": name, "price": str(price), "priceCurrency": "TWD", "description": desc, "availability": "https://schema.org/InStock"}


PROVIDER = {"@type": "Organization", "name": "編織日和 Knitting Hiyori", "url": "https://knittinghiyori.com/"}

# 首頁的區塊，分頁直接沿用（改首頁，分頁跟著變）
def section(sid):
    m = re.search(rf'  <section[^>]*id="{sid}".*?</section>', zh, flags=re.S)
    return m.group(0)


cert_sec = section("cert").replace('href="#quote" data-pick-sy="', 'data-cta="page_quote" data-cta-type="wedding" href="/?sy=')
cert_sec = re.sub(r'href="/\?sy=(\d)"', r'href="/?sy=\1#quote"', cert_sec)
cert_sec = re.sub(r'\s*<a class="more" href="/marriage-certificate/".*?</a>', "", cert_sec)
web_sec = re.sub(r'\s*<a class="more" href="/web-invitation/".*?</a>', "", section("web"))
folio_sec = re.sub(r'\s*<a class="more" href="/caricature/".*?</a>', "", section("portfolio")).replace('style="padding-top:0"', "")
flow_sec = re.search(r'  <section style="padding-top:0">\s*<div class="wrap">\s*<div class="chapter"><span class="no">04</span>.*?</section>', zh, flags=re.S).group(0)
duo_sec = re.search(r'  <section style="padding-top:0">\s*<div class="wrap duo">.*?</section>', zh, flags=re.S).group(0)
faq_all = dict(re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", zh))

def faqs(*qs):
    return [(q, faq_all[q]) for q in qs]

def faq_sec(qa, no="FAQ"):
    return f"""  <section id="faq">
    <div class="wrap">
      <div class="chapter"><span class="no">✦</span><div><span class="kicker">{no}</span><h2>常見問題</h2></div></div>
      {faq_html(qa)}
    </div>
  </section>"""

def cta_sec(text, href):
    return f"""  <section style="padding-top:0">
    <div class="wrap">
      <a class="pill" href="{href}" data-cta="page_quote" data-cta-type="wedding">{text} <span class="arr">→</span></a>
    </div>
  </section>"""

built = []

# ── 結婚書約 ──
cert_qa = faqs("結婚書約 4 種方案差在哪裡？", "同婚可以做嗎？", "結婚書約可以用在台灣以外的國家嗎？印好的書約怎麼寄？", "書約的小圖示可以換成我們的寵物嗎？", "製作要多久？可以趕急件嗎？")
law_sec = """  <section style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">Two versions</span>
      <h2>同婚版、一般版：書約上的法條文字不一樣</h2>
      <p>結婚書約上會寫雙方「依照哪一條法律」結婚。同性伴侶和異性伴侶適用的法律不同，書約上的法條文字也不一樣。詢價時選好版本，我們會套用對應的文字。</p>
      <div class="law">
        <div><b>一般版</b>依《民法》第 982 條的結婚要件撰寫，適用異性伴侶。</div>
        <div><b>同婚版</b>依《司法院釋字第 748 號解釋施行法》撰寫，適用同性伴侶。</div>
      </div>
      <p class="note-box">登記規定可能調整，登記前請先向戶政事務所確認最新的書約格式與應備文件。</p>
    </div>
  </section>"""
cert_body = hero("結婚書約", "似顏繪結婚書約：<br>把你們畫進登記那天的書約",
                 "先畫好你們兩人的全身彩色似顏繪（NT$1,800），再放進手繪邊框的結婚書約。書約有 4 種方案，NT$1,000 起；同婚、非同婚都有對應的法條版本。",
                 '<a class="pill" href="/?sy=4#quote" data-cta="page_quote" data-cta-type="wedding">估價這個方案 <span class="arr">→</span></a><a class="pill ghost" href="#cert">看 4 種方案</a>') + \
    "\n" + cert_sec + "\n" + law_sec + "\n" + flow_sec + "\n" + faq_sec(cert_qa) + "\n" + cta_sec("開始估價結婚書約", "/?sy=4#quote")
cert_ld = [{"@type": "Service", "name": "似顏繪結婚書約客製", "serviceType": "結婚書約設計", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
            "offers": [offer("方案 1：書約設計", 1000, "設計圖面費，交付設計預覽，不含圖檔（另需雙人似顏繪 NT$1,800）"), offer("方案 2：書約設計＋PDF 電子檔", 1600, "可列印的 PDF"),
                       offer("方案 3：書約設計＋印刷 3 張", 2380, "台灣印製，郵局掛號寄台灣地址"), offer("方案 4：設計＋印刷 3 張＋PDF", 2880, "組合價")]}, faq_ld(cert_qa)]
built.append(page("/marriage-certificate/", "結婚書約", "似顏繪結婚書約客製｜同婚版・一般版 4 種方案 NT$1,000 起｜編織日和",
                  "似顏繪結婚書約 4 種方案：設計 NT$1,000、加 PDF NT$1,600、印刷 3 張 NT$2,380、組合價 NT$2,880（另需雙人似顏繪 NT$1,800）。同婚版、一般版用對應的法條文字，8 款書約模板，郵局掛號寄台灣。",
                  "喜帖|結婚書約|似顏繪結婚書約客製", cert_body, cert_ld))

# ── 似顏繪 ──
cari_qa = faqs("要準備什麼照片？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "你們會公開我們的作品嗎？", "似顏繪喜帖包含哪些東西？價格怎麼算？")
cari_body = hero("似顏繪", "新人似顏繪：<br>照你們最喜歡的婚紗照畫",
                 "雙人全身彩色似顏繪 NT$1,800，免費修改 2 次；毛小孩、小朋友每位加 NT$800 一起畫進來。這張圖之後可以放進結婚書約和電子喜帖，整套看起來是同一個風格。",
                 '<a class="pill" href="/#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#portfolio">看作品</a>') + \
    "\n" + folio_sec + "\n" + duo_sec + "\n" + flow_sec + "\n" + faq_sec(cari_qa) + "\n" + cta_sec("開始估價似顏繪", "/#quote")
cari_ld = [{"@type": "Service", "name": "新人似顏繪客製", "serviceType": "婚禮似顏繪", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
            "offers": [offer("雙人全身彩色似顏繪", 1800, "免費修改 2 次"), offer("加畫寵物或小孩（每位）", 800, "毛小孩、小朋友一起入鏡")]}, faq_ld(cari_qa)]
built.append(page("/caricature/", "似顏繪", "新人似顏繪客製｜雙人全身彩色 NT$1,800、可加畫寵物｜編織日和",
                  "新人似顏繪：照婚紗照畫雙人全身彩色似顏繪 NT$1,800，免費修改 2 次，加畫寵物或小孩每位 NT$800。西式婚紗、和服、中式禮服都能畫，可延伸做結婚書約與電子喜帖。",
                  "喜帖|似顏繪|新人似顏繪客製", cari_body, cari_ld, extra_js=""))

# ── 電子喜帖 ──
web_qa = faqs("電子喜帖可以用多久？會被搜尋到嗎？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "怎麼付款？什麼時候開始製作？")
web_body = hero("電子喜帖", "網頁電子喜帖：<br>手機一點就開，賓客線上回覆出席",
                "把你們的似顏繪做成喜帖網頁：開場動畫、婚禮倒數、婚宴流程、Dress code、地圖、加入行事曆、出席回覆都在裡面。3 種風格同價 NT$3,000（另需雙人似顏繪 NT$1,800）。",
                '<a class="pill" href="/?web=A#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#web">看 3 種風格</a>') + \
    "\n" + web_sec + "\n" + flow_sec + "\n" + faq_sec(web_qa) + "\n" + cta_sec("開始估價電子喜帖", "/?web=A#quote")
web_ld = [{"@type": "Service", "name": "似顏繪網頁電子喜帖", "serviceType": "電子喜帖設計", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
           "offers": [offer("網頁電子喜帖（3 種風格同價）", 3000, "交付起 3 個月上線與維護"), offer("延長上線（每月）", 600, "交付 3 個月後每延長 1 個月")]}, faq_ld(web_qa)]
built.append(page("/web-invitation/", "電子喜帖", "網頁電子喜帖客製｜似顏繪＋出席回覆、地圖、倒數 3 種風格 NT$3,000｜編織日和",
                  "似顏繪網頁電子喜帖：開場動畫、婚禮倒數、流程、Dress code、地圖、加入行事曆、出席回覆。書約手繪風、日系清新、雪景 3 種風格同價 NT$3,000，網址不公開、不被搜尋引擎收錄。",
                  "喜帖|電子喜帖|似顏繪網頁電子喜帖", web_body, web_ld))

# ── 關於我們（文字依 Alison 2026-11-21 提供） ──
about_body = hero("關於我們", "關於我們",
                  "似顏繪喜帖是「編織日和」的接案服務。我們自己也是同婚伴侶，相信好的設計能帶來美感，也帶來力量。",
                  '<a class="pill" href="/#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a>') + """
  <section style="padding-top:0">
    <div class="wrap prose">
      <h2>我們自己也是同婚伴侶</h2>
      <p>我們走過同婚登記，知道挑書約、確認法條文字時那份小小的緊張。所以每一份結婚書約，我們都會依照你們的狀況套用對應的版本：同婚版依《司法院釋字第 748 號解釋施行法》，一般版依《民法》第 982 條。</p>
      <p>不管你們是誰，都值得一份畫得像你們、看了會笑的喜帖和書約。</p>
      <h2>相信好的設計</h2>
      <p>我們相信好的設計，會為重要的日子帶來美感，也帶來力量。似顏繪由 Zoe 主筆，並和散居各地、同樣過著數位遊牧生活的設計師朋友合作，一起打造屬於你們的似顏繪、結婚書約和電子喜帖。</p>
      <h2>我們也在做的事</h2>
      <p>除了喜帖，我們也經營<a href="https://knittinghiyori.com/">編織日和</a>網站，以及數位遊牧主題的 YouTube 頻道<a href="https://www.youtube.com/@coffeebreak.Japanese" rel="noopener" target="_blank">「1 Hour Pomodoro 25/5 🏙️ | Focus World」</a>。未來，我們期盼成為完全的數位遊牧工作者。</p>
      <h2>聯絡我們</h2>
      <p>只用 Email 聯絡：theperfectmatchfilters@gmail.com。先用<a href="/#quote">估價工具</a>選好項目，會自動寫好一封詢價信。</p>
    </div>
  </section>"""
built.append(page("/about/", "關於我們", "關於我們｜同婚伴侶經營的似顏繪喜帖・編織日和",
                  "編織日和的似顏繪喜帖由同婚伴侶經營：相信好的設計帶來美感與力量，與各地數位遊牧的設計師朋友合作，打造似顏繪、結婚書約與電子喜帖。",
                  "喜帖|關於我們|同婚伴侶經營的似顏繪喜帖", about_body))

# ── 部落格（第一篇上線前 noindex） ──
blog_body = hero("部落格", "婚禮筆記",
                 "婚禮歌單、結婚登記、同婚書約要注意的地方⋯⋯我們把籌備婚禮時用得到的資訊整理在這裡。",
                 '<a class="pill ghost" href="/">回似顏繪喜帖</a>') + """
  <section style="padding-top:0">
    <div class="wrap prose">
      <p>第一篇文章準備中。</p>
    </div>
  </section>"""
built.append(page("/blog/", "部落格", "婚禮筆記｜婚禮歌單、結婚登記與同婚書約｜編織日和",
                  "編織日和的婚禮筆記：婚禮歌單、結婚登記流程、同婚書約法條等籌備婚禮用得到的資訊。",
                  "喜帖|部落格|婚禮筆記", blog_body, robots="noindex, follow"))

# 3. sitemap：英日西保持原樣，中文分頁只放可收錄的頁
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
sm = re.sub(r"  <!--HY-PAGES-->.*?<!--/HY-PAGES-->\n", "", sm, flags=re.S)
rows = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u, ok in built if ok)
sm = sm.replace("</urlset>", f"  <!--HY-PAGES-->\n{rows}  <!--/HY-PAGES-->\n</urlset>")
open(sm_path, "w", encoding="utf-8").write(sm)
print("built:", ", ".join(u + ("" if ok else "（noindex）") for u, ok in built))
