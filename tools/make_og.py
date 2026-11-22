"""產生喜帖的分享預覽圖（LINE、Messenger、FB 貼連結時出現的那張圖），1200×630。
用法：
  python3 tools/make_og.py --couple 似顏繪去背.png --names "阿哲 & 小晴" --date "2027.03.20 SAT" --style a --out og.jpg
  --line2 可加一行小字（例：會場城市），--title 可換上方英文字（預設 We're getting married!）
做好後，喜帖 <head> 的 og:image 填這張圖的完整網址（https://invite.knittinghiyori.com/<網址代號>/og.jpg）。
"""
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONTS = "/System/Library/Fonts/Supplemental/"
STYLE = {   # 背景、亮點、主字色、細字色
    "a": ((251, 245, 233), (246, 200, 115), (59, 52, 49), (133, 122, 115)),
    "b": ((251, 248, 244), (216, 180, 171), (74, 67, 64), (141, 132, 126)),
    "c": ((240, 245, 250), (207, 223, 240), (51, 65, 80), (125, 138, 150)),
}

ap = argparse.ArgumentParser()
ap.add_argument("--couple", required=True)
ap.add_argument("--names", required=True)
ap.add_argument("--date", required=True)
ap.add_argument("--style", default="a", choices=STYLE)
ap.add_argument("--title", default="We're getting married!")
ap.add_argument("--line2", default="")
ap.add_argument("--out", required=True)
a = ap.parse_args()

bg, glow, ink, mute = STYLE[a.style]
W, H = 1200, 630
im = Image.new("RGB", (W, H), bg)
# 右側柔光
g = Image.new("L", (W, H), 0); ImageDraw.Draw(g).ellipse((640, 40, 1180, 620), fill=255)
g = g.filter(ImageFilter.GaussianBlur(90))
im.paste(Image.new("RGB", (W, H), glow), (0, 0), g.point(lambda v: int(v * .55)))
d = ImageDraw.Draw(im)

f_title = ImageFont.truetype(FONTS + "SnellRoundhand.ttc", 54)
f_names = ImageFont.truetype(FONTS + "Songti.ttc", 78, index=1) if a.names and any(ord(c) > 0x2E80 for c in a.names) else ImageFont.truetype(FONTS + "Didot.ttc", 84)
f_date = ImageFont.truetype(FONTS + "Didot.ttc", 40)
f_small = ImageFont.truetype(FONTS + "Songti.ttc", 30, index=1)
f_brand = ImageFont.truetype(FONTS + "Didot.ttc", 22)

x = 80
d.text((x, 150), a.title, font=f_title, fill=tuple(int(c * .85) for c in glow) if a.style != "c" else mute)
d.text((x, 240), a.names, font=f_names, fill=ink)
d.line((x, 362, x + 120, 362), fill=glow if a.style != "a" else (201, 138, 58), width=3)
d.text((x, 390), a.date, font=f_date, fill=ink)
if a.line2:
    d.text((x, 452), a.line2, font=f_small, fill=mute)
d.text((x, H - 70), "Illustrated wedding invitation · Knitting Hiyori", font=f_brand, fill=mute)

cp = Image.open(a.couple).convert("RGBA")
th = 560
cp = cp.resize((int(cp.width * th / cp.height), th), Image.LANCZOS)
if cp.width > 520:
    cp = cp.resize((520, int(cp.height * 520 / cp.width)), Image.LANCZOS)
im.paste(cp, (W - 80 - cp.width - (520 - cp.width) // 2, H - cp.height - 20), cp)
im.save(a.out, "JPEG", quality=88)
print(a.out, im.size)
