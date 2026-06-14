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
	stakes: {
		q1: {
			heading: 'Ang iminungkahing mapa ba ay isang gerrymander?',
			body:
				'Ang "gerrymander" ay hindi terminong ginagamit ng mga korte sa Canada. Ngunit kung gagamitin ito — sa pang-araw-araw na kahulugang ibinibigay ng karamihan — ang mga ebidensya sa audit na ito ay makatuwirang sumusuporta sa pagtawag sa <em>panukala ng minorya</em>, kung ito ay magiging batas, bilang isang mapa na malalim na gerrymandered. Apat sa limang istrukturang pagsusulit ng audit na ito ang tumutukoy sa <em>panukala ng minorya</em> at wala ni isa ang tumutukoy sa kabilang panukala (ang <em>panukala ng mayorya</em>); ang ikalimang pagsusulit ay neutral para sa parehong mapa.',
			footnote:
				'Ang mga pangalang "mayorya" at "minorya" ay galing sa 3–2 na paghahati sa Electoral Boundaries Commission (pinamumunuan ni Justice Miller), na nagprodyus ng dalawang nagtutunggaling panukala sa halip na isang rekomendasyon. Mula noon ay isinantabi na ng lehislatura ang parehong panukala at inihatid ang muling pagguhit ng mga hangganan sa isang limang-MLA na komite na pinamumunuan ni Brandon Lunty (isang MLA na hinirang ng Premier); ang komite ay nangangasiwa sa isang hiwalay na apat na miyembrong Independent Advisory Panel — dalawang miyembrong hinirang ng Premier (Hon. Monte Solberg at Darwin Durnie), at dalawa ng Pinuno ng Oposisyon (Dr. Gerard Kennedy at Brent Robinson) — na inatasang gumawa ng bagong 91-puwesto na panukalang hangganan bago ang takdang petsa ng Nobyembre 2026.'
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
		stakes: 'Hatol',
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
		p3: 'Iyon ang karaniwang proseso. Sa pagkakataong ito, ang karaniwang proseso ay nagprodyus ng isang bagay na hindi karaniwan. Ang limang miyembro ng komisyon ay naghati-hati ng 3 sa 2 sa kung anong itsura ng mapa ay dapat, at sa halip na magkasundo sa isang rekomendasyon, sila ay nagprodyus ng dalawa: isang <em>panukala ng mayorya</em> (sinusuportahan ng tatlong komisyonado) at isang <em>panukala ng minorya</em> (sinusuportahan ng dalawa). Ang dalawa ay nakapatong sa mesa — at ang lehislatura ay isinantabi na ang dalawa. Isang hiwalay na komite ng mga MLA na pinamumunuan ni Brandon Lunty — hinirang ng Premier para sa partikular na desisyong ito — ang ngayon ay nangangasiwa sa isang apat na miyembrong Independent Advisory Panel, na binuo sa ilalim ng Government Motion 37 (ipinasa noong Abril 21, 2026), na inatasang gumawa ng bagong 91-puwesto na mapa. Ang lehislatura ay dapat aprubahan kung anuman ang ihatid ng komite bago ang Nobyembre 2026.',
		p4: 'Kung bakit ito mahalaga sa iyo: ang mga linya ay nagdedesisyon kung sino ang iyong MLA. Sila ang nagdedesisyon kung anong mga kapitbahayan, bayan, at alalahanin ang kinakatawan nang magkasama. Kung ang iyong lungsod ay nahahati sa apat na MLA sa halip na isa, walang iisang kinatawan ang may pananagutan para sa lungsod sa kabuuan. Kung ang iyong komunidad ng interes — isang maliit na bayan, isang rural na rehiyon, isang sentro ng lungsod — ay nahahati sa pagitan ng mga distrito, ang iyong boses sa mga desisyon ng probinsya ay nalalabnaw. Hinuhubog din ng mapa kung anong partido ang maaaring magtatag ng gobyerno, at sa anong margin. Ang partikular na natuklasan ng audit (na ang panukala ng minorya ay nasa isang sukdulan ng istraktura) ay ang dahilan kung bakit binabasa mo ang site na ito, ngunit ang mas malawak na tanong ay mas matanda at naaangkop sa bawat redistricting cycle: ang mga linya ba ay sumasalamin sa kung paano nakatira ang mga Albertan, o hinuhubog ba nila ang pulitika na susunod?',
		p5: 'Ang natitirang bahagi ng pahinang ito ay tumatakbo sa kung ano talaga ang ginagawa ng dalawang iminungkahing mapa.',
		key_terms_lead: 'Mga pangunahing termino sa seksyong ito — i-click upang basahin:'
	},
	boundary: {
		heading: 'Kung ano ang masasabi at hindi masasabi ng audit na ito',
		can_1:
			'Mas mababa sa 1 sa 350,000 random na nilikhang mga mapa ng paghahambing ang nagprodyus ng mga pattern na kasinghirap ng panukala ng minorya sa lahat ng apat na estadistikong sukat na pinagsama.',
		can_2:
			'Ang panukala ng minorya ay bumagsak sa 4 sa 5 pre-registered na istrukturang pagsusulit; ang ikalima (anchoring) ay neutral — ang parehong mapa ay nasa loob ng pamantayang Canadian. Ang panukala ng mayorya ay bumagsak sa 0 sa 4 na tumama.',
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
	},
	top_callouts: {
		gerrymander_body: 'Sa pinagsamang marka ng partisan bias ng audit, ang mapa ng minorya ng komisyon ay nasa matinding dulo ng 1,010,000 algoritmikong-ginawang neutral na mga mapa ng paghahambing — tinatayang 66 sa kanila ang umaabot sa tipping-point na seats@50/50 na halaga nito, na may dependence-robust na pinagsamang itaas na hangganan na humigit-kumulang 1&nbsp;sa&nbsp;350,000 sa ilalim ng reference distribution na iyon. Ang mapa ng mayorya ay maayos sa loob ng normal na saklaw.',
		tldr_p2: 'Sinubukan ng audit na ito ang parehong mapa ng komisyon sa parehong paraan, gamit ang 1,010,000 computer-drawn na neutral na mapa na binuo mula sa opisyal na shapefile ng Elections Alberta bilang sanggunian. Ang panukala ng mayorya ay nasa loob ng neutral na saklaw sa bawat pre-registered na pagsusulit. Ang panukala ng minorya ay lumagpas sa apat sa limang istrukturang pagsusulit, at ang partisan-fairness seat split nito sa isang 50/50 na boto ay naaabot ng humigit-kumulang 66 sa 1,010,000 neutral na mga mapa — isang dependence-robust na pinagsamang itaas na hangganan na humigit-kumulang 1 sa 350,000 sa ilalim ng reference distribution na iyon. (Ang naunang framing ng “1 sa 15 milyon” ay pinagsama ang dalawang channel na nagbabahagi ng pinagbabatayan na data at nagpalaki ng pinagsamang kahalagahan; ang figure sa itaas ay ang naitamang, mapagtiwalaan na hangganan.) Ang efficiency-gap metric ng audit para sa minorya ay nasa ika-94 na persentil — <em>malapit, ngunit nasa ibaba</em> ng sariling 95th-percentile na threshold ng audit.'
	},
	body: {
		clean: {
			sub3_p: 'Ang panukala ng minorya ay nasa matinding dulo ng 1,010,000-plan na ensemble sa tatlo sa apat na partisan-fairness metric, na ang ikaapat (efficiency gap, +4.0%) ay nasa ika-94 na persentil — <em>malapit, ngunit nasa ibaba</em> ng pre-registered na Alberta-calibrated na threshold ng ika-95. Ang tapat na pinagsamang pagbabasa ay hindi isang solong isa-sa-labinlimang-milyong numero: ang dalawang joint-test channel ay nagbabahagi ng pinagbabatayan na efficiency-gap data at hindi statistically independent, kaya ang pagsasama ng kanilang mga p-value sa ilalim ng paraan ni Fisher ay nagpapalaki ng kahalagahan. Ang mapagtiwalaan na itaas na hangganan mula sa isang dependence-robust na kombinasyon ay humigit-kumulang <strong>isa sa 350,000</strong> (Bonferroni; p&nbsp;≤2.8\xd710<sup>−6</sup>). Nananatiling matinding resulta iyon, na higit pa sa karaniwang mga threshold ng kahalagahan — ngunit iniuulat bilang isang hangganan, hindi bilang apat na independiyenteng instrumento na nagkakasundo.',
			details_p1: 'Ang isang p-value ay sumasagot sa isang tanong: kung ang mapa ay ginawa ng isang neutral na proseso, gaano kadalas nating makikita ang ganitong matinding resulta o mas matindi pa? Sa dependence-robust na hangganan na p&nbsp;≤2.8\xd710<sup>−6</sup>, ang sagot ay hindi hihigit sa isang beses sa 350,000 na pagsubok.',
			details_p2: 'Ito ay isang frequentist hypothesis test, hindi isang pagsukat ng intensyon. Hindi sinasabi nito na ang komisyon ay may intensyong mag-gerrymander, at hindi nito sinusukat kung gaano ka-unfair ang mapa sa praktikal na mga termino. Sinasabi nito na ang pattern ng hangganan ay statistically inconsistent sa ReCom neutral-drawing reference distribution — isang malakas na panlabas na pagsusuri, ngunit hindi perpekto (hindi nito ipinapatupad ang bawat statutory na pamantayan na sinunod ng komisyon, hal., mga tier ng s.15(2) at mga hadlang sa community-of-interest).',
			details_p3: 'Ang structural test battery (populasyon, paghahati, anchoring, compactness, mga lagda) ay nairehistro na may mga timestamp bago ang canonical recomputation. Ang mga partisan-bias channel (pinagsamang Mahalanobis, SZAT, Fisher/Bonferroni na kombinasyon) ay may label na "exploratory" sa sariling §4.3.1 ng audit: dokumentado sa repository, ngunit hindi pre-data. Iniuulat ng audit ang bawat channel nang hiwalay at pinagsasama ang mga ito sa ilalim ng dependence-robust na hangganan sa halip na ipakilala ang mga ito bilang ganap na independiyenteng confirmatory test.',
			super_lead: 'Sa isang 89-puwesto na lehislatura, ang isang dalawang-katlong supermayorya ay nangangailangan ng eksakto 60 upuan. Ang seats@50/50 ng panukala ng minorya na 51.7% (p99.99 laban sa 1,010,000-plan na ensemble) ay nasa rehiyon kung saan ang isang UCP supermayorya ay nagiging statistically reachable sa 2023 na heograpiya ng Alberta — ngunit ang ensemble null ay hindi nagpapatupad ng bawat statutory na pamantayan na sinunod ng komisyon, kaya ito ay isang malakas na panlabas na pagsusuri, hindi isang patunay na walang legal na mapa ng Alberta ang makakarating sa bilang na ito ng upuan. Ang structural-lane evidence sa Mga Natuklasan 1, 2 at 4 (na hindi nakasalalay sa null na ito) ang nagtataglay ng karamihan ng bigat; ang posisyon ng dulo ng seats@50/50 ay ang sumusuportang konteksto.',
			t5_r2_c: 'posisyon sa dulo sa tatlo sa apat na partisan-fairness metric — <code>seats@50/50</code> 51.7% (p99.99, humigit-kumulang 66 sa 1,010,000 ang umaabot dito); mean-median p99.98; declination p98.8 (UCP-tail); efficiency gap +4.0% (p94.4, <em>malapit ngunit nasa ibaba</em> ng pre-registered na 95th-percentile na threshold); dependence-robust na pinagsamang hangganan p&nbsp;≤2.8\xd710<sup>−6</sup> (≈ 1 sa 350,000)',
			defense4: '<strong>Ang "Incompetence o Masamang Swerte" na Depensa:</strong> <em>("Gumawa lang sila ng magulo na mapa at naswertehang masamang numero.")</em> Ang pag-hit ng isang 60-upuang supermayorya na configuration habang hinahati rin ang Airdrie sa apat na piraso at inilalagay ang tatlong hangganan sa mga eksaktong zone na ang sariling punong komisyon ay nagbandila bilang anomalous ay nangangailangan ng katumpakan. Ang pinagsamang dependence-robust na itaas na hangganan sa posibilidad ng aksidenteng pagguhit ng isang mapang ganito kasukdulan sa parehong analytical channel sa ilalim ng ReCom neutral reference distribution ay humigit-kumulang <strong>1 sa 350,000</strong> (p&nbsp;≤2.80\xd710<sup>−6</sup>). Ang naunang framing ng "1 sa 15 milyon" ay nag-assume ng channel independence na wala ang dalawang channel; ang naitamang hangganan ay matindi pa rin — higit pa sa karaniwang kahalagahan — ngunit iniuulat bilang isang hangganan, hindi bilang isang tumpak na solong posibilidad.',
			details2_p: 'Ang audit ay pre-registered ng limang istrukturang irregularity test noong Abril 24, 2026 bago naitipon ang mga resulta ng huling simulation. Ang anchoring ay neutral para sa parehong mapa; sa natitirang apat na pagsusulit ang minorya ay lumagpas sa bawat isa at ang mayorya ay wala ni isa. Ang mga sukat na iyon ay geometric — hindi sila nakasalalay sa anumang statistical sampler o anumang attribution ng boto. <strong>Ito ang sentral na natuklasan.</strong> Ang Lane 1 (ang mga numero ng partisan-fairness) ay nagpapatunay ng Lane 2 sa ilalim ng canonical na opisyal na shapefile: ang minorya ay nasa dulo ng 1,010,000-plan na ensemble sa tatlo sa apat na pre-registered na metric, na ang efficiency gap ay nasa p94.4 (<em>malapit, ngunit nasa ibaba</em> ng pre-registered na 95th-percentile na threshold), sa ilalim ng isang dependence-robust na pinagsamang itaas na hangganan na p&nbsp;≤2.8\xd710<sup>−6</sup> (≈ 1 sa 350,000; pinapalitan ang naunang Fisher-combined na figure na nagpalaki ng pinagsamang kahalagahan sa pamamagitan ng pagtrato ng dalawang channel na may magkaparehong data bilang independiyente). Ang tanong kung ang hindi pangkaraniwang geometry ng Lane 2 ay ang partikular na <em>mekanismo</em> sa likod ng mga numero ng Lane 1 ay sinubukan at ang sagot ay hindi — tingnan ang <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>. Ipinapakita ng Swing-Zone Allocation Test na ang mga pinagtatalunang pagpili ng hangganan ay partisan-skewed; ang sinubukan na tanong ay kung ang mga hugis ng hangganan mismo — ang laso corridor, ang park extension — ang direktang sanhi ng seat swing; hindi sila. Ang epekto ng upuan ay nagmumula sa kung paano inililipat ng mga muling ginawang Voting Area assignment ang kahusayan ng boto sa mga distrito, hindi mula sa mga hugis per se. Ang parehong lane ay nagbabandila sa mapa ng minorya; naaabot nila ito sa pamamagitan ng mga independiyenteng instrumento. Ang Lane 2 ang nagtataglay ng kaso. Ang Lane 1 ay nagpapatunay nang hindi nagtataglay.'
		}
	}
} as const;
