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
/* 紙本喜帖：價格小卡 */
.pcard { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr); gap: 22px 32px; align-items: center; background: var(--cream); border: 2px solid var(--wine); border-radius: 20px; padding: 24px 26px; box-shadow: 6px 6px 0 var(--rose); }
.pcard-n { font-family: var(--serif); color: var(--wine); font-size: 22px; margin: 4px 0 2px; line-height: 1.3; }
.pcard-n b { font-family: var(--latin); font-weight: 400; font-size: clamp(40px, 6vw, 56px); letter-spacing: -.01em; margin-left: 4px; }
.pcard-eq { font-weight: 700; color: var(--ink); margin: 0 0 10px; }
.pcard-more { padding-left: 1.1em; margin: 0 0 16px; font-size: 14.5px; color: var(--muted); }
.pcard-more li { margin-bottom: 4px; }
.pcard-kit-t { font-family: var(--serif); color: var(--wine); font-weight: 700; margin: 0 0 10px; }
.kit3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
.kit3 figure { margin: 0; }
.kit3 img { display: block; width: 100%; aspect-ratio: 1; object-fit: cover; border-radius: 12px; border: 1px solid var(--line); background: #fff; }
.kit3 figcaption { font-size: 13px; color: var(--muted); line-height: 1.45; margin-top: 6px; }
.kit3 figcaption b { display: block; font-family: var(--serif); color: var(--wine); font-size: 16px; }
@media (max-width: 760px) { .pcard { grid-template-columns: 1fr; padding: 20px 18px; } .kit3 { gap: 8px; } .kit3 figcaption { font-size: 12px; } }
/* 電子喜帖：範例入口、安心說明、三步驟 */
.samples { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 18px; }
.samples a { display: block; text-decoration: none; background: var(--cream); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; transition: border-color .2s, transform .2s; }
.samples a:hover { border-color: var(--wine); transform: translateY(-2px); }
.samples b { display: block; font-family: var(--serif); color: var(--wine); font-size: 18px; }
.samples b i { font-style: normal; display: inline-grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--blush); margin-right: 8px; font-size: 14px; }
.samples span { display: block; color: var(--muted); font-size: 14.5px; margin-top: 4px; }
.samples em { display: block; font-style: normal; color: var(--rose-d); font-size: 14px; font-weight: 700; margin-top: 8px; }
.trust { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-top: 18px; }
.trust > div { display: grid; grid-template-columns: 44px 1fr; gap: 14px; align-items: start; background: var(--cream); border: 1px solid var(--line); border-radius: 16px; padding: 18px 20px; }
.trust svg { width: 44px; height: 44px; }
.trust b { display: block; font-family: var(--serif); color: var(--wine); font-size: 17.5px; margin-bottom: 2px; }
.trust p { margin: 0; font-size: 15px; color: var(--ink); }
.steps { list-style: none; padding: 0; margin: 22px 0 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; counter-reset: st; }
.steps li { position: relative; background: var(--cream); border: 1px solid var(--line); border-radius: 18px; padding: 22px 20px 20px; }
.steps .no { position: absolute; top: -14px; left: 18px; font-family: var(--latin); font-size: 13px; letter-spacing: .14em; color: var(--wine); background: var(--blush); border: 1px solid var(--wine); border-radius: 999px; padding: 3px 12px; }
.steps svg { display: block; width: 100%; max-width: 220px; height: auto; margin: 8px auto 12px; }
.steps b { display: block; font-family: var(--serif); color: var(--wine); font-size: 19px; margin-bottom: 6px; }
.steps p { margin: 0; font-size: 15px; }
.steps small { display: block; margin-top: 8px; color: var(--muted); font-size: 13.5px; }
@media (max-width: 860px) { .samples { grid-template-columns: repeat(2, minmax(0, 1fr)); } .steps { grid-template-columns: 1fr; gap: 26px; } .steps svg { max-width: 260px; } }
@media (max-width: 560px) { .trust { grid-template-columns: 1fr; } .samples { gap: 10px; } .samples a { padding: 14px; } }
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
        <div><span class="kicker">All in one</span><h3>想一次搞定？全套方案加送兩份贈品</h3><p>似顏繪＋結婚書約＋網頁電子喜帖＋紙本喜帖四樣都選，加送 Save the Date 分享圖和迎賓板列印檔（例：書約方案 4＋紙本喜帖 30 份，全套 NT$13,630）。同一張似顏繪延伸成整套設計，估價工具會幫你全部勾好，再依需要調整。</p></div>
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
cari_qa = faqs("要準備什麼照片？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "你們會公開我們的作品嗎？", "似顏繪喜帖包含哪些東西？價格怎麼算？")
cari_body = hero("似顏繪", "新人似顏繪：<br>照你們最喜歡的婚紗照畫",
                 "雙人全身彩色似顏繪 NT$1,800，免費修改 2 次；毛小孩、小朋友每位加 NT$800 一起畫進來。這張圖之後可以放進結婚書約和電子喜帖，整套看起來是同一個風格。",
                 '<a class="pill" href="/#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#portfolio">看作品</a>') + \
    "\n" + folio_sec + "\n" + duo_sec + "\n" + flow_sec + "\n" + read_more_auto("/caricature/") + "\n" + faq_sec(cari_qa) + "\n" + cta_sec("開始估價似顏繪", "/#quote") + "\n" + BUNDLE
cari_ld = [{"@type": "Service", "name": "新人似顏繪客製", "serviceType": "婚禮似顏繪", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
            "offers": [offer("雙人全身彩色似顏繪", 1800, "免費修改 2 次"), offer("加畫寵物或小孩（每位）", 800, "毛小孩、小朋友一起入鏡")]}, faq_ld(cari_qa)]
built.append(page("/caricature/", "似顏繪", "新人似顏繪客製｜雙人全身彩色 NT$1,800、可加畫寵物｜編織日和",
                  "新人似顏繪：照婚紗照畫雙人全身彩色似顏繪 NT$1,800，免費修改 2 次，加畫寵物或小孩每位 NT$800。西式婚紗、和服、中式禮服都能畫，可延伸做結婚書約與電子喜帖。",
                  "喜帖|似顏繪|新人似顏繪客製", cari_body, cari_ld, extra_js=""))

# 電子喜帖：直接打開範例
SAMPLES = """  <section style="padding-top:0">
    <div class="wrap prose" style="max-width:none">
      <span class="kicker">Live demo</span>
      <h2>直接打開範例喜帖</h2>
      <p>範例就是成品的樣子，用手機打開最準。右下角可以切換配色。</p>
      <div class="samples">
        <a href="/a/" target="_blank" rel="noopener" data-cta="style_a" data-cta-type="wedding"><b><i>A</i>書約手繪風</b><span>黑線小花和拱門</span><em>打開範例 ↗</em></a>
        <a href="/b/" target="_blank" rel="noopener" data-cta="style_b" data-cta-type="wedding"><b><i>B</i>日系清新</b><span>拉門開場、直書</span><em>打開範例 ↗</em></a>
        <a href="/c/" target="_blank" rel="noopener" data-cta="style_c" data-cta-type="wedding"><b><i>C</i>雪景</b><span>雪山和燈串</span><em>打開範例 ↗</em></a>
        <a href="/a/?photo" target="_blank" rel="noopener" data-cta="style_photo" data-cta-type="wedding"><b><i>♡</i>婚紗照版</b><span>不畫似顏繪，放你們的照片；A、B、C 都能做</span><em>打開範例 ↗</em></a>
      </div>
    </div>
  </section>"""

# 線條小圖示（酒紅線＋粉色塊，跟首頁同色系）
def ico(body):
    return f'<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="#5a2232" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'

TRUST_ITEMS = [
    ('<path d="M24 5l15 6v11c0 10-6.5 17-15 21C15.5 39 9 32 9 22V11z" fill="#f5dfe0"/><path d="M17 24l5 5 9-10"/>',
     "賓客資料留在你們手上", "喜帖是我們在台灣製作的獨立網頁，不是外部平台或 App。賓客不用下載、不用註冊，也不會被要求留下個資。"),
    ('<rect x="7" y="9" width="34" height="30" rx="5" fill="#f5dfe0"/><path d="M14 18h20M14 25h14M14 32h9"/><path d="M33 29l6 6M39 29l-6 6"/>',
     "全繁體中文，沒有廣告", "頁面上只有你們的內容：沒有簡體字、沒有跳出來的廣告，也沒有別人家的商標。"),
    ('<rect x="5" y="10" width="28" height="20" rx="3"/><path d="M13 36h12M19 30v6"/><rect x="31" y="16" width="12" height="22" rx="3" fill="#f5dfe0"/><path d="M35.5 34h3"/>',
     "手機、電腦都好讀", "先照手機畫面設計，賓客在 LINE 裡點開就能看；用電腦打開版面一樣完整。"),
    ('<circle cx="16" cy="18" r="7" fill="#f5dfe0"/><circle cx="31" cy="15" r="6"/><circle cx="33" cy="31" r="7" fill="#e6a9b5"/><circle cx="17" cy="33" r="5"/>',
     "文字、照片、配色可以換", "名字、日期、流程、Dress code 和照片都照你們的寫；每種風格有幾款配色可選。動畫、版型和字型是固定設計，這樣才能把品質和交期顧好。"),
    ('<rect x="6" y="12" width="26" height="28" rx="3" fill="#f5dfe0"/><rect x="14" y="7" width="28" height="28" rx="3" fill="#fffaf7"/><path d="M18 30l7-8 5 5 4-4 6 7"/><circle cx="33" cy="15" r="2.5"/>',
     "最多放 20 張照片", "婚紗照、生活照都可以，做成左右滑的照片區，點開看大圖。"),
    ('<rect x="9" y="6" width="30" height="36" rx="4" fill="#f5dfe0"/><path d="M16 16h16M16 23h16M16 30h9"/><path d="M28 32l3 3 6-7"/>',
     "出席回覆用你們自己的表單", "回覆表單由你們用習慣的 Google 表單或 SurveyCake 建立，喜帖放上連結。回覆直接進你們的帳號，我們拿不到賓客的個人資料。"),
    ('<path d="M20 28l8-8"/><path d="M23 13l4-4a7 7 0 0 1 10 10l-4 4"/><path d="M25 35l-4 4a7 7 0 0 1-10-10l4-4"/><rect x="28" y="30" width="15" height="11" rx="2" fill="#f5dfe0"/>',
     "專屬網址＋分享預覽圖", "每對新人一個網址（用婚禮日期和英文名），貼到 LINE、Facebook 會出現你們的預覽圖。不讓搜尋引擎收錄，只有拿到連結的人看得到。"),
    ('<rect x="7" y="10" width="34" height="31" rx="4" fill="#f5dfe0"/><path d="M7 19h34M16 6v8M32 6v8"/><path d="M17 30l5 5 9-10"/>',
     "交付起 3 個月保證打得開", "從交付當天算起 3 個月內網址都有效，婚禮後也能回來看；想放久一點，每延長 1 個月 NT$600。"),
]
TRUST = """  <section style="padding-top:0">
    <div class="wrap prose" style="max-width:none">
      <span class="kicker">Peace of mind</span>
      <h2>寄給長輩和朋友之前，你可能想知道的事</h2>
      <div class="trust">
""" + "\n".join(f"        <div>{ico(i)}<div><b>{t}</b><p>{d}</p></div></div>" for i, t, d in TRUST_ITEMS) + """
      </div>
    </div>
  </section>"""

# 三步驟（每一步一張小插圖）
STEP_ART = [
    # 1. 手機上的估價單＋信封
    '<svg viewBox="0 0 220 130" aria-hidden="true" fill="none" stroke="#5a2232" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="110" cy="118" rx="88" ry="7" fill="#f5dfe0" stroke="none"/>'
    '<rect x="48" y="8" width="62" height="108" rx="10" fill="#fffaf7"/><path d="M70 16h18"/>'
    '<rect x="57" y="28" width="44" height="10" rx="3" fill="#f5dfe0"/><path d="M58 48h10M74 48h26M58 58h10M74 58h20M58 68h10M74 68h24"/>'
    '<path d="M58 82h42"/><path d="M80 92h20" stroke-width="3"/>'
    '<rect x="57" y="100" width="44" height="10" rx="5" fill="#e6a9b5"/>'
    '<g transform="translate(122 46) rotate(-8)"><rect width="66" height="44" rx="4" fill="#fffaf7"/><path d="M2 3l31 22L64 3"/><circle cx="33" cy="30" r="6" fill="#e6a9b5"/></g>'
    '<path d="M114 40c6-8 14-10 22-8" stroke-dasharray="3 5"/></svg>',
    # 2. 報價單＋勾勾
    '<svg viewBox="0 0 220 130" aria-hidden="true" fill="none" stroke="#5a2232" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="110" cy="118" rx="88" ry="7" fill="#f5dfe0" stroke="none"/>'
    '<path d="M60 10h70l14 14v90H60z" fill="#fffaf7"/><path d="M130 10v14h14"/>'
    '<path d="M72 34h40M72 46h52M72 58h46M72 70h52"/><path d="M72 88h22M108 88h24" stroke-width="3"/>'
    '<circle cx="150" cy="92" r="20" fill="#e6a9b5"/><path d="M141 92l7 7 12-14" stroke-width="2.4"/>'
    '<path d="M40 40l-8-4M40 54h-10M40 68l-8 4"/></svg>',
    # 3. 手機上的成品喜帖＋照片＋愛心
    '<svg viewBox="0 0 220 130" aria-hidden="true" fill="none" stroke="#5a2232" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="110" cy="118" rx="88" ry="7" fill="#f5dfe0" stroke="none"/>'
    '<g transform="translate(30 30) rotate(-10)"><rect width="46" height="56" rx="3" fill="#fffaf7"/><rect x="5" y="5" width="36" height="36" fill="#f5dfe0"/><path d="M8 38l10-12 8 8 6-5 9 9"/></g>'
    '<rect x="84" y="8" width="62" height="108" rx="10" fill="#fffaf7"/><path d="M106 16h18"/>'
    '<path d="M98 76V46a17 17 0 0 1 34 0v30z" fill="#f5dfe0"/><path d="M104 32c2-4 6-6 11-6"/>'
    '<path d="M96 88h38M102 98h26"/>'
    '<path d="M174 40c-9-6-12-11-10-15 2-3 7-3 10 1 3-4 8-4 10-1 2 4-1 9-10 15z" fill="#e6a9b5"/>'
    '<path d="M164 70l18-6M166 84l16 2" stroke-dasharray="3 5"/></svg>',
]
STEP_TXT = [
    ("估價、寄出詢價信", "在估價工具選風格和配色（要不要加似顏繪也在這裡選），價格馬上算好，按一下就寄出詢價信。", "看得到總價才寄，不用先私訊問價。"),
    ("確認報價、付款", "我們回信確認細節和最終報價，附上匯款帳號；收到全額匯款就幫你們排進製作。", "開始畫草稿前取消可以全額退款。"),
    ("給資料與照片、看草稿、交付", "寄來喜帖文字和照片，我們做好草稿給你們確認，修改後交付專屬網址和分享預覽圖。", "一般約 4～5 週，建議婚禮前 2 個月詢價。"),
]
STEPS = """  <section style="padding-top:0">
    <div class="wrap prose" style="max-width:none">
      <span class="kicker">How to order</span>
      <h2>簡單三步驟訂購</h2>
      <ol class="steps">
""" + "\n".join(f'        <li><span class="no">STEP {i + 1}</span>{art}<b>{t}</b><p>{d}</p><small>{n}</small></li>' for i, (art, (t, d, n)) in enumerate(zip(STEP_ART, STEP_TXT))) + """
      </ol>
    </div>
  </section>"""

# ── 電子喜帖 ──
web_qa = faqs("電子喜帖可以用多久？會被搜尋到嗎？", "可以修改幾次？", "製作要多久？可以趕急件嗎？", "怎麼付款？什麼時候開始製作？")
web_body = hero("電子喜帖", "網頁電子喜帖：<br>手機一點就開，賓客線上回覆出席",
                "把你們的似顏繪做成喜帖網頁：開場動畫、婚禮倒數、婚宴流程、Dress code、地圖、加入行事曆、出席回覆都在裡面。3 種風格同價 NT$3,800，搭配雙人似顏繪 NT$1,800；不畫似顏繪、改放婚紗照的婚紗照版，總價就是 NT$3,800。",
                '<a class="pill" href="/?web=A#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a><a class="pill ghost" href="#web">看 3 種風格</a>') + \
    "\n" + web_sec + "\n" + SAMPLES + "\n" + TRUST + "\n" + STEPS + "\n" + read_more_auto("/web-invitation/") + "\n" + faq_sec(web_qa) + "\n" + cta_sec("開始估價電子喜帖", "/?web=A#quote") + "\n" + BUNDLE
web_ld = [{"@type": "Service", "name": "似顏繪網頁電子喜帖", "serviceType": "電子喜帖設計", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
           "offers": [offer("網頁電子喜帖（3 種風格同價）", 3800, "交付起 3 個月上線與維護"), offer("網頁電子喜帖婚紗照版（不畫似顏繪）", 3800, "放新人的婚紗照，交付起 3 個月上線與維護"), offer("延長上線（每月）", 600, "交付 3 個月後每延長 1 個月")]}, faq_ld(web_qa)]
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
# 紙本喜帖：第一屏價格小卡（30 份總價直接算好）＋一組包含的 3 樣東西
PAPER_DESIGN, PAPER_EACH, PAPER_MIN = 2000, 105, 30
def ntd(n):
    return f"NT${n:,}"
PAPER_KIT = [
    ("paper-invitation-welcome-pink-two-pages", "似顏繪紙本喜帖，正面似顏繪封面、背面邀請資訊", 800, 1066, "喜帖", "148×105mm，300 磅雪銅紙，正反兩頁"),
    ("envelope-burgundy-photo", "酒紅色信封，燙金 Save the Date 實拍", 900, 609, "燙金信封", "185×125mm，燙金 Save the Date，21 色"),
    ("seal-sticker-rose", "古銅色玫瑰蠟封信封貼紙", 500, 518, "蠟封貼紙", "古銅色玫瑰，直徑 3cm，背面有雙面膠"),
]
paper_price = f"""  <section id="price" style="padding-top:0">
    <div class="wrap">
      <div class="pcard">
        <div class="pcard-sum">
          <span class="kicker">Price</span>
          <p class="pcard-n">30 份 <b>{ntd(PAPER_DESIGN + PAPER_EACH * PAPER_MIN)}</b></p>
          <p class="pcard-eq">兩頁設計 {ntd(PAPER_DESIGN)}＋印刷 {ntd(PAPER_EACH * PAPER_MIN)}（每份 {ntd(PAPER_EACH)}）</p>
          <ul class="pcard-more">
            <li>每多 1 份 +{ntd(PAPER_EACH)}：40 份 {ntd(PAPER_DESIGN + PAPER_EACH * 40)}、50 份 {ntd(PAPER_DESIGN + PAPER_EACH * 50)}</li>
            <li>同款式 30 份起印，加印也是 30 份起</li>
            <li>另需雙人全身彩色似顏繪 NT$1,800；複雜的設計另外報價</li>
          </ul>
          <a class="pill" href="/?paper=1#quote" data-cta="page_quote" data-cta-type="wedding">開始估價 <span class="arr">→</span></a>
        </div>
        <div class="pcard-kit">
          <p class="pcard-kit-t">一組包含這 3 樣</p>
          <div class="kit3">
""" + "\n".join(f'            <figure data-src="/assets/paper/{f}.webp"><img src="/assets/paper/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy"><figcaption><b>{t}</b>{d}</figcaption></figure>' for f, alt, w, h, t, d in PAPER_KIT) + """
          </div>
        </div>
      </div>
    </div>
  </section>"""
paper_folio = """  <section id="portfolio" style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">✦</span><div><span class="kicker">Portfolio</span><h2>紙本喜帖作品</h2><p>可以沿用作品集的設計，也可以依你們的婚禮主題設計新的。正面是似顏繪封面，背面是邀請細節與婚宴流程（固定兩頁，不做單頁）。</p></div></div>
      <div class="folio-grid" id="folio">
""" + "\n".join(f'        <figure class="rv" style="--i:{i % 4}" data-src="/assets/paper/{f}.webp"><img src="/assets/paper/{f}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy"><figcaption>{cap}</figcaption></figure>' for i, (f, alt, cap, w, h) in enumerate(PAPER_FOLIO)) + """
      </div>
    </div>
  </section>"""
env_sec = """  <section id="envelope" style="padding-top:0">
    <div class="wrap prose">
      <span class="kicker">Envelope colors</span>
      <h2>信封顏色：21 色</h2>
      <p>詢價時從色卡選一個顏色，寫上編號就可以；確定顏色後才排印刷。顏色名稱只是方便溝通，實際以色卡為準。</p>
      <div class="folio-grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">
        <figure data-src="/assets/paper/envelope-colors-1-12.webp"><img src="/assets/paper/envelope-colors-1-12.webp" alt="信封色卡 1 到 12 號" width="900" height="1030" loading="lazy"><figcaption>1～12 號</figcaption></figure>
        <figure data-src="/assets/paper/envelope-colors-13-21.webp"><img src="/assets/paper/envelope-colors-13-21.webp" alt="信封色卡 13 到 21 號" width="900" height="797" loading="lazy"><figcaption>13～21 號</figcaption></figure>
      </div>
      <p style="margin-top:16px">""" + "、".join(f"{i + 1}. {c}" for i, c in enumerate(ENV)) + """</p>
    </div>
  </section>"""

# 安心清單、三步驟（版型和電子喜帖頁一樣：.trust、.steps，ico() 在電子喜帖段定義）

PAPER_TRUST_ITEMS = [
    ('<path d="M24 5l15 6v11c0 10-6.5 17-15 21C15.5 39 9 32 9 22V11z" fill="#f5dfe0"/><path d="M17 24l5 5 9-10"/>',
     "台灣印製", "喜帖、信封、貼紙都在台灣印製，印好直接寄到你們指定的台灣地址。"),
    ('<rect x="9" y="6" width="30" height="36" rx="4" fill="#f5dfe0"/><path d="M16 16h16M16 23h16M16 30h9"/><path d="M28 32l3 3 6-7"/>',
     "校稿確認才印", "設計可以免費修改 2 次，你們確認校稿後才送印。定稿後就不能再改；超過免費次數或定稿後要修改，會酌收費用。"),
    ('<circle cx="18" cy="24" r="12" fill="#f5dfe0"/><circle cx="30" cy="24" r="12"/><path d="M24 14v20"/>',
     "先知道會有一點色差", "螢幕發光、紙張印墨水，印出來的顏色通常比螢幕上稍微暗、稍微淡一點。信封顏色以色卡為準。"),
    ('<path d="M6 16h24v18H6z" fill="#f5dfe0"/><path d="M30 22h7l5 6v6H30z"/><circle cx="13" cy="36" r="3.5" fill="#fffaf7"/><circle cx="35" cy="36" r="3.5" fill="#fffaf7"/>',
     "只寄台灣地址", "紙本喜帖只寄台灣；海外新人可以選網頁電子喜帖，用連結傳給賓客。"),
]
PAPER_TRUST = """  <section style="padding-top:0">
    <div class="wrap prose" style="max-width:none">
      <span class="kicker">Peace of mind</span>
      <h2>下訂之前，你可能想知道的事</h2>
      <div class="trust">
""" + "\n".join(f"        <div>{ico(i)}<div><b>{t}</b><p>{d}</p></div></div>" for i, t, d in PAPER_TRUST_ITEMS) + """
      </div>
    </div>
  </section>"""

_SV = '<svg viewBox="0 0 220 130" aria-hidden="true" fill="none" stroke="#5a2232" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="110" cy="118" rx="88" ry="7" fill="#f5dfe0" stroke="none"/>'
PAPER_STEP_ART = [
    # 1. 手機上的估價單＋信封
    _SV + '<rect x="48" y="8" width="62" height="108" rx="10" fill="#fffaf7"/><path d="M70 16h18"/>'
    '<rect x="57" y="28" width="44" height="10" rx="3" fill="#f5dfe0"/><path d="M58 48h10M74 48h26M58 58h10M74 58h20M58 68h10M74 68h24"/>'
    '<path d="M58 82h42"/><path d="M80 92h20" stroke-width="3"/><rect x="57" y="100" width="44" height="10" rx="5" fill="#e6a9b5"/>'
    '<g transform="translate(122 46) rotate(-8)"><rect width="66" height="44" rx="4" fill="#fffaf7"/><path d="M2 3l31 22L64 3"/><circle cx="33" cy="30" r="6" fill="#e6a9b5"/></g>'
    '<path d="M114 40c6-8 14-10 22-8" stroke-dasharray="3 5"/></svg>',
    # 2. 喜帖草稿＋勾勾
    _SV + '<rect x="46" y="14" width="64" height="92" rx="4" fill="#fffaf7"/><path d="M60 64V40a18 18 0 0 1 36 0v24z" fill="#f5dfe0"/><path d="M60 78h36M66 88h24"/>'
    '<rect x="118" y="14" width="64" height="92" rx="4" fill="#fffaf7"/><path d="M130 30h40M130 42h32M130 54h40M130 66h28M130 78h36"/>'
    '<circle cx="172" cy="96" r="18" fill="#e6a9b5"/><path d="M164 96l6 6 11-13" stroke-width="2.4"/></svg>',
    # 3. 印好的喜帖＋蠟封信封
    _SV + '<g transform="translate(40 26) rotate(-8)"><rect width="56" height="76" rx="3" fill="#fffaf7"/><path d="M12 48V30a16 16 0 0 1 32 0v18z" fill="#f5dfe0"/><path d="M12 60h32"/></g>'
    '<rect x="104" y="42" width="84" height="58" rx="4" fill="#fffaf7"/><path d="M106 45l40 28 40-28"/><circle cx="146" cy="74" r="9" fill="#e6a9b5"/>'
    '<path d="M118 92h20" stroke-width="2.4" stroke="#c97487"/><path d="M168 24l4 8 8 2-8 3-4 8-3-8-8-3 8-2z" fill="#f5dfe0"/></svg>',
]
PAPER_STEP_TXT = [
    ("估價、寄出詢價信", "在估價工具勾選紙本喜帖、填份數，總價馬上算好，按一下寄出詢價信，附上婚紗照和想要的信封顏色。", "建議在需要拿到喜帖的 3～5 週前詢價。"),
    ("確認設計並付款", "似顏繪、喜帖設計一起討論，確認樣式和最終報價後，我們提供帳戶，匯款後開始製作。", "目前只能匯款，還沒有信用卡付款。"),
    ("校稿、印刷、寄送", "設計可以免費修改 2 次，你們確認校稿後送印，台灣印製，寄到台灣地址。", "定稿後不能再改；之後要修改會酌收費用。"),
]
PAPER_STEPS = """  <section style="padding-top:0">
    <div class="wrap prose" style="max-width:none">
      <span class="kicker">How to order</span>
      <h2>簡單三步驟訂購</h2>
      <ol class="steps">
""" + "\n".join(f'        <li><span class="no">STEP {i + 1}</span>{art}<b>{t}</b><p>{d}</p><small>{n}</small></li>' for i, (art, (t, d, n)) in enumerate(zip(PAPER_STEP_ART, PAPER_STEP_TXT))) + """
      </ol>
    </div>
  </section>"""
paper_qa = [
    ("紙本喜帖多少錢？", "兩頁設計費 NT$2,000，印刷每份 NT$105，同款式 30 份起印，所以 30 份總共 NT$5,150（設計 NT$2,000＋印刷 NT$3,150）。另外需要雙人全身彩色似顏繪 NT$1,800；複雜的設計另外報價。"),
    ("一組紙本喜帖包含什麼？", "1 張喜帖（148×105mm，300 磅雪銅紙）、1 個信封（185×125mm，燙金 Save the Date，21 色可選）、1 枚古銅色玫瑰信封貼紙（直徑 3cm）。"),
    ("設計可以改幾次？", "設計可以免費修改 2 次。你們確認校稿（定稿）後就會送印，不能再改；超過免費次數或定稿後要修改，會酌收費用。"),
    ("會有色差嗎？", "會有一點。螢幕是發光顯示，紙張是用墨水印刷，印出來的顏色通常會比螢幕上稍微暗、稍微淡一點，每支手機和電腦螢幕看到的也不太一樣。信封顏色請以色卡為準。"),
    ("可以加印嗎？", "可以。加印一樣是同款式 30 份起印，每份 NT$105（30 份 NT$3,150）。份數不確定的話，建議第一次訂就把可能要的份數一起算進去。"),
    ("可以只印喜帖、不訂似顏繪嗎？", "不行。印刷喜帖只提供給訂製似顏繪與喜帖設計的新人加購。可以沿用作品集的設計，也可以討論新設計，兩種都會收設計費。"),
    ("要多久前訂？可以寄到國外嗎？", "建議在需要拿到喜帖的 3～5 週前訂製。紙本喜帖只寄台灣地址；海外新人可以選網頁電子喜帖。"),
    ("怎麼付款？", "確認細節與報價後，我們會提供帳戶，請用匯款付款；目前還沒有信用卡付款。"),
]
paper_body = hero("紙本喜帖", "似顏繪紙本喜帖：<br>把你們的似顏繪印成喜帖",
                  "用你們的似顏繪設計兩頁喜帖，連同燙金信封和蠟封貼紙一起在台灣印好，寄到台灣地址。",
                  '<a class="pill ghost" href="#portfolio">看作品</a><a class="pill ghost" href="#faq">常見問題</a>') + \
    "\n" + paper_price + "\n" + PAPER_TRUST + "\n" + PAPER_STEPS + "\n" + paper_folio + "\n" + env_sec + "\n" + read_more_auto("/paper-invitation/") + "\n" + faq_sec(paper_qa) + "\n" + cta_sec("開始估價紙本喜帖", "/?paper=1#quote") + "\n" + BUNDLE
paper_ld = [{"@type": "Service", "name": "似顏繪紙本喜帖", "serviceType": "紙本喜帖設計與印刷", "areaServed": {"@type": "Country", "name": "Taiwan"}, "provider": PROVIDER,
             "offers": [offer("紙本喜帖 兩頁設計", PAPER_DESIGN, "可沿用作品集設計或討論新設計，免費修改 2 次"), offer("紙本喜帖 印刷（每份）", PAPER_EACH, "同款式 30 份起印（加印也是），含信封與信封貼紙，只寄台灣")]}, faq_ld(paper_qa)]
built.append(page("/paper-invitation/", "紙本喜帖", "似顏繪紙本喜帖客製｜30 份 NT$5,150（設計 NT$2,000＋每份 NT$105）｜編織日和",
                  "似顏繪紙本喜帖：30 份 NT$5,150（兩頁設計 NT$2,000＋印刷每份 NT$105，30 份起印），含 300 磅雪銅喜帖、燙金 Save the Date 信封（21 色）與玫瑰蠟封貼紙。免費修改 2 次，台灣印製只寄台灣，建議 3～5 週前訂製。",
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
