// Tagalog (tl). AI-translated, awaiting native-speaker review.
// Register choices: formal kayo/ninyo; assumes standard Tagalog (not regional);
// civic-document register without po/opo markers (the audit's voice is direct
// rather than deferential, matching the English first-person).
export default {
	selector: {
		label: 'Pumili ng wika'
	},
	disclaimer: {
		text:
			'Isinalin ang site na ito sa pamamagitan ng AI. Maaaring may mga nilalamang nasa Ingles pa habang isinasagawa ang pagsasalin. Kung may mga mali o nais ninyong tumulong sa pagsasalin ng proyektong ito, mangyaring %s.',
		link_label: 'makipag-ugnayan sa amin'
	},
	opener: {
		heading: 'Para kanino ito?',
		body:
			"Para sa atin. Para sa ating lahat. Sa mga taga-bukid, sa mga taga-lungsod, sa mga curious, sa mga mahilig sa pulitika, sa mga mamamahayag, sa mga abugado, sa mga akademiko, sa mga pulitiko — para sa ating lahat. Dahil nakakaapekto ito sa ating lahat. Anuman ang iyong palagay sa partidong nasa poder, ang ginawa ng hating komisyon ay hindi pa nangyari noon. At binigyan tayo nito ng pagkakataong masilip ang loob ng makinarya sa paraang hindi pa natin nagawa. Ngayon ay maaari na tayong magtatag ng isang batayan — isang serye ng mga pagsusulit, at lahat ng susunod ay maaaring sukatin batay dito. Hayaan ninyong ipakita ko sa inyo ang aking natuklasan."
	},
	verdict: {
		q1: {
			heading: 'Ang iminungkahing mapa ba ay isang gerrymander?',
			body:
				'Ang "gerrymander" ay hindi terminong ginagamit ng mga korte sa Canada. Ngunit kung gagamitin ito — sa pang-araw-araw na kahulugang ibinibigay ng karamihan — ang mga ebidensya sa audit na ito ay makatuwirang sumusuporta sa pagtawag sa panukala ng minorya, kung ito ay magiging batas, bilang isang mapa na malalim na gerrymandered. Lahat ng istrukturang pagsusulit ng audit na ito ay tumutukoy sa panukala ng minorya; wala ni isa ang tumutukoy sa kabilang panukala (ang panukala ng mayorya).'
		},
		q2: {
			heading: 'Ano ang ibig sabihin ng "gerrymander" sa batas ng Canada?',
			body:
				'Wala. Iba ang pagsusuri ng Canada: kung binibigyan ng epektibong representasyon ang mga botante sa ilalim ng seksyon 3 ng Charter. Ang panukala ng minorya ay nagdudulot ng mga seryosong tanong sa ilalim ng pagsusuring iyon; isang hukom lamang ang makakasagot ng tiyak, at walang sinuman pa ang nagtanong sa kanya.'
		},
		q3: {
			heading: 'Ano ang ibig sabihin nito para sa mga Albertan?',
			body:
				'Sa isang 50/50 na boto sa probinsya, inilalagay ng mga sukat ng audit ang panukala ng minorya sa isang istrukturang sukdulan — mas mababa sa 100 ng 1.01 milyong neutral na mga mapa ng paghahambing ang nagbibigay ng kaparehong uri ng kawalan ng balanse sa upuan. Mahalaga ang kawalan ng balanseng iyon dahil sa 58 ng 87 upuan — isang dalawang-katlong supermayorya — ang naghaharing partido ay nakakakuha ng pambihirang mga kapangyarihang pamamaraan: maaari nitong tanggalin ang karaniwang mga panahon ng abiso at itulak ang mga panukalang batas sa pamamagitan ng maraming yugto ng pambabatasan sa isang araw lamang, lampas sa mga pagsusuri ng paglalapat na karaniwang nagpipigil sa kanya. Kung ang pagkakahilig ng panukala ng minorya ay sapat na laki upang itulak ang isang partido lampas sa hangganang 58-upuan sa mga sukat ng boto bukod sa 50/50 ay isang tanong na hindi pa sinuri ng audit na ito. Kung katanggap-tanggap ang pagpapalitan mismo ay isang tanong para sa mga Albertan, hindi para sa audit na ito.'
		},
		cta_law: 'Basahin ang legal na konteksto →',
		cta_methods: 'Tingnan kung paano namin sinubukan →'
	},
	head: {
		title: 'Pag-audit ng Hangganan ng Halalan sa Alberta',
		meta_description:
			'Estadistikong pag-audit ng komisyon ng hangganan ng halalan sa Alberta sa 2026 — 1,010,000 neutral na mga mapa, opisyal na mga shapefile ng Elections Alberta, mga pre-registered na pagsusulit.'
	},
	nav: {
		home_aria: 'Bumalik sa itaas',
		theme_aria: 'Palitan ang madilim / maliwanag na mode',
		theme_title: 'Palitan ang madilim na mode',
		map: 'Mapa',
		split: 'Ang Paghahati',
		litmus: 'Pagsusulit',
		crack_pack: 'Crack at Pack',
		impact: 'Epekto',
		gerrymanders: 'Mga Gerrymander',
		november: 'Nobyembre',
		invisible: 'Hindi Nakikita',
		retractions: 'Mga Pagbawi',
		references: 'Mga Sanggunian',
		resources: 'Mga Mapagkukunan'
	},
	hero: {
		h1: 'Pag-audit ng Hangganan ng Halalan sa Alberta',
		subtitle:
			'Ang komisyon ng Alberta ay nagprodyus ng dalawang mapa ng riding sa 2026. Inihambing ng audit na ito ang mga ito — gamit ang parehong mga pagsusulit, na inilapat nang pantay sa pareho — upang itanong kung pareho nilang itinuturing ang mga botante.',
		badge: 'Mga opisyal na mapa ng Elections Alberta — Inilathala noong Mayo 2026',
		cover_note_1:
			'Ang mapang ito ang pinakamahusay na paraan upang magsimula. I-click ito upang mag-zoom at galugarin. Ang mga pindutan sa itaas ay nagpapalipat sa pagitan ng mapa ng minorya, mapa ng mayorya, at mga hangganan na nasaad noong 2019 — o ilatag ang lahat ng tatlo upang makita kung saan sila eksaktong nag-iiba. Kinukulayan ng <strong>Detail</strong> ang bawat polling area ayon sa paano bumoto ang mga tao noong 2023; nagdadagdag ang <strong>Trend</strong> ng partisan shading bawat distrito (asul UCP, kahel NDP); ginagawang on/off ng <strong>Lines</strong> ang mga hangganan. Ang <strong>Find</strong> ay lumulukso sa anumang riding ayon sa pangalan.',
		cover_note_2:
			'Subukang i-lock ang viewport at mag-flip sa pagitan ng mga mapa — pagmasdan ang isang hangganan na lumilipat habang ang mga botante sa ilalim ay nananatiling tahimik. Iyon ang buong tanong sa isang galaw.',
		cover_note_3:
			'Kapag tapos ka nang mag-explore, mag-scroll pababa para sa buod. Para sa kumpletong teknikal na pagsusuri, tingnan ang seksyon ng Mga Mapagkukunan. Lahat ng data ay mula sa opisyal na shapefile ng Elections Alberta at iba pang gobyerno at open-source na mga rekord.',
		image_alt:
			'Mga mapa ng distritong pang-eleksyon sa Alberta — panukala ng minorya ng komisyon, kinulayan ayon sa boto noong 2023',
		map_hint: 'I-click upang galugarin nang interactive',
		btn_title: 'I-click upang buksan ang interactive na mapa',
		btn_aria: 'Buksan ang interactive na mapa'
	}
} as const;
