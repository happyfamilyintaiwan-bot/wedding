/* B、C 共用：往下滑時的出現動畫（參考 A 書約手繪風）
   - 段落標題逐字跳出、新人名字逐字彈出
   - 故事、流程、提醒、交通：左右交錯滑入，圖示一筆一筆畫出來，水彩底色彈出
   - 月曆日期依序淡入、倒數數字翻出來、服裝色票往上跳
   - 桌機兩側插畫跟著捲動輕微視差
   需要在主程式填好內容之後、開場 begin() 之前載入；?still 與減少動態時全部直接顯示 */
(() => {
  const css = `
.hy-ch { display: inline-block; opacity: 0; transform: translateY(18px) rotate(5deg); transition: opacity .7s ease, transform .9s cubic-bezier(.2,1.4,.4,1); transition-delay: calc(var(--ci) * 70ms + var(--c0, .2s)); }
.in .hy-ch { opacity: 1; transform: none; }
.hy-l, .hy-r { opacity: 0; transition: opacity 1s ease, transform 1.1s cubic-bezier(.2,.9,.25,1); transition-delay: calc(var(--i, 0) * 120ms); }
.hy-l { transform: translateX(-34px) rotate(-1.2deg); } .hy-r { transform: translateX(34px) rotate(1.2deg); }
.in .hy-l, .in .hy-r { opacity: 1; transform: none; }
.hy-wash { transform: scale(0); transform-box: fill-box; transform-origin: center; transition: transform 1s cubic-bezier(.3,1.5,.5,1); transition-delay: calc(var(--i, 0) * 120ms + .25s); }
.in .hy-wash { transform: scale(1); }
.dab .ico { position: relative; z-index: 1; }
.hy-draw { transition: stroke-dashoffset 1.3s cubic-bezier(.6,.05,.3,1); transition-delay: calc(var(--i, 0) * 120ms + .45s); }
.in .hy-draw { stroke-dashoffset: 0 !important; }
.in .cal-grid span { animation: hyDay .5s ease both; animation-delay: calc(var(--k, 0) * 16ms + .3s); }
@keyframes hyDay { from { opacity: 0; transform: translateY(6px); } }
.in .cal-grid .day svg { animation: hyPop .9s cubic-bezier(.3,1.6,.5,1) both; animation-delay: 1s; }
@keyframes hyPop { from { transform: scale(0); } }
.in .cd { animation: hyFlip .9s cubic-bezier(.2,.9,.3,1) both; animation-delay: calc(var(--k, 0) * 120ms + .3s); }
@keyframes hyFlip { from { opacity: 0; transform: perspective(300px) rotateX(-80deg); } }
.hy-up { opacity: 0; transform: translateY(26px) scale(.92); transition: opacity .8s ease, transform 1s cubic-bezier(.3,1.5,.5,1); transition-delay: calc(var(--i, 0) * 110ms + .3s); }
.in .hy-up { opacity: 1; transform: none; }
.still .hy-ch, .still .hy-l, .still .hy-r, .still .hy-up { opacity: 1 !important; transform: none !important; }
.still .hy-wash { transform: none !important; } .still .hy-draw { stroke-dashoffset: 0 !important; }
@media (prefers-reduced-motion: reduce) { .hy-ch, .hy-l, .hy-r, .hy-up { opacity: 1 !important; transform: none !important; } .hy-wash { transform: none !important; } .hy-draw { stroke-dashoffset: 0 !important; } }`;
  const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  // 逐字拆開（保留換行、空白）
  const split = (el, c0) => {
    if (!el || el.dataset.hySplit) return;
    const txt = el.textContent; el.dataset.hySplit = "1"; el.setAttribute("aria-label", txt);
    el.innerHTML = [...txt].map((c, i) => c.trim() ? `<span class="hy-ch" aria-hidden="true" style="--ci:${i}">${c.replace(/[<>&]/g, "")}</span>` : c).join("");
    if (c0) el.style.setProperty("--c0", c0);
  };
  document.querySelectorAll(".sh h2").forEach((h) => { h.classList.remove("fade"); split(h); });
  ["n-groom", "n-bride"].forEach((id, k) => split(document.getElementById(id), (.9 + k * .35) + "s"));

  // 清單：左右交錯、圖示畫線、水彩彈出
  document.querySelectorAll(".st, .sr, .tip, .tr").forEach((el, n) => {
    const i = [...el.parentElement.children].indexOf(el);
    el.classList.remove("fade");
    el.classList.add(i % 2 ? "hy-r" : "hy-l");
    el.style.setProperty("--i", i);
    el.querySelectorAll(".dab svg.wash, .dab > svg:first-child").forEach((w) => { w.classList.add("hy-wash"); w.style.setProperty("--i", i); });
    el.querySelectorAll(".ico .s, .ico path").forEach((p) => {
      try {
        const L = Math.ceil(p.getTotalLength()) + 2;
        p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
        p.classList.add("hy-draw"); p.style.setProperty("--i", i);
      } catch (e) {}
    });
  });
  document.querySelectorAll(".dz").forEach((el, i) => { el.classList.add("hy-up"); el.style.setProperty("--i", i); });

  // 月曆、倒數：記下順序給動畫用（月曆、倒數會被重畫，所以用 MutationObserver 補上）
  const tagCal = () => document.querySelectorAll(".cal-grid span").forEach((s, k) => s.style.setProperty("--k", k));
  const tagCd = () => document.querySelectorAll(".cd").forEach((s, k) => s.style.setProperty("--k", k));
  tagCal(); tagCd();
  ["cal", "countdown"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) new MutationObserver(() => { tagCal(); tagCd(); }).observe(el, { childList: true });
  });

  // 桌機兩側：輕微視差
  const sides = document.querySelectorAll(".side");
  if (sides.length && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let ticking = false;
    addEventListener("scroll", () => {
      if (ticking) return; ticking = true;
      requestAnimationFrame(() => {
        const y = scrollY * .08;
        sides.forEach((s, k) => { s.style.translate = `0 ${k ? -y : y}px`; });
        ticking = false;
      });
    }, { passive: true });
  }
})();
