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
				'Ang "gerrymander" ay hindi terminong ginagamit ng mga korte sa Canada. Ngunit kung gagamitin ito — sa pang-araw-araw na kahulugang ibinibigay ng karamihan — ang mga ebidensya sa audit na ito ay makatuwirang sumusuporta sa pagtawag sa <em>panukala ng minorya</em>, kung ito ay magiging batas, bilang isang mapa na malalim na gerrymandered. Lahat ng istrukturang pagsusulit ng audit na ito ay tumutukoy sa <em>panukala ng minorya</em>; wala ni isa ang tumutukoy sa kabilang panukala (ang <em>panukala ng mayorya</em>).',
			footnote:
				'Ang mga pangalang "mayorya" at "minorya" ay galing sa 3–2 na paghahati sa Electoral Boundaries Commission (pinamumunuan ni Justice Miller), na nagprodyus ng dalawang nagtutunggaling panukala sa halip na isang rekomendasyon. Isang hiwalay na komite ng mga MLA na pinamumunuan ni Brandon Lunty — isang MLA na hinirang ng Premier — ang pumipili ngayon sa pagitan ng mga ito bago ang takdang petsa ng Nobyembre 2026.'
		},
		q2: {
			heading: 'Ano ang ibig sabihin ng "gerrymander" sa batas ng Canada?',
			body:
				'Wala. Iba ang pagsusuri ng Canada: kung binibigyan ng <em>epektibong representasyon</em> ang mga botante sa ilalim ng seksyon 3 ng Charter. Ang panukala ng minorya ay nagdudulot ng mga seryosong tanong sa ilalim ng pagsusuring iyon; isang hukom lamang ang makakasagot ng tiyak, at walang sinuman pa ang nagtanong sa kanya.'
		},
		q3: {
			heading: 'Ano ang ibig sabihin nito para sa mga Albertan?',
			body:
				'Sa isang 50/50 na boto sa probinsya, inilalagay ng mga sukat ng audit ang panukala ng minorya sa isang istrukturang sukdulan — mas mababa sa 100 ng 1.01 milyong neutral na mga mapa ng paghahambing ang nagbibigay ng kaparehong uri ng kawalan ng balanse sa upuan. Mahalaga ang kawalan ng balanseng iyon dahil sa 58 ng 87 upuan — isang dalawang-katlong supermayorya — ang naghaharing partido ay nakakakuha ng pambihirang mga kapangyarihang pamamaraan: maaari nitong tanggalin ang karaniwang mga panahon ng abiso at itulak ang mga panukalang batas sa pamamagitan ng maraming yugto ng pambabatasan sa isang araw lamang, lampas sa mga pagsusuri ng paglalapat na karaniwang nagpipigil sa kanya. Kung ang pagkakahilig ng panukala ng minorya ay sapat na laki upang itulak ang isang partido lampas sa hangganang 58-upuan sa mga sukat ng boto na <em>iba</em> sa 50/50 ay isang tanong na hindi pa sinuri ng audit na ito. Kung katanggap-tanggap ang pagpapalitan mismo ay isang tanong para sa mga Albertan, hindi para sa audit na ito.'
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
		nav_aria: 'I-toggle ang nabigasyon',
		drawer_top: '↑ Itaas',
		verdict: 'Hatol',
		why: 'Bakit?',
		map: 'Mapa',
		split: 'Ang Paghahati',
		litmus: 'Pagsusulit',
		crack_pack: 'Crack at Pack',
		for_you: 'Para Sa Iyo',
		impact: 'Epekto',
		history: 'Kasaysayan',
		canada: 'Canada',
		gerrymanders: 'Mga Gerrymander',
		november: 'Nobyembre',
		lunty: 'Lunty',
		invisible: 'Hindi Nakikita',
		suggestions: 'Mga Mungkahi',
		retractions: 'Mga Pagbawi',
		references: 'Mga Sanggunian',
		resources: 'Mga Mapagkukunan',
		technical: 'Teknikal'
	},
	hero: {
		h1: 'Pag-audit ng Hangganan ng Halalan sa Alberta',
		subtitle:
			'Ang komisyon ng Alberta ay nagprodyus ng dalawang mapa ng riding sa 2026. Inihambing ng audit na ito ang mga ito — gamit ang parehong mga pagsusulit, na inilapat nang pantay sa pareho — upang itanong kung pareho nilang itinuturing ang mga botante.',
		badge: 'Mga opisyal na mapa ng Elections Alberta — Inilathala noong Mayo 2026',
		cover_note: 'I-click upang mag-zoom at galugarin ang lahat ng tatlong panukala ng hangganan nang sabay-sabay. I-pin ang viewport at mag-flip sa pagitan ng mga mapa — gumagalaw ang mga hangganan, nananatili ang mga botante. Mag-scroll pababa para sa pagsusuri.',
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
	},
	editorial_intro: {
		heading: 'Ano ang redistricting at bakit ito ay dapat mahalaga sa iyo?',
		p1: 'Ang bawat botante sa Alberta ay naninirahan sa isang <em>elektoral na distrito</em> — isang seksyon ng probinsya na pumipili ng isang tao sa lehislatura. May 87 distrito. Ang bawat distrito ay pumipili ng isang MLA. Kapag ikaw ay bumoboto sa isang elektoral na probinsya, pinipili mo ang MLA para sa distrito kung saan ka nakatira. Iyon ang buong koneksyon ng karamihan sa mga Albertan sa lehislatura: isang MLA, isang distrito, isang boto.',
		p2: 'Ang mga linyang ito ng distrito ay hindi permanente. Lumilipat ang mga tao, lumalago ang mga kapitbahayan, ang mga lugar sa kanayunan ay nagiging manipis, at ang mga lungsod ay lumalawak. Tuwing walo hanggang sampung taon, dapat na muling iguhit ng Alberta ang mga linya upang ang bawat distrito ay nasa tamang sukat at sumasalamin sa kung paano talaga nakatira ang mga Albertan ngayon. Ang katawan na muling gumuhit ay ang <em>Komisyon ng Hangganan ng Halalan</em> — isang independiyenteng komisyon na may mga huwes, abugado, at miyembro ng publiko, hindi mga politiko.',
		p3: 'Iyon ang karaniwang proseso. Sa pagkakataong ito, ang karaniwang proseso ay nagprodyus ng isang bagay na hindi karaniwan. Ang limang miyembro ng komisyon ay naghati-hati ng 3 sa 2 sa kung anong itsura ng mapa ay dapat, at sa halip na magkasundo sa isang rekomendasyon, sila ay nagprodyus ng dalawa: isang <em>panukala ng mayorya</em> (sinusuportahan ng tatlong komisyonado) at isang <em>panukala ng minorya</em> (sinusuportahan ng dalawa). Ang dalawa ay nakapatong sa mesa. Isang hiwalay na komite ng mga MLA na pinamumunuan ni Brandon Lunty — hinirang ng Premier para sa partikular na desisyong ito — ang pumipili sa pagitan ng mga ito. Ang lehislatura ay dapat aprubahan kung alin ang makakaligtas sa komiteng iyon bago ang Nobyembre 2026.',
		p4: 'Kung bakit ito mahalaga sa iyo: ang mga linya ay nagdedesisyon kung sino ang iyong MLA. Sila ang nagdedesisyon kung anong mga kapitbahayan, bayan, at alalahanin ang kinakatawan nang magkasama. Kung ang iyong lungsod ay nahahati sa apat na MLA sa halip na isa, walang iisang kinatawan ang may pananagutan para sa lungsod sa kabuuan. Kung ang iyong komunidad ng interes — isang maliit na bayan, isang rural na rehiyon, isang sentro ng lungsod — ay nahahati sa pagitan ng mga distrito, ang iyong boses sa mga desisyon ng probinsya ay nalalabnaw. Hinuhubog din ng mapa kung anong partido ang maaaring magtatag ng gobyerno, at sa anong margin. Ang partikular na natuklasan ng audit (na ang panukala ng minorya ay nasa isang sukdulan ng istraktura) ay ang dahilan kung bakit binabasa mo ang site na ito, ngunit ang mas malawak na tanong ay mas matanda at naaangkop sa bawat redistricting cycle: ang mga linya ba ay sumasalamin sa kung paano nakatira ang mga Albertan, o hinuhubog ba nila ang pulitika na susunod?',
		p5: 'Ang natitirang bahagi ng pahinang ito ay tumatakbo sa kung ano talaga ang ginagawa ng dalawang iminungkahing mapa.',
		key_terms_lead: 'Mga pangunahing termino sa seksyong ito — i-click upang basahin:'
	},
	boundary: {
		heading: 'Kung ano ang masasabi at hindi masasabi ng audit na ito',
		can_1:
			'Mas mababa sa 1 sa 14.5 milyong random na nilikhang mga mapa ng paghahambing ang nagprodyus ng mga pattern na kasinghirap ng panukala ng minorya sa lahat ng apat na estadistikong sukat na pinagsama.',
		can_2:
			'Ang panukala ng minorya ay bumagsak sa 5 sa 5 pre-registered na istrukturang pagsusulit. Ang panukala ng mayorya ay bumagsak sa 0 sa 5.',
		can_3:
			'Ang mga resultang ito ay tugma sa mga mapa na nagpoprodyus ng malalakas na epektong partisan, at hindi tugma sa kung ano ang prinopodyus ng random na set ng paghahambing.',
		cant_1:
			'Ang audit ay <strong>hindi</strong> nagtatatag na anumang komisyonado ay may intensyon sa mga epektong partisan na sinusukat nito. Hindi maipakikita ng geometriya ng hangganan ang intensyon.',
		cant_2:
			'Ang audit ay <strong>hindi</strong> humuhula kung ano ang pipiliin ng Lunty committee, kung ano ang magiging boto sa Nobyembre 2026, o kung paano magrereaksyon ang mga Albertan.',
		cant_3:
			'Ang audit ay <strong>hindi</strong> humuhula kung paano huhusgahan ng isang korte kung magsasampa ng Charter challenge laban sa alinmang panukala.',
		cant_4:
			'Ang audit ay <strong>hindi</strong> nagsasabi sa anumang indibidwal na botante kung anong posisyon ang dapat kunin o ano ang gagawin sa impormasyong ito. Sa inyo iyon na desisyon.'
	}
} as const;
