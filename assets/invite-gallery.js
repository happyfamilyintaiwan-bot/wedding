/* 電子喜帖：婚紗照輪播（A／B／C 共用）
   - 照片寫在 WEDDING.photos：["photo-1.webp", { src: "photo-2.webp", caption: "第一次旅行" }, ...]，最多 20 張
   - 左右滑一次一張，旁邊露出下一張；點照片全螢幕看大圖，也可以左右滑
   - 沒有照片（或 hide 裡有 "gallery"）就整段拿掉
   - 顏色用各範本自己的 --ink、--accent、--paper，不寫死 */
window.HYG = (() => {
  const MAX = 20;
  const TXT = {
    zh: { region: "婚紗照輪播", open: (n) => `放大第 ${n} 張照片`, prev: "上一張", next: "下一張", close: "關閉", photo: (n) => `婚紗照 ${n}` },
    en: { region: "Photo gallery", open: (n) => `Open photo ${n}`, prev: "Previous", next: "Next", close: "Close", photo: (n) => `Photo ${n}` },
    ja: { region: "写真ギャラリー", open: (n) => `${n}枚目を拡大`, prev: "前へ", next: "次へ", close: "閉じる", photo: (n) => `写真 ${n}` },
    es: { region: "Galería de fotos", open: (n) => `Abrir foto ${n}`, prev: "Anterior", next: "Siguiente", close: "Cerrar", photo: (n) => `Foto ${n}` },
  };
  const CSS = `
.hyg { position: relative; margin: 0 -24px; --w: min(76vw, 340px); }
.hyg-track { display: flex; gap: 14px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 10px calc(50% - var(--w) / 2) 22px; scrollbar-width: none; -webkit-overflow-scrolling: touch; overscroll-behavior-x: contain; }
.hyg-track::-webkit-scrollbar { display: none; }
.hyg-track:focus-visible { outline: 2px dashed var(--accent); outline-offset: -6px; }
.hyg-slide { flex: 0 0 var(--w); scroll-snap-align: center; margin: 0; transition: transform .5s ease, opacity .5s ease; transform: scale(.92); opacity: .62; }
.hyg-slide.on { transform: none; opacity: 1; }
.hyg-open { display: block; width: 100%; padding: 0; border: 0; background: none; cursor: zoom-in; -webkit-tap-highlight-color: transparent; }
.hyg-open img { display: block; width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 18px; background: color-mix(in srgb, var(--ink) 8%, var(--paper));
  border: 6px solid #fff; box-shadow: 0 0 0 1.5px var(--ink), 8px 10px 0 color-mix(in srgb, var(--accent) 26%, transparent); }
.hyg-slide figcaption { margin-top: 12px; text-align: center; font-size: 15px; color: var(--muted, var(--ink)); }
.hyg-bar { display: flex; align-items: center; justify-content: center; gap: 18px; margin-top: 2px; }
.hyg-nav { width: 44px; height: 44px; border-radius: 50%; border: 1.5px solid var(--ink); background: var(--paper); color: var(--ink); font-size: 20px; line-height: 1; cursor: pointer; display: grid; place-items: center; }
.hyg-nav:disabled { opacity: .3; cursor: default; }
.hyg-count { min-width: 74px; text-align: center; font-size: 15px; letter-spacing: .14em; color: var(--muted, var(--ink)); }
.hyg-count b { color: var(--accent); font-size: 20px; font-weight: 700; }
.hyg-box { position: fixed; inset: 0; width: 100%; max-width: none; height: 100%; max-height: none; margin: 0; padding: 0; border: 0; background: var(--paper); }
.hyg-box::backdrop { background: transparent; }
.hyg-box .hyg-track { height: 100%; padding: 0; gap: 0; align-items: center; }
.hyg-box .hyg-big { flex: 0 0 100%; height: 100%; scroll-snap-align: center; display: grid; place-items: center; padding: 64px 16px 84px; }
.hyg-box .hyg-big img { max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 10px; border: 5px solid #fff; box-shadow: 0 0 0 1.5px var(--ink); }
.hyg-box .hyg-x { position: absolute; top: 14px; right: 14px; }
.hyg-box .hyg-bar { position: absolute; left: 0; right: 0; bottom: 22px; }
@media (prefers-reduced-motion: reduce) { .hyg-slide { transition: none; } .hyg-track { scroll-behavior: auto; } }`;

  const esc = (t) => String(t).replace(/[<>&"]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
  const norm = (p) => (typeof p === "string" ? { src: p } : p);

  // 一組「軌道＋上下張按鈕＋計數」，大圖和小圖共用
  function rail(track, bar, n, onIndex) {
    const slides = [...track.children];
    const [prev, count, next] = bar.children;
    let cur = 0;
    const go = (i, smooth = true) => {
      const s = slides[Math.max(0, Math.min(n - 1, i))];
      track.scrollTo({ left: s.offsetLeft - (track.clientWidth - s.clientWidth) / 2, behavior: smooth && !matchMedia("(prefers-reduced-motion: reduce)").matches ? "smooth" : "auto" });
    };
    const set = (i) => {
      cur = i;
      slides.forEach((s, k) => s.classList.toggle("on", k === i));
      count.innerHTML = `<b>${String(i + 1).padStart(2, "0")}</b> / ${String(n).padStart(2, "0")}`;
      prev.disabled = i === 0; next.disabled = i === n - 1;
      if (onIndex) onIndex(i);
    };
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.intersectionRatio > .6) set(slides.indexOf(e.target)); }), { root: track, threshold: [.6] });
    slides.forEach((s) => io.observe(s));
    prev.addEventListener("click", () => go(cur - 1));
    next.addEventListener("click", () => go(cur + 1));
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1); }
    });
    set(0);
    return { go, get cur() { return cur; } };
  }

  function render(W, lang, box) {
    const sec = box.closest("section");
    const photos = (W.photos || []).map(norm).filter((p) => p && p.src).slice(0, MAX);
    if (!photos.length || (W.hide || []).includes("gallery")) { if (sec) sec.remove(); return; }
    const T = TXT[lang] || TXT.zh;
    if (!document.getElementById("hyg-css")) document.head.insertAdjacentHTML("beforeend", `<style id="hyg-css">${CSS}</style>`);
    const n = photos.length;
    box.classList.add("hyg");
    const barHtml = `<div class="hyg-bar"><button type="button" class="hyg-nav" aria-label="${T.prev}">‹</button><span class="hyg-count" aria-live="polite"></span><button type="button" class="hyg-nav" aria-label="${T.next}">›</button></div>`;
    box.innerHTML = `<div class="hyg-track" tabindex="0" role="region" aria-label="${T.region}">` +
      photos.map((p, i) => `<figure class="hyg-slide"><button type="button" class="hyg-open" aria-label="${T.open(i + 1)}"><img src="${esc(p.src)}" alt="${esc(p.alt || p.caption || T.photo(i + 1))}" loading="${i < 2 ? "eager" : "lazy"}" decoding="async"></button>${p.caption ? `<figcaption>${esc(p.caption)}</figcaption>` : ""}</figure>`).join("") +
      `</div>${n > 1 ? barHtml : ""}`;
    const track = box.querySelector(".hyg-track");
    if (n > 1) rail(track, box.querySelector(".hyg-bar"), n);

    // 全螢幕大圖
    const dlg = document.createElement("dialog");
    dlg.className = "hyg-box";
    dlg.innerHTML = `<div class="hyg-track">` + photos.map((p, i) => `<div class="hyg-big"><img src="${esc(p.src)}" alt="${esc(p.alt || p.caption || T.photo(i + 1))}" loading="lazy" decoding="async"></div>`).join("") +
      `</div><button type="button" class="hyg-nav hyg-x" aria-label="${T.close}">✕</button>${n > 1 ? barHtml : ""}`;
    document.body.appendChild(dlg);
    const big = n > 1 ? rail(dlg.querySelector(".hyg-track"), dlg.querySelector(".hyg-bar"), n) : null;
    box.querySelectorAll(".hyg-open").forEach((b, i) => b.addEventListener("click", () => {
      dlg.showModal(); document.body.style.overflow = "hidden";
      if (big) requestAnimationFrame(() => big.go(i, false));
    }));
    dlg.querySelector(".hyg-x").addEventListener("click", () => dlg.close());
    dlg.addEventListener("close", () => { document.body.style.overflow = ""; });
    dlg.addEventListener("click", (e) => { if (e.target.classList.contains("hyg-big")) dlg.close(); });
  }
  return { render, MAX };
})();
