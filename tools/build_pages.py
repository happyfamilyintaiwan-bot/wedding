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
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_posts import POSTS
from blog_kit import CHEAT, SERVICES, end_card

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://wedding.knittinghiyori.com"
SPEC = "core-v1.11"
TODAY = "2026-11-21"

PAGES = [  # (網址, 選單文字)
    ("/caricature/", "似顏繪"),
    ("/marriage-certificate/", "結婚書約"),
    ("/web-invitation/", "電子喜帖"),
    ("/paper-invitation/", "紙本喜帖"),
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
/* 部落格文章 */
.post { max-width: 760px; font-size: 17px; }
.post h2 { font-family: var(--serif); color: var(--wine); font-size: clamp(22px, 3vw, 29px); margin: 44px 0 12px; line-height: 1.4; }
.post h3 { font-family: var(--serif); color: var(--wine); font-size: 19px; margin: 26px 0 8px; }
.post p { margin-bottom: 14px; }
.post a { color: var(--wine); }
.post ul, .post ol { padding-left: 1.3em; margin-bottom: 14px; }
.post li { margin-bottom: 6px; }
.post .tldr { background: var(--cream); border: 1px solid var(--wine); border-radius: 16px; padding: 18px 22px 8px; margin: 8px 0 18px; }
.post .tldr b { font-family: var(--serif); color: var(--wine); }
.post .tbl { overflow-x: auto; margin: 10px 0 18px; }
.post table { border-collapse: collapse; width: 100%; min-width: 480px; font-size: 15px; background: #fff; }
.post th, .post td { border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }
.post th { background: var(--blush); color: var(--wine); }
.post ul.songs { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.post ul.songs li { margin: 0; line-height: 1.5; }
.post ul.songs li > a { display: block; height: 100%; text-decoration: none; background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; transition: border-color .2s, transform .2s; }
.post ul.songs li > a:hover { border-color: var(--wine); transform: translateY(-2px); }
.post ul.songs b { display: block; color: var(--wine); }
.post ul.songs b .play { display: inline; font-size: 11px; color: var(--rose-d); }
.post ul.songs span { display: block; font-size: 14px; color: var(--muted); }
.post ul.songs small { display: block; font-size: 13px; color: var(--ink); margin-top: 2px; }
.post .tags { margin-top: 4px; }
.post .tag { font-style: normal; font-size: 12px; border-radius: 999px; padding: 1px 8px; margin-right: 4px; display: inline-block; }
.post .tag.a { background: var(--rose); color: var(--wine); }
.post .tag.t { background: var(--blush); color: var(--muted); }
.post .tag.f { background: #efe6d6; color: #6b4e00; }
.post .tag.o { background: #e3ecf3; color: #2f4a63; }
.post .cta-inline { background: var(--blush); border-radius: 12px; padding: 12px 16px; }
.post .meta { font-size: 14px; color: var(--muted); }
.post .sources { font-size: 14px; color: var(--muted); }
.post-list { display: grid; gap: 16px; max-width: 760px; }
.post-list a { display: block; text-decoration: none; background: var(--cream); border: 1px solid var(--line); border-radius: 16px; padding: 18px 22px; }
.post-list b { font-family: var(--serif); color: var(--wine); font-size: 19px; display: block; margin-bottom: 4px; }
.post-list span { color: var(--muted); font-size: 15px; }
@media (max-width: 560px) { .post ul.songs { grid-template-columns: 1fr; } .post { font-size: 16px; } }
/* 文章元件（build_pages.py） */
.post-cover { margin: 0 0 18px; border-radius: 18px; overflow: hidden; border: 1px solid var(--line); aspect-ratio: 1200 / 630; background: var(--blush); }
.post-cover img { display: block; width: 100%; height: 100%; object-fit: cover; }
.sum3 { position: relative; background: var(--cream); border: 2px solid var(--wine); border-radius: 18px; padding: 22px 22px 14px; margin: 0 0 20px; box-shadow: 6px 6px 0 var(--rose); }
.sum3 > b { position: absolute; top: -14px; left: 18px; background: var(--wine); color: var(--cream); font-family: var(--serif); font-size: 14px; letter-spacing: .08em; padding: 3px 12px; border-radius: 999px; }
.sum3 ol { list-style: none; padding: 0; margin: 4px 0 0; counter-reset: s; }
.sum3 li { counter-increment: s; display: grid; grid-template-columns: 30px 1fr; gap: 10px; margin-bottom: 10px; font-size: 16.5px; line-height: 1.65; }
.sum3 li::before { content: counter(s); width: 26px; height: 26px; border-radius: 50%; background: var(--rose); color: var(--wine); font-family: var(--latin); font-weight: 700; display: grid; place-items: center; margin-top: 2px; }
.toc { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 26px; padding: 0; list-style: none; }
.toc a { display: inline-block; font-size: 14px; text-decoration: none; color: var(--wine); background: #fff; border: 1px solid var(--line); border-radius: 999px; padding: 5px 12px; }
.toc a:hover { border-color: var(--wine); }
.post ol.steps { list-style: none; padding: 0; counter-reset: st; margin: 12px 0 20px; }
.post ol.steps > li { counter-increment: st; position: relative; padding: 0 0 18px 50px; margin: 0; }
.post ol.steps > li::before { content: counter(st); position: absolute; left: 0; top: 0; width: 34px; height: 34px; border-radius: 50%; background: var(--wine); color: var(--cream); font-family: var(--latin); font-weight: 700; font-size: 17px; display: grid; place-items: center; }
.post ol.steps > li:not(:last-child)::after { content: ""; position: absolute; left: 16.5px; top: 38px; bottom: 4px; width: 1px; background: var(--rose); }
.post ol.steps > li > b { display: block; color: var(--wine); font-size: 17.5px; margin-bottom: 2px; }
.post ul.check { list-style: none; padding: 0; }
.post ul.check > li { position: relative; padding-left: 28px; }
.post ul.check > li::before { content: "✓"; position: absolute; left: 4px; top: 0; color: var(--rose-d); font-weight: 700; }
.box { border-radius: 14px; padding: 14px 18px 4px; margin: 16px 0 20px; border-left: 5px solid; }
.box > b { display: block; font-size: 15.5px; margin-bottom: 4px; }
.box p { margin-bottom: 10px; }
.box.tip { background: var(--blush); border-color: var(--rose-d); }
.box.tip > b { color: var(--wine); }
.box.warn { background: #fff4d6; border-color: #c9962b; }
.box.warn > b { color: #6b4e00; }
.box.note { background: #e9f0f5; border-color: #5b7d99; }
.box.note > b { color: #2f4a63; }
.cheat { margin: 26px 0; text-align: center; }
.cheat img { width: 100%; max-width: 480px; height: auto; border-radius: 14px; border: 1px solid var(--line); box-shadow: 0 20px 40px -26px rgba(90, 34, 50, .55); }
.cheat figcaption { font-size: 14px; color: var(--muted); margin-top: 8px; }
.cheat .acts { display: flex; gap: 8px; justify-content: center; margin-top: 10px; flex-wrap: wrap; }
.cheat .acts .pill { min-height: 38px; padding: 6px 16px; font-size: 14px; }
.svc-mid { display: grid; grid-template-columns: 84px 1fr; gap: 14px; align-items: center; text-decoration: none; color: var(--ink); background: #fff; border: 1px solid var(--wine); border-radius: 16px; padding: 12px 16px 12px 12px; margin: 22px 0; transition: transform .25s var(--ease), box-shadow .25s; }
.svc-mid:hover { transform: translateY(-2px); box-shadow: 0 14px 26px -18px rgba(90, 34, 50, .6); }
.svc-mid img { width: 84px; height: 84px; object-fit: cover; border-radius: 12px; background: var(--blush); }
.svc-mid i { font-style: normal; display: block; font-size: 13.5px; color: var(--rose-d); }
.svc-mid b { display: block; font-family: var(--serif); color: var(--wine); font-size: 17px; line-height: 1.4; }
.svc-mid span { display: block; font-size: 14px; color: var(--muted); }
.svc-end { display: grid; grid-template-columns: 200px 1fr; gap: 22px; align-items: center; background: var(--cream); border: 2px solid var(--wine); border-radius: 20px; padding: 20px; margin: 40px 0 10px; }
.svc-end img { width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 14px; background: var(--blush); }
.svc-end h3 { font-family: var(--serif); color: var(--wine); font-size: 22px; margin: 4px 0 8px; line-height: 1.35; }
.svc-end ul { list-style: none; padding: 0; margin: 0 0 12px; font-size: 15px; }
.svc-end li { margin: 0 0 4px; padding-left: 20px; position: relative; }
.svc-end li::before { content: "✦"; position: absolute; left: 0; color: var(--rose-d); font-size: 12px; top: 3px; }
.svc-end .price { font-family: var(--latin); color: var(--wine); font-size: 26px; margin-bottom: 12px; }
.svc-end .acts { display: flex; gap: 8px; flex-wrap: wrap; }
@media (max-width: 560px) {
  .svc-end { grid-template-columns: 1fr; padding: 16px; }
  .svc-end img { aspect-ratio: 4 / 3; object-position: center 70%; }
  .svc-end .acts .pill { flex: 1; }
  .post .tbl.stack table, .post .tbl.stack tbody, .post .tbl.stack tr, .post .tbl.stack td { display: block; min-width: 0; width: 100%; }
  .post .tbl.stack thead { display: none; }
  .post .tbl.stack tr { border: 1px solid var(--line); border-radius: 12px; margin-bottom: 10px; background: #fff; overflow: hidden; }
  .post .tbl.stack td { border: 0; border-bottom: 1px dashed var(--line); display: grid; grid-template-columns: 7.5em 1fr; gap: 8px; }
  .post .tbl.stack td:last-child { border-bottom: 0; }
  .post .tbl.stack td::before { content: attr(data-th); color: var(--muted); font-size: 13.5px; }
  .post .tbl.stack td:first-child { background: var(--blush); color: var(--wine); font-weight: 700; grid-template-columns: 1fr; }
  .post .tbl.stack td:first-child::before { display: none; }
}
.post-hero h1 { font-size: clamp(26px, 4.2vw, 42px); }
.post .lead-p { font-size: 17px; }
.post .note-box { font-size: 14.5px; color: var(--muted); }
.rel { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin: 10px 0 18px; }
.rel a, .post-list a.card { display: grid; grid-template-rows: auto 1fr; text-decoration: none; color: var(--ink); background: #fff; border: 1px solid var(--line); border-radius: 16px; overflow: hidden; transition: transform .25s var(--ease), border-color .25s; }
.rel a:hover, .post-list a.card:hover { transform: translateY(-2px); border-color: var(--wine); }
.rel img, .post-list a.card img { display: block; width: 100%; aspect-ratio: 1200 / 630; object-fit: cover; background: var(--blush); }
.rel a div, .post-list a.card div { padding: 12px 14px 14px; }
.rel i, .post-list a.card i { font-style: normal; font-size: 12.5px; color: var(--rose-d); display: block; margin-bottom: 2px; }
.rel b { font-family: var(--serif); color: var(--wine); font-size: 16.5px; line-height: 1.45; display: block; }
.cats { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; padding: 0; margin: 0 0 26px; }
.cats a { display: inline-block; text-decoration: none; color: var(--wine); background: #fff; border: 1px solid var(--line); border-radius: 999px; padding: 6px 14px; font-size: 14.5px; }
.cats a:hover { border-color: var(--wine); }
.blog-cat { margin-bottom: 40px; }
.blog-cat h2 { font-family: var(--serif); color: var(--wine); font-size: clamp(22px, 3vw, 28px); margin-bottom: 4px; }
.blog-cat > p { color: var(--muted); margin-bottom: 14px; max-width: 40em; }
.post-list.grid { grid-template-columns: repeat(2, minmax(0, 1fr)); max-width: 980px; }
.post-list a.card { padding: 0; }
.post-list a.card b { margin-bottom: 6px; }
.post-list a.card small { display: block; font-size: 13px; color: var(--muted); margin-top: 8px; }
@media (max-width: 640px) { .rel, .post-list.grid { grid-template-columns: 1fr; } }
</style>"""


def faq_html(qa):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in qa) + "</div>"


def faq_ld(qa):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in qa]}


def crumbs_ld(url, name):
    trail = [("似顏繪喜帖", "/")] + ([("部落格", "/blog/")] if url.startswith("/blog/") and url != "/blog/" else []) + [(name, url)]
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}


def page(url, name, title, desc, ga_title, body, ld=(), robots="index, follow, max-image-preview:large", extra_js="", og_image="/assets/og.jpg", og_alt="", article=None):
    graph = {"@context": "https://schema.org", "@graph": [crumbs_ld(url, name), *ld]}
    alt_tag = f'\n<meta property="og:image:alt" content="{html.escape(og_alt)}">' if og_alt else ""
    art_tags = (f'\n<meta property="article:published_time" content="{article[0]}">'
                f'\n<meta property="article:modified_time" content="{article[1]}">') if article else ""
    head = f"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:type" content="{'article' if article else 'website'}">
<meta property="og:site_name" content="編織日和">
<meta property="og:title" content="{html.escape(title.rsplit('｜', 1)[0])}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">{alt_tag}
<meta property="og:locale" content="zh_TW">{art_tags}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}{og_image}">
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

BUNDLE = """  <section style="padding-top:0">
    <div class="wrap">
      <div class="bundle" style="grid-template-columns:1fr">
        <div><span class="kicker">All in one</span><h3>想一次搞定？全套方案加送兩份贈品</h3><p>似顏繪＋結婚書約＋網頁電子喜帖＋紙本喜帖四樣都選，加送 Save the Date 分享圖和迎賓板列印檔（例：書約方案 4＋紙本喜帖 30 份，全套 NT$14,130）。同一張似顏繪延伸成整套設計，估價工具會幫你全部勾好，再依需要調整。</p></div>
        <div><a class="pill" href="/?all=1#quote" data-cta="bundle_quote" data-cta-type="wedding">一次估價全套 <span class="arr">→</span></a></div>
      </div>
    </div>
  </section>"""

def read_more(*links):
    """服務頁底部連到相關文章（文章與服務頁互相導引）"""
    return """  <section style="padding-top:0">
    <div class="wrap prose"><span class="kicker">Read more</span><h2>延伸閱讀</h2><ul>""" + "".join(f'<li><a href="{u}" data-cta="related_link" data-cta-type="wedding">{t}</a></li>' for u, t in links) + """</ul></div>
  </section>"""


# ── 部落格共用（文章元件：tools/blog_kit.py；寫作規範：CLAUDE.md「部落格寫作規範」） ──
CATS = [  # (代號, 分類名稱, 一句說明)；每篇的 cat 填代號，部落格首頁照這個順序分區
    ("registration", "結婚登記與法規", "結婚登記要帶什麼、書約怎麼寫、跨國與同婚伴侶的規定，照官方公告整理。"),
    ("planning", "婚禮籌備", "歌單、流程、喜帖與婚禮小細節，挑歌挑設計時用得到。"),
]
CAT_NAME = dict((c, n) for c, n, _ in CATS)


def strip(s):
    return re.sub("<[^>]+>", "", s)


def post_url(P):
    return f"/blog/{P['slug']}/"


def check_post(P):
    """每篇的固定元素，少了就停下來（規範見 CLAUDE.md）"""
    s, err = P["slug"], []
    for k in ("cat", "cover", "summary", "cheat", "service"):
        if not P.get(k):
            err.append(f"缺 {k}")
    if P.get("cat") and P["cat"] not in CAT_NAME:
        err.append(f"cat「{P['cat']}」不在 CATS 裡")
    if P.get("summary") and len(P["summary"]) != 3:
        err.append(f"summary 要剛好 3 句（現在 {len(P['summary'])} 句）")
    if P.get("service") and P["service"] not in SERVICES:
        err.append(f"service「{P['service']}」不在 blog_kit.SERVICES 裡")
    n_mid = P["body"].count('class="svc-mid"')
    if n_mid != 1:
        err.append(f"內文中間的情境卡 mid(...) 要剛好 1 張（現在 {n_mid} 張）")
    if P["body"].count(CHEAT) != 1:
        err.append("內文要放 1 次 {CHEAT}（懶人包圖的位置）")
    for k in ("cover", "cheat"):
        c = P.get(k) or {}
        if c and not (c.get("img") and c.get("alt")):
            err.append(f"{k} 要有 img 和 alt")
        if c.get("img") and not os.path.exists(os.path.join(ROOT, "assets", "blog", c["img"])):
            err.append(f"找不到 assets/blog/{c['img']}，先跑 python3 tools/make_blog_img.py {s}")
    if re.search("[–—]", P["body"] + P["title"] + P["desc"] + "".join(q + a for q, a in P["faq"])):
        err.append("有 em dash 或 en dash（—、–），改成逗號、冒號或括號")
    if err:
        sys.exit(f"文章 {s} 沒過檢查：\n- " + "\n- ".join(err))


def links_to(P, url):
    return f'href="{url}' in P["body"] or SERVICES[P["service"]]["url"] == url


def read_more_auto(url):
    """服務頁底部的延伸閱讀：自動列出連到這個服務頁的文章"""
    links = [(post_url(P), strip(P["h1"])) for P in POSTS if links_to(P, url)]
    return read_more(*links) if links else ""


def card(P, cta, small=True):
    c = P["cover"]
    return (f'<a class="card" href="{post_url(P)}" data-cta="{cta}" data-cta-type="wedding"><img src="/assets/blog/{c["img"]}" alt="{html.escape(c["alt"])}" loading="lazy" width="1200" height="630">'
            f'<div><i>{CAT_NAME[P["cat"]]}</i><b>{strip(P["h1"])}</b>' + (f'<span>{P["desc"][:64]}…</span><small>更新 {P["modified"]}</small>' if small else "") + "</div></a>")


def related(P):
    """延伸閱讀：同分類的文章排前面，最多 4 篇（服務頁交給兩張服務卡）"""
    others = sorted((o for o in POSTS if o["slug"] != P["slug"]), key=lambda o: o["modified"], reverse=True)
    others = sorted(others, key=lambda o: o["cat"] != P["cat"])   # 同分類排前面，各自新的在前
    others = others[:4]
    if not others:
        return ""
    return '<h2 id="related">延伸閱讀</h2><div class="rel">' + "".join(
        f'<a href="{post_url(o)}" data-cta="related_link" data-cta-type="wedding"><img src="/assets/blog/{o["cover"]["img"]}" alt="{html.escape(o["cover"]["alt"])}" loading="lazy" width="1200" height="630"><div><i>{CAT_NAME[o["cat"]]}</i><b>{strip(o["h1"])}</b></div></a>'
        for o in others) + "</div>"


def toc(P):
    heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', P["body"])
    names = P.get("toc", {})
    items = [(i, names.get(i, strip(t).rstrip("？?"))) for i, t in heads] + [("faq", "常見問題")]
    return '<ul class="toc" aria-label="文章目錄">' + "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items) + "</ul>"



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
      <p class="note-box">登記規定可能調整，登記前請先向戶政事務所確認最新的書約格式與應備文件。同性結婚登記要帶什麼、跨國伴侶能不能登記，整理在<a href="/blog/same-sex-marriage-registration-taiwan/">台灣同性結婚登記全攻略</a>。</p>
    </div>
  </section>"""
cert_body = hero("結婚書約", "似顏繪結婚書約：<br>把你們畫進登記那天的書約",
                 "先畫好你們兩人的全身彩色似顏繪（NT$1,800），再放進手繪邊框的結婚書約。書約有 4 種方案，NT$1,000 起；同婚、非同婚都有對應的法條版本。",
                 '<a class="pill" href="/?sy=4#quote" data-cta="page_quote" data-cta-type="wedding">估價這個方案 <span class="arr">→</span></a><a class="pill ghost" href="#cert">看 4 種方案</a>') + \
    "\n" + cert_sec + "\n" + law_sec + "\n" + flow_sec + "\n" + read_more_auto("/marriage-certificate/") + "\n" + faq_sec(cert_qa) + "\n" + cta_sec("開始估價結婚書約", "/?sy=4#quote") + "\n" + BUNDLE
cert_ld = [{"@type": "Service", "name": "似顏繪結婚書約客製", "serviceType": "結婚書約設計", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
            "offers": [offer("方案 1：書約設計", 1000, "設計圖面費，交付設計預覽，不含圖檔（另需雙人似顏繪 NT$1,800）"), offer("方案 2：書約設計＋PDF 電子檔", 1600, "可列印的 PDF"),
                       offer("方案 3：書約設計＋印刷 3 張", 2380, "台灣印製，郵局掛號寄台灣地址"), offer("方案 4：設計＋印刷 3 張＋PDF", 2880, "組合價")]}, faq_ld(cert_qa)]
built.append(page("/marriage-certificate/", "結婚書約", "似顏繪結婚書約客製｜同婚版・一般版 4 種方案 NT$1,000 起｜編織日和",
                  "似顏繪結婚書約 4 種方案：設計 NT$1,000、加 PDF NT$1,600、印刷 3 張 NT$2,380、組合價 NT$2,880（另需雙人似顏繪 NT$1,800）。同婚版、一般版用對應的法條文字，8 款書約模板，郵局掛號寄台灣。",
                  "喜帖|結婚書約|似顏繪結婚書約客製", cert_body, cert_ld))

# ── 似顏繪 ──
cari_qa = faqs("似顏繪喜帖包含哪些東西？價格怎麼算？") + [
    ("可以只畫似顏繪，不做書約和喜帖嗎？", "可以。雙人全身彩色似顏繪 NT$1,800 可以單獨訂，用估價工具只留似顏繪就好。之後想加結婚書約、電子喜帖或紙本喜帖，再用同一張圖延伸。"),
    ("只買似顏繪會拿到什麼檔案？", "高解析 JPG 和去背 PNG 各一份，用 Email 寄給你們。可以自己拿去做謝卡、桌卡、社群頭貼這類個人用途；不能商用或轉售。"),
    ("似顏繪可以印成大圖或迎賓板嗎？", "可以。似顏繪以 60×90cm、300dpi 繪製（約 7087×10630 px），印成迎賓板也清楚，縮小放進書約和喜帖也不會失真。四樣都選的全套方案，另外加送排好版的迎賓板列印檔（PDF）。"),
] + faqs("要準備什麼照片？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "你們會公開我們的作品嗎？")
uses_sec = """  <section style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">One portrait, every detail</span>
      <h2>一張圖，整場婚禮都用得到</h2>
      <p>似顏繪是整套設計的起點。同一張圖放進書約、喜帖和婚禮當天的小物，看起來就是同一套。</p>
      <div class="law">
        <div><b>結婚書約</b>放進手繪邊框的書約，登記那天拿在手上拍照。<a href="/marriage-certificate/">看結婚書約</a></div>
        <div><b>網頁電子喜帖</b>開場動畫的主角，賓客手機一點就看到你們。<a href="/web-invitation/">看電子喜帖</a></div>
        <div><b>紙本喜帖</b>印在喜帖正面，寄給長輩也好看。<a href="/paper-invitation/">看紙本喜帖</a></div>
        <div><b>Save the Date 分享圖</b>1080×1350，可以直接發社群通知好友。全套方案贈送。</div>
        <div><b>迎賓板</b>婚禮入口的大圖，交付排好版的列印檔（PDF）。全套方案贈送。</div>
        <div><b>謝卡、桌卡、頭貼</b>只買似顏繪也會拿到高解析 JPG 和去背 PNG，可以自己做個人用途的小物。</div>
      </div>
      <p class="note-box">似顏繪以 60×90cm、300dpi 繪製（約 7087×10630 px）。大圖縮小用不會失真，印成迎賓板也清楚。</p>
    </div>
  </section>"""
prep_sec = """  <section style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">Before you send</span>
      <h2>照片準備清單</h2>
      <ul>
        <li>一張你們最喜歡的婚紗照或合照；或每人 2～3 張清楚的正面照，加 1 張合照。</li>
        <li>臉要看得清楚：光線不要太暗，不要被頭紗、手或帽子擋住。</li>
        <li>想一起畫的毛小孩或小朋友，另外附 1～2 張清楚的照片。</li>
        <li>想穿的服裝、想放的小物（例如和服、貓咪坐在腳邊），寫在詢價信裡。</li>
        <li>用 Email 寄原始照片，通訊軟體傳過的圖會被壓縮，細節會變少。</li>
      </ul>
      <h2 style="margin-top:36px">安心清單</h2>
      <div class="law">
        <div><b>免費修改 2 次</b>不滿意的地方直接說，超過 2 次每次 NT$500。</div>
        <div><b>草稿前可全額退款</b>開始畫草稿之前取消，全額退款；草稿交出之後就不退款。</div>
        <div><b>照片不公開</b>你們寄來的照片不會公開。作品展示也不會放全名、地址和婚宴資訊。</div>
        <div><b>高解析交件</b>60×90cm、300dpi 繪製，交付高解析 JPG 和去背 PNG。</div>
      </div>
    </div>
  </section>"""
cari_body = hero("似顏繪", "新人似顏繪：<br>照你們最喜歡的婚紗照畫",
                 "雙人全身彩色似顏繪 NT$1,800，免費修改 2 次；毛小孩、小朋友每位加 NT$800。以 60×90cm 高解析度繪製，同一張圖從結婚書約、喜帖一路用到迎賓板。",
                 '<a class="pill" href="/#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#portfolio">看作品</a>') + \
    "\n" + uses_sec + "\n" + folio_sec + "\n" + duo_sec + "\n" + prep_sec + "\n" + flow_sec + "\n" + read_more_auto("/caricature/") + "\n" + faq_sec(cari_qa) + "\n" + cta_sec("開始估價似顏繪", "/#quote") + "\n" + BUNDLE
cari_ld = [{"@type": "Service", "name": "新人似顏繪客製", "serviceType": "婚禮似顏繪", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
            "offers": [offer("雙人全身彩色似顏繪", 1800, "免費修改 2 次；60×90cm、300dpi 繪製，交付高解析 JPG 與去背 PNG"), offer("加畫寵物或小孩（每位）", 800, "毛小孩、小朋友一起入鏡")]}, faq_ld(cari_qa)]
built.append(page("/caricature/", "似顏繪", "新人似顏繪客製｜雙人全身彩色 NT$1,800、可加畫寵物｜編織日和",
                  "新人似顏繪：照婚紗照畫雙人全身彩色似顏繪 NT$1,800，免費修改 2 次，加畫寵物或小孩每位 NT$800。60×90cm 高解析繪製，交付 JPG 與去背 PNG，可延伸做結婚書約、喜帖與迎賓板。",
                  "喜帖|似顏繪|新人似顏繪客製", cari_body, cari_ld, extra_js=""))

# ── 電子喜帖 ──
web_qa = faqs("電子喜帖可以用多久？會被搜尋到嗎？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "怎麼付款？什麼時候開始製作？")
web_body = hero("電子喜帖", "網頁電子喜帖：<br>手機一點就開，賓客線上回覆出席",
                "把你們的似顏繪做成喜帖網頁：開場動畫、婚禮倒數、婚宴流程、Dress code、地圖、加入行事曆、出席回覆都在裡面。3 種風格同價 NT$3,800（另需雙人似顏繪 NT$1,800）。",
                '<a class="pill" href="/?web=A#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#web">看 3 種風格</a>') + \
    "\n" + web_sec + "\n" + flow_sec + "\n" + read_more_auto("/web-invitation/") + "\n" + faq_sec(web_qa) + "\n" + cta_sec("開始估價電子喜帖", "/?web=A#quote") + "\n" + BUNDLE
web_ld = [{"@type": "Service", "name": "似顏繪網頁電子喜帖", "serviceType": "電子喜帖設計", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
           "offers": [offer("網頁電子喜帖（3 種風格同價）", 3800, "交付起 3 個月上線與維護"), offer("延長上線（每月）", 600, "交付 3 個月後每延長 1 個月")]}, faq_ld(web_qa)]
built.append(page("/web-invitation/", "電子喜帖", "網頁電子喜帖客製｜似顏繪＋出席回覆、地圖、倒數 3 種風格 NT$3,800｜編織日和",
                  "似顏繪網頁電子喜帖：開場動畫、婚禮倒數、流程、Dress code、地圖、加入行事曆、出席回覆。書約手繪風、日系清新、雪景 3 種風格同價 NT$3,800，網址不公開、不被搜尋引擎收錄。",
                  "喜帖|電子喜帖|似顏繪網頁電子喜帖", web_body, web_ld))

# ── 紙本喜帖（2026-11-21 新增，價格與規格由 Alison 提供） ──
ENV = ["橘", "紅", "酒紅", "奶茶", "咖啡", "深咖啡", "駝色", "米白", "淺卡其", "淺綠", "橄欖綠", "墨綠", "淺灰", "灰", "深藍", "乾燥玫瑰", "淺粉", "灰紫", "淺灰白", "白", "白（無字）"]
PAPER_FOLIO = [
    ("paper-invitation-welcome-pink-two-pages", "紙本喜帖作品：粉色花園，正面 Welcome 似顏繪、背面邀請資訊", "兩頁設計・粉色花園", 800, 1066),
    ("paper-invitation-garden-cats", "紙本喜帖作品：花拱門下的新人和兩隻貓", "花拱門＋兩隻貓", 700, 935),
    ("paper-invitation-beach-cats", "紙本喜帖作品：海邊的新人和兩隻虎斑貓", "海邊＋虎斑貓", 700, 935),
    ("paper-invitation-beach-heart", "紙本喜帖作品：海邊主題的邀請頁，愛心框裡放似顏繪", "海邊邀請頁", 700, 933),
    ("paper-invitation-welcome-black-dress", "紙本喜帖作品：黑色禮服新娘和西裝新郎在花拱門前", "黑色禮服・花拱門", 700, 935),
    ("paper-invitation-red-wedding-day", "紙本喜帖作品：紅底 Happy Wedding Day，新郎掀起頭紗", "紅底・Wedding Day", 700, 935),
    ("paper-invitation-timeline-dress-code", "紙本喜帖作品：婚禮流程時間軸與 Dress code 色票", "流程與 Dress code 頁", 700, 933),
]
paper_folio = """  <section id="portfolio">
    <div class="wrap">
      <div class="chapter"><span class="no">✦</span><div><span class="kicker">Portfolio</span><h2>紙本喜帖作品</h2><p>可以沿用作品集的設計，也可以討論新的設計；兩種都會收設計費，確保每一份都符合你們。點圖可以放大。</p></div></div>
      <div class="folio-grid" id="folio">
""" + "\n".join(f'        <figure class="rv" style="--i:{i % 4}" data-src="/assets/paper/{f}.webp"><img src="/assets/paper/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy"><figcaption>{cap}</figcaption></figure>' for i, (f, alt, cap, w, h) in enumerate(PAPER_FOLIO)) + """
      </div>
    </div>
  </section>"""
paper_spec = """  <section style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">What you get</span>
      <h2>價格與規格</h2>
      <ul>
        <li><b>固定正反兩頁，設計費 NT$2,500</b>：正面是似顏繪封面，背面是邀請細節與婚宴流程（不做單頁）。背景主題依你們的婚禮客製；複雜的設計另外報價。</li>
        <li><b>信封顏色要先選定</b>：詢價時請從色卡選一個顏色，確定後才排印刷。</li>
        <li><b>印刷每份 NT$105</b>：同款式 <b>30 份起印</b>（30 份 NT$3,150）。</li>
        <li><b>一組包含</b>：1 張喜帖（148×105mm，300 磅雪銅紙）、1 個信封（185×125mm，燙金 Save the Date）、1 枚信封貼紙（古銅色玫瑰蠟封貼，直徑 3cm，背面有雙面膠）。</li>
        <li><b>只寄台灣地址</b>；只提供給訂製似顏繪的新人加購。</li>
        <li>建議在<b>需要拿到喜帖的 4～5 週前</b>訂製。</li>
      </ul>
      <div class="folio-grid" style="margin-top:22px">
        <figure data-src="/assets/paper/card-size-save-the-date.webp"><img src="/assets/paper/card-size-save-the-date.webp" alt="信封尺寸 18.5×12.5cm，燙金 Save the Date" width="900" height="593" loading="lazy"><figcaption>信封 18.5×12.5cm</figcaption></figure>
        <figure data-src="/assets/paper/envelope-burgundy-photo.webp"><img src="/assets/paper/envelope-burgundy-photo.webp" alt="酒紅色信封，燙金 Save the Date 實拍" width="900" height="609" loading="lazy"><figcaption>燙金 Save the Date 實拍</figcaption></figure>
        <figure data-src="/assets/paper/seal-sticker-rose.webp"><img src="/assets/paper/seal-sticker-rose.webp" alt="古銅色玫瑰蠟封信封貼紙" width="500" height="518" loading="lazy"><figcaption>古銅色玫瑰信封貼</figcaption></figure>
      </div>
    </div>
  </section>"""
env_sec = """  <section id="envelope" style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">Envelope colors</span>
      <h2>信封顏色：21 色</h2>
      <p>下訂時備註信封編號就可以。顏色名稱只是方便溝通，實際以色卡為準。</p>
      <div class="folio-grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">
        <figure data-src="/assets/paper/envelope-colors-1-12.webp"><img src="/assets/paper/envelope-colors-1-12.webp" alt="信封色卡 1 到 12 號" width="900" height="1030" loading="lazy"><figcaption>1～12 號</figcaption></figure>
        <figure data-src="/assets/paper/envelope-colors-13-21.webp"><img src="/assets/paper/envelope-colors-13-21.webp" alt="信封色卡 13 到 21 號" width="900" height="797" loading="lazy"><figcaption>13～21 號</figcaption></figure>
      </div>
      <p style="margin-top:16px">""" + "、".join(f"{i + 1}. {c}" for i, c in enumerate(ENV)) + """</p>
    </div>
  </section>"""
paper_flow = """  <section style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">✦</span><div><span class="kicker">How to order</span><h2>訂製步驟</h2><p>確認細節與報價後，我們會提供帳戶，請用匯款付款（目前還沒有信用卡付款）。</p></div></div>
      <ol class="flow">
        <li class="rv"><b>估價＋寄信</b><span>用估價工具勾選，寫好詢價信，附上婚紗照</span></li>
        <li class="rv" style="--i:1"><b>討論設計</b><span>似顏繪、喜帖、結婚書約一起確認</span></li>
        <li class="rv" style="--i:2"><b>確認樣式後下訂</b><span>收到報價與帳戶，匯款後開始製作</span></li>
        <li class="rv" style="--i:3"><b>備註信封顏色</b><span>下訂喜帖時寫信封編號（1～21）</span></li>
        <li class="rv" style="--i:4"><b>印刷寄送</b><span>台灣印製，寄到台灣地址</span></li>
      </ol>
    </div>
  </section>"""
paper_qa = [
    ("紙本喜帖多少錢？", "兩頁設計費 NT$2,500，印刷每份 NT$105，同款式 30 份起印（30 份是 NT$3,150）。另外需要雙人全身彩色似顏繪 NT$1,800；複雜的設計另外報價。"),
    ("一組紙本喜帖包含什麼？", "1 張喜帖（148×105mm，300 磅雪銅紙）、1 個信封（185×125mm，燙金 Save the Date，21 色可選）、1 枚古銅色玫瑰信封貼紙（直徑 3cm）。"),
    ("可以只印喜帖、不訂似顏繪嗎？", "不行。印刷喜帖只提供給訂製似顏繪與喜帖設計的新人加購。可以沿用作品集的設計，也可以討論新設計，兩種都會收設計費。"),
    ("要多久前訂？可以寄到國外嗎？", "建議在需要拿到喜帖的 4～5 週前訂製。紙本喜帖只寄台灣地址；海外新人可以選網頁電子喜帖。"),
    ("怎麼付款？", "確認細節與報價後，我們會提供帳戶，請用匯款付款；目前還沒有信用卡付款。"),
]
paper_body = hero("紙本喜帖", "似顏繪紙本喜帖：<br>把你們的似顏繪印成喜帖",
                  "用你們的似顏繪設計兩頁喜帖，連同燙金信封和蠟封貼紙一起印好。兩頁設計 NT$2,500，印刷每份 NT$105（30 份起），只寄台灣。",
                  '<a class="pill" href="/?paper=1#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#portfolio">看作品</a>') + \
    "\n" + paper_folio + "\n" + paper_spec + "\n" + env_sec + "\n" + paper_flow + "\n" + read_more_auto("/paper-invitation/") + "\n" + faq_sec(paper_qa) + "\n" + cta_sec("開始估價紙本喜帖", "/?paper=1#quote") + "\n" + BUNDLE
paper_ld = [{"@type": "Service", "name": "似顏繪紙本喜帖", "serviceType": "紙本喜帖設計與印刷", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
             "offers": [offer("紙本喜帖 兩頁設計", 2500, "可沿用作品集設計或討論新設計"), offer("紙本喜帖 印刷（每份）", 105, "同款式 30 份起印，含信封與信封貼紙，只寄台灣")]}, faq_ld(paper_qa)]
built.append(page("/paper-invitation/", "紙本喜帖", "似顏繪紙本喜帖客製｜兩頁設計 NT$2,500、每份 NT$105 起印｜編織日和",
                  "似顏繪紙本喜帖：兩頁設計 NT$2,500，印刷每份 NT$105、30 份起印，含 148×105mm 300 磅雪銅喜帖、燙金 Save the Date 信封（21 色）與玫瑰蠟封貼紙。只寄台灣，建議 4～5 週前訂製。",
                  "喜帖|紙本喜帖|似顏繪紙本喜帖", paper_body, paper_ld))

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
      <p>我們相信好的設計，會為重要的日子帶來美感，也帶來力量。品牌由 Zoe 主筆，並和散居各地、同樣過著數位遊牧生活的設計師朋友合作，一起打造屬於你們的似顏繪、結婚書約和電子喜帖。</p>
      <h2>讓台灣的設計被世界看到</h2>
      <p>我們未來也想把服務帶到歐美、日本和西語國家，讓台灣的設計力與品牌被世界看到。網站已經有 <a href="/en/">English</a>、<a href="/ja/">日本語</a>、<a href="/es/">Español</a> 版本，海外的新人也可以找我們畫似顏繪、做電子喜帖。</p>
      <h2>我們也在做的事</h2>
      <p>除了喜帖，我們也經營<a href="https://knittinghiyori.com/">編織日和</a>網站，以及數位遊牧主題的 YouTube 頻道<a href="https://www.youtube.com/@coffeebreak.Japanese" rel="noopener" target="_blank">「1 Hour Pomodoro 25/5 🏙️ | Focus World」</a>。未來，我們期盼成為完全的數位遊牧工作者。</p>
      <h2>聯絡我們</h2>
      <p>請用 Email 聯繫 Zoe<br>Email：<a href="mailto:theperfectmatchfilters@gmail.com">theperfectmatchfilters@gmail.com</a></p>
      <p>也可以先用<a href="/#quote">估價工具</a>選好項目，會自動寫好一封詢價信。</p>
    </div>
  </section>"""
built.append(page("/about/", "關於我們", "關於我們｜同婚伴侶經營的似顏繪喜帖・編織日和",
                  "編織日和的似顏繪喜帖由同婚伴侶經營：相信好的設計帶來美感與力量，與各地數位遊牧的設計師朋友合作，打造似顏繪、結婚書約與電子喜帖。",
                  "喜帖|關於我們|同婚伴侶經營的似顏繪喜帖", about_body))

# ── 部落格文章與首頁（輔助函式在上面「部落格共用」） ──
AUTHOR = [{"@type": "Person", "name": "Zoe"}, {"@type": "Person", "name": "Alison"}]
for P in POSTS:
    check_post(P)
    url = post_url(P)
    cv, ch = P["cover"], P["cheat"]
    meta = f'<p class="meta">{CAT_NAME[P["cat"]]}｜Zoe & Alison｜發布 {P["published"]}' + (f'｜更新 {P["modified"]}' if P["modified"] != P["published"] else "") + "</p>"
    src = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n}</a></li>' for n, u in P["sources"])
    cheat_fig = (f'<figure class="cheat"><img src="/assets/blog/{ch["img"]}" alt="{html.escape(ch["alt"])}" loading="lazy" width="1080" height="1350">'
                 f'<figcaption>{ch.get("caption", strip(ch["title"]).replace(chr(10), ""))}</figcaption>'
                 f'<div class="acts"><a class="pill ghost" href="/assets/blog/{ch["img"]}" download data-cta="cheat_save" data-cta-type="wedding">⬇ 存圖</a></div></figure>')
    sum3 = '<div class="sum3"><b>3 句話看懂</b><ol>' + "".join(f"<li><span>{x}</span></li>" for x in P["summary"]) + "</ol></div>"
    body = f"""  <section class="page-hero post-hero">
    <div class="wrap post" style="padding:0">
      <p class="crumb"><a href="/">似顏繪喜帖</a> › <a href="/blog/">部落格</a> › <a href="/blog/#{P['cat']}">{CAT_NAME[P['cat']]}</a></p>
      <h1>{P['h1']}</h1>
      {meta}
    </div>
  </section>
  <section style="padding-top:0">
    <article class="wrap post">
      <figure class="post-cover"><img src="/assets/blog/{cv['img']}" alt="{html.escape(cv['alt'])}" width="1200" height="630" fetchpriority="high"></figure>
      {sum3}
      {toc(P)}
      <p class="lead-p">{P['lead']}</p>
{P['body'].replace(CHEAT, cheat_fig)}
      {end_card(P['service'])}
      {related(P)}
      <h2 id="faq">常見問題</h2>
      {faq_html(P['faq'])}
      <h2 id="sources">資料來源</h2>
      <ul class="sources">{src}</ul>
    </article>
  </section>
"""
    ld = [{"@type": "BlogPosting", "headline": strip(P["h1"]), "description": P["desc"], "datePublished": P["published"], "dateModified": P["modified"],
           "author": AUTHOR, "publisher": PROVIDER, "mainEntityOfPage": SITE + url, "inLanguage": "zh-Hant-TW", "articleSection": CAT_NAME[P["cat"]],
           "image": [{"@type": "ImageObject", "url": f"{SITE}/assets/blog/{cv['img']}", "width": 1200, "height": 630, "caption": cv["alt"]},
                     {"@type": "ImageObject", "url": f"{SITE}/assets/blog/{ch['img']}", "width": 1080, "height": 1350, "caption": ch["alt"]}]},
          faq_ld(P["faq"])]
    built.append(page(url, strip(P["h1"]).split("：")[0], P["title"], P["desc"], f"喜帖|部落格|{P['ga']}", body, ld,
                      og_image=f"/assets/blog/{cv['img']}", og_alt=cv["alt"], article=(P["published"], P["modified"])))

by_cat = [(c, n, d, sorted((P for P in POSTS if P["cat"] == c), key=lambda x: x["modified"], reverse=True)) for c, n, d in CATS]
by_cat = [x for x in by_cat if x[3]]
blog_body = hero("部落格", "婚禮筆記",
                 "結婚登記要帶什麼、書約法條怎麼寫、婚禮歌單怎麼挑⋯⋯我們把籌備婚禮時用得到的資訊整理在這裡，每篇開頭都先給 3 句話結論。",
                 "") + f"""
  <section style="padding-top:0">
    <div class="wrap">
      <ul class="cats" aria-label="文章分類">{"".join(f'<li><a href="#{c}">{n}（{len(ps)}）</a></li>' for c, n, _, ps in by_cat)}</ul>
      {"".join(f'<div class="blog-cat" id="{c}"><h2>{n}</h2><p>{d}</p><div class="post-list grid">' + "".join(card(P, "blog_card") for P in ps) + "</div></div>" for c, n, d, ps in by_cat) or "<p>第一篇文章準備中。</p>"}
    </div>
  </section>"""
blog_ld = [{"@type": "Blog", "name": "婚禮筆記｜編織日和", "url": SITE + "/blog/", "inLanguage": "zh-Hant-TW", "publisher": PROVIDER,
            "blogPost": [{"@type": "BlogPosting", "headline": strip(P["h1"]), "url": SITE + post_url(P), "datePublished": P["published"], "dateModified": P["modified"],
                          "image": f"{SITE}/assets/blog/{P['cover']['img']}"} for P in POSTS]}]
built.append(page("/blog/", "部落格", "婚禮筆記｜結婚登記、同婚書約與婚禮歌單｜編織日和",
                  "編織日和的婚禮筆記：結婚登記與法規（同性結婚登記、跨國婚姻）、婚禮籌備（婚禮歌單）等籌備婚禮用得到的資訊，每篇開頭先給 3 句話結論。",
                  "喜帖|部落格|婚禮筆記", blog_body, blog_ld, robots="index, follow, max-image-preview:large" if POSTS else "noindex, follow"))

# 3. sitemap：英日西保持原樣，中文分頁只放可收錄的頁
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
sm = re.sub(r"  <!--HY-PAGES-->.*?<!--/HY-PAGES-->\n", "", sm, flags=re.S)
LASTMOD = {post_url(P): P["modified"] for P in POSTS}
LASTMOD["/blog/"] = max(LASTMOD.values(), default=TODAY)
rows = "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{max(TODAY, LASTMOD.get(u, TODAY))}</lastmod></url>\n" for u, ok in built if ok)
sm = sm.replace("</urlset>", f"  <!--HY-PAGES-->\n{rows}  <!--/HY-PAGES-->\n</urlset>")
open(sm_path, "w", encoding="utf-8").write(sm)
print("built:", ", ".join(u + ("" if ok else "（noindex）") for u, ok in built))
