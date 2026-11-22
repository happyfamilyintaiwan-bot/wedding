"""wedding 部落格文章（中文）。build_pages.py 會讀這裡產生 /blog/<slug>/ 與部落格首頁。

每篇：slug、title（<title>）、h1、desc、ga（page_title 第三段）、published、modified、lead、body（HTML）、faq [(問, 答)]、sources [(名稱, 網址)]
"""

POSTS = []

# ── 1. 同性結婚登記（2026-02-04 原刊於 knittinghiyori.com/same-sex-marriage-in-taiwan/，2026-11-21 搬家改寫） ──
POSTS.append(dict(
    slug="same-sex-marriage-registration-taiwan",
    title="同性結婚登記怎麼辦？2026 台灣同婚登記流程、結婚書約法條與跨國伴侶規定｜編織日和",
    h1="台灣同性結婚登記全攻略：<br>流程、要帶什麼、書約法條與跨國伴侶規定",
    desc="台灣同性結婚登記一次看懂：誰可以登記（台灣人、外籍、港澳、中國大陸配偶與兩位外國人）、要帶哪些證件、同婚書約要引用哪條法條、一定要戶口名簿嗎、不能到場怎麼辦。依內政部戶政司資料整理，2026-11-21 查核。",
    ga="同性結婚登記全攻略",
    published="2026-02-04",
    modified="2026-11-21",
    lead="我們自己也是同婚伴侶，走過一次結婚登記。第一次走進戶政事務所，最怕的不是排隊，而是「文件到底對不對」。這篇把同性結婚登記的流程、要帶的東西、書約上的法條，還有跨國伴侶最常卡關的規定，照內政部戶政司的公告一次整理好。",
    body="""
<div class="tldr">
  <b>先說結論</b>
  <ul>
    <li>在台灣，婚姻是否成立，看的是<b>戶政事務所的結婚登記</b>；有沒有辦婚禮、宴客、拍婚紗都不影響。</li>
    <li>同性結婚的法律依據是<b>《司法院釋字第七四八號解釋施行法》</b>，不是《民法》婚姻章，所以書約上的法條要寫對。</li>
    <li>要帶：結婚書約（2 位證人簽名或蓋章）、雙方身分證、印章或簽名、戶口名簿、2 年內的證件照。</li>
    <li>台灣人＋外國人、台灣人＋港澳居民都可以登記；兩位外國人要<b>雙方國家都承認同性婚姻</b>才可以。</li>
  </ul>
</div>

<h2 id="who">誰可以在台灣辦同性結婚登記？</h2>
<p>同性婚姻在台灣是合法婚姻，流程跟異性婚姻原則上一樣。真正的差別在「你們兩個人的身分組合」：</p>
<div class="tbl"><table>
  <thead><tr><th>兩人的身分</th><th>可以在台灣登記嗎？</th><th>要注意的事</th></tr></thead>
  <tbody>
    <tr><td>兩位台灣人</td><td>✅ 可以</td><td>到任一戶政事務所辦理</td></tr>
    <tr><td>台灣人＋外國人</td><td>✅ 可以</td><td>外籍配偶的國家沒有同婚也可以；若是外交部公告的特定國家，要附駐外館處的面談結果通知函</td></tr>
    <tr><td>台灣人＋香港、澳門居民</td><td>✅ 可以</td><td>港澳作成的文件要經行政院指定的機構驗證</td></tr>
    <tr><td>台灣人＋中國大陸人士</td><td>⚠️ 有條件</td><td>要先在承認同性婚姻的第三地（例如美國）結婚生效，通過面談後才能在台登記（2024 年 9 月 19 日起）</td></tr>
    <tr><td>兩位外國人</td><td>⚠️ 有條件</td><td>雙方的國家或地區<b>都</b>承認同性婚姻，才可以在台灣登記</td></tr>
  </tbody>
</table></div>

<h3 id="hk">兩個香港人可以在台灣同性結婚嗎？</h3>
<p>依現行實務，<b>目前不行</b>。台灣處理港澳人士的婚姻，是依《香港澳門關係條例》類推適用《涉外民事法律適用法》，婚姻成立要看雙方原本適用的法律；香港、澳門目前都沒有承認同性婚姻，所以兩位港澳居民（都沒有台灣身分時）還沒辦法在台灣登記。</p>
<p>如果其中一方是台灣人，就可以登記。規定可能變動，實際狀況請在登記前先問戶政事務所。</p>

<h3 id="foreigners">兩個外國人可以在台灣同性結婚嗎？</h3>
<p>要看兩個人的國籍：<b>雙方的國家或地區都承認同性婚姻</b>，才可以在台灣辦結婚登記。只要其中一方的國家不承認，目前就沒辦法。哪些國家承認同婚，以戶政司「常見問答集」公告的名單為準。</p>

<h2 id="documents">結婚登記要帶什麼？</h2>
<p>在國內結婚，雙方都要帶<b>正本</b>：</p>
<ul class="check">
  <li>結婚書約（雙方簽名或蓋章，加上 2 位以上證人簽名或蓋章）</li>
  <li>國民身分證</li>
  <li>印章（或簽名）</li>
  <li>戶口名簿</li>
  <li>最近 2 年內拍攝、符合規格的證件照 1 張（或上傳數位相片；戶政系統裡的照片在 2 年內、人貌相符的話可以免附）</li>
</ul>
<p>外籍配偶另外要準備：護照或居留證、外籍配偶取用中文姓名聲明書、經駐外館處驗證的婚姻狀況證明（核發後 6 個月內有效）。外文文件要附經驗證或公證的中文譯本。</p>

<h3 id="household">同性結婚登記一定要戶口名簿嗎？</h3>
<p>要。戶政司列的應備證件裡，在國內結婚的雙方都要附戶口名簿。如果戶口名簿不在自己手上，可以先跟家人借，或到戶政事務所問能不能用其他方式處理。</p>

<h2 id="certificate">同性結婚書約要寫什麼？法條怎麼引用？</h2>
<p>這是最容易被忽略、也最重要的一步。同性婚姻適用的是《司法院釋字第七四八號解釋施行法》，書約上應該引用這部法律，而不是只寫《民法》的舊式異性婚姻範本。</p>
<div class="law">
  <div><b>第 2 條</b>相同性別之二人，得為經營共同生活之目的，成立具有親密性及排他性之永久結合關係。</div>
  <div><b>第 4 條</b>成立第二條關係應以書面為之，有二人以上證人之簽名，並應由雙方當事人，向戶政機關辦理結婚登記，方為有效。</div>
</div>
<p>書約上要寫的資料：</p>
<ul class="check">
  <li>雙方的姓名、出生日期</li>
  <li>國民身分證統一編號（外籍：護照號碼或居留證號碼）</li>
  <li>戶籍地址（外籍：國外居住地址）</li>
  <li>2 位以上證人的簽名或蓋章</li>
</ul>
<p>另外也建議留意書約的用字：很多傳統範本寫「夫／妻」、預設一男一女，甚至有「傳宗接代」這類句子。對同性伴侶來說，這不是流程錯誤，而是文件不友善。書約格式沒有規定一定要用戶政事務所的版本，只要內容符合上面的要件就可以；不確定的話，登記前把書約拿給戶政事務所看一下最保險。</p>
<p class="cta-inline">我們的<a href="/marriage-certificate/">似顏繪結婚書約</a>有同婚版和一般版，會依你們的狀況套用對應的法條文字。</p>

<h2 id="process">結婚登記當天怎麼走？</h2>
<ol class="steps">
  <li><b>預約（建議）</b>：多數戶政事務所可以不預約，但情人節、好日子名額很快就滿。各縣市網路預約的規則不太一樣，請看你要去的戶政事務所網站。</li>
  <li><b>到任一戶政事務所</b>：不限戶籍地。</li>
  <li><b>取號、交證件和書約</b>，承辦人員核對資料。</li>
  <li><b>雙方簽名或蓋章</b>，完成登記。通常 15～30 分鐘（不含等候）。</li>
</ol>
<h3 id="date">想指定結婚日期，但那天不能到場？</h3>
<p>可以在想要的結婚日<b>前 3 個辦公日內</b>先去戶政事務所辦，並指定結婚登記日；指定的日期不限上班日，週末或假日也可以。真的無法本人辦理的話，要有正當理由、經戶政事務所核准，才能用書面委託別人辦。</p>

<h2 id="abroad">已經在國外結婚了，回台灣要怎麼登記？</h2>
<p>帶經駐外館處驗證的國外結婚證明（或當地政府的結婚登記證明）和中文譯本，加註「符合行為地法」，就可以到任一戶政事務所登記，通常可以免附婚姻狀況證明。也可以在國外先向駐外館處申請驗證，再由他們轉回戶籍地的戶政事務所辦理。</p>

<h2 id="us">寫給正在準備登記的你</h2>
<p>不論是同性還是異性婚姻，在台灣你都有權利完成結婚登記，也有權利選一份尊重你們關係的書約。結婚登記不只是蓋章，而是被承認的那一刻——我們自己走過，知道那份緊張，也知道那份踏實。</p>
""",
    faq=[
        ("兩個香港人可以在台灣同性結婚嗎？", "依現行實務目前不行。台灣處理港澳人士婚姻是類推適用《涉外民事法律適用法》，要看雙方原本適用的法律；香港、澳門都沒有承認同性婚姻。若其中一方是台灣人就可以登記。登記前請向戶政事務所確認最新規定。"),
        ("兩個外國人可以在台灣同性結婚嗎？", "雙方的國家或地區都承認同性婚姻，才可以在台灣辦結婚登記；只要其中一方的國家不承認，目前就沒辦法。"),
        ("台灣人和外國人可以同性結婚嗎？", "可以。外籍配偶的國家沒有同婚也可以登記；若是外交部公告的特定國家人士，要附駐外館處核發的面談結果通知函。"),
        ("同性結婚登記一定要戶口名簿嗎？", "要。在國內結婚的雙方都要帶戶口名簿正本，另外還有身分證、印章或簽名、結婚書約和 2 年內的證件照。"),
        ("同性結婚書約要引用哪一條法律？", "引用《司法院釋字第七四八號解釋施行法》第 2 條與第 4 條，不是《民法》婚姻章。書約要寫雙方姓名、出生日期、身分證字號（或護照、居留證號碼）、戶籍地址，以及 2 位以上證人簽名或蓋章。"),
        ("同性結婚登記一定要本人到場嗎？", "原則上雙方要親自到戶政事務所。有正當理由並經戶政事務所核准，才能書面委託他人辦理；也可以在結婚日前 3 個辦公日內先辦，並指定結婚登記日。"),
    ],
    sources=[
        ("內政部戶政司：同性結婚登記（應備證件與注意事項）", "https://www.ris.gov.tw/documents/html/2/3/1/401.html"),
        ("內政部新聞：兩岸同性伴侶在第三地結婚後可在臺辦理結婚登記（2024-09-19）", "https://www.moi.gov.tw/News_Content.aspx?n=4&s=321066"),
        ("臺北市政府：常見問答－同性之結婚登記作業", "https://ca.gov.taipei/News_Content.aspx?n=59F2E04A34FDA3E8&s=99D8A9A946E09128"),
        ("台灣伴侶權益推動聯盟：跨國同婚 Q&A", "https://tapcpr.org/main-topics/transnational-same-sex-marriage/"),
    ],
))

# ── 2. 婚禮歌單（2026-11-21 初稿，11-22 依 Alison 選歌改寫） ──
# 每首：(歌名, 歌手, YouTube 影片 id, 標記, 備註)
# 標記：a＝我們私心推薦　t＝Threads 網友推薦　f＝電影／影集婚禮場景　o＝電影／戲劇原聲帶（OST）
# YouTube id 由 Alison 提供或 2026-11-22 搜尋官方頻道，換影片只改這裡
SCENE_SONGS = [
    ("welcome", "迎賓歌單", "賓客入場、簽到、找座位的時候播。挑輕快、溫暖、大家都聽得舒服的歌，音量不用太大。", [
        ("Stay with Me", "裘德", "UQgBwAzGgd8", "ao", "陸劇《今天是太陽雨》（2026）治癒主題曲"),
        ("有你的快樂", "王若琳", "qZiNigAO-zQ", "a", ""),
        ("想和你看五月的晚霞", "陳華 feat. 呂植宇", "ljd9ISixsWo", "a", ""),
        ("I'm Yours", "Jason Mraz", "EkHTsc9PU2A", "a", ""),
        ("Sugar", "Maroon 5", "09R8_2nJtjg", "a", "MV 就是樂團突襲別人的婚禮"),
        ("24/7, 365", "elijah woods", "-h_yBTriuaY", "a", ""),
        ("I Love You 3000", "Stephanie Poetri", "cPkE0IbDVs4", "a", "歌名來自電影《復仇者聯盟：終局之戰》的台詞"),
        ("Home", "Reese Lansangan", "L2SvzMjATLI", "a", ""),
        ("Little Things", "One Direction", "xGPeNN9S0Fg", "a", ""),
        ("blue", "yung kai", "4adZ7AguVcw", "a", ""),
        ("golden hour", "JVKE", "PEM0Vs8jf1w", "t", ""),
        ("Lucky", "Jason Mraz, Colbie Caillat", "acvIVA9-FMQ", "t", ""),
        ("讓我餘生只為你唱情歌", "冰球樂團", "I3440shDJYw", "t", ""),
        ("I Know You Know I Love You", "落日飛車", "fGEV6qi9aJQ", "t", ""),
    ]),
    ("first-entrance", "一進歌單（新人第一次進場）", "整場婚禮最重要的一首。挑你們聽了會想哭、或對你們有特別意義的歌；從前奏到走到台前大約 1～2 分鐘，可以先剪好段落。", [
        ("Can't Help Falling in Love", "Kina Grannis", "tyoAsprwDRc", "atf", "電影《瘋狂亞洲富豪》婚禮走紅毯，Kina Grannis 本人在片中現場演唱"),
        ("A Thousand Years", "Christina Perri", "rtOvBOTyX00", "tf", "電影《暮光之城：破曉 上》原聲帶，被很多新人拿來當進場曲"),
        ("Turning Page", "Sleeping At Last", "-hb2tecD13s", "f", "電影《暮光之城：破曉 上》Bella 走向 Edward 的婚禮紅毯"),
        ("第一支舞 feat. 劉若英", "傻子與白痴", "Dz6hLlLphcc", "at", ""),
        ("I Do（當我走向你）", "楊默依 Moi Yang", "pT5_E60cbkc", "atfo", "陸劇《當我飛奔向你》蘇在在與張陸讓的結婚曲"),
        ("你朝我的方向走來", "馬念先 & 9m88", "7L06_HW_HcA", "a", "歌名就是進場的畫面"),
        ("Yes, I Do", "Mary See the Future", "WDrashJRQK0", "at", ""),
        ("When You Say Nothing At All", "Ronan Keating", "IobNcpiwpSc", "ao", "電影《新娘百分百》（Notting Hill，1999）插曲"),
        ("Grow Old With You", "Adam Sandler", "TPsW2FYprfI", "o", "電影《婚禮歌手》（The Wedding Singer，1998）男主角為女主角寫的歌"),
        ("You Are the Reason", "Calum Scott", "ShZ978fBl6Y", "at", ""),
        ("Perfect", "Ed Sheeran", "2Vv-BfVoq4g", "t", "有網友的另一半在進場時現場唱"),
        ("Beautiful in White", "Shane Filan", "06-XXOTP3Gc", "t", ""),
        ("It's You", "HENRY", "0dLezZIZOAQ", "t", ""),
        ("I Belong to You", "Jacob Lee", "vtcBNdIq1ms", "t", "比較小眾，不容易撞歌"),
        ("Always in My Heart", "Tamaru Yamada", "FxcGYS2Ca7U", "t", ""),
    ]),
    ("family-entrance", "和爸爸、家人一起進場", "從父母把孩子交出去的角度寫的歌，很容易讓全場一起紅眼眶。", [
        ("Give Me Away", "Riley Roth", "vYHBlymJAxg", "t", ""),
        ("If You Love Her (feat. Meghan Trainor)", "Forest Blakk", "nvSO4sP5yGs", "t", ""),
    ]),
    ("instrumental", "純音樂進場（沒有歌詞）", "想讓誓詞或主持人說話時不被歌詞干擾，就選純音樂。", [
        ("A Thousand Years（婚禮版）", "Brooklyn Duo", "4Wxi4sVCeo0", "t", "大提琴＋鋼琴"),
        ("Canon in D（卡農）", "Brooklyn Duo", "Ptk_1Dc2iPY", "t", ""),
        ("拉赫曼尼諾夫 第二號交響曲 第三樂章", "古典", "QNRxHyZDU-Q", "t", "網友說聽了會哭"),
        ("Married Life", "Michael Giacchino", "S1uWHjhluTI", "fo", "動畫電影《天外奇蹟》（Up，2009）開場的婚禮與婚後人生"),
        ("Wedding Processional & Maria", "《真善美》原聲帶", "gyP7-OSixNk", "fo", "電影《真善美》（The Sound of Music，1965）瑪莉亞走向教堂聖壇"),
    ]),
    ("second-entrance", "二進歌單（換裝後第二次進場）", "換好第二套禮服再進場，氣氛可以輕快、甜一點，適合邊走邊和賓客互動。", [
        ("Marry You", "Bruno Mars", "dElRVQFqj-k", "af", "影集《歡樂合唱團》婚禮上的合唱"),
        ("Lover", "Taylor Swift", "-BjZmE2gtdo", "a", ""),
        ("Enchanted", "Taylor Swift", "rGAS66E9rMQ", "a", ""),
        ("My Universe", "Coldplay X BTS", "bZYPI4mYwhw", "a", ""),
        ("給你一瓶魔法藥水", "告五人", "lPKjHE6KjYY", "a", ""),
        ("讓我住進你心裡", "溫蒂漫步", "dUuhTw3gB5I", "a", ""),
        ("Lucky Me", "Jake Miller", "XysLGnlSjE0", "t", "從新郎的角度寫，MV 是求婚"),
        ("Love Wins All", "IU", "JleoAppaxi0", "t", "有網友用聲樂版進場"),
        ("1000x (feat. BROODS)", "Jarryd James", "l3FV7pnTNeo", "t", ""),
        ("10000 HOURS", "宇宙人", "uXEiWgnzSKU", "t", ""),
        ("Love Is All Around", "Wet Wet Wet", "h3gEkwhdXUE", "o", "電影《你是我今生的新娘》（Four Weddings and a Funeral，1994）主題曲"),
        ("사탕 (Candy)", "SEVENTEEN", "tA-FizlZp7Q", "t", ""),
    ]),
    ("dinner", "用餐歌單", "用餐時間最長，準備一份長歌單循環播放。挑溫柔、不搶話的歌，讓賓客能好好聊天。", [
        ("慢慢喜歡你", "莫文蔚", "kqqraGvoqVs", "a", ""),
        ("A Little Love", "馮曦妤 Fiona Fung", "ZT2k6CSZRks", "at", ""),
        ("그대가 해준 말 (My Beloved)", "LeeHi 李遐怡", "UU0SXJ9hV-Y", "a", ""),
        ("愛のカタチ", "ASA", "kyfDIElQYp0", "a", ""),
        ("黑暗的盡頭", "脆樂團", "k20rL10W6Nk", "a", ""),
        ("餘生是你", "蘇北北", "-1AIYFzPDIE", "a", ""),
        ("At My Worst", "Pink Sweat$", "8CEJoCr_9UI", "a", ""),
        ("Flightless Bird, American Mouth (Wedding Version)", "Iron & Wine", "JCH0KsYg0Yw", "f", "電影《暮光之城：破曉 上》婚禮"),
        ("Il Mondo", "Jimmy Fontana", "HFyCfFJC0no", "fo", "電影《真愛每一天》雨中婚禮"),
        ("Special Person", "方大同", "IscPlLsh6iU", "t", ""),
        ("My Only", "周深", "D3v6xi9iBL0", "to", "陸劇《開端》片尾曲 OST，網友推了 3 次"),
        ("Speechless", "James TW", "tfg_jftGPYc", "t", ""),
        ("Beautiful", "Crush", "W0cs6ciCt_k", "to", "韓劇《鬼怪》OST"),
        ("Home", "Janet Suhh", "D3xWVohUV5Y", "to", "韓劇《那年，我們的夏天》OST"),
        ("此刻", "袁婭維", "48dVMEuaN8g", "to", "陸劇《早春晴朗》OST（片尾曲）"),
        ("直到我遇見了你", "李友廷", "oRJKbrYznpk", "t", ""),
        ("愛是我們必經的辛苦", "脆樂團", "Y91dVmqF0jU", "t", ""),
        ("虹", "菅田將暉", "hkBbUf4oGfA", "tfo", "電影《STAND BY ME 哆啦A夢 2》（2020）主題曲，故事就是大雄和靜香的婚禮"),
        ("My Love", "李承哲", "hXiCB6SZp4U", "t", "MV 就是一段求婚"),
        ("Make You Feel My Love", "Adele", "0put0_a--Ng", "t", ""),
        ("How Long Will I Love You", "Ellie Goulding", "an4ySOlsUMY", "to", "電影《真愛每一天》（About Time，2013）插曲，Ellie Goulding 版收在電影原聲帶"),
    ]),
    ("toast", "逐桌敬酒歌單（如果有敬酒的話）", "敬酒時長輩比較多，放大家都會哼的經典老歌最保險，也可以穿插你們的新歌。", [
        ("牽手", "蘇芮", "wJNHRweW5WE", "a", ""),
        ("給你們", "張宇", "0OSXMi9_WBQ", "a", ""),
        ("最浪漫的事", "趙詠華", "VmeM46a3IDc", "a", ""),
        ("Nothing's Gonna Change My Love for You", "西城男孩 Westlife", "dmVtts8oPjA", "at", ""),
        ("不是因為天氣晴朗才愛妳", "理想混蛋", "9_068Ekk_fs", "a", ""),
        ("最後一個", "滅火器", "ErMqFuZx1x0", "t", ""),
        ("我的宣言 My Vow", "周柏豪", "z9zMcvn_xkI", "t", ""),
        ("How Deep Is Your Love", "Bee Gees", "XpqqjU7u5Yc", "t", ""),
        ("Truly Madly Deeply", "Savage Garden", "WQnAxOQxQIU", "t", ""),
        ("Because You Loved Me", "Céline Dion", "gMOovDrWWiI", "to", "電影《Up Close & Personal》（1996）主題曲"),
        ("The Rose", "西城男孩 Westlife", "VTCQBuYhq_s", "t", ""),
        ("Eternal Flame", "The Bangles", "PSoOFn3wQV4", "t", ""),
    ]),
    ("farewell", "送客歌單", "合照、送客時放快樂一點的歌，讓大家帶著好心情回家。", [
        ("Can't Stop the Feeling!", "Justin Timberlake", "ru0K8uYEZWw", "ao", "動畫電影《魔髮精靈》（Trolls，2016）主題曲"),
        ("I Do, I Do, I Do, I Do, I Do", "ABBA", "tW3HN_pvbE4", "f", "電影《媽媽咪呀！》婚禮"),
        ("All You Need Is Love", "Lynden David Hall", "m_2q1rclwNE", "f", "電影《愛是您，愛是我》教堂婚禮上的驚喜演出"),
        ("Nothin' on You (feat. Bruno Mars)", "B.o.B", "8PTDv_szmL0", "t", ""),
        ("Die With a Smile", "Lady Gaga, Bruno Mars", "kPa7bsKwL-c", "t", ""),
        ("Waste My Time", "Marc Atlas", "IS4BvLsl7tM", "t", ""),
        ("Hold On", "Wilson Phillips", "uIbXvaE39wM", "fo", "電影《伴娘我最大》（Bridesmaids，2011）婚禮上的驚喜演出"),
        ("Shout", "The Isley Brothers", "DPVf01jXL7M", "f", "電影《婚禮終結者》（Wedding Crashers，2005）婚宴上全場跳舞"),
    ]),
]
SONG_COUNT = sum(len(s[3]) for s in SCENE_SONGS)
_ALL = {t: (t, a, v, m, n) for _, _, _, rows in SCENE_SONGS for t, a, v, m, n in rows}
TOP = ["A Thousand Years", "Can't Help Falling in Love", "Perfect", "My Only", "Beautiful in White", "You Are the Reason", "第一支舞 feat. 劉若英", "Speechless"]
TOP_WHY = {"A Thousand Years": "網友心中的「感人婚禮歌」代表", "Can't Help Falling in Love": "我們最推 Kina Grannis 版", "Perfect": "進場經典，網友推最多次之一",
           "My Only": "網友推了 3 次", "Beautiful in White": "經典進場曲", "You Are the Reason": "我們和網友都推", "第一支舞 feat. 劉若英": "華語進場首選", "Speechless": "網友推了 2 次"}
FILMS = [  # 電影／影集裡的婚禮場景
    ("真善美（The Sound of Music，1965）", "Wedding Processional & Maria", "《真善美》原聲帶", "瑪莉亞走向教堂聖壇"),
    ("愛是您，愛是我（Love Actually，2003）", "All You Need Is Love", "Lynden David Hall", "教堂婚禮的驚喜演出"),
    ("婚禮終結者（Wedding Crashers，2005）", "Shout", "The Isley Brothers", "婚宴上全場跳舞"),
    ("媽媽咪呀！（Mamma Mia!，2008）", "I Do, I Do, I Do, I Do, I Do", "ABBA", "婚禮"),
    ("天外奇蹟（Up，2009）", "Married Life", "Michael Giacchino", "開場的婚禮與婚後人生"),
    ("伴娘我最大（Bridesmaids，2011）", "Hold On", "Wilson Phillips", "婚禮上的驚喜演出"),
    ("暮光之城：破曉 上（2011）", "Turning Page", "Sleeping At Last", "Bella 走向 Edward 的紅毯"),
    ("暮光之城：破曉 上（2011）", "Flightless Bird, American Mouth (Wedding Version)", "Iron & Wine", "婚禮"),
    ("真愛每一天（About Time，2013）", "Il Mondo", "Jimmy Fontana", "雨中婚禮"),
    ("瘋狂亞洲富豪（Crazy Rich Asians，2018）", "Can't Help Falling in Love", "Kina Grannis", "婚禮走紅毯，歌手本人在片中演唱"),
    ("STAND BY ME 哆啦A夢 2（2020）", "虹", "菅田將暉", "主題曲，故事是大雄和靜香的婚禮"),
    ("影集《歡樂合唱團》（Glee）", "Marry You", "Bruno Mars", "婚禮上的合唱"),
    ("陸劇《當我飛奔向你》", "I Do（當我走向你）", "楊默依 Moi Yang", "蘇在在與張陸讓的結婚曲"),
]
PICK = "Stay with Me"  # 編輯私心推薦第 1 首（Zoe 2026-11-22）
PICK_WHY = "陸劇《今天是太陽雨》（2026，楊超越、董思成主演）的治癒主題曲。歌名「Stay with Me」就是一句「留在我身邊」，是婚禮上最想對另一半說的話；放在迎賓或用餐時間，看過這部劇的賓客一聽就會會心一笑。"
NEUTRAL = ["A Thousand Years", "Can't Help Falling in Love", "Make You Feel My Love", "How Long Will I Love You", "Lucky", "Special Person"]


def _yt(v):
    return f"https://www.youtube.com/watch?v={v}"


def _song_li(t, a, v, m, n):
    tags = ("<i class=\"tag a\">我們推</i>" if "a" in m else "") + ("<i class=\"tag t\">網友推</i>" if "t" in m else "") + ("<i class=\"tag f\">🎬 婚禮場景</i>" if "f" in m else "") + ("<i class=\"tag o\">🎵 影視原聲</i>" if "o" in m else "")
    note = f"<small>{n}</small>" if n else ""
    return f'<li><a href="{_yt(v)}" target="_blank" rel="noopener" data-cta="song_play" data-cta-type="wedding"><b>{t} <span class="play">▶</span></b><span>{a}</span>{note}<span class="tags">{tags}</span></a></li>'


def _scene(sid, name, intro, rows, level="h2"):
    return f'<{level} id="{sid}">{name}</{level}><p>{intro}</p><ul class="songs">' + "".join(_song_li(*r) for r in rows) + "</ul>"


_scenes = dict((s[0], s) for s in SCENE_SONGS)
_body = f"""
<div class="tldr" id="pick">
  <b>編輯私心推薦第 1 首</b>
  <ul class="songs" style="grid-template-columns:1fr;margin:10px 0 6px">{_song_li(*_ALL[PICK])}</ul>
  <p>{PICK_WHY}</p>
</div>
<div class="tldr">
  <b>婚禮歌單怎麼分？</b>
  <ul>
    <li><b>迎賓</b>：賓客入場、簽到時，輕快溫暖。</li>
    <li><b>一進</b>：新人第一次進場，整場最重要、最感人的一首。</li>
    <li><b>二進</b>：換第二套禮服後再進場，輕快甜蜜。</li>
    <li><b>用餐</b>：最長的一段，準備一份溫柔不搶話的長歌單。</li>
    <li><b>逐桌敬酒</b>：長輩多，放大家都會哼的經典老歌。</li>
    <li><b>送客</b>：合照、送客，快樂收尾。</li>
  </ul>
</div>
<p class="note-box">點歌名會開 YouTube 影片，可以直接試聽。「我們推」是我們自己喜歡的歌；「網友推」整理自 Threads 網友推薦（2026-11-21 擷取，很多是新人自己婚禮真的用過的）；「🎬 婚禮場景」是在電影或影集婚禮裡出現過的歌；「🎵 影視原聲」是電影或戲劇原聲帶裡的歌。</p>

<h2 id="how-many">一進、二進是什麼？婚禮歌單要準備幾首？</h2>
<p><b>一進</b>是新人在婚宴開場第一次進場，<b>二進</b>是新人換第二套禮服後再次進場。婚禮音樂可以分成兩種：</p>
<ul class="check">
  <li><b>儀式歌</b>：一進、二進、和家人進場、送客等時刻，各挑 1 首，大約 4～6 首，最需要花心思。</li>
  <li><b>背景歌單</b>：迎賓、用餐、敬酒時循環播放，長度抓整場婚宴的時間（常見 2～3 小時），用一份長歌單就好。</li>
</ul>

<h2 id="top">網友推最多、我們也最推的婚禮歌</h2>
<div class="tbl"><table><thead><tr><th>歌名</th><th>歌手</th><th>為什麼推</th></tr></thead><tbody>""" + "".join(
    f'<tr><td><a href="{_yt(_ALL[t][2])}" target="_blank" rel="noopener" data-cta="song_play" data-cta-type="wedding">{t} ▶</a></td><td>{_ALL[t][1]}</td><td>{TOP_WHY[t]}</td></tr>' for t in TOP) + """</tbody></table></div>
<p><b>我們特別推 Kina Grannis 版的〈Can't Help Falling in Love〉。</b>電影《瘋狂亞洲富豪》的婚禮，新娘走紅毯時就是 Kina Grannis 本人在片中演唱這首，比原唱更溫柔，非常適合一進。</p>
""" + _scene(*_scenes["welcome"]) + _scene(*_scenes["first-entrance"]) + _scene(*_scenes["family-entrance"], level="h3") + _scene(*_scenes["instrumental"], level="h3") + \
    _scene(*_scenes["second-entrance"]) + _scene(*_scenes["dinner"]) + _scene(*_scenes["toast"]) + _scene(*_scenes["farewell"]) + """
<h2 id="movies">電影、影集婚禮場景裡的歌</h2>
<p>想要「一聽就有畫面」的歌，可以從電影婚禮場景找。賓客認出來的時候，也會多一份驚喜：</p>
<div class="tbl"><table><thead><tr><th>電影／影集</th><th>歌名</th><th>歌手</th><th>出現在哪裡</th></tr></thead><tbody>""" + "".join(
    f'<tr><td>{f}</td><td><a href="{_yt(_ALL[t][2])}" target="_blank" rel="noopener" data-cta="song_play" data-cta-type="wedding">{t} ▶</a></td><td>{a}</td><td>{w}</td></tr>' for f, t, a, w in FILMS) + """</tbody></table></div>

<h2 id="ost">電影、戲劇原聲帶（OST）裡的婚禮歌</h2>
<p>這些歌是電影或戲劇的原聲帶。看過那部作品的賓客，一聽就會想起劇情：</p>
<div class="tbl"><table><thead><tr><th>歌名</th><th>歌手</th><th>出處</th></tr></thead><tbody>""" + "".join(
    f'<tr><td><a href="{_yt(v)}" target="_blank" rel="noopener" data-cta="song_play" data-cta-type="wedding">{t} ▶</a></td><td>{a}</td><td>{n}</td></tr>' for t, a, v, m, n in _ALL.values() if "o" in m) + """</tbody></table></div>

<h2 id="same-sex">同婚婚禮也適合：歌詞不分性別的歌</h2>
<p>我們自己是同婚伴侶，挑歌時會多看一眼歌詞：很多經典情歌寫的是「她」或「他」、「新郎」或「新娘」。下面這幾首的歌詞沒有限定性別，同婚、異性婚都適合：</p>
<ul class="songs">""" + "".join(_song_li(*_ALL[t]) for t in NEUTRAL) + """</ul>
<p class="note-box">用在儀式前，建議再讀一次完整歌詞，確認每一段都是你們想說的話。</p>

<h2 id="invite">把你們的歌放進喜帖</h2>
<p>挑好歌之後，可以把歌名寫進婚宴流程，例如「一進：〈Can't Help Falling in Love〉」，賓客聽到時就知道這首歌對你們的意義。我們的<a href="/web-invitation/">網頁電子喜帖</a>有婚宴流程區塊，<a href="/paper-invitation/">紙本喜帖</a>也可以設計一頁放流程和 Dress code。</p>
"""

POSTS.append(dict(
    slug="wedding-songs",
    title=f"婚禮歌單 2026｜{SONG_COUNT} 首婚禮歌曲依迎賓、一進、二進、敬酒、送客分好，每首直接聽｜編織日和",
    h1=f"婚禮歌單：{SONG_COUNT} 首婚禮歌曲，<br>依迎賓、一進、二進、用餐、敬酒、送客分好了",
    desc=f"婚禮歌曲 {SONG_COUNT} 首，依迎賓、一進、二進、用餐、逐桌敬酒、送客六個時刻分類，每首點了就能在 YouTube 試聽。我們私心推薦＋Threads 網友真實婚禮用歌，另外整理電影婚禮場景的歌，和歌詞不分性別、同婚也適合的歌。",
    ga="婚禮歌單",
    published="2026-11-21",
    modified="2026-11-22",
    lead="這份婚禮歌單，一半是我們自己私心喜歡的歌，一半來自 Threads 上一篇「求感人婚禮歌單」的網友推薦——上百則留言裡，很多是新人分享自己婚禮真的用過的歌。我們把它們依婚禮流程分成六個時刻，每首都能直接點開聽，挑歌時省一點力氣。",
    body=_body,
    faq=[
        ("一進、二進是什麼意思？", "一進是新人在婚宴開場第一次進場，二進是新人換第二套禮服後再次進場。一進通常選最感人、最有意義的歌，二進可以輕快甜一點。"),
        ("婚禮歌單要準備幾首？", "儀式歌（一進、二進、和家人進場、送客）各挑 1 首，大約 4～6 首；迎賓、用餐、敬酒用背景歌單循環播放，長度抓整場婚宴的時間，常見 2～3 小時。"),
        ("婚禮一進歌推薦哪些？", "我們最推 Kina Grannis 版〈Can't Help Falling in Love〉（電影《瘋狂亞洲富豪》婚禮紅毯曲），網友推最多的還有〈A Thousand Years〉、Ed Sheeran〈Perfect〉、Shane Filan〈Beautiful in White〉、傻子與白痴〈第一支舞〉。"),
        ("哪些電影婚禮場景的歌適合用在婚禮？", "進場可以選《瘋狂亞洲富豪》的〈Can't Help Falling in Love〉、《暮光之城：破曉 上》的〈Turning Page〉、《真善美》的婚禮進行曲；純音樂可以選《天外奇蹟》的〈Married Life〉；送客想熱鬧一點，可以選《婚禮終結者》的〈Shout〉、《伴娘我最大》的〈Hold On〉、《媽媽咪呀！》的〈I Do, I Do, I Do, I Do, I Do〉、《愛是您，愛是我》的〈All You Need Is Love〉。"),
        ("敬酒的時候適合放什麼歌？", "敬酒時長輩比較多，放大家都會哼的經典老歌最保險，例如蘇芮〈牽手〉、張宇〈給你們〉、趙詠華〈最浪漫的事〉、西城男孩〈Nothing's Gonna Change My Love for You〉。"),
        ("同婚婚禮適合放什麼歌？", "可以選歌詞不限定性別的歌，例如〈A Thousand Years〉、〈Can't Help Falling in Love〉、Adele〈Make You Feel My Love〉、Ellie Goulding〈How Long Will I Love You〉、〈Lucky〉、方大同〈Special Person〉。用之前建議再讀一次完整歌詞。"),
    ],
    sources=[
        ("Threads：求感人婚禮歌單的貼文與網友留言（2026-11-21 擷取）", "https://www.threads.com/@mimi07040819/post/Df7CD7fo_LU"),
        ("歌曲影片：各歌手官方 YouTube 頻道（2026-11-22 查核）", "https://www.youtube.com/"),
    ],
))
