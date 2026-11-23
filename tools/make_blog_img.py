#!/usr/bin/env python3
"""部落格文章的封面圖（1200×630，同時當 og:image）與懶人包圖（1080×1350）產生器。

讀 tools/blog_posts.py 裡每篇的 cover、cheat 欄位，輸出到 assets/blog/：
    python3 tools/make_blog_img.py            # 全部重做
    python3 tools/make_blog_img.py wedding-songs   # 只做一篇
封面不放浮水印；懶人包最下面一行小字寫網站網址，方便被轉傳後找得回來。
欄位寫法見 CLAUDE.md「部落格寫作規範」。cover 沒寫 art 時畫兩個交扣的戒指。
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_posts import POSTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "blog")
SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"   # 2＝Songti TC Bold、7＝Songti TC Regular
LATIN = "/System/Library/Fonts/Supplemental/Didot.ttc"
PAPER, BLUSH, ROSE, ROSE_D, WINE, INK, MUTED, CREAM = (251, 244, 242), (245, 223, 224), (230, 169, 181), (201, 116, 135), (90, 34, 50), (58, 33, 40), (124, 93, 100), (255, 250, 247)


def font(size, bold=True):
    return ImageFont.truetype(SONG, size, index=2 if bold else 7)


def wrap(d, text, f, width):
    """中文逐字換行，英文單字不拆開；\n 強制換行"""
    lines = []
    for para in text.split("\n"):
        cur, tokens, buf = "", [], ""
        for ch in para:
            if ch.isascii() and not ch.isspace():
                buf += ch
                continue
            if buf:
                tokens.append(buf); buf = ""
            tokens.append(ch)
        if buf:
            tokens.append(buf)
        for t in tokens:
            if d.textlength(cur + t, font=f) > width and cur:
                lines.append(cur.rstrip()); cur = t.lstrip()
            else:
                cur += t
        lines.append(cur)
    return lines


def art(path, box_h, max_w):
    im = Image.open(os.path.join(ROOT, path)).convert("RGBA")
    im = im.resize((int(im.width * box_h / im.height), box_h), Image.LANCZOS)
    if im.width > max_w:
        im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    return im


def paste_art(base, im, xy):
    """有透明背景直接貼；白底的作品用色彩增值（multiply），白色會融進背景"""
    if im.getextrema()[3][0] < 250:
        base.paste(im, xy, im)
    else:
        region = base.crop((xy[0], xy[1], xy[0] + im.width, xy[1] + im.height)).convert("RGB")
        base.paste(ImageChops.multiply(region, im.convert("RGB")), xy)


def cover(P):
    c = P["cover"]
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), PAPER)
    g = Image.new("L", (W, H), 0)
    ImageDraw.Draw(g).ellipse((700, 30, 1200, 640), fill=255)
    im.paste(Image.new("RGB", (W, H), BLUSH), (0, 0), g.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(im)
    d.ellipse((760, 70, 1150, 460), fill=(240, 200, 206))
    if c.get("art"):
        a = art(c["art"], c.get("art_h", 540), 420)
        paste_art(im, a, (955 - a.width // 2, H - a.height - c.get("art_bottom", 10)))
    else:   # 沒有指定插圖：畫兩個交扣的戒指（不分性別）
        for cx, col in ((900, WINE), (1010, ROSE_D)):
            d.ellipse((cx - 95, 170, cx + 95, 360), outline=col, width=14)
        d.polygon([(1010, 128), (990, 150), (1010, 172), (1030, 150)], fill=CREAM, outline=ROSE_D)
    x = 70
    f, fs = font(64), font(30, bold=False)
    tl = wrap(d, c["title"], f, 640)
    sl = wrap(d, c["sub"], fs, 640) if c.get("sub") else []
    y = (H - (68 + len(tl) * 86 + (14 + len(sl) * 44 if sl else 0))) // 2   # 文字區塊垂直置中
    d.text((x, y), c.get("kicker", "Wedding notes"), font=ImageFont.truetype(LATIN, 30), fill=ROSE_D)
    d.line((x, y + 48, x + 70, y + 48), fill=ROSE_D, width=2)
    y += 68
    for ln in tl:
        d.text((x, y), ln, font=f, fill=WINE); y += 86
    y += 14
    for ln in sl:
        d.text((x, y), ln, font=fs, fill=INK); y += 44
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, c["img"])
    im.save(p, "JPEG", quality=86, optimize=True, progressive=True)
    return p


def cheat(P):
    c = P["cheat"]
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    ft = font(60)
    tl = wrap(d, c["title"], ft, W - 140)
    band = 104 + len(tl) * 76 + 44
    d.rectangle((0, 0, W, band), fill=WINE)
    d.text((70, 58), c.get("kicker", "懶人包"), font=font(30, bold=False), fill=ROSE)
    y = 104
    for ln in tl:
        d.text((70, y), ln, font=ft, fill=CREAM); y += 76
    top = band + 40
    pts = c["points"]
    # 點數多時自動縮小字和留白，直到放得下
    for hb, hn, lb, ln_, padc, gap in ((36, 29, 48, 42, 60, 22), (33, 27, 44, 38, 44, 16), (30, 25, 40, 35, 34, 12)):
        fb, fn = font(hb), font(hn, bold=False)
        blocks = []
        for head, text in pts:
            hl = wrap(d, head, fb, W - 260)
            tl = wrap(d, text, fn, W - 260) if text else []
            blocks.append((hl, tl, len(hl) * lb + len(tl) * ln_ + padc))
        avail = H - 120 - top - gap * (len(pts) - 1)
        if sum(b[2] for b in blocks) <= avail:
            break
    pad = max(0, (avail - sum(b[2] for b in blocks)) // max(1, len(pts)))
    for i, (hl, tl, h) in enumerate(blocks):
        h += pad
        d.rounded_rectangle((60, top, W - 60, top + h), radius=26, fill=(255, 255, 255), outline=(225, 200, 205), width=2)
        ty = top + (h - (len(hl) * lb + len(tl) * ln_)) // 2 - 4   # 卡片內文字垂直置中
        cy = ty + lb // 2 + 2
        d.ellipse((92, cy - 28, 148, cy + 28), fill=ROSE)
        d.text((120, cy), str(i + 1), font=ImageFont.truetype(LATIN, 36), fill=WINE, anchor="mm")
        for ln in hl:
            d.text((190, ty), ln, font=fb, fill=WINE); ty += lb
        for ln in tl:
            d.text((190, ty + 4), ln, font=fn, fill=INK); ty += ln_
        top += h + gap
    foot = c.get("foot", "")
    fs = font(24, bold=False)
    line = (foot + "　" if foot else "") + "wedding.knittinghiyori.com"
    d.text((W / 2 - d.textlength(line, font=fs) / 2, H - 78), line, font=fs, fill=MUTED)
    p = os.path.join(OUT, c["img"])
    im.save(p, "JPEG", quality=86, optimize=True, progressive=True)
    return p


if __name__ == "__main__":
    want = set(sys.argv[1:])
    for P in POSTS:
        if want and P["slug"] not in want:
            continue
        for k, fn in (("cover", cover), ("cheat", cheat)):
            if P.get(k):
                print(fn(P))
