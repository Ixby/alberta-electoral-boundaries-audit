// Simplified Chinese (zh-Hans). AI-translated, awaiting native-speaker review.
// Target reader: Mandarin speakers, primarily mainland-China-origin.
// Register: standard written Chinese (formal civic-document), informal 你 to
// match the audit's first-person personal voice rather than bureaucratic 您.
export default {
	selector: {
		label: '选择语言'
	},
	disclaimer: {
		text:
			'本网站由 AI 翻译。在翻译进行期间,部分内容可能仍以英文显示。如果您发现错误或希望帮助翻译本项目,请%s。',
		link_label: '联系我们'
	},
	opener: {
		heading: '这是为谁准备的?',
		body:
			'为我们。为我们所有人。无论你是乡村居民、城市居民、好奇者、政治爱好者、记者、律师、学者还是政治人物——我们所有人。因为这影响着我们所有人。无论你是否喜欢执政党,分裂的委员会所产生的结果是前所未有的。它给了我们一个前所未有的机会,得以窥视这台机器的内部运作。现在我们可以建立一个基准——一系列测试,之后的一切都可以以此为标准进行评估。让我向你展示我所发现的。'
	},
	verdict: {
		q1: {
			heading: '所提议的地图是否构成选区不公?',
			body:
				'"Gerrymander"(选区不公划分)并非加拿大法院使用的术语。但如果以普通人理解的日常意义来衡量——本次审计的证据合理地支持将少数派提议(若被采纳)称为一份严重经过党派划分的地图。本次审计运行的每一项结构性测试都标记了少数派提议;没有任何一项测试标记了另一份提议(多数派提议)。'
		},
		q2: {
			heading: '"Gerrymander" 在加拿大法律中是什么意思?',
			body:
				'没有意义。加拿大的检验标准不同:即边界是否在《宪章》第3条之下给予选民有效代表权。少数派提议在该标准下提出了严重问题;只有法官才能给出确定性的回答,而目前尚无人提起诉讼。'
		},
		q3: {
			heading: '这对阿尔伯塔人意味着什么?',
			body:
				'在50/50的省级投票情况下,审计的测量将少数派提议置于结构性极端——在101万张中立比较地图中,产生类似议席不平衡的不到100张。这种不平衡之所以重要,是因为在87席中获得58席——即三分之二的超级多数——执政党便解锁了非常规的程序权力:它可以免除标准通知期,并在一天内将公共法案推过多个立法阶段,绕过通常约束它的审议性检查。少数派提议的倾斜是否大到足以在非50/50的投票比例下将一个政党推过58席门槛,这是本次审计尚未测试的问题。这种取舍本身是否可接受,这是属于阿尔伯塔人的问题,而非本次审计的问题。'
		},
		cta_law: '阅读法律背景 →',
		cta_methods: '查看我们如何测试 →'
	}
} as const;
