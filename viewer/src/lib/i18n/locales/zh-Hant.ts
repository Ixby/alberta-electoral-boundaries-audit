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
				'「Gerrymander」(選區不公劃分)並非加拿大法院使用的術語。但如果以普通人理解的日常意義來衡量——本次審計的證據合理地支持將少數派提議(若被採納)稱為一份嚴重經過黨派劃分的地圖。本次審計運行的每一項結構性測試都標記了少數派提議;沒有任何一項測試標記了另一份提議(多數派提議)。'
		},
		q2: {
			heading: '「Gerrymander」在加拿大法律中是什麼意思?',
			body:
				'沒有意義。加拿大的檢驗標準不同:即邊界是否在《憲章》第3條之下給予選民有效代表權。少數派提議在該標準下提出了嚴重問題;只有法官才能給出確定性的回答,而目前尚無人提起訴訟。'
		},
		q3: {
			heading: '這對阿爾伯塔人意味著什麼?',
			body:
				'在50/50的省級投票情況下,審計的測量將少數派提議置於結構性極端——在101萬張中立比較地圖中,產生類似議席不平衡的不到100張。這種不平衡之所以重要,是因為在87席中獲得58席——即三分之二的超級多數——執政黨便解鎖了非常規的程序權力:它可以免除標準通知期,並在一天內將公共法案推過多個立法階段,繞過通常約束它的審議性檢查。少數派提議的傾斜是否大到足以在非50/50的投票比例下將一個政黨推過58席門檻,這是本次審計尚未測試的問題。這種取捨本身是否可接受,這是屬於阿爾伯塔人的問題,而非本次審計的問題。'
		},
		cta_law: '閱讀法律背景 →',
		cta_methods: '查看我們如何測試 →'
	}
} as const;
