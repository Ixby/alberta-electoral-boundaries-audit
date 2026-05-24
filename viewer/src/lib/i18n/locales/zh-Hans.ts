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
				'"Gerrymander"(选区不公划分)并非加拿大法院使用的术语。但如果以普通人理解的日常意义来衡量——本次审计的证据合理地支持将<em>少数派提议</em>(若被采纳)称为一份严重经过党派划分的地图。本次审计运行的每一项结构性测试都标记了<em>少数派提议</em>;没有任何一项测试标记了另一份提议(<em>多数派提议</em>)。',
			footnote:
				'"多数派"和"少数派"的称谓源自选举边界委员会(由 Miller 法官主持)内部 3 比 2 的分裂——该委员会未能形成单一建议,而是提出了两份相互竞争的提议。一个由 Brandon Lunty(由省长任命的 MLA)主持的独立 MLA 委员会正在于 2026 年 11 月截止日期前在两者之间作出选择。'
		},
		q2: {
			heading: '"Gerrymander" 在加拿大法律中是什么意思?',
			body:
				'没有意义。加拿大的检验标准不同:即边界是否在《宪章》第3条之下给予选民<em>有效代表权</em>。少数派提议在该标准下提出了严重问题;只有法官才能给出确定性的回答,而目前尚无人提起诉讼。'
		},
		q3: {
			heading: '这对阿尔伯塔人意味着什么?',
			body:
				'在50/50的省级投票情况下,审计的测量将少数派提议置于结构性极端——在101万张中立比较地图中,产生类似议席不平衡的不到100张。这种不平衡之所以重要,是因为在87席中获得58席——即三分之二的超级多数——执政党便解锁了非常规的程序权力:它可以免除标准通知期,并在一天内将公共法案推过多个立法阶段,绕过通常约束它的审议性检查。少数派提议的倾斜是否大到足以在<em>非</em>50/50的投票比例下将一个政党推过58席门槛,这是本次审计尚未测试的问题。这种取舍本身是否可接受,这是属于阿尔伯塔人的问题,而非本次审计的问题。'
		},
		cta_law: '阅读法律背景 →',
		cta_methods: '查看我们如何测试 →'
	},
	head: {
		title: '阿尔伯塔选举边界审计',
		meta_description:
			'对阿尔伯塔2026年选举边界委员会的统计审计——101万张中立地图、Elections Alberta官方shapefile、预先注册的测试。'
	},
	nav: {
		home_aria: '返回顶部',
		theme_aria: '切换深色 / 浅色模式',
		theme_title: '切换深色模式',
		verdict: '结论',
		why: '为什么?',
		map: '地图',
		split: '分裂',
		litmus: '试金石',
		crack_pack: '分散与集中',
		for_you: '对你而言',
		impact: '影响',
		history: '历史',
		canada: '加拿大',
		gerrymanders: '选区操控',
		november: '十一月',
		invisible: '隐形',
		retractions: '撤回',
		references: '参考资料',
		resources: '资源'
	},
	hero: {
		h1: '阿尔伯塔选举边界审计',
		subtitle:
			'阿尔伯塔的委员会在2026年提出了两份选区地图。本次审计对它们进行了比较——使用相同的测试,平等地应用于两者——以询问它们是否以同样的方式对待选民。',
		badge: 'Elections Alberta 官方地图——2026年5月发布',
		cover_note_1:
			'这张地图是最好的入口。点击它即可缩放和探索。顶部按钮可在少数派地图、多数派地图和2019年颁布的边界之间切换——或叠加三者以查看它们的分歧之处。<strong>Detail</strong> 根据2023年人们的投票情况为每个投票区上色;<strong>Trend</strong> 按选区添加党派色调(蓝色UCP,橙色NDP);<strong>Lines</strong> 切换边界的开关。<strong>Find</strong> 按名称跳转到任何选区。',
		cover_note_2:
			'尝试锁定视图并在地图之间切换——观察一条边界在下方选民保持不动时如何移动。这就是整个问题,用一个动作表达。',
		cover_note_3:
			'当您探索完毕后,向下滚动查看摘要。如需完整的技术分析,请参阅"资源"部分。所有数据均来自 Elections Alberta 官方shapefile以及其他政府和开源记录。',
		image_alt: '阿尔伯塔选区地图——委员会少数派提议,按2023年投票上色',
		map_hint: '点击进行交互式探索',
		btn_title: '点击打开交互式地图',
		btn_aria: '打开交互式地图'
	},
	boundary: {
		heading: '本次审计能告诉你什么,不能告诉你什么',
		can_1:
			'在1450万张随机生成的比较地图中,少数派提议在所有四项统计指标综合方面所产生的极端模式不到1张。',
		can_2: '少数派提议在5项预先注册的结构性测试中全部失败。多数派提议在5项中失败0项。',
		can_3:
			'这些结果与产生强烈党派效应的地图一致,与随机比较集所产生的结果不一致。',
		cant_1:
			'本次审计<strong>未能</strong>证明任何委员有意制造其所测量的党派效应。边界几何无法揭示意图。',
		cant_2:
			'本次审计<strong>不</strong>预测 Lunty 委员会会做出什么选择,2026 年 11 月投票结果如何,或阿尔伯塔人会如何反应。',
		cant_3:
			'本次审计<strong>不</strong>预测如果对任一提议提起《宪章》诉讼,法院将如何裁决。',
		cant_4:
			'本次审计<strong>不</strong>告诉任何选民应采取什么立场或如何处理这些信息。这是由你决定的。'
	}
} as const;
