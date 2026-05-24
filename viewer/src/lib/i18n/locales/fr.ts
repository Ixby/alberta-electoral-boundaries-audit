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
				"« Gerrymander » n'est pas un terme employé par les tribunaux canadiens. Mais s'il l'était — au sens courant que la plupart des gens lui donnent — les éléments de cet audit appuieraient raisonnablement la qualification de la proposition minoritaire, si elle était adoptée, comme une carte fortement remaniée à des fins partisanes. Tous les tests structurels de cet audit signalent la proposition minoritaire ; aucun ne signale l'autre (la proposition majoritaire)."
		},
		q2: {
			heading: 'Que signifie « gerrymander » en droit canadien ?',
			body:
				"Rien. Le critère canadien est différent : il s'agit de savoir si les limites garantissent aux électeurs une représentation effective au sens de l'article 3 de la Charte. La proposition minoritaire soulève de sérieuses questions sous ce critère ; seul un juge peut y répondre de façon définitive, et personne n'en a saisi un."
		},
		q3: {
			heading: 'Qu\'est-ce que cela signifie pour les Albertains ?',
			body:
				"Lors d'un vote provincial à 50/50, les mesures de l'audit placent la proposition minoritaire dans un extrême structurel — moins de 100 des 1,01 million de cartes neutres de comparaison produisent un déséquilibre de sièges comparable. Ce déséquilibre compte parce qu'à 58 sièges sur 87 — une majorité des deux tiers — le parti au pouvoir débloque des pouvoirs procéduraux exceptionnels : il peut écarter les délais d'avis habituels et faire franchir à un projet de loi public plusieurs étapes législatives en une seule journée, contournant les freins délibératifs qui le contraignent normalement. Savoir si l'inclinaison de la proposition minoritaire est assez forte pour porter un parti au-delà de ce seuil de 58 sièges à des résultats de vote autres que 50/50 est une question que cet audit n'a pas encore examinée. Savoir si le compromis lui-même est acceptable est une question pour les Albertains, et non pour cet audit."
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
	}
} as const;
