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

# ── 2. 婚禮歌單（2026-11-21） ──
SONG_TOP = [
    ("Perfect", "Ed Sheeran", "進場；有網友的新郎在進場時現場唱"),
    ("My Only（《開端》片尾曲）", "周深", "感人系，被推了 3 次"),
    ("Can't Help Falling in Love", "原唱 Elvis Presley，網友推 Kina Grannis 等翻唱版", "進場，翻唱版更溫柔"),
    ("Beautiful in White", "Shane Filan", "經典進場曲"),
    ("Speechless", "James TW", "慢歌"),
    ("Lucky Me", "Jake Miller", "新郎進場，從新郎的角度寫"),
    ("拉赫曼尼諾夫 第二號交響曲 第三樂章", "古典", "純音樂，網友說「聽了會哭」"),
]
SCENES = [
    ("新人進場", [("It's You", "HENRY"), ("You Are the Reason", "Calum Scott"), ("I Belong to You", "Jacob Lee"), ("1000x (feat. BROODS)", "Jarryd James"), ("Love Wins All（聲樂版）", "IU"), ("Always in My Heart", "Tamaru Yamada"), ("golden hour", "JVKE")]),
    ("和爸爸、家人一起進場", [("Give Me Away", "Riley Roth"), ("If You Love Her (feat. Meghan Trainor)", "Forest Blakk")]),
    ("純音樂、不要歌詞", [("A Thousand Years（弦樂版）", "Brooklyn Duo feat. Dover Quartet"), ("拉赫曼尼諾夫 第二號交響曲 第三樂章", "古典"), ("卡農", "古典"), ("最重要的決定（鋼琴版）", "鋼琴演奏")]),
    ("敬酒、送客、輕快一點", [("Lucky", "Jason Mraz, Colbie Caillat"), ("Nothin' on You (feat. Bruno Mars)", "B.o.B"), ("Waste My Time", "Marc Atlas"), ("Die With a Smile", "Lady Gaga, Bruno Mars"), ("Candy", "SEVENTEEN")]),
]
LANGS = [
    ("華語／粵語", [("Special Person", "方大同"), ("此刻", "袁婭維"), ("最後一個", "滅火器"), ("A Little Love", "馮曦妤"), ("Not Perfect", "Kiri T"), ("My Vow", "周柏豪"), ("Shine Brighter（《玫瑰的故事》插曲）", "希林娜依高")]),
    ("台灣獨立樂團", [("讓我餘生只為你唱情歌", "冰球樂團"), ("Yes, I Do", "Mary See the Future"), ("I Know You Know I Love You", "落日飛車"), ("10000 HOURS", "宇宙人"), ("愛是我們必經的辛苦", "脆樂團"), ("第一支舞", "傻子與白痴"), ("直到我遇見了你", "李友廷")]),
    ("韓文、日文", [("Beautiful（《鬼怪》OST）", "Crush"), ("My Love", "李承哲"), ("사랑, 하자 Let's Love", "SUHO"), ("Home", "Janet Suhh"), ("虹", "菅田將暉"), ("CAN YOU CELEBRATE?", "安室奈美惠")]),
    ("經典老歌", [("How Deep Is Your Love", "Bee Gees"), ("Truly Madly Deeply", "Savage Garden"), ("Because You Loved Me", "Céline Dion"), ("Eternal Flame", "The Bangles"), ("The Rose", "Westlife"), ("I Finally Found Someone", "Barbra Streisand & Bryan Adams")]),
]
NEUTRAL = [("A Thousand Years", "Christina Perri"), ("Can't Help Falling in Love", "Elvis Presley"), ("Make You Feel My Love", "Adele"), ("How Long Will I Love You", "Ellie Goulding"), ("Lucky", "Jason Mraz, Colbie Caillat"), ("Special Person", "方大同")]


def _songs(rows):
    return "<ul class=\"songs\">" + "".join(f"<li><b>{t}</b><span>{a}</span></li>" for t, a in rows) + "</ul>"


POSTS.append(dict(
    slug="wedding-songs",
    title="婚禮歌單 2026｜網友推爆的感人婚禮歌曲，依進場、敬酒、送客分好了｜編織日和",
    h1="婚禮歌單：網友推爆的感人婚禮歌曲，<br>依進場、敬酒、送客分好了",
    desc="婚禮歌單整理：Threads 上一篇「求感人婚禮歌單」的網友推薦，整理成新人進場、和爸爸進場、純音樂、敬酒送客，以及華語、台灣獨立樂團、韓日、經典老歌；另外挑出歌詞不分性別、同婚婚禮也適合的歌。",
    ga="婚禮歌單",
    published="2026-11-21",
    modified="2026-11-21",
    lead="Threads 上有一位新人問：「有沒有人可以推薦婚禮歌單？想要很感人、會落淚的那種，有點像 A Thousand Years。」一天之內就有上百則留言，很多是新人分享自己婚禮真的用過的歌。我們把這些推薦整理起來，依婚禮的不同時刻分好，讓你挑歌時省一點力氣。",
    body="""
<p class="note-box">整理自 Threads 網友推薦（2026-11-21 擷取，只列歌名與歌手，不是完整清單）。有些是翻唱版本，挑好之後建議到 Spotify 或 YouTube 確認你想要的版本。</p>

<h2 id="how-many">婚禮歌單要幾首？先分清楚「儀式歌」和「背景音樂」</h2>
<p>婚禮上的音樂大致分兩種：</p>
<ul class="check">
  <li><b>儀式歌</b>：新人進場、和家人進場、交換誓詞、敬酒、送客，每個時刻挑 1 首，大約 4～6 首。這幾首最需要花心思。</li>
  <li><b>背景音樂</b>：賓客入座和用餐時播的，長度抓整場婚宴的時間（常見 2～3 小時），可以直接用一份長歌單。</li>
</ul>
<p>所以真正要「挑」的，其實是那幾首儀式歌。下面就是網友推薦、而且很多是新人自己用過的歌。</p>

<h2 id="top">網友推最多次的婚禮歌</h2>
""" + "<div class=\"tbl\"><table><thead><tr><th>歌名</th><th>歌手</th><th>網友怎麼用</th></tr></thead><tbody>" + "".join(f"<tr><td>{t}</td><td>{a}</td><td>{n}</td></tr>" for t, a, n in SONG_TOP) + "</tbody></table></div>" + """

<h2 id="scenes">依婚禮時刻挑歌</h2>
""" + "".join(f"<h3>{name}</h3>" + _songs(rows) for name, rows in SCENES) + """
<p>和爸爸或家人進場的歌，網友特別推從「父母把孩子交出去」角度寫的歌，歌詞很容易讓全場一起紅眼眶。</p>

<h2 id="languages">依語言和風格挑歌</h2>
""" + "".join(f"<h3>{name}</h3>" + _songs(rows) for name, rows in LANGS) + """
<p>想要不撞歌，可以從台灣獨立樂團或比較小眾的英文歌找，例如網友推的 Jacob Lee〈I Belong to You〉、Moi Yang〈I Do〉。</p>

<h2 id="same-sex">同婚婚禮也適合：歌詞不分性別的歌</h2>
<p>我們自己是同婚伴侶，挑歌時會多看一眼歌詞：很多經典情歌寫的是「她」或「他」、「新郎」或「新娘」。下面這幾首的歌詞沒有限定性別，同婚、異性婚都適合：</p>
""" + _songs(NEUTRAL) + """
<p class="note-box">用在儀式前，建議再讀一次完整歌詞，確認每一段都是你們想說的話。</p>

<h2 id="invite">把你們的歌放進喜帖</h2>
<p>挑好歌之後，也可以把歌名寫進喜帖，或在婚宴流程裡標出「新人進場：〈某首歌〉」，讓賓客聽到時知道這首歌對你們的意義。我們的<a href="/web-invitation/">網頁電子喜帖</a>有婚宴流程區塊，<a href="/paper-invitation/">紙本喜帖</a>也可以設計一頁放流程和 Dress code。</p>
""",
    faq=[
        ("婚禮歌單要幾首？", "儀式歌（新人進場、家人進場、交換誓詞、敬酒、送客）每個時刻 1 首，大約 4～6 首；背景音樂的長度抓整場婚宴的時間，常見 2～3 小時。"),
        ("婚禮進場歌推薦哪些？", "網友推最多的有 Ed Sheeran〈Perfect〉、Shane Filan〈Beautiful in White〉、HENRY〈It's You〉、Calum Scott〈You Are the Reason〉；想要純音樂可以選弦樂版〈A Thousand Years〉或拉赫曼尼諾夫第二號交響曲第三樂章。"),
        ("和爸爸一起進場可以放什麼歌？", "網友推 Riley Roth〈Give Me Away〉和 Forest Blakk〈If You Love Her〉，都是從父母把孩子交出去的角度寫的。"),
        ("同婚婚禮適合放什麼歌？", "可以選歌詞不限定性別的歌，例如〈A Thousand Years〉、〈Can't Help Falling in Love〉、Adele〈Make You Feel My Love〉、Ellie Goulding〈How Long Will I Love You〉、Jason Mraz 與 Colbie Caillat〈Lucky〉、方大同〈Special Person〉。用之前建議再讀一次完整歌詞。"),
    ],
    sources=[
        ("Threads：求感人婚禮歌單的貼文與網友留言（2026-11-21 擷取）", "https://www.threads.com/@mimi07040819/post/Df7CD7fo_LU"),
    ],
))
