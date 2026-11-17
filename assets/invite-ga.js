/* 成品喜帖 GA4（只有 WEDDING.ga 有設定時才啟用；範例喜帖不追蹤）
   隱私：不送新人姓名、不送賓客名字（網址的 ?to= 會被拿掉）、不送任何輸入內容。
   不放 AdSense、不放 Travelpayouts（core §1、§7-1）。
   事件：
   - page_view：content_group=wedding、page_title=喜帖|成品喜帖|<風格>、invite_id、page_lang
   - invite_open：打開信封／拉門（option=personal 有 ?to 的專屬連結；direct 一般連結）
   - invite_section：看到某一段（option=段落 id，每段只送一次）
   - cta_click：rsvp、map、calendar_google、calendar_ics、transport_link、credit（點署名回介紹頁）
   用法：WEDDING.ga = { id: "270124-xz", style: "a" } */
(() => {
  try {
    if (typeof WEDDING === "undefined" || !WEDDING.ga || !WEDDING.ga.id) return;
    const ID = "G-ZQZHTYTRMQ", P = new URLSearchParams(location.search);
    if (P.has("still") || P.has("embed")) return;   // 截圖與預覽框不算
    const dbg = P.has("hy_debug");
    const lang = { zh: "zh-Hant", en: "en", ja: "ja", es: "es" }[WEDDING.lang || "zh"] || "zh-Hant";
    const style = ({ a: "A書約手繪風", b: "B日系清新", c: "C雪景" })[WEDDING.ga.style] || "A書約手繪風";
    const s = document.createElement("script"); s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    const page_title = "喜帖|成品喜帖|" + style;
    const base = { content_group: "wedding", page_lang: lang, invite_id: WEDDING.ga.id };   // 每個事件都直接帶（set 不一定會送出）
    gtag("set", base);
    const cfg = Object.assign({ cookie_domain: ".knittinghiyori.com", page_title, page_location: location.origin + location.pathname }, base);   // 不帶 ?to= 賓客名字
    if (dbg) cfg.debug_mode = true;
    gtag("config", ID, cfg);
    const send = (name, p) => { try { const q = Object.assign({}, base, p); if (dbg) console.log("[hy-invite]", name, q); gtag("event", name, q); } catch (e) {} };

    // 打開信封／拉門
    const personal = P.has("to") ? "personal" : "direct";
    let opened = false;
    document.addEventListener("click", (e) => {
      if (opened || !e.target.closest) return;
      if (e.target.closest("#env, #open-btn")) { opened = true; send("invite_open", { option: personal }); }
    }, true);

    // 看到哪些段落
    const seen = new Set();
    const io = new IntersectionObserver((es) => es.forEach((en) => {
      const id = en.target.id;
      if (!en.isIntersecting || !id || seen.has(id)) return;
      seen.add(id); send("invite_section", { option: id }); io.unobserve(en.target);
    }), { threshold: .4 });
    document.querySelectorAll("section[data-r][id]").forEach((sec) => io.observe(sec));

    // 按鈕
    const CTA = [["#rsvp-btn", "rsvp", "other"], ["#map-btn", "map", "other"], ["#gcal-btn", "calendar_google", "other"],
      ["#ics-btn", "calendar_ics", "other"], [".tr-link", "transport_link", "other"], ["footer a.credit", "credit", "wedding"]];
    document.addEventListener("click", (e) => {
      if (!e.target.closest) return;
      for (const [sel, id, type] of CTA) {
        const a = e.target.closest(sel);
        if (a) { send("cta_click", { cta_id: id, cta_type: type, link_url: a.href ? a.href.split("?")[0] : "" }); break; }
      }
    }, true);

    // 頁尾 Cookie 說明（core §6）
    const note = { "zh-Hant": "本頁使用 Cookie 進行流量分析（Google Analytics）。", en: "This page uses cookies for analytics (Google Analytics).", ja: "このページはアクセス解析（Google Analytics）のためにCookieを使用しています。", es: "Esta página usa cookies para analítica (Google Analytics)." }[lang];
    const f = document.querySelector("footer");
    if (f) f.insertAdjacentHTML("beforeend", `<p class="kh-legal" style="font-size:11px;opacity:.7;margin-top:6px;letter-spacing:0">${note} <a href="https://knittinghiyori.com/privacy-policy/" target="_blank" rel="noopener" style="color:inherit">Privacy</a></p>`);
  } catch (e) {}
})();
