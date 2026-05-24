// Traditional Chinese (zh-Hant). AI-translated, awaiting native-speaker review.
// Target reader: Cantonese speakers, primarily Hong-Kong-origin; also Taiwan
// readers. Same text as zh-Hans in standard written Chinese, converted to
// Traditional characters. Colloquial written Cantonese (粵文) is not the
// target — formal civic-document register is essentially identical between
// Simplified and Traditional.
export default {
	selector: {
		label: '選擇語言'
	},
	disclaimer: {
		text:
			'本網站由 AI 翻譯。在翻譯進行期間,部分內容可能仍以英文顯示。如果您發現錯誤或希望幫助翻譯本項目,請%s。',
		link_label: '聯絡我們'
	},
	opener: {
		heading: '這是為誰準備的?',
		body:
			'為我們。為我們所有人。無論你是鄉村居民、城市居民、好奇者、政治愛好者、記者、律師、學者還是政治人物——我們所有人。因為這影響著我們所有人。無論你是否喜歡執政黨,分裂的委員會所產生的結果是前所未有的。它給了我們一個前所未有的機會,得以窺視這台機器的內部運作。現在我們可以建立一個基準——一系列測試,之後的一切都可以以此為標準進行評估。讓我向你展示我所發現的。'
	},
	verdict: {
		q1: {
			heading: '所提議的地圖是否構成選區不公?',
			body:
				'「Gerrymander」(選區不公劃分)並非加拿大法院使用的術語。但如果以普通人理解的日常意義來衡量——本次審計的證據合理地支持將<em>少數派提議</em>(若被採納)稱為一份嚴重經過黨派劃分的地圖。本次審計運行的每一項結構性測試都標記了<em>少數派提議</em>;沒有任何一項測試標記了另一份提議(<em>多數派提議</em>)。',
			footnote:
				'「多數派」和「少數派」的稱謂源自選舉邊界委員會(由 Miller 法官主持)內部 3 比 2 的分裂——該委員會未能形成單一建議,而是提出了兩份相互競爭的提議。一個由 Brandon Lunty(由省長任命的 MLA)主持的獨立 MLA 委員會正在於 2026 年 11 月截止日期前在兩者之間作出選擇。'
		},
		q2: {
			heading: '「Gerrymander」在加拿大法律中是什麼意思?',
			body:
				'沒有意義。加拿大的檢驗標準不同:即邊界是否在《憲章》第3條之下給予選民<em>有效代表權</em>。少數派提議在該標準下提出了嚴重問題;只有法官才能給出確定性的回答,而目前尚無人提起訴訟。'
		},
		q3: {
			heading: '這對阿爾伯塔人意味著什麼?',
			body:
				'在50/50的省級投票情況下,審計的測量將少數派提議置於結構性極端——在101萬張中立比較地圖中,產生類似議席不平衡的不到100張。這種不平衡之所以重要,是因為在87席中獲得58席——即三分之二的超級多數——執政黨便解鎖了非常規的程序權力:它可以免除標準通知期,並在一天內將公共法案推過多個立法階段,繞過通常約束它的審議性檢查。少數派提議的傾斜是否大到足以在<em>非</em>50/50的投票比例下將一個政黨推過58席門檻,這是本次審計尚未測試的問題。這種取捨本身是否可接受,這是屬於阿爾伯塔人的問題,而非本次審計的問題。'
		},
		cta_law: '閱讀法律背景 →',
		cta_methods: '查看我們如何測試 →'
	},
	head: {
		title: '阿爾伯塔選舉邊界審計',
		meta_description:
			'對阿爾伯塔2026年選舉邊界委員會的統計審計——101萬張中立地圖、Elections Alberta官方shapefile、預先註冊的測試。'
	},
	nav: {
		home_aria: '返回頂部',
		theme_aria: '切換深色 / 淺色模式',
		theme_title: '切換深色模式',
		map: '地圖',
		split: '分裂',
		litmus: '試金石',
		crack_pack: '分散與集中',
		impact: '影響',
		gerrymanders: '選區操控',
		november: '十一月',
		invisible: '隱形',
		retractions: '撤回',
		references: '參考資料',
		resources: '資源'
	},
	hero: {
		h1: '阿爾伯塔選舉邊界審計',
		subtitle:
			'阿爾伯塔的委員會在2026年提出了兩份選區地圖。本次審計對它們進行了比較——使用相同的測試,平等地應用於兩者——以詢問它們是否以同樣的方式對待選民。',
		badge: 'Elections Alberta 官方地圖——2026年5月發佈',
		cover_note_1:
			'這張地圖是最好的入口。點擊它即可縮放和探索。頂部按鈕可在少數派地圖、多數派地圖和2019年頒布的邊界之間切換——或疊加三者以查看它們的分歧之處。<strong>Detail</strong> 根據2023年人們的投票情況為每個投票區上色;<strong>Trend</strong> 按選區添加黨派色調(藍色UCP,橙色NDP);<strong>Lines</strong> 切換邊界的開關。<strong>Find</strong> 按名稱跳轉到任何選區。',
		cover_note_2:
			'嘗試鎖定視圖並在地圖之間切換——觀察一條邊界在下方選民保持不動時如何移動。這就是整個問題,用一個動作表達。',
		cover_note_3:
			'當您探索完畢後,向下滾動查看摘要。如需完整的技術分析,請參閱「資源」部分。所有數據均來自 Elections Alberta 官方shapefile以及其他政府和開源記錄。',
		image_alt: '阿爾伯塔選區地圖——委員會少數派提議,按2023年投票上色',
		map_hint: '點擊進行互動式探索',
		btn_title: '點擊打開互動式地圖',
		btn_aria: '打開互動式地圖'
	},
	boundary: {
		heading: '本次審計能告訴你什麼,不能告訴你什麼',
		can_1:
			'在1450萬張隨機生成的比較地圖中,少數派提議在所有四項統計指標綜合方面所產生的極端模式不到1張。',
		can_2: '少數派提議在5項預先註冊的結構性測試中全部失敗。多數派提議在5項中失敗0項。',
		can_3:
			'這些結果與產生強烈黨派效應的地圖一致,與隨機比較集所產生的結果不一致。',
		cant_1:
			'本次審計<strong>未能</strong>證明任何委員有意製造其所測量的黨派效應。邊界幾何無法揭示意圖。',
		cant_2:
			'本次審計<strong>不</strong>預測 Lunty 委員會會做出什麼選擇,2026 年 11 月投票結果如何,或阿爾伯塔人會如何反應。',
		cant_3:
			'本次審計<strong>不</strong>預測如果對任一提議提起《憲章》訴訟,法院將如何裁決。',
		cant_4:
			'本次審計<strong>不</strong>告訴任何選民應採取什麼立場或如何處理這些信息。這是由你決定的。'
	}
} as const;
