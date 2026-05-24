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
	}
} as const;
