"""部落格文章元件（2026-11-23，部落格版型子對話）。blog_posts.py 用這些函式寫內文，build_pages.py 用 SERVICES 做服務卡片。

寫法與規則見 CLAUDE.md「部落格寫作規範」。內文是 f-string，元件用 {steps(...)}、{table(...)}、{box(...)}、{mid(...)}、{CHEAT} 放進去。
"""
import html as _html

CHEAT = "<!--HY-CHEAT-->"   # 懶人包圖放在內文的哪裡

# 服務卡片：價格改了這裡也要改（另外三處見 CLAUDE.md）
SERVICES = {
    "caricature": dict(
        url="/caricature/", quote="/#quote", img="/assets/portfolio/couple-portrait-wedding-dress-cats-balloons.webp",
        name="新人似顏繪", line="照婚紗照畫雙人全身彩色似顏繪，NT$1,800 起",
        title="把你們畫成似顏繪，<br>放進書約和喜帖",
        points=["照你們最喜歡的婚紗照畫雙人全身彩色似顏繪", "同一張圖延伸成結婚書約、電子喜帖、紙本喜帖", "毛小孩、小朋友可以一起畫進來"],
        price="NT$1,800 起", more="看作品"),
    "cert": dict(
        url="/marriage-certificate/", quote="/?sy=4#quote", img="/assets/shoyaku/t2.webp",
        name="似顏繪結婚書約｜同婚版・一般版", line="法條文字幫你套好，NT$1,000 起",
        title="登記那天的書約，<br>畫上你們兩個",
        points=["同婚版、一般版用對應的法條文字", "8 款手繪邊框，印好 3 張寄到台灣地址", "另需雙人似顏繪 NT$1,800"],
        price="NT$1,000 起", more="看 4 種方案"),
    "web": dict(
        url="/web-invitation/", quote="/?web=A#quote", img="/assets/og-invite-a.jpg",
        name="似顏繪網頁電子喜帖", line="婚宴流程、地圖、出席回覆都在裡面，NT$3,800",
        title="手機一點就開的<br>似顏繪電子喜帖",
        points=["婚宴流程、Dress code、地圖、加入行事曆", "賓客線上回覆出席，不用一個個問", "3 種風格同價，搭配似顏繪 +NT$1,800，或選婚紗照版不畫"],
        price="NT$3,800", more="看 3 種風格"),
    "paper": dict(
        url="/paper-invitation/", quote="/?paper=1#quote", img="/assets/paper/paper-invitation-welcome-pink-two-pages.webp",
        name="似顏繪紙本喜帖", line="兩頁設計 NT$2,500，印刷每份 NT$105",
        title="把似顏繪<br>印成紙本喜帖",
        points=["正面似顏繪封面，背面邀請細節與流程", "燙金 Save the Date 信封 21 色、玫瑰蠟封貼", "30 份起印，只寄台灣地址"],
        price="NT$2,500＋每份 NT$105", more="看作品"),
    "package": dict(
        url="/taiwan-wedding/", quote="/taiwan-wedding/#price", quote_label="看專案價格", img="/assets/couple-kimono.webp",
        name="回台結婚全包專案", line="住國外、回台灣結婚的新人一次備齊，NT$22,000",
        title="住在國外，<br>回台灣結婚一次備齊",
        points=["似顏繪、結婚書約 PDF、中英雙語電子喜帖", "外國賓客專區、迎賓板與 Save the Date", "全程線上，不用收包裹"],
        price="NT$22,000", more="看專案內容", more_url="/taiwan-wedding/#included"),
}


def steps(*items):
    """有先後順序的步驟：steps(("標題", "說明"), ...)"""
    return '<ol class="steps">' + "".join(f"<li><b>{t}</b>{d}</li>" for t, d in items) + "</ol>"


def table(head, *rows, stack=True):
    """比較、文件用表格：第一個參數是表頭，後面每一列一個 list。手機上自動變成小卡（stack=False 改回左右滑）"""
    th = "".join(f"<th>{h}</th>" for h in head)
    plain = [_html.escape(_strip(h), quote=True) for h in head]
    tr = "".join("<tr>" + "".join(f'<td data-th="{plain[i]}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tbl{" stack" if stack else ""}"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


BOX = {"tip": "💡 小撇步", "warn": "⚠️ 注意", "note": "📌 提醒"}


def box(kind, text, title=None):
    """重點框：tip 小撇步（粉紅）、warn 注意（黃）、note 提醒（藍）。text 可以是一段或多段（用 <p> 包）"""
    body = text if text.lstrip().startswith("<") else f"<p>{text}</p>"
    return f'<div class="box {kind}"><b>{title or BOX[kind]}</b>{body}</div>'


def mid(service, hook):
    """文章中間的情境卡片（全文 1 張）：hook 寫讀者當下心裡的那句話，例：「登記那天要帶書約？」"""
    s = SERVICES[service]
    return (f'<a class="svc-mid" href="{s["url"]}" data-cta="post_context" data-cta-type="wedding">'
            f'<img src="{s["img"]}" alt="" loading="lazy" width="84" height="84">'
            f'<div><i>{hook}</i><b>{s["name"]}</b><span>{s["line"]} →</span></div></a>')


RINGS = ('<div class="art" aria-hidden="true"><svg viewBox="0 0 120 80"><circle cx="46" cy="44" r="26" fill="none" stroke="#5a2232" stroke-width="6"/>'
         '<circle cx="74" cy="44" r="26" fill="none" stroke="#c07a8c" stroke-width="6"/><path d="M74 6l6 6-6 6-6-6z" fill="#fff" stroke="#c07a8c" stroke-width="2"/></svg></div>')


def end_card(service, art=None):
    """文末服務卡片（build_pages.py 依每篇的 service 欄位自動放）。art="rings" 把插圖換成交扣戒指（同婚文章在有同性伴侶似顏繪前先用）"""
    s = SERVICES[service]
    pts = "".join(f"<li>{p}</li>" for p in s["points"])
    pic = RINGS if art == "rings" else f'<img src="{s["img"]}" alt="" loading="lazy">'
    return (f'<div class="svc-end">{pic}'
            f'<div><span class="kicker">Our service</span><h3>{s["title"]}</h3><ul>{pts}</ul><div class="price">{s["price"]}</div>'
            f'<div class="acts"><a class="pill" href="{s["quote"]}" data-cta="post_service" data-cta-type="wedding">{s.get("quote_label", "開始估價")} <span class="arr">→</span></a>'
            f'<a class="pill ghost" href="{s.get("more_url", s["url"])}" data-cta="post_service" data-cta-type="wedding">{s["more"]}</a></div></div></div>')


def _strip(s):
    import re
    return re.sub("<[^>]+>", "", s)
