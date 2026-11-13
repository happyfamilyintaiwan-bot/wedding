/* 電子喜帖多語（A／B／C 共用）
   - 語言：WEDDING.lang（"zh"／"en"／"ja"／"es"），網址 ?lang=en 可以臨時切換
   - 介面文字在 UI；靜態 HTML 用 data-i18n="鍵" 標記，非中文時換掉
   - 範例內容在 SAMPLE（只在 WEDDING.sample 為 true 時套用；正式交付的喜帖直接把內容寫在 WEDDING） */
window.HYI = (() => {
  const MON_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const MON_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
  const UI = {
    zh: {
      html: "zh-Hant-TW", title: (g, b) => `${g} & ${b} 婚禮`, namesAria: (g, b) => `${g} 與 ${b}`,
      calHead: (y, m) => `${y} 年 ${m + 1} 月`, wk: "日一二三四五六", cd: ["天", "時", "分", "秒"], cdB: ["日", "時", "分", "秒"],
      cdDone: "謝謝你來參加我們的婚禮", to: "To. ", toB: "致　", sign: (g, b) => `${g} ＆ ${b}　敬邀`,
      map: "開啟 Google 地圖", gcal: "Google 日曆", ics: "iPhone 行事曆", rsvp: "填寫出席回覆", theme: "配色",
      contactH: "有問題嗎？直接聯絡新人", pending: "（待填寫）", roles: { groom: "新郎", bride: "新娘" },
    },
    en: {
      html: "en", title: (g, b) => `${g} & ${b}'s Wedding`, namesAria: (g, b) => `${g} and ${b}`,
      calHead: (y, m) => `${MON_EN[m]} ${y}`, wk: ["S", "M", "T", "W", "T", "F", "S"], cd: ["Days", "Hours", "Min", "Sec"], cdB: ["Days", "Hours", "Min", "Sec"],
      cdDone: "Thank you for celebrating with us", to: "To. ", toB: "To ", sign: (g, b) => `With love, ${g} & ${b}`,
      map: "Open in Google Maps", gcal: "Google Calendar", ics: "Apple Calendar", rsvp: "RSVP now", theme: "Colors",
      contactH: "Questions? Contact the couple", pending: "(to be added)", roles: { groom: "Groom", bride: "Bride" },
      t: {
        intro_label: "Wedding invitation", intro_sub: "You have a wedding invitation", open_label: "Open the invitation",
        to_default: "To. Dear friend", to_default_b: "To our dear friend",
        hint_a: "Tap the envelope to open", hint_b: "Tap to open", hint_c: "Tap to clear the frost",
        vcopy_b: "Join us as we celebrate", vcopy_c: "Invited in the snowy season",
        h_date: "The Date", h_story: "Our Story", h_sched: "Schedule", h_dress: "Dress Code", h_tips: "Good to Know", h_venue: "Venue", h_rsvp: "RSVP",
        cd_cap: "Counting down to the big day", cal_tip_a: "Add it to your calendar so you don't miss the day", cal_tip: "Add to calendar",
        rsvp_p: "We can't wait to see you!", rsvp_p_b: "We can't wait to celebrate with you", rsvp_before: "Please reply by", rsvp_seat: "so we can save you a good seat",
        thanks_a: "Thank you<br>for being part of our story", thanks_b: "Thank you for being part of our story",
      },
    },
    ja: {
      html: "ja", title: (g, b) => `${g} & ${b} 結婚式`, namesAria: (g, b) => `${g}と${b}`,
      calHead: (y, m) => `${y}年${m + 1}月`, wk: "日月火水木金土", cd: ["日", "時間", "分", "秒"], cdB: ["日", "時間", "分", "秒"],
      cdDone: "ご参列いただきありがとうございました", to: "To. ", toB: "", sign: (g, b) => `${g}・${b}`,
      map: "Google マップで開く", gcal: "Google カレンダー", ics: "iPhone カレンダー", rsvp: "出欠を回答する", theme: "カラー",
      contactH: "ご質問はおふたりへ", pending: "（記入予定）", roles: { groom: "新郎", bride: "新婦" },
      t: {
        intro_label: "結婚式の招待状", intro_sub: "結婚式の招待状が届いています", open_label: "招待状をひらく",
        to_default: "To. 大切なあなたへ", to_default_b: "大切なあなたへ",
        hint_a: "封筒をタップしてひらく", hint_b: "タップしてひらく", hint_c: "タップして　くもりを晴らす",
        vcopy_b: "わたしたちの門出を　見届けてください", vcopy_c: "雪の季節に　ご招待します",
        h_date: "挙式日", h_story: "ふたりの物語", h_sched: "当日の流れ", h_dress: "ドレスコード", h_tips: "ご案内", h_venue: "会場", h_rsvp: "ご出欠",
        cd_cap: "結婚式まで あと", cal_tip_a: "カレンダーに登録して、当日をお忘れなく", cal_tip: "カレンダーに登録",
        rsvp_p: "当日お会いできるのを楽しみにしています", rsvp_p_b: "当日お会いできるのを楽しみにしています", rsvp_before: "下記の日付までにご回答ください", rsvp_seat: "よいお席をご用意してお待ちしています",
        thanks_a: "わたしたちの物語の<br>一部になってくれて、ありがとう", thanks_b: "わたしたちの物語の一部になってくれて　ありがとう",
      },
    },
    es: {
      html: "es", title: (g, b) => `Boda de ${g} y ${b}`, namesAria: (g, b) => `${g} y ${b}`,
      calHead: (y, m) => `${MON_ES[m]} ${y}`, wk: ["D", "L", "M", "M", "J", "V", "S"], cd: ["Días", "Horas", "Min", "Seg"], cdB: ["Días", "Horas", "Min", "Seg"],
      cdDone: "Gracias por celebrar con nosotros", to: "Para ", toB: "Para ", sign: (g, b) => `Con cariño, ${g} y ${b}`,
      map: "Abrir en Google Maps", gcal: "Google Calendar", ics: "Calendario de Apple", rsvp: "Confirmar asistencia", theme: "Colores",
      contactH: "¿Dudas? Escríbanle a la pareja", pending: "(por completar)", roles: { groom: "Novio", bride: "Novia" },
      t: {
        intro_label: "Invitación de boda", intro_sub: "Tienes una invitación de boda", open_label: "Abrir la invitación",
        to_default: "Para ti, con cariño", to_default_b: "Para ti, con cariño",
        hint_a: "Toca el sobre para abrirlo", hint_b: "Toca para abrir", hint_c: "Toca para quitar la escarcha",
        vcopy_b: "Acompáñanos a celebrar", vcopy_c: "Te invitamos en la temporada de nieve",
        h_date: "La fecha", h_story: "Nuestra historia", h_sched: "Itinerario", h_dress: "Código de vestimenta", h_tips: "Para tomar en cuenta", h_venue: "Lugar", h_rsvp: "Confirmación",
        cd_cap: "Faltan", cal_tip_a: "Agrégalo a tu calendario para no olvidar el día", cal_tip: "Agregar al calendario",
        rsvp_p: "¡Nos encantará verte ahí!", rsvp_p_b: "Nos encantará celebrar contigo", rsvp_before: "Por favor confirma antes del", rsvp_seat: "para apartarte un buen lugar",
        thanks_a: "Gracias<br>por ser parte de nuestra historia", thanks_b: "Gracias por ser parte de nuestra historia",
      },
    },
  };

  // 範例內容（共用）＋各風格的服裝建議與配色名稱
  const SAMPLE = {
    en: {
      groom: "Adam", bride: "Quinn", initials: ["A", "Q"], sealB: ["A", "Q"],
      invite: "We met in a college club\nand have shared ten years together.\nOn this day, we'd love you\nto be there with us.",
      parents: [{ role: "Groom's parents", names: "David & Linda Brown" }, { role: "Bride's parents", names: "Mark & Susan Lee" }],
      story: ["First hello at a club welcome party", "Our first trip together, to Kyoto", "Moved into our little home", "A beach proposal, and she said yes", "Now we want you there for our day"],
      schedule: [["Welcome & guestbook", "Leave a note and take photos with us"], ["Ceremony", "Witness our vows with us"], ["Lunch is served", "Enjoy the wedding feast"], ["Grand entrance", "Get ready to cheer"], ["Toasts", "We'll visit every table to say thank you"], ["Farewell treats", "Take something sweet home"]],
      tips: [["Vegetarian", "Just tick it on the RSVP form"], ["Kids' chairs", "Let us know if you bring little ones"], ["Parking", "Free for 3 hours on B2"], ["Photo corner", "At the entrance"]],
      venue: "(Sample) Garden Hall, 3F", address: "100 Sample Street, Your City",
      transport: ["Metro: Sample Station, Exit 2, 5-minute walk", "By car: search “Sample Wedding Hall”"],
      dress: {
        a: { name: "Garden Pastel", text: "Soft pastels, like walking into a spring garden with us.", colors: ["Cherry blossom", "Butter", "Mint", "Sky blue"], avoid: "Please avoid all white (the bride's color) and all black" },
        b: { name: "Muted Garden", text: "Soft, muted tones, like a light watercolor painting.", colors: ["Dusty rose", "Oat milk", "Sage", "Mist blue"], avoid: "Please avoid all white (the bride's color) and all black" },
        c: { name: "Snowy Pastel", text: "A touch of color in the snow: ice blue, oatmeal, dusty pink or pine green.", colors: ["Ice blue", "Oatmeal", "Dusty pink", "Pine green"], avoid: "Please avoid all white (the bride's color) and all black" },
      },
      themes: { honey: "Honey", candy: "Candy pink", mint: "Mint", lavender: "Lavender", rose: "Dusty rose", sage: "Sage", mist: "Mist blue", milktea: "Milk tea", ice: "Ice blue", silver: "Silver", rosy: "Pink snow", night: "Winter night" },
    },
    ja: {
      groom: "哲也", bride: "晴香", initials: ["T", "H"], sealB: ["哲", "晴"],
      invite: "大学のサークルで出会い\n十年を一緒に歩んできました\nこの日　大切なあなたに\n門出を見届けてほしいのです",
      parents: [{ role: "新郎の両親", names: "佐藤 大輔・美和" }, { role: "新婦の両親", names: "高橋 健一・裕子" }],
      story: ["サークルの新歓で初めて話した日", "はじめてのふたり旅は京都", "ふたりの小さな家に引っ越し", "海辺でのプロポーズ", "この日をあなたと一緒に"],
      schedule: [["受付", "メッセージと記念撮影を"], ["挙式", "ふたりの誓いを見届けてください"], ["披露宴 開宴", "おいしいお料理をどうぞ"], ["新郎新婦 入場", "拍手でお迎えください"], ["テーブルラウンド", "各テーブルへご挨拶に伺います"], ["お見送り", "甘いおみやげをどうぞ"]],
      tips: [["ベジタリアン", "出欠フォームでお知らせください"], ["子ども用イス", "お子さま連れの方はお知らせください"], ["駐車場", "B2 で3時間無料"], ["フォトスポット", "入口にご用意しています"]],
      venue: "（サンプル）ウェディング会館 3F ガーデンホール", address: "○○市○○区○○ 100",
      transport: ["○○駅 2番出口から徒歩5分", "お車は「○○ウェディング会館」で検索"],
      dress: {
        a: { name: "Garden Pastel", text: "やわらかなパステルカラーで、春の庭へ一緒に出かけましょう。", colors: ["さくら", "クリーム", "ミント", "そら色"], avoid: "全身白（花嫁の色）と全身黒はお控えください" },
        b: { name: "Muted Garden", text: "淡い水彩画のような、やさしく落ち着いた色でお越しください。", colors: ["灰桜", "オーツミルク", "セージ", "霧の青"], avoid: "全身白（花嫁の色）と全身黒はお控えください" },
        c: { name: "Snowy Pastel", text: "雪景色に映える色を。アイスブルー、オートミール、くすみピンク、松の緑がおすすめです。", colors: ["アイスブルー", "オートミール", "くすみピンク", "松の緑"], avoid: "全身白（花嫁の色）と全身黒はお控えください" },
      },
      themes: { honey: "はちみつ", candy: "キャンディピンク", mint: "ミント", lavender: "ラベンダー", rose: "灰桜", sage: "セージ", mist: "霧の青", milktea: "ミルクティー", ice: "アイスブルー", silver: "シルバー", rosy: "桜雪", night: "冬の夜" },
    },
    es: {
      groom: "Andrés", bride: "Lucía", initials: ["A", "L"], sealB: ["A", "L"],
      invite: "Nos conocimos en un club de la universidad\ny llevamos diez años juntos.\nEse día queremos que estés\ncon nosotros para celebrar.",
      parents: [{ role: "Padres del novio", names: "Jorge Ramírez y Ana Torres" }, { role: "Padres de la novia", names: "Luis Martínez y Carmen Ruiz" }],
      story: ["Nos saludamos por primera vez en una fiesta del club", "Nuestro primer viaje juntos, a Kioto", "Nos mudamos a nuestro pequeño hogar", "Propuesta en la playa, y dijo que sí", "Ahora queremos que estés en nuestro gran día"],
      schedule: [["Recepción y libro de firmas", "Déjanos un mensaje y tómate fotos con nosotros"], ["Ceremonia", "Acompáñanos en nuestros votos"], ["Banquete", "Disfruta la comida"], ["Entrada de los novios", "¡Prepárate para aplaudir!"], ["Brindis", "Pasaremos a cada mesa a agradecerte"], ["Despedida", "Llévate un detalle dulce"]],
      tips: [["Vegetariano", "Márcalo en el formulario de confirmación"], ["Sillas para niños", "Avísanos si vienes con peques"], ["Estacionamiento", "Gratis 3 horas en el B2"], ["Rincón de fotos", "En la entrada"]],
      venue: "(Ejemplo) Salón Jardín, 3.er piso", address: "Calle Ejemplo 100, tu ciudad",
      transport: ["Metro: estación Ejemplo, salida 2, a 5 minutos caminando", "En auto: busca “Salón de Bodas Ejemplo”"],
      dress: {
        a: { name: "Garden Pastel", text: "Colores pastel suaves, como entrar con nosotros a un jardín en primavera.", colors: ["Rosa cerezo", "Mantequilla", "Menta", "Azul cielo"], avoid: "Por favor evita vestir todo de blanco (el color de la novia) o todo de negro" },
        b: { name: "Muted Garden", text: "Tonos suaves y apagados, como una acuarela ligera.", colors: ["Rosa empolvado", "Avena", "Salvia", "Azul niebla"], avoid: "Por favor evita vestir todo de blanco (el color de la novia) o todo de negro" },
        c: { name: "Snowy Pastel", text: "Un toque de color en la nieve: azul hielo, avena, rosa empolvado o verde pino.", colors: ["Azul hielo", "Avena", "Rosa empolvado", "Verde pino"], avoid: "Por favor evita vestir todo de blanco (el color de la novia) o todo de negro" },
      },
      themes: { honey: "Miel", candy: "Rosa dulce", mint: "Menta", lavender: "Lavanda", rose: "Rosa empolvado", sage: "Salvia", mist: "Azul niebla", milktea: "Té con leche", ice: "Azul hielo", silver: "Plata", rosy: "Nieve rosa", night: "Noche de invierno" },
    },
  };

  const pick = (fallback) => {
    const q = new URLSearchParams(location.search).get("lang");
    return UI[q] ? q : (UI[fallback] ? fallback : "zh");
  };

  // 把範例內容套進 WEDDING（保留時間、圖示、色碼等設定）
  function applySample(W, lang, style) {
    const s = SAMPLE[lang]; if (!s) return;
    W.groom = s.groom; W.bride = s.bride;
    W.initials = style === "a" ? s.initials : s.sealB;
    W.invite = s.invite; W.parents = s.parents;
    W.story = W.story.map((x, i) => ({ ...x, text: s.story[i] || x.text }));
    W.schedule = W.schedule.map((x, i) => ({ ...x, title: (s.schedule[i] || [])[0] || x.title, note: (s.schedule[i] || [])[1] || x.note }));
    W.tips = W.tips.map((x, i) => ({ ...x, title: (s.tips[i] || [])[0] || x.title, text: (s.tips[i] || [])[1] || x.text }));
    W.venue = s.venue; W.address = s.address;
    W.transport = W.transport.map((x, i) => ({ ...x, text: s.transport[i] || x.text }));
    const d = s.dress[style];
    if (d) W.dressCode = { ...W.dressCode, name: d.name, text: d.text, avoid: d.avoid, colors: W.dressCode.colors.map((c, i) => ({ ...c, name: d.colors[i] || c.name })) };
  }

  // 換掉靜態文字；英文、西文把直書改成橫書
  function applyStatic(lang) {
    const u = UI[lang]; document.documentElement.lang = u.html;
    if (!u.t) return;
    document.title = u.t.intro_label;
    document.querySelectorAll("[data-i18n]").forEach((el) => { const v = u.t[el.dataset.i18n]; if (v != null) el.innerHTML = v; });
    document.querySelectorAll("[data-i18n-ui]").forEach((el) => { const v = u[el.dataset.i18nUi]; if (typeof v === "string") el.textContent = v; });
    document.querySelectorAll("[data-i18n-label]").forEach((el) => { const v = u.t[el.dataset.i18nLabel]; if (v != null) el.setAttribute("aria-label", v); });
    if (lang === "en" || lang === "es") {
      const st = document.createElement("style");
      st.textContent = ".vert, .v-copy, .intro-to { writing-mode: horizontal-tb !important; height: auto !important; letter-spacing: .04em !important; line-height: 1.9 !important; }" +
        ".v-copy { position: static !important; margin: 10px auto 0; text-align: center; max-width: 18em; }" +
        ".vert { text-align: center !important; max-width: 22em; }" +
        ".names b { letter-spacing: .06em !important; font-size: 26px !important; } .names { gap: 10px; }" +
        "h1.names { font-size: clamp(28px, 9vw, 44px) !important; letter-spacing: .02em !important; }" +
        ".sh h2 { letter-spacing: .08em !important; } .sr h3, .tip h3, .st p { letter-spacing: .03em !important; }";
      document.head.appendChild(st);
    }
  }

  // 聯絡新人：type 可以是 email／line／instagram；value 留空時顯示「待填寫」
  const LINK = {
    email: (v) => "mailto:" + v,
    line: (v) => "https://line.me/ti/p/~" + encodeURIComponent(v.replace(/^@/, "")),
    instagram: (v) => "https://instagram.com/" + encodeURIComponent(v.replace(/^@/, "")),
  };
  const LABEL = { email: "Email", line: "LINE", instagram: "Instagram" };
  function renderContacts(W, lang, el) {
    if (!el || !W.contacts || !W.contacts.length) return;
    const u = UI[lang], esc = (t) => String(t).replace(/[<>&"]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
    const rows = W.contacts.map((c) => {
      const name = c.who === "bride" ? W.bride : c.who === "groom" ? W.groom : (c.name || "");
      const role = c.role || u.roles[c.who] || "";
      const type = LINK[c.type] ? c.type : "email";
      const v = (c.value || "").trim();
      const val = v ? `<a href="${esc(LINK[type](v))}" target="_blank" rel="noopener">${esc(v)}</a>` : `<span class="hy-pending">${u.pending}</span>`;
      const sep = lang === "zh" || lang === "ja" ? "・" : " · ";
      return `<li><span class="hy-who">${esc(role)}${sep}${esc(name)}</span><span class="hy-how">${LABEL[type]}</span>${val}</li>`;
    }).join("");
    el.innerHTML = `<p class="hy-ch">${u.contactH}</p><ul>${rows}</ul>`;
    if (!document.getElementById("hy-contact-css")) {
      const st = document.createElement("style"); st.id = "hy-contact-css";
      st.textContent = ".hy-contact { margin-top: 22px; padding-top: 18px; border-top: 1px dashed var(--line, rgba(0,0,0,.15)); text-align: center; }" +
        ".hy-contact .hy-ch { font-size: 13.5px; color: var(--muted, #888); letter-spacing: .08em; margin-bottom: 8px; }" +
        ".hy-contact ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 8px; }" +
        ".hy-contact li { display: flex; flex-wrap: wrap; justify-content: center; align-items: baseline; gap: 4px 10px; font-size: 14px; }" +
        ".hy-contact .hy-who { font-weight: 600; } .hy-contact .hy-how { font-size: 12px; color: var(--muted, #888); border: 1px solid var(--line, rgba(0,0,0,.15)); border-radius: 99px; padding: 0 8px; }" +
        ".hy-contact a { color: inherit; text-underline-offset: 3px; word-break: break-all; } .hy-contact .hy-pending { color: var(--muted, #888); }";
      document.head.appendChild(st);
    }
  }

  // 版面：WEDDING.hide 可以拿掉不需要的段落（story／dress／tips／parents／schedule），
  // 拿掉後 A 的色帶重新交錯、B／C 的段落編號重新排
  const HIDE = { story: "story", dress: "dress-sec", tips: "tips-sec", parents: "parents", schedule: "schedule" };
  function applyLayout(W) {
    (W.hide || []).forEach((k) => { const el = document.getElementById(HIDE[k] || k); if (el) el.remove(); });
    const secs = [...document.querySelectorAll("section[data-r]")].filter((s) => !["hero", "invite", "thanks"].includes(s.id));
    if (secs.some((s) => s.classList.contains("band"))) secs.forEach((s, i) => s.classList.toggle("band", i % 2 === 0));
    document.querySelectorAll(".sh .no").forEach((n, i) => { n.textContent = `— ${String(i + 1).padStart(2, "0")} —`; });
  }

  const themeName = (lang, k, zh) => ((SAMPLE[lang] || {}).themes || {})[k] || zh;
  return { UI, SAMPLE, pick, applySample, applyStatic, applyLayout, themeName, renderContacts };
})();
