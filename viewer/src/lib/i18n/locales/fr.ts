// Canadian French (fr-CA). AI-translated, awaiting native-speaker review.
// Register choices: vous (formal/respectful); élus over politiciens;
// mordus de politique over passionnés; point de repère over référentiel.
export default {
	selector: {
		label: 'Choisir la langue'
	},
	disclaimer: {
		text:
			"Ce site a été traduit par IA. Certains contenus peuvent encore apparaître en anglais pendant que les traductions sont en cours. Si vous remarquez des erreurs ou souhaitez aider à traduire ce projet, n'hésitez pas à %s.",
		link_label: 'nous contacter'
	},
	opener: {
		heading: "À qui s'adresse ce document ?",
		body:
			"À nous. À nous tous. Aux ruraux, aux urbains, aux curieux, aux mordus de politique, aux journalistes, aux avocats, aux universitaires, aux élus — à nous tous. Parce que cela nous touche tous. Que vous aimiez ou non le parti au pouvoir, ce que la commission divisée a produit ne s'était jamais vu auparavant. Et cela nous donne l'occasion d'observer la mécanique de l'intérieur comme nous n'avions jamais pu le faire. Nous pouvons maintenant établir un point de repère — une série de tests, et tout ce qui suivra pourra être évalué à cette aune. Laissez-moi vous montrer ce que j'ai trouvé."
	},
	verdict: {
		q1: {
			heading: 'La carte proposée est-elle un découpage partisan ?',
			body:
				"« Gerrymander » n'est pas un terme employé par les tribunaux canadiens. Mais s'il l'était — au sens courant que la plupart des gens lui donnent — les éléments de cet audit appuieraient raisonnablement la qualification de la <em>proposition minoritaire</em>, si elle était adoptée, comme une carte fortement remaniée à des fins partisanes. Tous les tests structurels de cet audit signalent la <em>proposition minoritaire</em> ; aucun ne signale l'autre (la <em>proposition majoritaire</em>).",
			footnote:
				"Les noms « majorité » et « minorité » proviennent d'une division 3 contre 2 au sein de la Commission de délimitation électorale (présidée par le juge Miller), qui a produit deux propositions concurrentes plutôt qu'une seule recommandation. Un comité distinct de MLA présidé par Brandon Lunty — un MLA nommé par le Premier ministre — choisit actuellement entre les deux avant la date limite de novembre 2026."
		},
		q2: {
			heading: 'Que signifie « gerrymander » en droit canadien ?',
			body:
				"Rien. Le critère canadien est différent : il s'agit de savoir si les limites garantissent aux électeurs une <em>représentation effective</em> au sens de l'article 3 de la Charte. La proposition minoritaire soulève de sérieuses questions sous ce critère ; seul un juge peut y répondre de façon définitive, et personne n'en a saisi un."
		},
		q3: {
			heading: 'Qu\'est-ce que cela signifie pour les Albertains ?',
			body:
				"Lors d'un vote provincial à 50/50, les mesures de l'audit placent la proposition minoritaire dans un extrême structurel — moins de 100 des 1,01 million de cartes neutres de comparaison produisent un déséquilibre de sièges comparable. Ce déséquilibre compte parce qu'à 58 sièges sur 87 — une majorité des deux tiers — le parti au pouvoir débloque des pouvoirs procéduraux exceptionnels : il peut écarter les délais d'avis habituels et faire franchir à un projet de loi public plusieurs étapes législatives en une seule journée, contournant les freins délibératifs qui le contraignent normalement. Savoir si l'inclinaison de la proposition minoritaire est assez forte pour porter un parti au-delà de ce seuil de 58 sièges à des résultats de vote <em>autres</em> que 50/50 est une question que cet audit n'a pas encore examinée. Savoir si le compromis lui-même est acceptable est une question pour les Albertains, et non pour cet audit."
		},
		cta_law: 'Lire le contexte juridique →',
		cta_methods: 'Voir notre méthodologie →'
	},
	head: {
		title: 'Audit des limites électorales de l\'Alberta',
		meta_description:
			"Audit statistique de la commission albertaine de délimitation électorale de 2026 — 1 010 000 cartes neutres, fichiers officiels d'Elections Alberta, tests pré-enregistrés."
	},
	nav: {
		home_aria: 'Retour en haut',
		theme_aria: 'Basculer le mode sombre / clair',
		theme_title: 'Basculer le mode sombre',
		map: 'Carte',
		split: 'La Division',
		litmus: 'Test décisif',
		crack_pack: 'Diviser et entasser',
		impact: 'Conséquences',
		gerrymanders: 'Découpages partisans',
		november: 'Novembre',
		invisible: 'L\'invisible',
		retractions: 'Rétractations',
		references: 'Références',
		resources: 'Ressources'
	},
	hero: {
		h1: 'Audit des limites électorales de l\'Alberta',
		subtitle:
			"La commission albertaine a produit deux cartes de circonscriptions en 2026. Cet audit les a comparées — en appliquant les mêmes tests, également aux deux — pour déterminer si elles traitent les électeurs de la même manière.",
		badge: 'Cartes officielles d\'Elections Alberta — publiées en mai 2026',
		cover_note_1:
			"Cette carte est la meilleure porte d'entrée. Cliquez pour zoomer et explorer. Les boutons en haut permettent de basculer entre la proposition minoritaire, la proposition majoritaire et les limites adoptées en 2019 — ou de superposer les trois pour voir exactement où elles divergent. <strong>Detail</strong> colore chaque zone de vote selon le résultat de 2023 ; <strong>Trend</strong> ajoute un ombrage partisan par circonscription (bleu UCP, orange NDP) ; <strong>Lines</strong> active ou désactive les limites. <strong>Find</strong> permet de trouver une circonscription par son nom.",
		cover_note_2:
			"Essayez de verrouiller l'affichage et de passer d'une carte à l'autre — observez une limite se déplacer tandis que les électeurs en dessous restent en place. C'est toute la question en un seul geste.",
		cover_note_3:
			"Quand vous avez fini d'explorer, faites défiler vers le bas pour le résumé. Pour l'analyse technique complète, voir la section Ressources. Toutes les données proviennent des fichiers officiels d'Elections Alberta et d'autres sources gouvernementales et ouvertes.",
		image_alt:
			'Cartes des circonscriptions électorales de l\'Alberta — proposition minoritaire de la commission, coloriée selon les votes de 2023',
		map_hint: 'Cliquer pour explorer de façon interactive',
		btn_title: 'Cliquer pour ouvrir la carte interactive',
		btn_aria: 'Ouvrir la carte interactive'
	},
	boundary: {
		heading: "Ce que cet audit peut et ne peut pas vous dire",
		can_1:
			"Moins d'une carte sur 14,5 millions de cartes de comparaison générées aléatoirement a produit des motifs aussi extrêmes que la proposition minoritaire sur l'ensemble des quatre mesures statistiques combinées.",
		can_2:
			"La proposition minoritaire échoue à 5 des 5 tests structurels pré-enregistrés. La proposition majoritaire échoue à 0 sur 5.",
		can_3:
			"Ces résultats sont cohérents avec des cartes qui produisent de forts effets partisans, et incohérents avec ce que produit l'ensemble de comparaison aléatoire.",
		cant_1:
			"L'audit n'établit <strong>pas</strong> qu'un commissaire ait eu l'intention de produire les effets partisans mesurés. La géométrie des limites ne peut révéler l'intention.",
		cant_2:
			"L'audit ne prédit <strong>pas</strong> ce que le comité Lunty choisira, ce que sera le vote de novembre 2026, ni comment les Albertains réagiront.",
		cant_3:
			"L'audit ne prédit <strong>pas</strong> comment un tribunal trancherait si une contestation fondée sur la Charte était intentée contre l'une ou l'autre proposition.",
		cant_4:
			"L'audit ne dit <strong>pas</strong> à un électeur quelle position adopter ni quoi faire de cette information. Cela vous appartient."
	},
	section1: {
		heading: 'Qu\'est-ce que la redéfinition des circonscriptions et pourquoi devriez-vous vous y intéresser ?',
		p1: "Chaque électeur de l'Alberta vit dans une <em>circonscription électorale</em> — une portion de la province qui élit une personne à l'assemblée législative. Il y a 87 circonscriptions. Chaque circonscription élit un MLA. Quand vous votez à une élection provinciale, vous choisissez le MLA de la circonscription où vous habitez. C'est tout le lien que la plupart des Albertains entretiennent avec l'assemblée législative : un MLA, une circonscription, un vote.",
		p2: "Ces limites ne sont pas permanentes. Les gens déménagent, les quartiers grandissent, les régions rurales se vident, les villes s'étendent. Tous les huit à dix ans, l'Alberta est censée redessiner les limites pour que chaque circonscription soit à peu près de la bonne taille et reflète la façon dont les Albertains vivent réellement aujourd'hui. L'organisme qui s'en charge est la <em>Commission de délimitation électorale</em> — une commission indépendante composée de juges, d'avocats et de membres du public, et non de politiciens.",
		p3: "C'est le processus standard. Cette fois, le processus standard a produit quelque chose d'inhabituel. Les cinq membres de la commission se sont divisés 3 contre 2 sur ce à quoi la carte devait ressembler et, plutôt que de s'entendre sur une seule recommandation, ils en ont produit deux : une <em>proposition majoritaire</em> (appuyée par trois commissaires) et une <em>proposition minoritaire</em> (appuyée par deux). Les deux sont sur la table. Un comité distinct de MLA présidé par Brandon Lunty — nommé par le Premier ministre pour cette décision précise — est en train de choisir entre les deux. L'assemblée législative doit approuver celle qui survivra à ce comité avant novembre 2026.",
		p4: "Pourquoi cela compte pour vous : les limites décident qui est votre MLA. Elles décident quels quartiers, quelles villes et quelles préoccupations sont représentés ensemble. Si votre ville est divisée entre quatre MLA plutôt qu'un seul, aucun représentant unique n'est responsable de la ville dans son ensemble. Si votre communauté d'intérêts — une petite ville, une région rurale, un centre-ville — est divisée entre plusieurs circonscriptions, votre voix sur les décisions provinciales est diluée. La carte façonne aussi quel parti peut former un gouvernement, et à quelle marge. La conclusion précise de cet audit (que la proposition minoritaire se situe dans un extrême structurel) est la raison pour laquelle vous lisez ce site, mais la question plus large est plus ancienne et s'applique à chaque cycle de redécoupage : les limites reflètent-elles la façon dont les Albertains vivent, ou façonnent-elles la politique qui suit ?",
		p5: "Le reste de cette page parcourt ce que les deux cartes proposées font réellement."
	},
	section5: {
		heading: 'Ce que cela signifie pour vous et votre communauté',
		intro_p1:
			"Mettons de côté, pour un instant, la question de savoir quel parti gagne ou perd des sièges. Les politiciens et les partis tendent à présenter cela comme une lutte pour la concentration du pouvoir à l'assemblée législative, et à cette échelle c'en est une. Mais la concentration du pouvoir à l'assemblée n'est pas là où vous vivez ces cartes. Vous les vivez à travers trois questions concrètes sur votre propre circonscription :",
		intro_q1: 'Où vit votre MLA ?',
		intro_q2: 'Est-il investi dans votre communauté ?',
		intro_q3: 'Les exigences de la tête vont-elles dominer celles de la queue ?',
		intro_p2:
			"Tout autre cadrage — avantage partisan, seuil de supermajorité, extrême statistique — renvoie en fin de compte à ces trois questions. Les cinq échelons ci-dessous parcourent la manière dont chaque carte proposée y répond, à cinq échelles.",
		you_h: 'Vous.',
		you_p:
			"Votre circonscription électorale décide qui vous représente à l'assemblée législative. En ce moment, vous vivez dans l'une des 87 circonscriptions. Sous les deux cartes proposées, vous pourriez vous retrouver dans une autre — possiblement avec un autre MLA, possiblement rattaché à des communautés voisines différentes. Si vous ne savez pas dans quelle circonscription vous êtes en ce moment, ou qui est votre MLA, vous n'êtes pas seul : la plupart des Albertains ne sauraient nommer leur MLA. Mais les limites ne sont pas abstraites. Elles décident dont le numéro de téléphone est sur le mur du bureau de votre représentant local, dont la pétition de quartier porte votre nom, dont les préoccupations votre MLA entend en premier. La recherche par code postal sur ce site indique dans quelle circonscription vous vous trouvez sous chaque proposition. Si votre circonscription change, votre représentant change — et la relation de votre représentant avec votre communauté change avec lui.",
		community_h: 'Votre communauté.',
		community_p:
			"Les communautés ne sont pas abstraites non plus. La zone de fréquentation d'une école secondaire, une chambre de commerce, une communauté religieuse, une association de quartier — ce sont de véritables regroupements de personnes ayant des préoccupations locales communes. Lorsqu'une limite coupe à travers eux, aucun MLA unique n'est responsable de l'ensemble. Prenez Airdrie sous la proposition minoritaire : une ville d'environ 74 000 habitants découpée en quatre circonscriptions, chacune ancrée à un arrière-pays rural différent. Aucun représentant unique n'est responsable d'Airdrie comme ville. La même dynamique se joue partout où une ville, un quartier ou une communauté d'intérêts reconnue est divisée — plus la division est grande, plus la représentation est faible. L'audit mesure l'<em>ancrage municipal</em> (la fraction du périmètre de chaque circonscription qui suit les limites municipales existantes), et la proposition minoritaire obtient un score nettement inférieur à la majoritaire sur ce test.",
		municipality_h: 'Votre municipalité.',
		municipality_p:
			"Lorsqu'une ville est fragmentée entre de nombreux représentants, sa capacité à négocier sur les décisions provinciales s'affaiblit. Un conseil qui demande du financement pour le transport en commun, une commission scolaire qui négocie une nouvelle école, un maire qui fait pression pour des prolongements d'autoroute — chacun de ces dossiers progresse mieux quand la ville peut s'appuyer sur quelques MLA qui doivent rendre des comptes à la ville dans son ensemble. La proposition minoritaire divise le quadrant nord-ouest de Calgary entre plusieurs circonscriptions dont les schémas de vote suggèrent l'<em>entassement</em> (concentrer les électeurs d'un parti dans quelques sièges à forte marge) en plus du <em>fractionnement</em> (répartir les électeurs de l'autre parti dans plusieurs sièges à faible marge). Savoir si ce schéma est intentionnel est une question à laquelle l'audit ne peut pas répondre — la géométrie des limites ne révèle pas l'intention. Ce qu'il peut dire, c'est que les quatre mesures statistiques signalent les mêmes circonscriptions que les tests structurels signalent, et que la proposition alternative ne produit pas la même empreinte.",
		region_h: 'Votre région.',
		region_p1:
			"Si vous vivez en dehors des villes de l'Alberta, vous avez probablement remarqué que les conversations politiques sur les limites semblent toujours centrer les villes. C'est une plainte légitime, alors soyons directs sur ce que cet audit dit et ne dit pas sur l'Alberta rurale.",
		region_p2:
			"Ce qu'il ne dit <strong>pas</strong> : que l'Alberta rurale a trop de sièges. La loi sur la délimitation électorale permet aux populations des circonscriptions de varier jusqu'à 25 % afin qu'un MLA rural ne représente pas une géographie de la taille du sud de la France. Les tribunaux canadiens traitent cette variance comme légitime. Les deux cartes proposées la préservent. Rien dans cet audit ne change cela.",
		region_p3:
			"Ce qu'il <strong>dit</strong> : en plusieurs endroits sur la proposition minoritaire, des communautés rurales sont rattachées comme <em>queue</em> d'une circonscription dont le centre de population se trouve dans une ville. Regardez comment la proposition minoritaire traite Airdrie — une ville d'environ 74 000 habitants découpée en quatre circonscriptions, chacune prolongée dans un tronçon différent de la campagne rurale. Le centre de population de chaque nouvelle circonscription est la portion urbaine, pas la queue rurale. Un MLA élu d'une telle circonscription est le plus susceptible d'habiter, de faire campagne et de prioriser là où sont les voix — ce qui signifie que les communautés rurales autrefois représentées par un MLA rural dédié deviennent l'arrière d'un siège dirigé par la ville. Ce schéma se répète sur la proposition minoritaire d'une manière qu'il ne se répète pas sur la proposition majoritaire.",
		region_p4:
			"L'audit ne propose pas de retirer des sièges à l'Alberta rurale. Il demande si les limites respectent les communautés rurales que ces sièges sont censés représenter, ou si la géographie rurale est utilisée comme ballast pour absorber les votes urbains dans des circonscriptions dont le centre est ailleurs. Si vous vivez dans l'une de ces queues rurales, la question de savoir laquelle des cartes sera adoptée décide si votre MLA représente la communauté rurale où vous vivez réellement, ou un district urbain dont les limites incluent simplement votre terrain.",
		province_h: 'Votre province.',
		province_p:
			"L'assemblée législative est ce que vous obtenez quand vous additionnez les réponses de chaque circonscription aux trois questions ci-dessus. Si la plupart des circonscriptions sont ancrées à des communautés dont les MLA y vivent réellement, l'assemblée représente ces communautés. Si la plupart des circonscriptions ont des queues rurales rattachées à des têtes urbaines, l'assemblée représente les têtes — et les queues obtiennent l'attention qui reste. La question partisane — quel parti remporte la majorité — est en aval de cela. La question de la supermajorité — savoir si un parti franchit 58 des 87 sièges et débloque des raccourcis procéduraux comme la levée des délais d'avis ou l'accélération de projets de loi à travers plusieurs étapes en une seule journée — est en aval de <em>cela</em>. Lors d'un vote provincial hypothétique à 50/50, les mesures de l'audit placent la proposition minoritaire dans un extrême structurel : moins de 100 des 1,01 million de cartes neutres de comparaison produisent un déséquilibre de sièges comparable. Savoir si ce déséquilibre porte un parti au-delà de 58 sièges aux résultats de vote que les Albertains livrent réellement est une question que cet audit n'a pas encore directement examinée ; le verdict en haut de cette page est honnête sur cette lacune. Savoir si la réponse à l'une de ces questions compte assez pour agir est, encore une fois, une question pour vous."
	},
	section6: {
		heading: 'Une brève histoire du découpage partisan',
		p1: "Le mot vient de 1812. Le gouverneur du Massachusetts Elbridge Gerry a approuvé une carte sénatoriale dont les circonscriptions étaient si tordues pour favoriser son parti qu'un caricaturiste bostonien en a dessiné une comme une salamandre — ailes, griffes, langue fourchue. Le jeu de mots du caricaturiste, <em>Gerry-mander</em>, est resté. La forme aussi : deux siècles plus tard, le mot signifie toujours tracer des limites électorales pour produire un résultat partisan.",
		p2: "Le terme perdure parce que le problème perdure. Partout où les électeurs choisissent des représentants à partir de circonscriptions géographiques, quelqu'un doit tracer les limites, et les limites peuvent être tracées de plusieurs façons. Différents pays sont arrivés à différentes réponses sur qui devrait faire le tracé et ce qui devrait l'encadrer.",
		p3: "<strong>Les États-Unis</strong> traitent le découpage partisan comme un problème que les tribunaux fédéraux ne peuvent généralement pas régler. Dans <em>Rucho v. Common Cause</em> (2019), la Cour suprême des États-Unis a statué que les découpages partisans sont des « questions politiques » qui échappent à sa compétence. Certains États (Californie, Michigan) ont réagi en créant des commissions citoyennes indépendantes pour tracer leurs propres limites ; d'autres (Texas, Caroline du Nord) ont continué à tracer des cartes ouvertement partisanes et les ont défendues en s'appuyant sur le fait que <em>Rucho</em> le permet.",
		p4: "<strong>Le Royaume-Uni</strong> utilise quatre Commissions permanentes de délimitation — une pour l'Angleterre, l'Écosse, le Pays de Galles et l'Irlande du Nord — composées de juges et de hauts fonctionnaires. Elles retracent les limites tous les huit ans environ selon des règles fixes (égalité de population, cohérence géographique, respect des limites des administrations locales). Le Parlement peut en théorie rejeter les recommandations des commissions, mais dans la pratique ne le fait pratiquement jamais ; la convention veut que le jugement des commissions tienne.",
		p5: "<strong>L'Australie</strong> délègue le travail à la Commission électorale australienne, une agence fédérale indépendante avec autorité complète sur l'administration des élections et sur les limites. Les redécoupages ont lieu automatiquement quand le nombre de sièges d'un État change ou que sept ans se sont écoulés depuis le dernier. Les décisions des commissaires peuvent être révisées sur des motifs procéduraux mais pas sur des motifs partisans. Comme au Royaume-Uni, le résultat est que le découpage partisan tel que les Américains le connaissent est pratiquement inconnu.",
		p6: "Ces trois cas encadrent le spectre : tribunaux qui restent à l'écart (États-Unis), commissions indépendantes avec forte déférence parlementaire (Royaume-Uni), et agence indépendante permanente avec autorité complète (Australie). Le Canada se situe encore ailleurs — ce que la prochaine section aborde."
	},
	section7: {
		heading: 'Le Canada est différent — et semblable',
		p1: "Le Canada appartient à la même famille que les États-Unis, le Royaume-Uni et l'Australie. Nous élisons des membres uniques à partir de circonscriptions géographiques selon le scrutin majoritaire uninominal. Nous retraçons les limites périodiquement — au fédéral après chaque recensement décennal, dans les provinces selon des calendriers échelonnés. Nous avons hérité de la machinerie de base des mêmes racines de Westminster. Jusqu'ici, aucune surprise.",
		p2: "Ce qui distingue le Canada, c'est le critère que les limites doivent satisfaire.",
		p3: "Dans le droit constitutionnel américain, la règle contraignante est <em>une personne, un vote</em> — les circonscriptions doivent avoir des populations aussi égales que possible, et les écarts importants exigent une justification stricte. Dans le droit constitutionnel canadien, la règle contraignante est différente. L'article 3 de la <em>Charte canadienne des droits et libertés</em> garantit à chaque citoyen le droit de vote. Dans le <em>Renvoi : Circonscriptions électorales provinciales (Sask.)</em> — le Renvoi de la Saskatchewan de 1991, l'arrêt de référence — la Cour suprême du Canada a interprété ce droit comme un droit à une <em>représentation effective</em>, et non comme un droit à l'égalité mathématique des populations de circonscriptions.",
		p4: "Cette distinction compte. La représentation effective permet aux populations des circonscriptions de varier, parfois substantiellement, lorsqu'il y a de bonnes raisons : de vastes géographies rurales qu'un MLA ne peut raisonnablement desservir à une densité de population standard, des communautés d'intérêts qui doivent rester groupées, une représentation des minorités que l'égalité mathématique diluerait. Le Renvoi de la Saskatchewan a rendu cette flexibilité constitutionnelle. La variance de population de 25 % de la loi sur la délimitation électorale — la règle qui protège les sièges ruraux de l'Alberta — en découle directement.",
		p5: "Le hic, c'est que la flexibilité fonctionne dans les deux sens. Si une commission peut légitimement s'écarter de l'égalité de population pour les bonnes raisons, elle peut aussi s'en écarter pour les mauvaises. Le droit canadien n'a pas de plancher mathématique à l'américaine sur lequel se rabattre. Il a le critère de représentation effective, appliqué par les juges, après coup, en cas de litige. La plupart des juridictions se prémunissent contre les mauvaises raisons avec des protections structurelles : les commissions fédérales de redécoupage sont isolées par la loi et leurs recommandations entrent en vigueur automatiquement si le Parlement n'agit pas dans un délai imparti. Le Québec utilise une commission permanente indépendante dont l'Assemblée nationale ne peut renverser le travail qu'à une majorité des deux tiers. La Colombie-Britannique fonctionne selon une règle d'adoption par défaut similaire.",
		p6: "L'Alberta est l'exception. En vertu de la <em>Electoral Boundaries Commission Act</em>, le rapport de la commission n'est qu'une recommandation — l'assemblée législative doit voter pour l'adopter. C'est normalement une formalité. Dans le cycle 2026, la commission s'est divisée 3 contre 2 et a produit deux propositions concurrentes ; l'assemblée a créé un comité distinct de MLA, présidé par un MLA nommé par le Premier ministre, pour choisir entre elles. Rien dans le droit constitutionnel canadien n'exigeait que ce comité existe. Rien n'exige que son choix suive le processus de la commission. C'est la lacune structurelle que cet audit examine.",
		p7: "Donc, quand les tribunaux canadiens disent que « découpage partisan » n'est pas leur vocabulaire juridique, ils ne disent pas que le concept sous-jacent ne s'applique pas ici. Ils disent que le critère est différent — représentation effective, et non égalité mathématique. Savoir si la proposition minoritaire répond à ce critère est exactement la question contre laquelle cet audit a mesuré la géométrie, et exactement la question à laquelle seul un juge peut répondre de façon définitive. Le raisonnement complet du <em>Renvoi de la Saskatchewan</em>, le contraste avec d'autres provinces, la question de la qualité pour agir et les voies de réforme disponibles sont traités dans <a href=\"#references\">la section des références ci-dessous</a>."
	}
} as const;
