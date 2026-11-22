"""產生「回台結婚」全包專案頁（中文 /taiwan-wedding/、英文 /en/taiwan-wedding/）。
版面與 CSS 沿用中文首頁 index.html；作品集用 folio.py。
用法：python3 tools/build_package.py          → 輸出到 _proposals/package/（本機預覽，noindex）
      python3 tools/build_package.py --live   → 輸出到 taiwan-wedding/ 與 en/taiwan-wedding/
改價只改 PRICE_TWD、PRICE_USD。
"""
import json, os, re, sys
import folio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "--live" in sys.argv
BASE = "https://wedding.knittinghiyori.com"
MAIL = "theperfectmatchfilters@gmail.com"
PRICE_TWD, PRICE_USD = "22,000", "690"
PATHS = {"zh": "/taiwan-wedding/", "en": "/en/taiwan-wedding/"}

zh_home = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
STYLE = re.search(r"<style>.*?</style>", zh_home, re.S).group(0)
TRACK = zh_home[zh_home.index("<script>\n/* 點擊追蹤"):zh_home.index("</body>")]

EXTRA = """
<style>
.inc { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 40px; border-top: 1px solid var(--wine); }
.inc li { list-style: none; padding: 22px 0; border-bottom: 1px solid var(--line); display: grid; grid-template-columns: 44px 1fr; gap: 4px 12px; }
.inc li i { font-family: var(--latin); font-style: italic; color: var(--rose-d); font-size: 20px; grid-row: span 2; }
.inc li b { font-family: var(--serif); font-size: 19px; color: var(--wine); letter-spacing: .03em; }
.inc li span { color: var(--muted); font-size: 15px; }
.who { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
.who article { background: var(--cream); border: 1px solid var(--wine); border-radius: 22px; padding: 28px 30px; }
.who h3 { font-family: var(--serif); color: var(--wine); font-size: 21px; margin-bottom: 6px; }
.who p { color: var(--muted); }
.pricebox { background: var(--wine); color: var(--cream); border-radius: 28px; padding: clamp(30px, 5vw, 56px); display: grid; grid-template-columns: 1.1fr 1fr; gap: 30px; align-items: center; }
.pricebox .big { font-family: var(--latin); font-size: clamp(52px, 8vw, 96px); line-height: 1; }
.pricebox .alt { font-family: var(--latin); font-size: 26px; color: var(--rose); margin-top: 8px; }
.pricebox ul { list-style: none; display: grid; gap: 10px; color: #e8cfd4; font-size: 15.5px; }
.pricebox li::before { content: "✓ "; color: var(--rose); }
.pricebox .pill { background: var(--rose); margin-top: 22px; }
.cmp { width: 100%; border-collapse: collapse; font-size: 15.5px; }
.cmp th, .cmp td { padding: 14px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.cmp th { font-family: var(--serif); color: var(--wine); font-size: 16px; }
.cmp td:nth-child(3), .cmp th:nth-child(3) { background: var(--blush); }
.cmp-wrap { overflow-x: auto; }
.hero h1 { letter-spacing: .04em; }
@media (max-width: 760px) { .inc, .who, .pricebox { grid-template-columns: 1fr; } .cmp { font-size: 14.5px; min-width: 520px; } }
</style>"""

EN_FONT = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<style>:root { --serif: "Bodoni Moda", serif; --sans: "Inter", system-ui, sans-serif; } .hero h1 { letter-spacing: .01em; }</style>"""

T = {
"zh": dict(
    html="zh-Hant-TW", page_lang="zh-Hant", og_locale="zh_TW", brand="編織日和", site="・似顏繪喜帖",
    title="回台結婚全包專案｜似顏繪、結婚書約、雙語電子喜帖｜編織日和",
    desc=f"住在國外、要回台灣結婚的新人專案：雙人似顏繪、結婚書約 PDF、中英雙語電子喜帖、外國賓客專區、迎賓板與 Save the Date，一次備齊 NT${PRICE_TWD}（US${PRICE_USD}）。全程線上，不用收包裹。",
    og_title="回台結婚全包專案｜似顏繪、書約、雙語電子喜帖",
    nav=["專案內容", "價格", "流程", "常見問題"], nav_cta="詢問專案",
    big=("Home", "to wed"), vert="回台結婚・雙語喜帖・似顏繪",
    h1="住在國外，<b>回台灣結婚</b>：<br>似顏繪、書約、雙語喜帖一次備齊",
    lead="人在國外，不方便收包裹、也沒時間一樣一樣找廠商。我們把婚禮需要的畫和喜帖都做成數位檔，全程用 Email 完成。兩位都是台灣人，或另一半是外國人，都適合。",
    cta1="詢問專案", cta2="看專案內容",
    who_k="For you", who_h="這個專案適合誰", who_p="",
    who=[("兩位都是台灣人，住在國外", "回台辦婚禮，親友分散在不同國家。一個連結，長輩和朋友都收得到。"), ("另一半是外國人", "喜帖中文、英文都有，外國親友看得懂；還有一區專門告訴他們怎麼到會場、紅包怎麼包。")],
    inc_k="What’s included", inc_h="專案內容", inc_p="以下全部包含在專案價格裡。",
    inc=[
        ("雙人全身彩色似顏繪", "照你們喜歡的照片畫；可以加 1 隻寵物或 1 位小孩；可修改 4 次。"),
        ("結婚書約設計＋PDF", "台灣戶政登記用的書約格式，交付可列印的 PDF，自己印或請家人印。"),
        ("中英雙語電子喜帖", "同一個連結，中文、英文可以切換。三種風格任選，上線 6 個月。"),
        ("外國賓客專區", "機場到會場怎麼走、住宿建議、台灣婚禮小禮儀（例如紅包），放在喜帖裡。"),
        ("雙語出席回覆表單", "我們提供做好的表單範本，你們用自己的 Google 帳號建立副本。賓客的回覆只在你們手上，我們看不到。"),
        ("迎賓板檔案＋Save the Date 圖", "用同一張似顏繪做成可列印的迎賓板，以及可以發在社群的 Save the Date 圖。"),
    ],
    addon="需要印刷嗎？書約或紙本喜帖可以另外加購，印好後用郵局掛號寄到你們在台灣的收件地址（另外報價）。",
    cmp_k="Compare", cmp_h="和單點有什麼不同", cmp_head=["項目", "單點", "回台結婚專案"],
    cmp=[("電子喜帖語言", "單一語言", "中英雙語，可切換"), ("喜帖上線時間", "交付起 3 個月", "交付起 6 個月"), ("似顏繪修改", "2 次", "4 次"), ("加畫寵物或小孩", "每位 +NT$800", "含 1 位"),
         ("出席回覆表單", "新人自己建立", "提供雙語範本"), ("外國賓客專區", "沒有", "有"), ("迎賓板與 Save the Date", "沒有", "有")],
    price_k="One price", price_h="專案價格", price_alt=f"或 US${PRICE_USD}",
    price_li=["台幣：轉帳到台灣帳戶", "美金：用 Wise 付款", "一次付清後開始製作", "開始畫草稿前可以全額退款；開始畫之後不退款"],
    how_k="How it works", how_h="從詢問到交件", how_p="一般製作約 4～5 週，建議在婚禮前<b>至少 2 個月</b>詢問。",
    steps=[("寄信詢問", "告訴我們婚禮日期和城市"), ("確認內容與報價", "我們回信確認細節"), ("付款", "台幣轉帳或 Wise"), ("寄照片與資料", "婚紗照、喜帖文字"), ("確認草稿與交件", "全部用 Email 完成")],
    rush_h="急件", rush_p="比 4 週短算急件：要看當下案量，排得進來才接，急件費是總價的 30%。",
    share_h="作品公開與隱私", share_p="完成的設計可能放在網站或社群作為作品展示；不會公開你們的個人資料和提供的照片。每份喜帖都是不公開的網址，搜尋引擎找不到。",
    faq_h="常見問題",
    faq=[
        ("回台結婚專案包含什麼？多少錢？", f"包含雙人似顏繪、結婚書約 PDF、中英雙語電子喜帖、外國賓客專區、雙語出席回覆表單範本、迎賓板檔案和 Save the Date 圖，專案價 NT${PRICE_TWD}（或 US${PRICE_USD}）。"),
        ("人在國外，要怎麼付款？", "可以用台幣轉帳到台灣的帳戶，或用 Wise 付美金。確認內容後我們會提供付款資訊，一次付清後開始製作。"),
        ("可以退款嗎？", "開始畫草稿之前取消，可以全額退款；開始畫之後就不退款。"),
        ("我們不在台灣，東西怎麼收？", "專案內容全部是數位檔，用 Email 交付，不用收包裹。如果加購印刷，會用郵局掛號寄到你們在台灣的收件地址。"),
        ("賓客的回覆資料會經過你們嗎？", "不會。出席回覆表單是你們用自己的 Google 帳號建立的，賓客的回覆只存在你們的帳號裡。"),
        ("喜帖可以用中文和英文以外的語言嗎？", "可以加日文或西班牙文，請在詢問時告訴我們。"),
        ("結婚書約可以用在戶政登記嗎？", "書約是照台灣戶政登記用的結婚書約格式設計的。登記需要的證件和流程，請以戶政事務所的規定為準。"),
        ("製作要多久？", "一般約 4～5 週，建議在婚禮前至少 2 個月詢問。比 4 週短算急件，排得進來才接，急件費是總價的 30%。"),
        ("同婚可以做嗎？", "可以，結婚書約會用對應的法條版本。"),
    ],
    end_h="Let’s draw <span>your day.</span>", end_p=f"聯絡人與插畫：Zoe @KnittingHiyori<br>只用 Email 聯絡：{MAIL}", end_cta="詢問專案",
    other=("只需要其中一項？", "看單點價目表", "/"),
    mail_subject="【回台結婚專案詢問】", mail_body="你好，我想詢問回台結婚專案。\n\n稱呼：\n目前居住的國家：\n婚禮日期：\n婚禮城市／會場：\n喜帖語言（中英，或加其他語言）：\n想用的付款方式（台幣轉帳／Wise 美金）：\n其他想說的：\n",
    legal="本站使用 Cookie 進行流量分析（Google Analytics）。", privacy="隱私權政策", close="關閉",
),
"en": dict(
    html="en", page_lang="en", og_locale="en_US", brand="Knitting Hiyori", site=" · Illustrated Wedding",
    title="Getting Married in Taiwan: Illustrated Wedding Package | Portrait, Bilingual Invitation | Knitting Hiyori",
    desc=f"For couples living abroad who are getting married in Taiwan: a hand-drawn couple portrait, Taiwan marriage certificate design (PDF), a bilingual Chinese and English wedding invitation website, a guide for overseas guests, welcome sign and save-the-date. One package, US${PRICE_USD} (NT${PRICE_TWD}). Fully online.",
    og_title="Getting Married in Taiwan: Illustrated Wedding Package",
    nav=["What's included", "Price", "How it works", "FAQ"], nav_cta="Ask about it",
    big=("Home", "to wed"), vert="Taiwan wedding · Bilingual invitation",
    h1="Getting married in <b>Taiwan</b>?<br>Portrait, certificate and a bilingual invitation in one package",
    lead="You live abroad, so you can't receive parcels or chase vendors one by one. We make the illustrations and the invitation as digital files, all by email. For Taiwanese couples overseas and international couples alike.",
    cta1="Ask about the package", cta2="See what's included",
    who_k="For you", who_h="Who it's for", who_p="",
    who=[("Two Taiwanese partners living abroad", "A wedding back home, with family and friends in different countries. One link reaches everyone."), ("One partner is from another country", "The invitation is in Chinese and English, with a section that tells overseas guests how to get to the venue and how red envelopes work.")],
    inc_k="What's included", inc_h="What's in the package", inc_p="Everything below is included in the package price.",
    inc=[
        ("Full-body color couple portrait", "Drawn from your favorite photo. One pet or child included. Up to 4 revisions."),
        ("Marriage certificate design (PDF)", "In the format used for household registration in Taiwan, delivered as a printable PDF."),
        ("Bilingual wedding invitation website", "One link, with a Chinese and English switch. Choose from three styles. Online for 6 months."),
        ("Guide for overseas guests", "Airport to venue, where to stay, and Taiwanese wedding customs such as red envelopes, built into the invitation."),
        ("Bilingual RSVP form", "We give you a ready-made form template. You copy it into your own Google account, so your guests' replies stay with you. We never see them."),
        ("Welcome sign file + save-the-date image", "Made from the same portrait: a printable welcome sign and an image to share online."),
    ],
    addon="Need printing? Printed certificates or paper invitations can be added and sent by registered mail to your address in Taiwan (quoted separately).",
    cmp_k="Compare", cmp_h="Package vs. single items", cmp_head=["Item", "Single items", "Taiwan wedding package"],
    cmp=[("Marriage certificate PDF", "+US$50", "Included"), ("Portrait revisions", "2", "4"), ("Pet or child", "+US$25 each", "1 included"),
         ("RSVP form", "You set it up", "Bilingual template provided"), ("Guide for overseas guests", "No", "Yes"), ("Welcome sign and save-the-date", "No", "Yes")],
    price_k="One price", price_h="Package price", price_alt=f"or NT${PRICE_TWD}",
    price_li=["US dollars: pay by Wise", "Taiwan dollars: bank transfer to a Taiwan account", "We start after full payment", "Full refund before we start the first sketch; no refund once drawing has started"],
    how_k="How it works", how_h="From first email to delivery", how_p="Usually 4 to 5 weeks. Please contact us <b>at least 2 months</b> before your wedding.",
    steps=[("Email us", "Tell us your date and city"), ("Confirm the details", "We reply with the plan"), ("Pay", "Wise or Taiwan bank transfer"), ("Send photo and text", "Your photo and invitation details"), ("Review and delivery", "Everything by email")],
    rush_h="Rush orders", rush_p="Less than 4 weeks counts as a rush order. We accept it only if our schedule allows, for an extra 30% of the total.",
    share_h="Portfolio and privacy", share_p="Finished designs may appear on our website or social media as portfolio work. We never publish your personal details or the photos you send. Every invitation has a private link that search engines can't find.",
    faq_h="Questions",
    faq=[
        ("What is in the Taiwan wedding package, and how much is it?", f"A couple portrait, a marriage certificate design (PDF), a bilingual Chinese and English invitation website, a guide for overseas guests, a bilingual RSVP form template, a welcome sign file and a save-the-date image. The package is US${PRICE_USD} (or NT${PRICE_TWD})."),
        ("How do we pay from abroad?", "Pay in US dollars by Wise, or in Taiwan dollars by bank transfer to a Taiwan account. We send payment details after confirming your order, and start after full payment."),
        ("Can we get a refund?", "Yes, a full refund if you cancel before we start the first sketch. Once drawing has started, we can't offer a refund."),
        ("We're not in Taiwan. How do we receive everything?", "Everything in the package is digital and delivered by email. If you add printing, we send it by registered mail to your address in Taiwan."),
        ("Do you see our guests' RSVP replies?", "No. You create the RSVP form in your own Google account, so replies are stored only in your account."),
        ("Can the invitation include other languages?", "Yes, Japanese or Spanish can be added. Tell us when you get in touch."),
        ("Can we use the certificate for marriage registration in Taiwan?", "It is designed in the marriage certificate format used for household registration in Taiwan. For the documents and steps you need, please follow the rules of the Household Registration Office."),
        ("How long does it take?", "Usually 4 to 5 weeks. Please contact us at least 2 months before your wedding. Less than 4 weeks is a rush order: an extra 30% of the total, and only if our schedule allows."),
        ("Do you work with same-sex couples?", "Yes. The certificate uses the matching legal wording."),
    ],
    end_h="Let's draw <span>your day.</span>", end_p=f"Illustrations and contact: Zoe @KnittingHiyori<br>Email only: {MAIL}", end_cta="Ask about the package",
    other=("Only need one item?", "See single-item prices", "/en/"),
    mail_subject="[Taiwan wedding package]", mail_body="Hello, I'd like to ask about the Taiwan wedding package.\n\nName:\nCountry we live in:\nWedding date:\nCity / venue in Taiwan:\nInvitation languages (Chinese + English, or others):\nPreferred payment (Wise USD / Taiwan bank transfer):\nAnything else:\n",
    legal="This site uses cookies for analytics (Google Analytics).", privacy="Privacy", close="Close",
),
}


def strip(h):
    return re.sub(r"<[^>]+>", "", h)


def build(lang):
    from urllib.parse import quote
    t = T[lang]
    url = BASE + PATHS[lang]
    price_main = f"NT${PRICE_TWD}" if lang == "zh" else f"US${PRICE_USD}"
    mailto = f"mailto:{MAIL}?subject={quote(t['mail_subject'])}&body={quote(t['mail_body'])}"
    alts = "\n".join(f'<link rel="alternate" hreflang="{h}" href="{BASE}{p}">' for h, p in [("zh-Hant", PATHS["zh"]), ("en", PATHS["en"]), ("x-default", PATHS["zh"])])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": t["og_title"], "description": t["desc"], "url": url,
         "provider": {"@type": "Organization", "name": "編織日和 Knitting Hiyori", "url": "https://knittinghiyori.com/", "email": MAIL},
         "areaServed": "Worldwide",
         "offers": [{"@type": "Offer", "name": t["og_title"], "price": PRICE_TWD.replace(",", ""), "priceCurrency": "TWD"},
                    {"@type": "Offer", "name": t["og_title"], "price": PRICE_USD, "priceCurrency": "USD"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}]}
    cur = ' aria-current="page"'
    langs = "".join(f'<a href="{PATHS[c]}" hreflang="{"zh-Hant" if c == "zh" else c}"{cur if c == lang else ""} data-cta="lang_switch" data-cta-type="wedding">{n}</a>' for c, n in [("zh", "中文"), ("en", "EN")])
    cta = lambda label, cls="pill": f'<a class="{cls}" href="{mailto}" data-cta="package_email" data-cta-type="other">{label} <span class="arr">→</span></a>'
    who = "".join(f'<article class="rv" style="--i:{i}"><h3>{a}</h3><p>{b}</p></article>' for i, (a, b) in enumerate(t["who"]))
    inc = "\n".join(f'        <li class="rv"><i>{i + 1:02d}</i><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(t["inc"]))
    cmp_rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in t["cmp"])
    steps = "\n".join(f'        <li class="rv" style="--i:{i}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(t["steps"]))
    faq = "\n".join(f"        <details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
    robots = "index, follow, max-image-preview:large" if LIVE else "noindex, nofollow"
    title_ga = "喜帖|回台結婚專案|似顏繪書約雙語喜帖全包"
    html = f"""<!doctype html>
<html lang="{t['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url}">
{alts}
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{t['brand']}">
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
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400;1,6..96,500&family=Noto+Sans+TC:wght@400;500;700&family=Noto+Serif+TC:wght@500;700;900&display=swap" rel="stylesheet">
{STYLE}{folio.CSS}{EXTRA}{EN_FONT if lang == "en" else ""}
<!-- wedding 子網域：不放 Travelpayouts、不放 Google 廣告（core §1） -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-ZQZHTYTRMQ"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments);}}
gtag("js",new Date());
gtag("set",{{content_group:"wedding",page_lang:"{t['page_lang']}",page_title:"{title_ga}"}});
gtag("config","G-ZQZHTYTRMQ",/[?]hy_debug=1/.test(location.search)?{{cookie_domain:".knittinghiyori.com",debug_mode:true}}:{{cookie_domain:".knittinghiyori.com"}});
</script>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<meta name="spec-version" content="core-v1.9.1">
</head>
<body>

<header class="top">
  <div class="wrap">
    <a class="kh-brand" href="{BASE}{'/' if lang == 'zh' else '/en/'}" data-google-vignette="false" data-cta="brand_hub" data-cta-type="wedding"><img src="/icons/logo-knitting-120.webp" width="40" height="40" alt="">{t['brand']}<span class="site">{t['site']}</span></a>
    <nav class="nav"><a href="#included">{t['nav'][0]}</a><a href="#price">{t['nav'][1]}</a><a href="#how">{t['nav'][2]}</a><a href="#faq">{t['nav'][3]}</a><span class="langs">{langs}</span>{cta(t['nav_cta'])}</nav>
  </div>
</header>

<main>
  <section class="hero wrap" style="padding-top:28px">
    <div class="l"><p class="big split" data-split>{t['big'][0]}</p></div>
    <div class="arch-wrap" style="position:relative">
      <div class="arch rv" style="--i:2"><span class="sun"></span><img src="/assets/couple-kimono.webp" alt="{strip(t['og_title'])}" width="766" height="1500"></div>
      <svg class="badge" viewBox="0 0 132 132" aria-hidden="true"><defs><path id="circ" d="M66 66m-50 0a50 50 0 1 1 100 0a50 50 0 1 1 -100 0"/></defs><circle class="core" cx="66" cy="66" r="5"/><text><textPath href="#circ">Taiwan Wedding · Knitting Hiyori · 回台結婚 ·</textPath></text></svg>
    </div>
    <div class="r"><p class="big split" data-split><em>{t['big'][1]}</em></p></div>
    <span class="vert">{t['vert']}</span>
    <div class="hero-copy">
      <h1 class="rv" style="--i:3">{t['h1']}</h1>
      <div class="meta rv" style="--i:4">
        <p>{t['lead']}</p>
        <div style="display:flex;gap:10px;flex-wrap:wrap">{cta(t['cta1'])}<a class="pill ghost" href="#included" data-cta="hero_price" data-cta-type="wedding">{t['cta2']}</a></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="chapter"><span class="no">01</span><div><span class="kicker">{t['who_k']}</span><h2 class="split" data-split>{t['who_h']}</h2></div></div>
      <div class="who">{who}</div>
    </div>
  </section>

  <section id="included" style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">02</span><div><span class="kicker">{t['inc_k']}</span><h2 class="split" data-split>{t['inc_h']}</h2><p>{t['inc_p']}</p></div></div>
      <ul class="inc">
{inc}
      </ul>
      <p class="note" style="margin-top:22px;font-size:15px">{t['addon']}</p>
    </div>
  </section>
{folio.section(lang, "03")}
  <section id="price">
    <div class="wrap">
      <div class="pricebox rv">
        <div><span class="kicker" style="color:var(--rose)">{t['price_k']}</span><p style="font-family:var(--serif);font-size:22px;margin:8px 0 10px">{t['price_h']}</p><p class="big">{price_main}</p><p class="alt">{t['price_alt']}</p>{cta(t['cta1'])}</div>
        <ul>{''.join(f'<li>{x}</li>' for x in t['price_li'])}</ul>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">04</span><div><span class="kicker">{t['cmp_k']}</span><h2 class="split" data-split>{t['cmp_h']}</h2></div></div>
      <div class="cmp-wrap"><table class="cmp"><thead><tr>{''.join(f'<th>{h}</th>' for h in t['cmp_head'])}</tr></thead><tbody>{cmp_rows}</tbody></table></div>
      <p class="note" style="margin-top:18px;font-size:15px">{t['other'][0]} <a href="{t['other'][2]}" data-cta="package_single" data-cta-type="wedding">{t['other'][1]}</a></p>
    </div>
  </section>

  <section id="how" style="padding-top:0">
    <div class="wrap">
      <div class="chapter"><span class="no">05</span><div><span class="kicker">{t['how_k']}</span><h2 class="split" data-split>{t['how_h']}</h2><p>{t['how_p']}</p></div></div>
      <ol class="flow">
{steps}
      </ol>
      <div class="promise rv">
        <div><h3>{t['rush_h']}</h3><p>{t['rush_p']}</p></div>
        <div><h3>{t['share_h']}</h3><p>{t['share_p']}</p></div>
      </div>
    </div>
  </section>

  <section id="faq" style="background:var(--blush)">
    <div class="wrap">
      <div class="chapter"><span class="no">06</span><div><span class="kicker">FAQ</span><h2 class="split" data-split>{t['faq_h']}</h2></div></div>
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
    {cta(t['end_cta'])}
    <small><a href="https://knittinghiyori.com/">編織日和 Knitting Hiyori</a></small>
    <p class="kh-legal" style="font-size:13px;color:#c9a7ae;margin:8px 0 0">{t['legal']} <a href="https://knittinghiyori.com/privacy-policy/">{t['privacy']}</a></p>
  </div>
</footer>
<script>
(() => {{
  if (new URLSearchParams(location.search).has("still")) document.documentElement.classList.add("still");
  document.querySelectorAll("[data-split]").forEach((el) => {{
    const walk = (node) => [...node.childNodes].forEach((n) => {{
      if (n.nodeType === 3) {{
        const frag = document.createDocumentFragment();
        (n.textContent.match(/[A-Za-z''.,?]+|\\s+|./gu) || []).forEach((ch) => {{
          if (/^\\s+$/.test(ch)) {{ frag.appendChild(document.createTextNode(" ")); return; }}
          const w = document.createElement("span"); w.className = "w"; const s = document.createElement("span"); s.textContent = ch; w.appendChild(s); frag.appendChild(w);
        }});
        n.replaceWith(frag);
      }} else walk(n);
    }});
    walk(el); el.querySelectorAll(".w > span").forEach((s, i) => s.style.setProperty("--i", i));
  }});
  const io = new IntersectionObserver((es) => es.forEach((e) => {{ if (e.isIntersecting) {{ e.target.classList.add("in"); io.unobserve(e.target); }} }}), {{ threshold: .12 }});
  document.querySelectorAll(".rv, [data-split]").forEach((el) => io.observe(el));
}})();
</script>
{TRACK}</body>
</html>
"""
    out = os.path.join(ROOT, PATHS[lang].strip("/")) if LIVE else os.path.join(ROOT, "_proposals", "package", lang)
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
    return out


for l in ("zh", "en"):
    print(build(l))
