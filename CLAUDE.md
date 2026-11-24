# wedding.knittinghiyori.com：給 Claude Code 的規則

- 似顏繪喜帖介紹頁（接案用）。**2026-11-07 起 Zoe 完全接手**（原本由 Alison 製作，2026-11-05 交接）。**2026-11-23 起交接給 Alison**（主對話＋所有子對話），接手先讀 `docs/HANDOVER.md`；Alison 在 `alison/<主題>` 分支開 PR，由 Zoe 這邊合併。
- 規則以 knittinghiyori-specs 的 `core.md` §7-1 為準（沒有另開站別檔），cta_id 見 `registry.md`「似顏繪喜帖」。開工前先在 `~/Sites/knittinghiyori/knittinghiyori-specs` `git pull` 再讀。
- 不放 AdSense、不放 Travelpayouts；只放 GA4（content_group `wedding`）。
- `/a/ /b/ /c/` 是範例喜帖：`noindex, nofollow`、不放 GA4、robots.txt 不擋。
- **新人的成品喜帖絕對不要放進這個 repo**（公開 repo 會露出姓名和地址）。成品喜帖放 Cloudflare Pages 專案 `hiyori-invite`，直接上傳，見 core §7-1。
- 估價價格改了要同時改三處：方案卡、估價工具的 `SY` 物件、JSON-LD。
- **範例喜帖多語**（2026-11-07）：A／B／C 共用 `assets/invite-i18n.js`。介面文字在 `UI`，範例內容在 `SAMPLE`。網址加 `?lang=en|ja|es` 切換；做正式喜帖時把 `WEDDING.lang` 設成新人的語言、刪掉 `sample: true`，內容直接寫在 `WEDDING`。英日西介紹頁的範例框與連結帶對應的 `lang`。
- **聯絡新人**（2026-11-08）：`WEDDING.contacts`，每位 `{ who: "groom"|"bride", type: "email"|"line"|"instagram", value: "" }`（同婚可加 `role` 自訂稱呼）；`value` 留空顯示「待填寫」。B、C 的出現動畫在 `assets/invite-reveal.js`。三版結尾都寫 Illustration by Zoe @KnittingHiyori。
- **中文分頁與部落格**（2026-11-21）：`/caricature/ /marriage-certificate/ /web-invitation/ /paper-invitation/ /about/ /blog/` 由 `tools/build_pages.py` 產生（CSS、品牌列、頁尾、首頁選單都從 `index.html` 取），文章寫在 `tools/blog_posts.py`。改完跑 `python3 tools/build_pages.py`，它也會更新 sitemap 的 `<!--HY-PAGES-->` 段。估價工具只在首頁，分頁用 `/?sy=…`、`/?web=…`、`/?paper=1`、`/?all=1` 帶入方案。價格改了多兩處：`build_pages.py`、`tools/blog_kit.py` 的 `SERVICES`（文章裡的服務卡片）。
- **成品喜帖網址**（Zoe 2026-11-22）：`<婚禮日期 YYMMDD>-<新人英文名>`，例 `270124-zoe-alison`。GA4 `WEDDING.ga.until` 填上線到期日 YYMMDD（例 `270228`），報表看到過期就去關掉。
- **分享預覽**：每份成品喜帖的 `<head>` 都要改 og:title、og:description、og:image（完整網址），預覽圖用 `python3 tools/make_og.py --couple 去背似顏繪.png --names "名字 & 名字" --date "2027.03.20  SAT" --line2 "一句話" --style a|b|c --out og.jpg` 產生，放進喜帖資料夾一起上傳。

- **工作模式**（Zoe 2026-11-22，Alison 同樣適用）：見 `docs/WORKFLOW.md`。子對話把各自的頁面、文章系列、客戶做好；主對話是整體顧問。

## 部落格寫作規範（2026-11-23，部落格版型子對話；文章系列子對話照這個寫）

讀者沒耐心、沒時間，**一眼就要看到重點**。元件在 `tools/blog_kit.py`，文章寫在 `tools/blog_posts.py`，範例看「同性結婚登記」與「婚禮歌單」兩篇。少了固定元素，`build_pages.py` 會停下來說缺什麼。

**做一篇的順序**：先給 Zoe 大綱 → 同意後寫進 `blog_posts.py` → `python3 tools/make_blog_img.py <slug>` 產生兩張圖 → `python3 tools/build_pages.py` → 390／1200 寬看過 → 開 PR。新文章在 knittinghiyori-specs `registry.md`「似顏繪喜帖」加一列（page_title `喜帖|部落格|<ga>`），寫 CHANGELOG。

**每篇的欄位**

| 欄位 | 寫什麼 |
|---|---|
| `slug` | 英文網址，用搜尋關鍵字（例 `wedding-songs`） |
| `cat` | 分類代號，見 `build_pages.py` 的 `CATS`（`registration` 結婚登記與法規、`planning` 婚禮籌備）；要新分類請版型子對話加 |
| `title` | `<title>`：關鍵字放最前面，含年份或數字，結尾「｜編織日和」 |
| `h1` | 頁面標題，可用 `<br>` 換行 |
| `desc` | 120～160 字，回答「這篇能幫我什麼」 |
| `ga` | GA4 page_title 第三段 |
| `published`、`modified` | YYYY-MM-DD；改內容就更新 `modified`（sitemap 跟著變） |
| `cover` | 封面圖（1200×630，也是 og:image）：`img` 檔名＝slug＋`.jpg`、`alt` 一句含關鍵字的描述、`title`（`\n` 換行）、`sub`、`kicker`（英文小字）、`art`（右邊插圖，不寫就畫兩個交扣的戒指）。**不放浮水印** |
| `summary` | **剛好 3 句**結論，重點用 `<b>`；放在封面正下方 |
| `toc` | 選填，`{"h2 的 id": "短一點的目錄字"}`；目錄會自動抓每個 `<h2 id="…">` |
| `cheat` | 懶人包圖（1080×1350）：`img`、`alt`、`kicker`、`title`、`points`＝3～6 個 `("標題", "一句說明")`、`caption`、`foot`（例「2026-11 依戶政司資料查核」）。圖最下面自動放網站網址 |
| `service` | 文末服務卡片：`caricature`、`cert`、`web`、`paper`、`package` |
| `lead` | 開場一段（在結論與目錄下面） |
| `body` | f-string，用下面的元件 |
| `faq` | `[(問, 答)]`，3～6 題，問句用讀者會搜尋的說法；頁面和 JSON-LD 自動同一份文字 |
| `sources` | `[(名稱, 網址)]`，法規類一定附官方連結 |

**內文元件**（在 `body=f"""…"""` 裡用 `{…}` 放）

- `{steps(("標題", "說明"), …)}`：有先後順序的事一律用編號步驟。
- `{table(["欄 1", "欄 2"], [列…], [列…])}`：比較、文件清單用表格；手機自動變小卡（第一欄當卡片標題）。很寬、不適合變小卡的表格加 `stack=False`。
- `{box("tip"|"warn"|"note", "內文", title=None)}`：粉紅＝💡 小撇步、黃＝⚠️ 注意（會出錯、會被退件）、藍＝📌 提醒（規定可能變動）。**一篇最多 4 個**。
- `{CHEAT}`：懶人包圖放的位置，全文 1 次，放在讀者最想存起來的那段後面。
- `{mid("服務代號", "讀者心裡的那句話")}`：中間情境卡，**全文剛好 1 張**，放在「讀者剛好需要這個服務」的段落後面。例 `mid("cert", "登記那天要帶書約？")`。不寫「推薦」「廣告」。
- 清單用 `<ul class="check">`；`<h2>` 一定要有 `id`（目錄和錨點用）。

**服務只放 2 處**：中間情境卡 1 張＋文末服務卡 1 張（自動）。內文的文字連結可以有，但不要再加按鈕或其他卡片。文章底部不放全套方案框。

**SEO 與連結**

- 每篇自動產生：BlogPosting（含封面與懶人包兩張圖、分類）、FAQPage、麵包屑、og:type article、發布與更新時間。
- 文章之間：「延伸閱讀」自動列同分類的文章（最多 4 篇）；內文提到其他文章時直接寫文字連結。
- 文章與服務頁：服務頁底部的「延伸閱讀」會自動列出連到它的文章（內文有連結、`mid` 或 `service` 指到它就算），不用手動加。
- 用字：中文全形標點，不用 em dash、en dash（build 會擋）；法規類以官方公告為主，不確定的寫「待確認」並問 Zoe。

