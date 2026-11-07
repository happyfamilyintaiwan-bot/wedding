# wedding.knittinghiyori.com：給 Claude Code 的規則

- 似顏繪喜帖介紹頁（接案用）。**2026-11-07 起 Zoe 完全接手**（原本由 Alison 製作，2026-11-05 交接）。
- 規則以 knittinghiyori-specs 的 `core.md` §7-1 為準（沒有另開站別檔），cta_id 見 `registry.md`「似顏繪喜帖」。開工前先在 `~/Sites/knittinghiyori/knittinghiyori-specs` `git pull` 再讀。
- 不放 AdSense、不放 Travelpayouts；只放 GA4（content_group `wedding`）。
- `/a/ /b/ /c/` 是範例喜帖：`noindex, nofollow`、不放 GA4、robots.txt 不擋。
- **新人的成品喜帖絕對不要放進這個 repo**（公開 repo 會露出姓名和地址）。成品喜帖放 Cloudflare Pages 專案 `hiyori-invite`，直接上傳，見 core §7-1。
- 估價價格改了要同時改三處：方案卡、估價工具的 `SY` 物件、JSON-LD。
- **範例喜帖多語**（2026-11-07）：A／B／C 共用 `assets/invite-i18n.js`。介面文字在 `UI`，範例內容在 `SAMPLE`。網址加 `?lang=en|ja|es` 切換；做正式喜帖時把 `WEDDING.lang` 設成新人的語言、刪掉 `sample: true`，內容直接寫在 `WEDDING`。英日西介紹頁的範例框與連結帶對應的 `lang`。
- **聯絡新人**（2026-11-08）：`WEDDING.contacts`，每位 `{ who: "groom"|"bride", type: "email"|"line"|"instagram", value: "" }`（同婚可加 `role` 自訂稱呼）；`value` 留空顯示「待填寫」。B、C 的出現動畫在 `assets/invite-reveal.js`。三版結尾都寫 Illustration by Zoe @KnittingHiyori。
