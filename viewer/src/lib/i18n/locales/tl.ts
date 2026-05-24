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
	}
} as const;
