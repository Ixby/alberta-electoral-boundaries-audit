// Spanish (es). AI-translated, awaiting native-speaker review.
// Target reader: Alberta's hispanophone community — predominantly Mexican,
// Colombian, Venezuelan, and Central American origin. Neutral Latin American
// Spanish (not peninsular).
// Register: formal usted, civic-document register, preserving the audit's
// first-person personal voice.
export default {
	selector: {
		label: 'Elegir idioma'
	},
	disclaimer: {
		text:
			'Este sitio ha sido traducido por IA. Es posible que parte del contenido todavía aparezca en inglés mientras las traducciones están en curso. Si nota errores o quisiera ayudar a traducir este proyecto, por favor %s.',
		link_label: 'contáctenos',
		// {count} is replaced at runtime with the live word count of the
		// English prose, so volunteer translators know the size of the job
		// before raising their hand. Computed, never hardcoded — it stays
		// correct as the prose grows.
		word_count: 'Para darle una idea de la escala: la prosa en inglés suma alrededor de {count} palabras. Puede contribuir con todo o solo con una parte — en la mayoría de los casos el trabajo consiste en corregir errores menores que cometió la máquina, no en traducir desde cero.'
	},
	opener: {
		heading: '¿Para quién es esto?',
		body:
			'Para nosotros. Para todos nosotros. Gente rural, urbana, curiosa, aficionados a la política, periodistas, abogados, académicos, políticos — todos nosotros. Porque nos afecta a todos. Le guste o no el partido en el poder, lo que produjo la comisión dividida nunca se había hecho antes. Y nos ha dado la oportunidad de mirar dentro de la maquinaria como nunca antes pudimos. Ahora podemos establecer una línea de base — una serie de pruebas — y todo lo que venga después podrá calificarse contra ella. Permítame mostrarle lo que encontré.'
	},
	stakes: {
		q1: {
			heading: '¿Es el mapa propuesto un gerrymander?',
			body:
				'"Gerrymander" no es un término que usen los tribunales canadienses. Pero si lo fuera — en el sentido cotidiano que la mayoría de la gente le da — la evidencia de esta auditoría respaldaría razonablemente calificar la <em>propuesta minoritaria</em>, de ser promulgada, como un mapa fuertemente manipulado. Cuatro de las cinco pruebas estructurales que ejecuta esta auditoría señalan la <em>propuesta minoritaria</em> y ninguna señala la alternativa (la <em>propuesta mayoritaria</em>); la quinta prueba es neutral para ambas.',
			footnote:
				'Los nombres "mayoritaria" y "minoritaria" provienen de una división 3–2 dentro de la Comisión de Límites Electorales (presidida por el juez Miller), que produjo dos propuestas rivales en lugar de una sola recomendación. La Legislatura ha dejado desde entonces ambas de lado y remitió la redistritación a un comité de cinco MLA (miembros de la Asamblea Legislativa) presidido por Brandon Lunty (un MLA designado por el premier); el comité supervisa un Panel Asesor Independiente de cuatro personas — dos nominadas por el premier (el Hon. Monte Solberg y Darwin Durnie) y dos por el líder de la oposición (el Dr. Gerard Kennedy y Brent Robinson) — encargado de producir una nueva propuesta de límites de 91 escaños antes de la fecha límite de noviembre de 2026.'
		},
		q2: {
			heading: '¿Qué significa "gerrymander" en el derecho canadiense?',
			body:
				'No existe tal definición. La prueba canadiense es distinta: si los límites otorgan a los votantes una <em>representación efectiva</em> conforme al artículo 3 de la Carta. La propuesta minoritaria plantea serias preguntas bajo el estándar de representación efectiva; solo un juez puede responderlas de manera definitiva, y nadie se lo ha pedido todavía.'
		},
		q3: {
			heading: '¿Qué está en juego para los albertanos?',
			body:
				'Con un voto provincial de 50/50, las mediciones de la auditoría sitúan la propuesta minoritaria en un extremo estructural: menos de 100 de los 1.01 millones de mapas neutrales de comparación producen el mismo tipo de desequilibrio de escaños. Ese desequilibrio importa porque con 58 de 87 escaños (una supermayoría de dos tercios) el partido gobernante desbloquea poderes procedimentales extraordinarios. Puede dispensar los plazos de aviso estándar e impulsar proyectos de ley públicos a través de múltiples etapas legislativas en un solo día, eludiendo los controles deliberativos en los que la Legislatura normalmente se apoya. Si la inclinación de la propuesta minoritaria es lo bastante grande como para empujar a un partido más allá de ese umbral de 58 escaños con porcentajes de voto <em>distintos</em> de 50/50 es una pregunta que esta auditoría aún no ha puesto a prueba. Si ese desequilibrio es aceptable es una pregunta para los albertanos, no para esta auditoría.'
		},
		cta_law: 'Lea el contexto legal →',
		cta_methods: 'Vea cómo lo probamos →',
		scorecard_h: 'El tablero de resultados',
		scorecard_fig_alt:
			'Gráfico de dispersión: la brecha de eficiencia en el eje horizontal, el número de pruebas estructurales reprobadas en el eje vertical. El mapa promulgado en 2019 y el mapa mayoritario de 2026 se agrupan en la esquina segura, abajo a la izquierda. El mapa minoritario de 2026 aparece solo en la región de valores atípicos, arriba a la derecha.',
		scorecard_fig_caption:
			'Las dos vías en una sola imagen. Horizontal: qué tan sesgada es la cifra de equidad partidista (derecha = más favorable al UCP). Vertical: cuántas de las cinco pruebas de equidad estructural reprueba el mapa. La esquina inferior izquierda es la zona segura donde los procedimientos neutrales aterrizan de forma rutinaria; la superior derecha es la región de valores atípicos. El mapa promulgado en 2019 y el mayoritario de 2026 están en la esquina segura. El minoritario de 2026 está solo en la región atípica.',
		scorecard_intro:
			'Dos mediciones independientes aplicadas a ambos mapas bajo los mismos umbrales preregistrados. La estructura usa solo la forma de las líneas — ningún resultado electoral. Los números prueban cómo las líneas convierten votos en escaños. Ambas vías llegan a la misma conclusión.',
		scorecard_close:
			'Dos mediciones independientes, una sola respuesta. La convergencia es la señal individual más fuerte de la auditoría.'
	},
	top_callouts: {
		gerrymander_lead: '\u00bfEs el mapa minoritario un gerrymander?',
		gerrymander_body: 'En la puntuación de sesgo partidista conjunto de la auditoría, el mapa minoritario de la comisión se sitúa en la cola extrema de 1.010.000 mapas de comparación neutrales generados algorítmicamente — aproximadamente 66 de ellos alcanzan su valor de punto de inflexión seats@50/50, con una cota superior conjunta robusta a la dependencia de aproximadamente 1 en 350.000 bajo esa distribución de referencia. El mapa mayoritario queda cómodamente dentro del rango normal.',
		tldr_label: 'En breve',
		tldr_p1: 'La comisión de redistribución de Alberta se dividió 3-2 en 2026 y produjo dos mapas propuestos diferentes. El gobierno los apartó a ambos y asignó la redistribución a un comité de cinco MLA (el comité Lunty), que se espera informe en noviembre de 2026. Ninguno de los mapas de la comisión es ley.',
		tldr_p2: 'Esta auditoría puso a prueba ambos mapas de la comisión de la misma manera, usando 1.010.000 mapas neutros generados por computadora a partir de los shapefiles oficiales de Elections Alberta como punto de referencia. La propuesta mayoritaria se sitúa dentro del rango neutro en cada prueba preregistrada. La propuesta minoritaria cruza cuatro de cinco pruebas estructurales, y su reparto de escaños bajo equidad partidaria con un voto del 50/50 lo alcanzan aproximadamente 66 de esos mapas neutros &mdash; una cota superior robusta a la dependencia de aproximadamente 1 en 350.000 bajo un proceso de dibujo neutro. (La formulación anterior de "1 en 15 millones" combinaba dos canales que comparten datos subyacentes comunes y sobreestimaba la significancia conjunta; la cifra anterior es la cota corregida y defendible.)',
		tldr_p3: 'La auditoría mide resultados, no intenciones. Cuando el comité Lunty publique su mapa, esta auditoría le aplicará las mismas pruebas.',
		tldr_footer: 'Las condiciones de falsificación preregistradas y los compromisos de retractación están en %s.',
		tldr_footer_link: '\u00a79'
	},
	head: {
		title: 'Auditoría de los Límites Electorales de Alberta',
		meta_description:
			'Auditoría estadística de la comisión de límites electorales de Alberta de 2026 — 1,010,000 mapas neutrales, shapefiles oficiales de Elections Alberta, pruebas preregistradas.'
	},
	nav: {
		skip_to_content: 'Saltar al contenido',
		home_aria: 'Volver arriba',
		theme_aria: 'Alternar modo oscuro/claro',
		theme_title: 'Alternar modo oscuro',
		nav_aria: 'Abrir tabla de contenidos',
		drawer_top: '↑ Arriba',
		// Compact landmarks shown on the sticky bar
		stakes: 'En juego',
		findings: 'Hallazgos',
		history: 'Historia',
		reform: 'Reforma',
		notes: 'Notas',
		// Drawer group headings
		group_overview: 'Panorama',
		group_audit: 'La auditoría',
		group_context: 'Contexto',
		group_forward: 'Hacia adelante',
		group_apparatus: 'Aparato',
		// Drawer entries
		why: '¿Por qué importa esto?',
		map: 'El mapa de un vistazo',
		split: 'Cómo se dividió la comisión',
		litmus: 'Prueba de fuego de 1,010,000 mapas',
		crack_pack: 'Fragmentar, empaquetar, drenar',
		for_you: 'Qué significa esto para usted',
		impact: 'Impacto en el terreno',
		gerrymanders: 'Gerrymanders limpios',
		history_full: 'Una historia del gerrymandering',
		canada: 'Canadá es diferente',
		november: 'Noviembre',
		lunty: 'Lunty',
		invisible: 'Lo invisible',
		suggestions: 'Sugerencias de reforma',
		retractions: 'Retractaciones',
		references: 'Referencias',
		resources: 'Recursos',
		technical: 'Recursos técnicos'
	},
	hero: {
		h1: 'Auditoría de los Límites Electorales de Alberta',
		subtitle:
			'La comisión de Alberta produjo dos mapas de distritos en 2026. Esta auditoría los comparó — con las mismas pruebas, aplicadas por igual a ambos — para preguntar si tratan a los votantes de la misma manera.',
		badge: 'Mapas oficiales de Elections Alberta — publicados en mayo de 2026',
		cover_note: 'Haga clic para acercar y explorar las tres propuestas de límites simultáneamente. Fije la vista y alterne entre mapas — los límites se mueven, los votantes permanecen. Desplácese hacia abajo para ver el análisis.',
		cover_note_1:
			'Este mapa es la mejor puerta de entrada. Haga clic para acercar y explorar. Los botones de arriba alternan entre el mapa minoritario, el mapa mayoritario y los límites promulgados en 2019 — o superponga los tres para ver exactamente dónde divergen. <strong>Detail</strong> colorea cada área de votación según cómo votó la gente en 2023; <strong>Trend</strong> añade sombreado partidista por distrito (azul UCP, naranja NDP); <strong>Lines</strong> activa y desactiva los límites. <strong>Find</strong> salta a cualquier distrito por nombre.',
		cover_note_2:
			'Pruebe fijar la vista y alternar entre mapas — observe cómo un límite se desplaza mientras los votantes debajo permanecen quietos. Toda la cuestión, en un solo gesto.',
		cover_note_3:
			'Cuando termine de explorar, desplácese hacia abajo para el resumen. Para el análisis técnico completo, vea la sección de Recursos. Todos los datos son shapefiles oficiales de Elections Alberta y otros registros gubernamentales y de código abierto.',
		image_alt:
			'Mapas de distritos electorales de Alberta — propuesta minoritaria de la comisión, coloreada según el voto de 2023',
		map_hint: 'Haga clic para explorar interactivamente',
		btn_title: 'Haga clic para abrir el mapa interactivo',
		btn_aria: 'Haga clic para explorar interactivamente'
	},
	boundary: {
		heading: 'Lo que esta auditoría puede y no puede decirle',
		can_1:
			'La geometría del mapa minoritario cruza 4 de los 5 umbrales estructurales preregistrados <em>sin usar dato electoral alguno</em>. El quinto (el anclaje) es neutral. El mayoritario cruza 0 de los 4 que se activan. Estas pruebas miden propiedades de las propias líneas de los límites — la forma de los distritos, el anclaje municipal, la dispersión poblacional — y llegan a la conclusión antes de que se cuente un solo voto.',
		can_2:
			'Por separado, cuando se incorporan los datos electorales, el mapa minoritario se sitúa en el percentil 99.99 de 1.01 millones de mapas de comparación trazados algorítmicamente bajo las mismas reglas estatutarias. Menos de 100 de esos 1.01 millones de mapas neutrales alcanzan el mismo desequilibrio de escaños. La señal estadística combinada es de aproximadamente 1 en 350.000 bajo un proceso de trazado neutral. Dos instrumentos independientes — geométrico y estadístico — llegan a la misma conclusión.',
		can_3:
			'Tres de las configuraciones que contiene la propuesta minoritaria fueron señaladas por escrito por el presidente de la Comisión, el juez Miller, en el §5.8.2 del informe mayoritario y en el Apéndice C. Las pruebas de la auditoría se ejecutaron sin conocimiento de sus señalamientos y hacen aflorar las mismas regiones. Un tercer instrumento independiente — el judicial — converge en los mismos límites.',
		cant_1:
			'La auditoría <strong>no</strong> establece que algún comisionado haya tenido la intención de producir los efectos partidistas que mide. La geometría de los límites no puede revelar la intención.',
		cant_2:
			'La auditoría <strong>no</strong> predice qué elegirá el comité Lunty, cuál será el voto de noviembre de 2026, ni cómo reaccionarán los albertanos.',
		cant_3:
			'La auditoría <strong>no</strong> predice cómo fallaría un tribunal si se presentara una impugnación basada en la Carta contra cualquiera de las dos propuestas.',
		cant_4:
			'La auditoría <strong>no</strong> afirma que la cifra de 1 en 350.000 sea la probabilidad de que haya ocurrido un gerrymander. Ese número es la probabilidad de cola de la geometría minoritaria bajo un nulo algorítmico neutral. Es evidencia de que el nulo neutral es implausible. No es una probabilidad a posteriori de intención partidista — esa pregunta requiere evidencia que la geometría no puede aportar.',
		cant_5:
			'La auditoría <strong>no</strong> le dice a ningún votante individual qué posición tomar ni qué hacer con esta información. La decisión es suya.'
	},
	editorial_intro: {
		heading: 'Qué es la redistritación, y por qué importa',
		p1: 'Cada votante de Alberta vive en un <em>distrito electoral</em> — una porción de la provincia que elige a una persona para la Legislatura. Hay 87 distritos. Cada distrito elige un MLA. Cuando usted deposita su boleta en una elección provincial, está eligiendo al MLA del distrito donde vive. Para la mayoría de los albertanos, esa es toda la conexión con la Legislatura: un MLA, un distrito, un voto.',
		p2: 'Esas líneas de distrito no son permanentes. La gente se muda, los vecindarios crecen, las zonas rurales se despueblan, las ciudades se expanden. Cada ocho a diez años, se supone que Alberta redibuja las líneas para que cada distrito tenga aproximadamente el tamaño correcto y refleje la manera en que los albertanos viven realmente hoy. El órgano que hace el retrazado es la <em>Comisión de Límites Electorales</em> — una comisión independiente con jueces, abogados y miembros del público, no políticos.',
		p3: 'Ese es el proceso estándar. Esta vez, el proceso estándar produjo algo inusual. Los cinco miembros de la comisión se dividieron 3–2 sobre cómo debía verse el mapa y, en lugar de acordar una sola recomendación, produjeron dos: una <em>propuesta mayoritaria</em> (respaldada por tres comisionados) y una <em>propuesta minoritaria</em> (respaldada por dos). Ambas están sobre la mesa — y la Legislatura ha dejado ambas de lado. Un comité aparte de MLA presidido por Brandon Lunty — designado por el premier para esta decisión específica — supervisa ahora un Panel Asesor Independiente de cuatro personas, constituido bajo la Moción Gubernamental 37 (aprobada el 21 de abril de 2026), encargado de producir un nuevo mapa de 91 escaños. La Legislatura debe aprobar lo que el comité entregue antes de noviembre de 2026.',
		p4: 'Por qué le importa a usted: las líneas deciden quién es su MLA. Deciden qué vecindarios, pueblos y preocupaciones quedan representados juntos. Si su ciudad está dividida entre cuatro MLA en lugar de uno, ningún representante es responsable de la ciudad en su conjunto. Si su comunidad de interés — un pueblo pequeño, una región rural, un centro urbano — queda dividida entre distritos, su voz en las decisiones provinciales se diluye. El mapa también determina qué partido puede formar gobierno, y con qué márgenes. El hallazgo específico de la auditoría (que la propuesta minoritaria se sitúa en un extremo estructural) es la razón por la que usted está leyendo este sitio, pero la pregunta más amplia es más antigua y aplica a cada ciclo de redistritación: ¿reflejan las líneas la manera en que viven los albertanos, o moldean la política que viene después?',
		p5: 'El resto de esta página recorre lo que los dos mapas propuestos hacen en realidad.',
		key_terms_lead: 'Términos clave de esta sección — haga clic para leer:'
	},
	editorial_reflect: {
		heading: 'Interludio: qué significa esto para usted y su comunidad',
		intro_p1:
			'Deje de lado, por un momento, la pregunta de qué partido gana o pierde escaños. Los políticos y los partidos tienden a plantear esto como una lucha por la concentración de poder en la Legislatura, y a escala legislativa lo es. Pero la concentración de poder en la Legislatura no es donde usted experimenta estos mapas. Usted los experimenta a través de tres preguntas concretas sobre su propio distrito:',
		intro_q1: '¿Dónde vive su MLA?',
		intro_q2: '¿Está comprometido con su comunidad?',
		intro_q3: '¿Dominarán las exigencias de la cabeza sobre las exigencias de las colas?',
		intro_p2:
			'Cualquier otro encuadre — ventaja partidista, umbral de supermayoría, extremo estadístico — termina apuntando de vuelta a esas tres. Los cinco peldaños siguientes recorren cómo responde cada mapa propuesto a esas preguntas, en cinco escalas.',
		you_h: 'Usted.',
		you_p:
			'Su distrito electoral decide quién lo representa en la Legislatura. En este momento usted vive en uno de 87 distritos. Bajo ambos mapas propuestos podría vivir en uno distinto — posiblemente con un MLA distinto, posiblemente anclado a comunidades vecinas distintas. Si no sabe en qué distrito está ahora mismo, o quién es su MLA, no está solo: la mayoría de los albertanos no podría nombrar a su MLA. Pero las líneas de los límites no son abstractas. Deciden qué número de teléfono está en la pared de la oficina de su representante local, a qué petición de vecindario se adjunta su nombre, qué preocupaciones escucha primero su MLA. La búsqueda por código postal en este sitio muestra en qué distrito queda usted bajo cada propuesta. Si su distrito cambia, su representante cambia — y la relación de su representante con su comunidad cambia con él.',
		community_h: 'Su comunidad.',
		community_p:
			'Las comunidades tampoco son abstractas. La zona de influencia de una escuela secundaria, una cámara de comercio, una comunidad de fe, una asociación de vecinos — son agrupaciones reales de personas con preocupaciones locales compartidas. Cuando una línea de límite las corta, ningún MLA es responsable del conjunto. Tome Airdrie bajo la propuesta minoritaria: una ciudad de aproximadamente 85,800 personas rebanada en cuatro distritos electorales, cada uno anclado a un interior rural distinto. Ningún representante es responsable de Airdrie como ciudad. La misma dinámica ocurre dondequiera que se divide un pueblo, un vecindario o una comunidad de interés reconocida — cuanto mayor la división, más débil la representación. La auditoría mide el <em>anclaje municipal</em> (qué fracción del perímetro de cada distrito sigue las líneas municipales existentes), y la propuesta minoritaria obtiene una puntuación notablemente menor que la mayoritaria en la prueba de anclaje.',
		municipality_h: 'Su municipio.',
		municipality_p:
			'Cuando una ciudad queda fracturada entre muchos representantes, su capacidad de negociar en las decisiones provinciales se debilita. Un concejo que pide financiamiento para el transporte público, una junta escolar que negocia una escuela nueva, un alcalde que cabildea por extensiones de carretera — cada una de esas gestiones va mejor cuando la ciudad puede señalar a unos pocos MLA que deben rendir cuentas a la ciudad en su conjunto. La propuesta minoritaria divide el cuadrante noroeste de Calgary entre múltiples distritos cuyos patrones de proporción de voto sugieren <em>empaquetamiento</em> (concentrar a los votantes de un partido en unos pocos escaños de margen alto) encima de <em>fragmentación</em> (repartir a los votantes del otro partido entre muchos escaños de margen bajo). Si el patrón es intencional es una pregunta que la auditoría no puede responder — la geometría de los límites no revela la intención. Lo que sí puede decir es que las cuatro medidas estadísticas señalan los mismos distritos que señalan las pruebas estructurales, y que la propuesta alternativa no produce la misma huella.',
		region_h: 'Su región.',
		region_p1:
			'Si usted vive fuera de las ciudades de Alberta, probablemente ha notado que las conversaciones políticas sobre los límites siempre parecen centrarse en las ciudades. Es una queja justa, así que seamos directos sobre lo que esta auditoría dice y no dice sobre la Alberta rural.',
		region_p2:
			'Lo que <strong>no</strong> dice: que la Alberta rural tiene demasiados escaños. La EBCA (la Ley de la Comisión de Límites Electorales de Alberta) permite que las poblaciones de los distritos varíen hasta en un 25% para que un solo MLA rural no represente una geografía del tamaño del sur de Francia. Los tribunales canadienses tratan esa variación como legítima. Ambos mapas propuestos la preservan. Nada en esta auditoría la cambia.',
		region_p3:
			'Lo que <strong>sí</strong> dice: en varios lugares de la propuesta minoritaria, comunidades rurales están siendo adjuntadas como la <em>cola</em> de un distrito cuyo centro de población está en una ciudad. Mire cómo la propuesta minoritaria trata a Airdrie — una ciudad de unas 85,800 personas rebanada en cuatro distritos, cada uno extendido hacia un tramo distinto del campo rural. El centro de población de cada nuevo distrito es la porción urbana, no la cola rural. Un MLA elegido en ese tipo de distrito tenderá a vivir, hacer campaña y priorizar donde están los votos — lo que significa que comunidades rurales antes representadas por un MLA rural dedicado se convierten en la mitad trasera de un escaño liderado por lo urbano. Ese patrón se repite en la propuesta minoritaria de maneras que no se repiten en la propuesta mayoritaria.',
		region_p4:
			'La auditoría no propone quitarle escaños a la Alberta rural. Pregunta si las líneas respetan a las comunidades rurales que esos escaños deben representar, o si la geografía rural está siendo usada como lastre para absorber votos urbanos en distritos cuyo centro está en otra parte. Si usted vive en una de esas colas rurales, la pregunta de qué mapa se promulga decide si su MLA representa a la comunidad rural en la que usted realmente vive, o a un distrito urbano cuyas líneas casualmente incluyen su tierra.',
		province_h: 'Su provincia.',
		province_p:
			'La Legislatura es lo que se obtiene al sumar las respuestas de cada distrito a las tres preguntas de arriba. Si la mayoría de los distritos están anclados a comunidades en las que sus MLA realmente viven, la Legislatura representa a esas comunidades. Si la mayoría de los distritos tienen colas rurales adjuntas a cabezas urbanas, la Legislatura representa a las cabezas — y las colas reciben la atención que sobra. La pregunta partidista — qué partido gana la mayoría — está aguas abajo de eso. La pregunta de la supermayoría — si un partido cruza 58 de 87 escaños y desbloquea atajos procedimentales como dispensar plazos de aviso o acelerar proyectos de ley a través de múltiples etapas en un solo día — está aguas abajo de <em>eso</em>. Con una división provincial hipotética de 50/50, las mediciones de la auditoría sitúan la propuesta minoritaria en un extremo estructural: menos de 100 de los 1.01 millones de mapas neutrales de comparación producen el mismo tipo de desequilibrio de escaños. Si ese desequilibrio empuja a un partido más allá de los 58 escaños con los porcentajes de voto que los albertanos realmente entregan es una pregunta que esta auditoría aún no ha probado directamente; las preguntas iniciales en la parte superior de esta página son honestas sobre esa brecha. Si la respuesta a cualquiera de estas preguntas importa lo suficiente como para actuar es, de nuevo, una pregunta para usted.'
	},
	editorial_history: {
		heading: 'Contexto: una breve historia del gerrymandering',
		p1: 'La palabra viene de 1812. El gobernador de Massachusetts, Elbridge Gerry, aprobó un mapa del senado estatal cuyos distritos estaban tan retorcidos a favor de su partido que un caricaturista de Boston dibujó uno de ellos como una salamandra — alas, garras, lengua bífida. El juego de palabras del caricaturista, <em>Gerry-mander</em>, perduró. La forma también: dos siglos después, la palabra sigue significando trazar líneas electorales para fabricar un resultado partidista.',
		p2: 'El término perdura porque el problema perdura. Dondequiera que los votantes eligen representantes por distritos geográficos, alguien tiene que trazar las líneas, y las líneas pueden trazarse de muchas maneras. Distintos países han llegado a distintas respuestas sobre quién debe hacer el trazado y qué debe limitarlo.',
		p3: '<strong>Estados Unidos</strong> trata el gerrymandering partidista como un problema que los tribunales federales en su mayoría no pueden corregir. En <em>Rucho v. Common Cause</em> (2019), la Corte Suprema de EE. UU. dictaminó que los gerrymanders partidistas son "cuestiones políticas" fuera de su jurisdicción. Algunos estados (California, Michigan) han respondido creando comisiones ciudadanas independientes para trazar sus propias líneas; otros (Texas, Carolina del Norte) han seguido trazando mapas abiertamente partidistas y los han defendido sobre la base de que <em>Rucho</em> lo permite.',
		p4: '<strong>El Reino Unido</strong> usa cuatro Comisiones de Límites permanentes — una para Inglaterra, Escocia, Gales e Irlanda del Norte — integradas por jueces y altos funcionarios de carrera. Redibujan las líneas aproximadamente cada ocho años contra reglas fijas (igualdad de población, coherencia geográfica, respeto a los límites de los gobiernos locales). El Parlamento puede en teoría rechazar las recomendaciones de las comisiones, pero en la práctica casi nunca lo hace; por convención, el juicio de las comisiones se mantiene.',
		p5: '<strong>Australia</strong> delega el trabajo en la Comisión Electoral Australiana, una agencia federal independiente con plena autoridad tanto sobre la administración electoral como sobre los límites. Las redistribuciones ocurren automáticamente cuando cambia el número de escaños de un estado o pasan siete años desde la última. Las decisiones de los comisionados son revisables por motivos procedimentales pero no por motivos partidistas. Como en el Reino Unido, el gerrymandering tal como lo conocen los estadounidenses es prácticamente inexistente.',
		p6: 'Estos tres casos delimitan el espectro: tribunales que se mantienen al margen (EE. UU.), comisiones independientes con fuerte deferencia parlamentaria (Reino Unido), y una agencia independiente permanente con plena autoridad (Australia). Canadá se sitúa en otro lugar distinto — que es lo que aborda la siguiente sección.'
	},
	glossary: {
		more_link: 'Más información →',
		'electoral-district': {
			term: 'Distrito electoral (ED)',
			definition:
				'El área geográfica que elige a un miembro de la Legislatura provincial. A menudo se abrevia "ED" (por electoral district) tras la primera mención. Cada ED tiene un MLA. (La palabra "riding" suele referirse a los distritos federales; en el contexto provincial el término correcto es distrito electoral.)'
		},
		riding: {
			term: 'Riding',
			definition:
				'En el uso canadiense, esta palabra se refiere casi siempre a un distrito electoral federal. El equivalente provincial en Alberta se llama "distrito electoral" (ED). La auditoría emplea el término provincial en todo el documento.'
		},
		mla: {
			term: 'MLA',
			definition:
				'Member of the Legislative Assembly (miembro de la Asamblea Legislativa) — la persona elegida en un distrito electoral para representarlo en la Legislatura de Alberta.'
		},
		ucp: {
			term: 'UCP',
			definition:
				'United Conservative Party (Partido Conservador Unido) — el actual partido provincial gobernante de Alberta. Formado en 2017 por la fusión de los Conservadores Progresistas y el Wildrose Party; gobierna desde 2019.'
		},
		ndp: {
			term: 'NDP',
			definition:
				'New Democratic Party (Nuevo Partido Democrático de Alberta) — la actual oposición oficial de Alberta. El NDP de Alberta gobernó de 2015 a 2019.'
		},
		gerrymander: {
			term: 'Gerrymander',
			definition:
				'Un mapa trazado para que un partido político gane más escaños de los que su proporción del voto sugeriría. La palabra viene de un distrito de Massachusetts de 1812 con forma de salamandra. No es un término legal en Canadá, pero el concepto se estudia ampliamente.'
		},
		cracking: {
			term: 'Fragmentación (cracking)',
			definition:
				'Una técnica de gerrymandering que divide un bloque de votantes entre muchos distritos para que nunca alcance la mayoría en ninguno. Por ejemplo, dividir una ciudad entre cuatro distritos de modo que sus votantes queden en minoría en cada uno.'
		},
		packing: {
			term: 'Empaquetamiento (packing)',
			definition:
				'Una técnica de gerrymandering que concentra a los votantes de un partido en un número reducido de distritos. El partido gana esos distritos de manera abrumadora pero "desperdicia" muchos votos — dejando a menos de sus votantes disponibles para competir en otros distritos.'
		},
		draining: {
			term: 'Drenaje (draining)',
			definition:
				'Un término que esta auditoría usa para un efecto derivado de la fragmentación y el empaquetamiento: los votos desperdiciados que esas técnicas producen se empujan hacia lugares elegidos estratégicamente, alterando el carácter político de los distritos electorales cercanos. Es un encuadre propio de la auditoría más que un concepto establecido en la literatura sobre redistritación — la auditoría prueba el efecto y encuentra resultados consistentes con él, pero lo trata como exploratorio en lugar de una metodología asentada.'
		},
		anchoring: {
			term: 'Anclaje (anchoring)',
			definition:
				'Qué tan firmemente los límites propuestos siguen las líneas municipales existentes (límites de ciudades, límites de pueblos). Un mapa muy anclado respeta esas líneas en su mayoría; un mapa poco anclado se aparta de ellas con frecuencia — especialmente en puntos políticamente significativos, lo cual es una señal de advertencia estructural.'
		},
		'charter-s3': {
			term: 'Artículo 3 de la Carta',
			definition:
				'El artículo de la Carta Canadiense de Derechos y Libertades que garantiza a los ciudadanos el derecho al voto. Los tribunales canadienses lo han interpretado no como una regla estricta de "una persona, un voto", sino como un derecho a la "representación efectiva".'
		},
		'effective-representation': {
			term: 'Representación efectiva',
			definition:
				'El estándar que los tribunales canadienses aplican al juzgar límites electorales. Significa que los votantes deben tener una voz significativa — no solo igualdad numérica de las poblaciones de los distritos, sino también reconocimiento de los lazos comunitarios, la geografía y la representación de minorías. El enunciado de referencia proviene del Saskatchewan Reference de 1991 de la Corte Suprema de Canadá.'
		},
		ebc: {
			term: 'Comisión de Límites Electorales (EBC)',
			definition:
				'El órgano que traza los límites electorales provinciales de Alberta bajo la EBCA. La comisión de 2026 fue presidida por el juez Miller y se dividió 3–2 entre sus comisionados, produciendo dos propuestas rivales (la mayoritaria y la minoritaria) en lugar de una sola recomendación.'
		},
		'lunty-committee': {
			term: 'Comité Lunty',
			definition:
				'Un Comité Especial Selecto sobre Límites Electorales de cinco MLA presidido por Brandon Lunty — un MLA designado por el premier — establecido por la Moción 19 de la Asamblea Legislativa (16 de abril de 2026), que dejó de lado ambos informes de la comisión. El comité supervisa un Panel Asesor Independiente aparte, de cuatro personas, constituido bajo la Moción Gubernamental 37 (aprobada el 21 de abril de 2026), que traza el mapa propiamente dicho; el comité luego informa a la Legislatura antes de la fecha límite de noviembre de 2026. Ambos órganos son distintos de la EBC y no forman parte del proceso estándar de la EBCA.'
		},
		'advisory-panel': {
			term: 'Panel Asesor Independiente',
			definition:
				'El panel de cuatro personas designado por el comité Lunty bajo la cláusula C(d)(ii) de la Moción Gubernamental 37 para trazar una recomendación de límites de 91 escaños. El premier nominó al Hon. Monte Solberg y a Darwin Durnie; el líder de la oposición nominó al Dr. Gerard Kennedy y a Brent Robinson. Un quinto asiento — un juez en funciones o jubilado para servir como presidente — quedó sin cubrir después de que la jueza en jefe interina de Alberta declinó nominar a uno.'
		},
		ebca: {
			term: 'EBCA',
			definition:
				'La Alberta Electoral Boundaries Commission Act (Ley de la Comisión de Límites Electorales de Alberta) — la ley que rige cómo se trazan los límites electorales en la provincia. Establece la comisión, el proceso de audiencias públicas y las reglas sobre cuándo entra en vigor un nuevo mapa.'
		},
		fsa: {
			term: 'Área de clasificación postal (FSA)',
			definition:
				'Los primeros tres caracteres de un código postal canadiense (la parte letra-dígito-letra). Unas 270 FSA cubren Alberta. La mayoría cae por completo dentro de un solo distrito electoral.'
		}
	},
	body: {
		section_link_aria: 'Enlace a la sección',
		the_map: {
			heading: '1: El mapa',
			p1: 'El mapa de portada es la mejor imagen individual de esta auditoría. Así se lee.',
			p2: 'Alberta está dividida en 4,765 Áreas de Votación — pequeñas zonas geográficas que Elections Alberta usa para contar las boletas de los centros de votación. Cada una está coloreada según cómo votó realmente la gente que vive en ella en 2023: naranja donde se concentran los votos del NDP, azul donde se concentran los del UCP. Pero el color solo se vuelve oscuro y saturado donde vive mucha gente. Un Área de Votación que cubre cientos de kilómetros cuadrados de parques o tierras de cultivo permanece pálida — casi invisible. El mapa se ilumina donde está la gente, y se apaga donde no está.',
			p3: 'Esto es muy distinto de la Alberta que usted ve la noche de las elecciones. La mayoría de los mapas electorales colorean distritos enteros de azul o naranja sólido según quién ganó. Los distritos rurales son geográficamente grandes y el UCP gana la mayoría de ellos, así que la Alberta de la noche electoral parece un muro de azul con pequeños bolsillos naranjas en Edmonton y Calgary. El mapa de portada usa los mismos votos y la misma geografía — pero los muestra ponderados por dónde vive realmente la gente. Lo que aparece es una provincia donde la mayor parte de la población se concentra en un denso arco de ciudades, y esas ciudades votan de manera muy distinta al mapa rural que normalmente las representa.',
			p4: 'Las líneas de límites dibujadas sobre el color son los 89 distritos electorales propuestos por la minoría de la comisión — el mapa que esta auditoría termina criticando. El trabajo de la auditoría es preguntar qué les hacen esas líneas a las personas que están debajo.',
			p5: 'Esta imagen es lo que deja claro lo que está en juego. Una provincia que parece votar de una manera en un mapa estándar es en realidad una provincia donde la mayoría de la gente vive en zonas que votan de la otra. Una vez que la población es visible bajo las decisiones de límites, esas decisiones dejan de parecer aleatorias.'
		},
		structural_results: {
			heading: 'Resultados de la auditoría estructural — antes de cualquier estadística:',
			body: 'El mapa mayoritario cruza <strong>cero de cinco</strong> umbrales estructurales preregistrados. El mapa minoritario cruza <strong>cuatro de los cinco</strong>; el quinto (el anclaje) es neutral — ambos mapas caen dentro de la norma canadiense de 70–85%. Estas son mediciones geométricas — dispersión poblacional, <button class="vocab-term" data-def="qué tan de cerca los bordes de un distrito siguen los límites municipales y de ciudad preexistentes, en lugar de atravesarlos" aria-expanded="false">anclaje municipal</button>, número de divisiones de Airdrie, exceso de población del noroeste de Calgary, y las siete configuraciones de límites que el propio presidente de la Comisión, el juez Miller, señaló por escrito (§5.8.2 del informe mayoritario y Apéndice C) — que no requieren datos electorales ni muestreador estadístico alguno. La siguiente sección prueba ambos mapas contra 1,010,000 mapas neutrales generados por computadora y llega a la misma conclusión a través de un instrumento completamente distinto. Tres instrumentos independientes — geométrico, judicial y estadístico — convergen.'
		},
		clean: {
			heading: '6: Cuando un mapa que parece justo no lo es',
			legal_label: 'UNA NOTA SOBRE TERMINOLOGÍA LEGAL',
			legal_body: '"Gerrymandering" no tiene definición legal en el derecho canadiense. La palabra se usa a lo largo de este informe en su sentido político cotidiano — manipular límites electorales para obtener ventaja partidista. Las pruebas legales que realmente aplican en Canadá son distintas: si los límites proporcionan "representación efectiva" bajo el artículo 3 de la <em>Carta de Derechos y Libertades</em> (el estándar constitucional que la Corte Suprema de Canadá fijó en el <em>Saskatchewan Reference</em> de 1991), y si la comisión siguió las reglas de la <em>Electoral Boundaries Commission Act</em> (Ley de la Comisión de Límites Electorales) de Alberta. Los hallazgos de la auditoría son evidencia pertinente a esas preguntas legales. No son prueba de un agravio definido legalmente, y este informe no los describe en esos términos.',
			intro_p1: 'La pregunta más limpia que se le puede hacer a cualquier mapa electoral es esta: si el voto de la provincia se dividiera exactamente en partes iguales entre los dos partidos principales, ¿qué conteo de escaños produciría el mapa? Esto mantiene constante al electorado y le pregunta al mapa, por sí solo, qué hace.',
			intro_p2: 'Para responderla, la auditoría generó 1,010,000 mapas de Alberta simulados por computadora y matemáticamente neutrales. La simulación usó los shapefiles oficiales de Elections Alberta y se atuvo exactamente a las mismas reglas estatutarias y límites geográficos que usó la comisión. Los dos mapas de la comisión de 2026 se colocaron luego en esa distribución para ver qué tan normales son. La simulación corrió cuatro cadenas independientes de 252,500 pasos cada una, con la semilla base extraída de la baliza drand de Cloudflare y preregistrada en OSF antes de la ejecución.',
			howmcmc_label: 'CÓMO FUNCIONA LA SIMULACIÓN',
			howmcmc_mcmc: '<strong>MCMC (Markov Chain Monte Carlo)</strong> es un método para explorar un espacio grande — aquí, el espacio de todos los mapas legales de Alberta — dando pasos aleatorios desde un punto de partida. Cada paso propone un pequeño intercambio entre distritos adyacentes; si el resultado se mantiene dentro de las reglas estatutarias, se convierte en el nuevo punto de partida. Tras suficientes pasos, los mapas visitados forman una muestra representativa de los planes legales. La simulación se siembra desde la baliza pública de aleatoriedad drand de Cloudflare para impedir cualquier selección interesada de las condiciones iniciales.',
			howmcmc_recom: '<strong>ReCom (Redistricting Compiler)</strong> es el algoritmo específico usado aquí. Cada paso fusiona dos distritos adyacentes en una sola región y la vuelve a dividir aleatoriamente en dos nuevos distritos válidos, preservando la contigüidad y el equilibrio poblacional por construcción — de modo que el algoritmo nunca necesita rechazar una propuesta inválida.',
			prereg_label: 'PREREGISTRO',
			prereg_body: 'Preregistrar significa dejar por escrito las pruebas exactas, los umbrales y las direcciones predichas antes de mirar cualquier dato, y fijar esos compromisos en un registro público con sello de tiempo. El Open Science Framework (OSF) es el repositorio público donde están archivados los compromisos de esta auditoría. Esto impide el ajuste retroactivo: si un resultado no emerge limpiamente, el umbral no puede cambiarse después y presentarse como si siempre hubiera sido la prueba. Las cinco pruebas estructurales y las cuatro métricas de equidad partidista de esta auditoría se registraron en OSF antes de ejecutar simulación alguna.',
			neutral_p: 'En Alberta, la respuesta neutral no es 50/50. <em>A lo largo de 1,010,000 mapas legales de Alberta simulados por computadora, el mapa mediano le da al UCP solo el 44.8% de los escaños con votos al 50/50</em> — un mapa típico de Alberta bajo votos neutrales le entrega al NDP una pequeña mayoría de escaños. Esto es contraintuitivo pero mecánico: los votantes rurales del UCP ganan sus distritos por márgenes de 60-40 (desperdiciando muchos votos UCP "sobrantes"), mientras que los votantes urbanos del NDP ganan los suyos por márgenes más ajustados de 51-49 (desperdiciando menos votos NDP por victoria). En neutralidad, el NDP sale adelante en eficiencia de escaños.',
			full_dist: 'La distribución completa de la simulación canónica de 1,010,000 mapas:',
			t1_col_a: 'Dónde se sitúa el mapa',
			t1_col_b: 'Escaños UCP con votos al 50/50',
			t1_r1_a: 'Mapa mediano de Alberta',
			t1_r1_b: '44.8% — ligera mayoría de escaños NDP',
			t1_r2_a: 'Mapa en el percentil 95',
			t1_r2_b: '47.1%',
			t1_r3_a: 'Mapa en el percentil 99',
			t1_r3_b: '48.4%',
			t1_r4_a: '<strong>Máximo entre 1,010,000 mapas</strong>',
			t1_r4_b: '<strong>por debajo de 51.7% (menos de 100 planes alcanzan este valor)</strong>',
			seat_count_note: 'Una nota sobre los conteos de escaños. Los mapas de la comisión de 2026 tienen <strong>89</strong> distritos cada uno; la simulación por computadora de la auditoría corre sobre el mapa de 2019 de <strong>87</strong> distritos (su sustrato inicial); el comité Lunty de noviembre producirá <strong>91</strong>. Todos los porcentajes son <em>proporciones</em> de escaños, comparables entre estos denominadores. La simulación usa el mapa de 2019 como punto de partida porque el algoritmo ReCom necesita un mapa legalmente promulgado desde el cual proponer intercambios — el mapa de 2019 es el último mapa electoral promulgado de Alberta. Usar cualquiera de las dos propuestas de la comisión como sustrato sería circular: estaríamos midiendo si un mapa es extremo comparado con mapas derivados de sí mismo.',
			pattern_intro: 'Los resultados — al colocar los tres mapas reales en esta distribución — apuntan a un patrón de trazado de límites específico y quirúrgico.',
			sub1_h: 'Las cuatro medidas estadísticas se activan simultáneamente',
			sub1_p: 'Cuando se usan los shapefiles oficiales de Elections Alberta, el mapa minoritario es un valor atípico estadístico en cada métrica de equidad partidista — no solo en la del punto de inflexión.',
			t2_col_a: 'Mapa',
			t2_col_b: 'Brecha de eficiencia',
			t2_col_c: 'Media-mediana',
			t2_col_d: '<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener" title="La declinación mide la diferencia angular entre la curva escaños-votos de cada partido. Los valores negativos favorecen al UCP; los positivos favorecen al NDP.">Declinación</a>',
			t2_col_e: 'Escaños al 50/50',
			t2_r1_a: 'Mayoritario 2026',
			t2_r1_b: '+0.04% (p15.5)',
			t2_r1_c: '−3.6% (p2)',
			t2_r1_d: '+0.027 (p81)',
			t2_r1_e: '46.1% (p78)',
			t2_r2_a: 'Minoritario 2026',
			t2_r2_b: '<strong>+3.96% (p94.4)</strong>',
			t2_r2_c: '<strong>+1.0% (p99.98)</strong>',
			t2_r2_d: '<strong>−0.077 (p1.2)</strong>',
			t2_r2_e: '<strong>51.7% (p99.99)</strong>',
			sub1_close: 'El mapa mayoritario se sitúa cómodamente dentro del rango normal en tres de las cuatro métricas. Su media-mediana se sitúa en p2 en la dirección favorable al NDP — un resultado inusual pero que apunta en el sentido equivocado para ayudar al UCP. La estrecha adhesión del mapa mayoritario a los límites municipales coloca los núcleos urbanos con fuerte voto NDP en sus propios distritos compactos, donde los votos NDP ganan por márgenes eficientes mientras que las victorias rurales del UCP tienden a ser por márgenes mayores; esa leve ventaja estructural de eficiencia del NDP es lo que aparece en la medida media-mediana. El mapa minoritario está en la cola en las cuatro, cada una apuntando en la misma dirección partidista.',
			sub2_h: 'El punto de inflexión al 50/50: menos de 100 de 1,010,000 mapas neutrales lo alcanzan',
			sub2_p: 'La métrica del punto de inflexión presentada arriba — escaños UCP con un voto provincial de 50/50 — es la manera más intuitiva de comparar los tres mapas.',
			t3_col_a: 'Mapa',
			t3_col_b: 'Escaños UCP con votos al 50/50',
			t3_col_c: 'Dónde se sitúa',
			t3_r1_a: 'Promulgado 2019',
			t3_r1_b: '46.0%',
			t3_r1_c: 'Percentil 78 — dentro del rango normal',
			t3_r2_a: '<strong>Mayoritario 2026</strong>',
			t3_r2_b: '<strong>46.1%</strong>',
			t3_r2_c: '<strong>Percentil 78 — bien dentro de los límites</strong>',
			t3_r3_a: '<strong>Minoritario 2026</strong>',
			t3_r3_b: '<strong>51.7% (46 escaños)</strong>',
			t3_r3_c: '<strong>Percentil 99.99 — menos de 100 de 1,010,000 extracciones neutrales lo alcanzan</strong>',
			sub2_close: 'Menos de 100 de 1,010,000 mapas neutrales de Alberta simulados por computadora produjeron un valor de <code>seats@50/50</code> tan alto como el de la propuesta minoritaria. Con base en patrones de voto recientes reales, le otorgaría al UCP 60 escaños (frente a 55 en la propuesta mayoritaria). La propuesta mayoritaria es el tipo de mapa que un procedimiento neutral genera de forma rutinaria. La propuesta minoritaria es el tipo de mapa que hay que proponerse dibujar específicamente.',
			sub3_h: 'Qué significa esto en lenguaje llano',
			sub3_p: 'Los shapefiles oficiales revelan un mapa estadísticamente extremo en la misma dirección partidista en tres de las cuatro medidas a la vez. Los dos canales de análisis de equidad partidista comparten datos subyacentes comunes de brecha de eficiencia y no son estadísticamente independientes; combinarlos bajo el método de Fisher sobreestimaría la significancia conjunta. La cota superior conjunta robusta a la dependencia es de aproximadamente uno en 350.000 (Bonferroni; p&nbsp;≤&nbsp;2,80×10<sup>−6</sup>). Los canales de equidad partidista se clasifican como "exploratorios" en el sentido del §4.3.1 de la auditoría: documentados en el repositorio, pero no preregistrados antes de los datos.',
			details_summary: 'Qué significa este valor p — y qué no',
			details_p1: 'Un valor p responde una sola pregunta: si el mapa hubiera sido trazado por un proceso neutral, ¿con qué frecuencia veríamos un resultado así de extremo o más? Con la cota robusta a la dependencia p&nbsp;≤&nbsp;2,80×10<sup>−6</sup>, la respuesta es como máximo aproximadamente una vez en 350.000 intentos.',
			details_p2: 'Esta es una prueba de hipótesis frecuentista, no una medición de intención. No dice que la comisión tuviera la intención de hacer un gerrymander, y no cuantifica qué tan injusto es el mapa en términos prácticos. Dice que el patrón de los límites es estadísticamente inconsistente con un proceso de trazado neutral — la misma conclusión a la que llegaría una auditoría aleatorizada sin importar quién trazó el mapa ni por qué. La distribución de referencia es de 1.010.000 mapas neutrales generados por el algoritmo ReCom, que no impone todos los criterios estatutarios bajo los que trabajó la comisión (niveles del art. 15(2) y restricciones de comunidades de interés) — lo que lo convierte en una sólida verificación externa, no en una prueba de que ningún mapa legalmente conforme de Alberta pudiera alcanzar este número de escaños.',
			details_p3: 'La batería de pruebas estructurales — población, divisiones, anclaje, compacidad, firmas — fue registrada con marcas de tiempo antes de la recomputación canónica (<a href="https://osf.io/w2s8k" rel="noopener">registro OSF w2s8k</a>). Los canales de equidad partidista (Mahalanobis conjunto, SZAT, combinación Bonferroni) se clasifican como "exploratorios" en el sentido del §4.3.1 de la auditoría: documentados en el repositorio, pero no preregistrados antes de los datos.',
			szat_label: 'PRUEBA DE ASIGNACIÓN DE ZONAS OSCILANTES (SZAT)',
			szat_body: 'La SZAT (Swing-Zone Allocation Test) es la segunda prueba independiente de la auditoría, y hace una pregunta distinta a la de la simulación: no "¿es este mapa extremo en general?" sino "¿son partidistamente neutrales las decisiones específicas de las líneas?". Funciona aislando solo las Áreas de Votación donde el mapa de la minoría difiere del de la mayoría — los retrazados en disputa — y probando si esas decisiones particulares, tomadas en conjunto, desplazan la eficiencia del voto en la dirección de un partido. Como compara solo los puntos de divergencia, controla automáticamente todo lo que los dos mapas comparten: la misma geografía, las mismas metas de población y las mismas reglas estatutarias. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Detalles técnicos y resultados bootstrap →</a>',
			two_q: '<strong>Dos preguntas, una respuesta.</strong> La simulación de 1,010,000 mapas pregunta: <em>¿es este mapa extremo comparado con mapas neutrales trazados sobre la misma geografía de Alberta?</em> Una segunda prueba aparte — llamada la <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/szat_summary.json" rel="noopener">Prueba de Asignación de Zonas Oscilantes</a> — hace una pregunta distinta: <em>¿son partidistamente neutrales las líneas específicas del mapa?</em> Funciona mirando solo las Áreas de Votación donde la minoría trazó distinto a la mayoría y preguntando si esas decisiones particulares, tomadas en conjunto, desplazaron la eficiencia del voto en la dirección de un partido. Como compara solo los lugares donde los dos mapas difieren, controla automáticamente todo lo que comparten — la misma geografía provincial, las mismas metas de población, las mismas reglas estatutarias. Ambas preguntas devuelven la misma respuesta. Por eso la cifra de uno en 350.000 es un resultado combinado y no una prueba única: son dos líneas de evidencia independientes que convergen.',
			super_lead: 'Esto explica por qué la propuesta minoritaria se sitúa en el régimen donde una supermayoría del UCP se vuelve estadísticamente alcanzable en la geografía de Alberta de 2023 — pero el nulo del conjunto no impone todos los criterios estatutarios bajo los que trabajó la comisión, lo que lo convierte en una sólida verificación externa, no en una prueba de que ningún mapa legalmente conforme de Alberta pudiera alcanzar este número de escaños.',
			super_label: 'POR QUÉ IMPORTA UNA SUPERMAYORÍA',
			super_body: 'Bajo el sistema parlamentario de Westminster de Canadá, una mayoría simple (45 escaños) basta para aprobar leyes y presupuestos de rutina. Una supermayoría de dos tercios (60 escaños) hace más. Le permite al partido gobernante invocar la "clausura" para cerrar el debate, reescribir las reglas de procedimiento sin el consentimiento de la oposición y controlar la composición de cada comité legislativo. También aísla al gobierno de la disidencia interna: incluso con media docena de diputados cruzando al otro lado, el gobierno conserva una mayoría operativa. Una mayoría simple le permite conducir el auto; una supermayoría de 60 escaños le permite reescribir las leyes de tránsito.',
			super_close: 'Al diluir estratégicamente a los votantes urbanos en los distritos circundantes del borde rural (el patrón de "hibridación urbana" identificado en la Vía 2), la propuesta minoritaria fabrica exactamente el cortafuegos estructural necesario para asegurar esos 60 escaños. El hallazgo estructural de la Vía 2 y el hallazgo estadístico de la Vía 1 convergen en la misma propuesta, la misma dirección y las mismas comunidades.',
			sub4_h: 'Confirmación desde la prueba de procedimiento dirigido',
			sub4_p: 'Para asegurarse de que esto no sea una peculiaridad de la conocida preferencia por la compacidad de la simulación neutral, la auditoría ejecutó un procedimiento dirigido de ascenso de colinas (<a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">Cannon et al. 2022 — citado y descrito en el informe técnico</a>) en ambas direcciones: maximizando escaños UCP y maximizando escaños NDP. El mismo número de pasos (40,000) en cada dirección, las mismas restricciones estatutarias, la misma geometría provincial.',
			t4_col_a: 'Procedimiento',
			t4_col_b: 'Valor más extremo alcanzado',
			t4_col_c: 'Qué nos dice',
			t4_r1_a: 'MCMC neutral, máximo producido',
			t4_r1_b: 'por debajo de 51.7% de escaños UCP @ 50/50',
			t4_r1_c: 'El techo natural bajo trazado neutral',
			t4_r2_a: 'MCMC neutral, mínimo producido',
			t4_r2_b: '~39% de escaños UCP @ 50/50',
			t4_r2_c: 'El piso natural bajo trazado neutral',
			t4_r3_a: 'Ascenso de colinas dirigido, maximizando al UCP',
			t4_r3_b: '<strong>52.9%</strong>',
			t4_r3_c: 'Lo que puede alcanzar un procedimiento que busca deliberadamente la ventaja del UCP',
			t4_r4_a: 'Ascenso de colinas dirigido, maximizando al NDP',
			t4_r4_b: '<strong>37.9%</strong>',
			t4_r4_c: 'Lo que puede alcanzar un procedimiento que busca deliberadamente la ventaja del NDP (por debajo del piso neutral)',
			sub4_close: 'El 51.7% del mapa minoritario se sitúa más cerca del techo dirigido pro-UCP (52.9%) que de la mediana neutral (44.8%). El 46.1% del mapa mayoritario se sitúa en la mediana neutral. Tanto el mapa promulgado en 2019 como el mayoritario de 2026 caen cómodamente dentro de lo que el procedimiento neutral produce de forma rutinaria — distintas proporciones de voto, la misma zona de resultados sin nada de particular. El mayoritario continúa la práctica albertana de 2019 en el eje de equidad partidista de la misma manera que continúa la práctica de 2019 en anclaje municipal (80.0% frente al 75.2% de 2019). Dos mapas trazados bajo las mismas reglas de Alberta, por los mismos cinco comisionados, en la misma sala: uno aterriza donde los procedimientos neutrales producen rutinariamente, el otro aterriza donde hay que apuntar específicamente para aterrizar.',
			sub4_quote: '<em>Esta</em> es la forma del hallazgo, y es también el encuadre que un tribunal aplicaría en la práctica.',
			sub5_h: 'Descartando explicaciones alternativas',
			sub5_p: 'Ante un valor atípico estadístico de esta magnitud, una auditoría rigurosa debe descartar explicaciones inocentes antes de atribuir estos patrones a un diseño deliberado. Los datos estructurales (Vía 2) desmontan sistemáticamente las defensas alternativas habituales:',
			defense1: '<strong>La defensa de la "geografía política natural":</strong> <em>("Los votantes urbanos están naturalmente empaquetados; el mapa solo refleja la geografía de Alberta.")</em> Las 1,010,000 simulaciones ya toman en cuenta la geografía natural de Alberta. La simulación demuestra: aunque la geografía le da al UCP una ventaja de eficiencia de base, esta se topa naturalmente con un techo alrededor del percentil 83 al 90. El mapa minoritario se sitúa en el percentil 99.99 — un valor atípico extremo <em>incluso comparado con la línea de base naturalmente sesgada de Alberta</em>.',
			defense2: '<strong>La defensa de las "comunidades de interés":</strong> <em>("Las formas extrañas se trazaron para mantener juntas a comunidades específicas.")</em> Si usted intenta mantener juntas a las comunidades, sigue los límites municipales. El mapa mayoritario siguió los límites de ciudad existentes el 80% del tiempo. El minoritario los siguió el 72% del tiempo — ambos dentro de la norma canadiense de 70–85%. Lo que el mapa minoritario sí hace es dividir activamente la ciudad unificada de Airdrie en cuatro piezas separadas, y colocar tres de sus decisiones de límites precisamente en las zonas del borde urbano que el presidente de la comisión señaló como geométricamente anómalas — decisiones que la lógica de comunidad de interés no explica.',
			defense3: '<strong>La defensa de la "igualdad poblacional":</strong> <em>("Tuvieron que trazar límites raros para asegurar que cada distrito tuviera exactamente la misma población.")</em> El mapa minoritario es en realidad mucho <em>peor</em> en igualdad poblacional. Su desviación media absoluta (MAD) de población fue 4,707 — 48% más amplia que la del mapa mayoritario (3,180) — situándolo en el percentil 99 del conjunto canónico (solo 1 de cada 100 mapas neutrales produce una dispersión peor). Sacrificó la igualdad poblacional para lograr su forma.',
			defense4: '<strong>La defensa de la "incompetencia o mala suerte":</strong> <em>("Solo trazaron un mapa descuidado y tuvieron mala suerte con los números.")</em> Acertar exactamente 60 escaños para una supermayoría mientras además se divide Airdrie en cuatro piezas y se colocan tres límites en las zonas exactas que el propio presidente de la comisión señaló como anómalas requiere precisión quirúrgica. La cota superior conjunta robusta a la dependencia sobre la probabilidad de trazar accidentalmente un mapa así de extremo en ambos canales analíticos bajo la distribución de referencia neutral de ReCom es de aproximadamente <strong>1 en 350.000</strong> (p&nbsp;≤&nbsp;2,80×10<sup>−6</sup>). La formulación anterior de "1 en 15 millones" asumía independencia de canales que los dos canales no tienen. No se llega al percentil 99.99 por torpeza.',
			sub5_close: 'Lo que muestran los datos es que la propuesta minoritaria empeoró tanto la paridad poblacional como la coherencia comunitaria en relación con lo que los mismos cinco comisionados produjeron simultáneamente bajo reglas estatutarias idénticas. La auditoría no determina qué pretendían los comisionados de la minoría — la geometría de los límites no puede revelar la intención — pero la desviación estructural tanto del conjunto neutral como del producto de la propuesta mayoritaria se sostiene con independencia de la intención.',
			sub6_h: 'Una nota sobre la validación cruzada en R',
			sub6_p1: 'Una versión anterior de esta auditoría (que usaba shapefiles aproximados en lugar de oficiales) validó de forma cruzada el conjunto ReCom de Python contra el muestreador Sequential Monte Carlo del paquete <code>redist</code> de R. La verificación cruzada produjo resultados inestables: en tres corridas con la misma semilla nominal, la fracción de planes que alcanzaba el antiguo valor minoritario (48.3% en la geometría aproximada) fue 5.6%, luego 28%, luego 58% — una falla de convergencia del muestreador, no un descubrimiento. El informe completo está en <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>.',
			sub6_p2: 'Con los shapefiles oficiales de Elections Alberta, el <code>seats@50/50</code> del mapa minoritario sube a 51.7% — un valor que menos de 100 de 1,010,000 planes neutrales alcanzan. La pregunta de la validación cruzada en R se vuelve irrelevante: cero planes de cualquiera de los dos muestreadores alcanzan el valor canónico con tamaños de muestra comparables.',
			sub6_asymm: '<strong>La asimetría alrededor del 50/50 es más reveladora que la inversión en sí.</strong> Un barrido de precisión de la curva escaños-votos con resolución de 0.01 puntos porcentuales encuentra que el mapa minoritario mantiene al UCP en o por encima del umbral de mayoría legislativa de 45 escaños hasta una proporción de voto provincial del UCP de alrededor de <strong>49.7%</strong>. Esto es técnicamente una inversión voto-escaño — el UCP formaría gobierno con el mapa minoritario aun perdiendo el voto popular por 0.3 puntos porcentuales — pero 0.3 puntos está bien dentro del ruido ordinario de las encuestas, así que por sí solo no es un hallazgo dramático. Lo que <em>sí</em> es dramático es el contraste: con el mapa <strong>mayoritario</strong>, el UCP necesitaría <em>ganar</em> el voto popular por unos 4 puntos porcentuales para alcanzar el mismo umbral de 45 escaños. Ambos mapas enfrentan la misma geografía de Alberta y las mismas reglas estatutarias; la brecha entre ellos — 0.3pp frente a +4pp — es diferencia estructural, no ruido.',
			sub6_close: 'Este es el hallazgo de sesgo estructural que la auditoría sostiene con confianza. Es solo geometría; no depende de ningún resultado electoral; no se mueve cuando se mueven las encuestas.',
			sub6_caveat: '<strong>Una salvedad que la auditoría se toma en serio.</strong> Un electorado real no es un 50/50 uniforme. Los votantes pueden arrasar la inclinación estructural de cualquier mapa con suficiente oscilación — un electorado particularmente molesto o inspirado inclinará el resultado sin importar cómo estén trazados los límites. La prueba del 50/50 aísla <em>la contribución del mapa al resultado</em>, no el resultado en sí. Lo que muestra es lo que hace el mapa cuando el electorado no decide por él.',
			sub7_h: 'La conclusión de fondo',
			sub7_p1: 'El hallazgo central de la auditoría es geométrico. <strong>La Vía 2 — el tablero de irregularidades estructurales — es el fundamento; la Vía 1 es la prueba de que la geometría está haciendo trabajo partidista.</strong>',
			sub7_p2: 'El gráfico siguiente pone ambas vías en una sola imagen. El eje horizontal es la Vía 1 (la brecha de eficiencia de equidad partidista, donde más a la derecha significa más favorable al UCP); el eje vertical es la Vía 2 (el número de pruebas de equidad estructural que la propuesta reprueba, de cinco, donde más alto significa más problemas estructurales).',
			stakes_fig_alt: 'Gráfico de dispersión con la brecha de eficiencia en el eje horizontal y el número de pruebas estructurales reprobadas en el eje vertical. El mapa promulgado en 2019 y el mapa mayoritario de 2026 se agrupan en la esquina segura, abajo a la izquierda. El mapa minoritario de 2026 aparece en la región de valores atípicos, arriba a la derecha.',
			stakes_fig_caption: 'Las dos maneras de medir las dos propuestas de la comisión, graficadas juntas. De izquierda a derecha: qué tan sesgada se ve la propuesta en la cifra de equidad partidista — cuanto más a la derecha, más favorece al UCP. De abajo hacia arriba: cuántas de las cinco pruebas de equidad estructural reprueba la propuesta — cuanto más alto, peor. El mapa promulgado en 2019 está en la esquina segura: bajo en ambas. La propuesta mayoritaria de 2026 se mantiene plana en cero problemas estructurales y un sesgo partidista casi nulo (+0.1%). La propuesta minoritaria de 2026 es un valor atípico estructural en cada prueba que distingue a los dos mapas (4 de 5; la quinta, el anclaje, es neutral para ambos); su brecha de eficiencia (+4.0%) se sitúa justo debajo de la línea de umbral de Alberta.',
			stakes_table_intro: 'Los mismos hallazgos en forma de resumen llano, encabezados por el hallazgo estructural porque la evidencia validada de forma cruzada lo respalda con más fuerza:',
			t5_col_b: 'Vía 2: Estructura (solo geometría, sin votos)',
			t5_col_c: 'Vía 1: Números (dependiente de los votos)',
			t5_r1_a: '<strong>Mayoritario 2026</strong>',
			t5_r1_b: 'limpio — no cruza <em>ningún</em> umbral estructural',
			t5_r1_c: 'dentro del rango normal en cada métrica (<code>seats@50/50</code> 46.1% — p78; brecha de eficiencia +0.04%)',
			t5_r2_a: '<strong>Minoritario 2026</strong>',
			t5_r2_b: '<strong>cruza 4 de 5 umbrales estructurales</strong> por un margen amplio (anclaje neutral — ambos mapas dentro de la norma canadiense)',
			t5_r2_c: 'posición en la cola en tres de las cuatro medidas de equidad partidista — <code>seats@50/50</code> 51.7% (p99.99, aproximadamente 66 de 1,010,000 lo alcanzan); brecha de eficiencia +3.96% (p94.4, cerca pero bajo el umbral); cota conjunta robusta a la dependencia p&nbsp;≤&nbsp;2,80×10<sup>−6</sup> (≈ 1 en 350.000)',
			details2_summary: 'Por qué la Vía 2 sostiene el caso — detalle técnico',
			details2_p: 'La auditoría preregistró cinco pruebas de irregularidad estructural el 24 de abril de 2026, antes de que se compilaran los resultados finales de la simulación. El anclaje es neutral para ambos mapas; en las cuatro pruebas restantes la minoría cruza todas y la mayoría no cruza ninguna. Esas mediciones son geométricas — no dependen de ningún muestreador estadístico ni de ninguna atribución de votos. La Vía 1 (los números de equidad partidista) corrobora con fuerza a la Vía 2 bajo los shapefiles oficiales canónicos: la minoría es un valor atípico estadístico en las medidas de equidad partidista, bajo una cota superior conjunta robusta a la dependencia de p&nbsp;≤&nbsp;2,80×10<sup>−6</sup> (≈ 1 en 350.000; reemplaza una cifra combinada de Fisher anterior que sobreestimaba la significancia conjunta al tratar dos canales con datos comunes como independientes; OSF <a href="https://osf.io/6pt83" rel="noopener">6pt83</a>). La pregunta de si la geometría inusual de la Vía 2 es el <em>mecanismo</em> específico detrás de los números de la Vía 1 fue puesta a prueba y la respuesta es no — vea <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/redist_python_comparison.md" rel="noopener">findings/redist_python_comparison.md</a>. La Prueba de Asignación de Zonas Oscilantes muestra que las decisiones de límites en disputa están sesgadas partidistamente, pero la pregunta probada era si las formas de los límites en sí — el corredor de lazo, la extensión hacia el parque — son la causa directa del vuelco de escaños; no lo son. El efecto en los escaños proviene de cómo las reasignaciones de Áreas de Votación retrazadas desplazan la eficiencia del voto entre distritos, no de las formas en sí. Ambas vías señalan el mapa minoritario; llegan a él por instrumentos independientes. La Vía 2 es el hallazgo central. La Vía 1 corrobora sin cargar el peso.'
		},
		impact: {
			heading: '5: Efectos sobre la representación',
			lanes_label: 'VÍA 1 Y VÍA 2',
			lanes_body: '<strong>La Vía 1 (números)</strong> usa resultados electorales para probar si el mapa convierte votos en escaños de manera justa — pregunta cómo se desempeña el mapa bajo distintas divisiones del voto. <strong>La Vía 2 (estructura)</strong> examina solo las líneas trazadas — divisiones de ciudades, dispersión poblacional, formas de los límites — sin dato electoral alguno. Cada vía es independiente: un mapa puede reprobar una y aprobar la otra. La propuesta minoritaria reprueba ambas; la mayoritaria aprueba ambas.',
			intro: 'La Vía 1 depende de contra qué resultados electorales se califiquen los mapas. La Vía 2 no. La evidencia estructural está en los mapas mismos — líneas trazadas, ciudades divididas, dónde los límites siguen o no las líneas administrativas que existen por otras razones. En estas pruebas, los dos mapas no están ni cerca.',
			fig_alt: 'Gráfico de barras que compara cinco pruebas de equidad estructural lado a lado. Las barras del mapa mayoritario se sitúan en cero o bien dentro de los rangos seguros. Las barras del mapa minoritario cruzan el umbral en cuatro de las cinco pruebas por un margen amplio; la quinta (el anclaje) es neutral para ambos mapas.',
			fig_caption: 'Las cinco pruebas de equidad estructural, lado a lado. Las barras verde azulado son el mapa mayoritario; las barras moradas son el minoritario. La línea discontinua en cada fila marca el umbral de reprobación. Las barras de la minoría cruzan el umbral en cuatro de las cinco pruebas por un margen amplio; la quinta (el anclaje) es neutral para ambos mapas. Las barras de la mayoría se mantienen planas en cero o bien dentro del rango seguro.',
			table_intro: 'Las mismas cinco pruebas en forma de tabla, con el umbral de cada prueba indicado junto al resultado. La fila inferior es el <em>resumen</em> de la auditoría — el número de pruebas que cada mapa reprueba de las cinco.',
			table_col_test: 'Prueba',
			table_col_majority: 'Mapa mayoritario',
			table_col_minority: 'Mapa minoritario',
			table_col_direction: 'Dirección / Beneficiario',
			table_r1_a: 'El borde sigue las líneas municipales existentes (norma canadiense de 70–85%)',
			table_r1_b: '80% — dentro de la norma',
			table_r1_c: '72% — dentro de la norma',
			table_r1_d: 'N/A — ambos dentro de la norma canadiense',
			table_r2_a: 'Dispersión poblacional (más ajustada es mejor)',
			table_r2_b: '3,180',
			table_r2_c: '4,707 — 48% más amplia',
			table_r2_d: 'Estructural (Reduce la igualdad del voto)',
			table_r3_a: 'Exceso de población del NO de Calgary sobre el promedio',
			table_r3_b: '2.8%',
			table_r3_c: '11.5%',
			table_r3_d: '<strong>UCP</strong> (Empaqueta votos urbanos del NDP)',
			table_r4_a: 'Límites señalados por el propio presidente de la comisión',
			table_r4_b: '0',
			table_r4_c: '3',
			table_r4_d: 'N/A',
			table_r5_a: 'División de Airdrie (mínimo por restricción: 2)',
			table_r5_b: '2 piezas',
			table_r5_c: '4 piezas',
			table_r5_d: '<strong>UCP</strong> (Fragmenta el poder urbano/suburbano)',
			table_r6_a: '<strong>Resumen preregistrado</strong> (&ge; 4 de 5 = valor atípico)',
			table_r6_b: '<strong>0 de 5 activadas</strong>',
			table_r6_c: '<strong>4 de 5 activadas</strong> (prueba de anclaje neutral — ambos mapas dentro de la norma canadiense; las 4 pruebas restantes se activan todas)',
			table_r6_d: '<strong>UCP</strong>',
			rationales_p: 'Un hallazgo aparte, aplicado solo a la minoría: <strong>cinco de las seis justificaciones publicadas por los comisionados de la minoría fallan bajo verificación independiente</strong>. La prueba se ejecuta solo contra la minoría porque la mayoría no publicó una lista de justificaciones de los retrazados en disputa — la auditoría no puede aplicarla simétricamente, y se reporta aquí como una sola señal en lugar de filas adicionales en el conteo de irregularidades estructurales. (Un séptimo retrazado que la auditoría había listado previamente resultó apoyarse en una afirmación sobre límites federales imposible de rastrear en el informe minoritario; se ha eliminado en lugar de dejarlo como una afirmación débil.)',
			chair_appendix_p: 'La auditoría también puso a prueba la afirmación general y separada del presidente en el Apéndice C de que las siete configuraciones híbridas en disputa de la minoría <strong>no tenían respaldo público</strong> en las más de 1,140 presentaciones públicas. Una búsqueda por palabras clave en el archivo completo de presentaciones (94% procesado por máquina, 6% solo imagen y excluido; metodología y evidencia por configuración en <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/findings/submission_search_findings.md" rel="noopener">findings/submission_search_findings.md</a>) devolvió un panorama más matizado que la afirmación general del presidente o su rechazo general: el presidente tenía razón en tres de siete (la división en cuatro de Airdrie, el híbrido Calgary–Nolan-Hill–Cochrane y la alternativa minoritaria de St. Albert carecen cada uno de respaldo documentado), se equivocó en tres de siete (Rocky Mountain House–Banff Park recibió una propuesta explícita y detallada de al menos una presentación de la zona de Clearwater más varias alineadas; Olds–Three-Hills–Didsbury fue apoyada por escrito por residentes de Beiseker; Chestermere recibió múltiples presentaciones que se oponían a una fusión con Calgary que se alinean materialmente con la intención de la minoría), y se equivocó parcialmente en una (los híbridos de Red Deer recibieron una propuesta híbrida peri-Red-Deer de un concejal en funciones de Red Deer, con alineación direccional pero no exacta en configuración). El barrido de "sin respaldo público" del Apéndice C del presidente es por lo tanto demostrablemente excesivo — tres de siete son demostrablemente falsas — pero no está inventado de la nada, ya que tres de siete sí se sostienen. <strong>Este hallazgo va en contra del presidente, no en contra de la minoría.</strong>',
			summary_p: '<strong>En la Vía 2, la mayoría cruza cero umbrales estructurales. La minoría cruza todos y cada uno por un margen amplio.</strong> El conteo es un recuento bruto y no una probabilidad familiar calibrada — su peso proviene de la unanimidad direccional (cada prueba activada apunta en el mismo sentido), no de un cálculo de distribución nula conjunta. La vía estadística (§3) aporta la probabilidad conjunta a través de un instrumento distinto.'
		},
		cpd: {
			heading: '4: Fragmentación, empaquetamiento y drenaje',
			vocab_label: 'Tres jugadas, un mismo manual',
			vocab_packing: '<strong>Empaquetar</strong> significa apiñar a los votantes de un partido en distritos que ese partido gana por aplastamiento — cada boleta empaquetada sigue contando, pero no aporta nada más allá de la victoria. Victorias grandes y desproporcionadas. Votos desperdiciados.',
			vocab_cracking: '<strong>Fragmentar</strong> significa dividir una comunidad entre múltiples distritos de modo que no gane ninguno por sí sola. Una ciudad con fuerza para llevarse dos escaños queda tallada en cuatro, cada uno amarrado a una zona rural distinta. Votos diluidos. Ningún escaño para nadie.',
			vocab_draining: '<strong>Drenar</strong> es el acompañante espacial: los distritos empaquetados y fragmentados se colocan uno junto al otro de modo que los simpatizantes sobreconcentrados de un lado "drenan" el poder de voto de los distritos en disputa cercanos. El patrón de adyacencia amplifica ambos efectos — el empaquetamiento y la fragmentación se refuerzan mutuamente a través de las líneas de distrito.',
			vocab_disclaimer: 'Las tres pueden ocurrir sin ninguna intención partidista explícita. Lo que la auditoría mide es si el patrón — y su magnitud estadística — es consistente con lo que produce un proceso neutral de trazado de mapas. <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md#5-results" rel="noopener">Metodología completa en el §5 del informe técnico.</a>',
			fig_alt: 'Mapa que muestra la división de Airdrie en cuatro distritos separados bajo el mapa minoritario',
			fig_caption: 'La división de Airdrie en cuatro distritos separados bajo el mapa minoritario, diluyendo su poder de voto urbano.',
			intro: 'Los cinco comisionados trabajaron con las mismas reglas estatutarias, la misma geografía provincial, el mismo archivo de 1,140 presentaciones públicas y los mismos datos demográficos. Sus dos borradores rivales coinciden en la mayor parte de Alberta. Donde los borradores divergen, divergen en decisiones que alguien en la sala tuvo que tomar. Tres de esas decisiones vale la pena verlas como decisiones, no como números.',
			airdrie_p: '<strong>Divide la Ciudad de Airdrie en cuatro piezas.</strong> La ley limita cada división electoral a una vez y cuarto el promedio provincial, así que Airdrie necesita al menos dos divisiones. El mapa mayoritario le da dos. El minoritario le da cuatro — el norte hacia Calgary-Nolan Hill-Cochrane, el este hacia Airdrie East, el oeste hacia Calgary-Foothills-Airdrie West, y el centro-sur hacia Calgary-Airdrie — cada una engrapada a un distrito rural o del borde de Calgary distinto. Una residente de Airdrie con una pregunta para su MLA tiene que saber en qué cuarto de la ciudad vive antes de poder llamar a la oficina correcta. Sus vecinos dos cuadras más allá le darán tres respuestas distintas. La asociación de padres de la escuela de su hijo no puede enviar una sola delegación a un MLA por una cuestión de financiamiento escolar; tiene que coordinar cuatro delegaciones a cuatro oficinas, cada MLA principalmente responsable ante una circunscripción rural o suburbana distinta. La asociación de hockey menor, el banco de alimentos, la Cámara de Comercio — cada organización que opera a escala de toda la ciudad ahora opera a través de cuatro distritos provinciales.',
			airdrie_callout_label: 'POR QUÉ IMPORTA AIRDRIE',
			airdrie_callout_p1: 'Airdrie es la ciudad más grande de Alberta sin un MLA propio. Con 85,805 personas (censo municipal de 2024) es más grande que Red Deer; tiene un solo concejo, una sola factura de impuestos, una sola división escolar — cada sistema cívico la trata como una unidad.',
			airdrie_callout_p2: 'Dividirla entre cuatro divisiones provinciales — Calgary-Airdrie, Calgary-Foothills-Airdrie West, Calgary-Nolan Hill-Cochrane y Airdrie East — cada una identificada principalmente con una jurisdicción circundante distinta, borra a Airdrie del mapa político en el nivel de gobierno que lo traza. La ciudad tiene 85,805 residentes y cero escaños en la Legislatura donde la mayoría de los votantes consideren ese lugar su hogar.',
			airdrie_callout_p3: 'Una división en cuatro es invisible para toda prueba de equidad partidista excepto la que pregunta: ¿puede un votante encontrar a su MLA?',
			airdrie_callout_summary: 'Ambos mapas son legales. La división en cuatro es una decisión.',
			airdrie_btn: 'Mostrar los distritos señalados en el mapa',
			anchoring_p: '<strong>Donde se aparta de las líneas municipales, se aparta en lugares estratégicamente importantes.</strong> Cuando los mapas electorales siguen el borde de una ciudad o pueblo, los votantes reconocen dónde empieza y termina su división — la línea del impuesto predial, la línea de la división escolar, la línea del distrito electoral local y la línea de la elección provincial coinciden. Statistics Canada publica estos límites gratuitamente. Sobre los shapefiles oficiales de Elections Alberta, ambos mapas siguen las líneas municipales a tasas generales comparables: el mayoritario al 80%, el minoritario al 72%, ambos dentro de la norma canadiense de 70–85% (Quebec: 78%, Ontario: 82%, BC: 71%; las comisiones comparadoras están documentadas en la monografía). (El análisis provisional inicial de la auditoría mostraba el anclaje de la minoría en solo 15%; la cifra no sobrevivió la recomputación sobre los shapefiles oficiales — vea la nota de corrección más abajo.) La observación llamativa no es la tasa general sino dónde se concentran las desviaciones de la minoría: los tres límites que el propio presidente de la comisión señaló como anómalos — la extensión de Rocky Mountain House–Banff Park <button class="ed-trigger" data-ed-name="Rocky Mountain House-Banff Park">ver ↗</button> hacia terreno deshabitado de parque nacional, el corredor de lazo de Nolan Hill–Cochrane <button class="ed-trigger" data-ed-name="Calgary-Nolan Hill-Cochrane">ver ↗</button>, y el alcance de Olds–North Airdrie <button class="ed-trigger" data-ed-name="Olds-Three Hills-Didsbury">ver ↗</button> — son cada uno desviaciones de la geografía cívica preexistente en las zonas exactas del borde urbano donde emparejar votantes urbanos y rurales afecta más directamente qué partido gana el escaño.',
			anchoring_followup: 'Los comisionados de la minoría dieron razones para cada uno de los tres límites señalados. Para Rocky Mountain House–Banff Park, citaron el tamaño geográfico, el corredor de la Highway 22 y la proximidad de reservas de Primeras Naciones a Rocky Mountain House; el presidente de la comisión calificó la extensión hacia terreno deshabitado de parque nacional como "un esfuerzo de mala fe" para satisfacer el criterio de superficie, y la frase aparece en el informe final oficial de la comisión. Para Nolan Hill–Cochrane, citaron lazos compartidos de transporte y empleo entre el noroeste de Calgary y Cochrane; los datos de desplazamiento al trabajo de Statistics Canada muestran que solo el 35.8% de los trabajadores de Cochrane viaja a Calgary siquiera, y la mayoría trabaja dentro del propio Cochrane. Para el alcance de Olds–North Airdrie, citaron la continuidad del corredor de la Highway 2; la auditoría encontró que la extensión específica hacia Airdrie falla por motivos de población. La verificación independiente encontró que cinco de las seis subjustificaciones publicadas por la minoría fallan o solo se sostienen parcialmente frente a los datos primarios.',
			packing_p: '<strong>Una zona de Calgary se talla para concentrar a los votantes del NDP en divisiones más grandes que el promedio.</strong> En el cuadrante noroeste de Calgary <button class="ed-trigger" data-ed-name="Calgary-North West-Bearspaw">ver ↗</button>, las divisiones del mapa minoritario promedian 11.5% por encima de la población provincial — frente a 2.8% en el mayoritario. La misma zona geográfica, trazada por la misma comisión bajo las mismas restricciones, produce distritos un cuarto más grandes en un mapa que en el otro. Esto encaja con la firma estructural del <em>empaquetamiento</em>: concentrar a los votantes de un partido en menos distritos y más grandes para que cada una de sus boletas pese menos. El empaquetamiento y la <em>fragmentación</em> (repartir delgadamente a los votantes de un partido entre distritos que pierden por poco) son las dos jugadas clásicas del gerrymandering; ambas reducen el número de escaños de un partido por debajo de su proporción del voto.',
			chair_p: 'El presidente de la comisión — designado bajo la misma Ley, trabajando con las mismas presentaciones — señaló tres límites del mapa minoritario como geográficamente anómalos: la extensión de Rocky Mountain House–Banff Park hacia terreno deshabitado de parque nacional; el corredor en forma de lazo de Calgary-Nolan Hill–Cochrane; el alcance de Olds–Three Hills–Didsbury hacia el norte de Airdrie. El mayoritario recibió cero señalamientos de ese tipo del mismo presidente. (La crítica publicada del presidente cubre siete configuraciones de límites en total — cuatro señalamientos geométricos en el informe principal y tres en el Apéndice C. Esta auditoría confirmó de forma independiente geometría anómala en tres de los cuatro señalamientos geométricos; el cuarto, Calgary-Foothills-Airdrie West <button class="ed-trigger" data-ed-name="Calgary-Foothills-Airdrie West">ver ↗</button>, no alcanzó el umbral de confirmación de la auditoría.)'
		},
		litmus: {
			heading: '3: La prueba de fuego de 1,010,000 mapas',
			fig_alt: 'Histograma que muestra la distribución de brechas de eficiencia entre 250,000 mapas neutrales de Alberta. La mayoría de los mapas se agrupan cerca de cero. El mapa de la comisión minoritaria (línea morada) se sitúa en el percentil 94 (+3.96%), en la cola derecha sombreada. El mapa mayoritario (línea verde azulado) se sitúa en +0.04%, bien dentro del rango normal.',
			fig_caption: 'Distribución de las <button class="vocab-term" data-def="una medida de qué tan desproporcionadamente se convierten los votos en escaños — los valores positivos favorecen al UCP, los negativos favorecen al NDP" aria-expanded="false">brechas de eficiencia</button> entre 250,000 mapas neutrales de Alberta trazados sobre la misma geografía. La mayoría de los mapas neutrales se agrupan cerca de cero; la cola derecha sombreada marca el 10% superior. El +3.96% de la propuesta minoritaria se sitúa en el <button class="vocab-term" data-def="el porcentaje de mapas que puntuaron más bajo — p94 significa que 94 de cada 100 mapas neutrales fueron menos partidistas que este" aria-expanded="false">percentil</button> 94 — una región que menos de 6 de cada 100 mapas neutrales alcanzan jamás. El +0.04% de la propuesta mayoritaria es indistinguible de lo que un proceso neutral típicamente produce.',
			table_intro: 'La tabla compara los dos mapas. Las primeras cinco filas no usan resultados electorales — son propiedades de las líneas mismas. Las últimas dos dependen de cómo se atribuyeron los votos a cada distrito.',
			table_col_measured: 'Qué se midió',
			table_col_majority: 'Mapa mayoritario',
			table_col_minority: 'Mapa minoritario',
			table_col_direction: 'Dirección / Beneficiario',
			table_r1_a: 'Dispersión poblacional entre distritos (más ajustada es mejor)',
			table_r1_b: '3,180',
			table_r1_c: '4,707 — 48% más amplia',
			table_r1_d: 'Estructural (Reduce la igualdad del voto)',
			table_r2_a: 'Exceso de población del NO de Calgary sobre el promedio',
			table_r2_b: '2.8%',
			table_r2_c: '11.5%',
			table_r2_d: '<strong>UCP</strong> (Empaqueta votos urbanos del NDP)',
			table_r3_a: 'División de Airdrie',
			table_r3_b: '2 divisiones',
			table_r3_c: '4 divisiones',
			table_r3_d: '<strong>UCP</strong> (Fragmenta el poder urbano/suburbano)',
			table_r4_a: 'Bordes que siguen las líneas municipales existentes',
			table_r4_b: '80% — dentro de la norma',
			table_r4_c: '72% — dentro de la norma',
			table_r4_d: 'N/A — ambos dentro de la norma canadiense (70–85%)',
			table_r5_a: 'Límites señalados por el presidente de la comisión',
			table_r5_b: '0',
			table_r5_c: '3',
			table_r5_d: 'N/A',
			table_r6_a: 'Escaños con votos al 50/50 (percentil en la simulación de 1,010,000 mapas)',
			table_r6_b: '46.1% — p78 (rango normal)',
			table_r6_c: '51.7% — p99.99 (menos de 100 de 1,010,000 lo alcanzan)',
			table_r6_d: '<strong>UCP</strong>',
			table_r7_a: 'Brecha de eficiencia (percentil en la simulación de 1,010,000 mapas)',
			table_r7_b: '+0.04% — p15.5 (rango normal)',
			table_r7_c: '+3.96% — p94.4',
			table_r7_d: '<strong>UCP</strong>',
			table_r8_a: 'Patrón de vecindad de empaquetamiento-fragmentación',
			table_r8_b: '6 señales de cadena acopladas',
			table_r8_c: '2 (APROBADO preregistrado)',
			table_r8_d: 'Neutral — la minoría logra el efecto partidista mediante hibridación, no drenaje por adyacencia (§5.3.5)',
			vocab_label: 'VOCABULARIO',
			vocab_eg: '<strong>Brecha de eficiencia.</strong> Un número único que mide qué tan desproporcionadamente se traducen los votos de un partido en escaños. Los números positivos favorecen al UCP; los negativos favorecen al NDP. La auditoría usa ~5% como la línea de valor atípico de Alberta — el valor superado por solo el 5% de las 1,010,000 simulaciones neutrales específicas de Alberta. Este umbral no está tomado de la literatura estadounidense ni general; un umbral calibrado para otra jurisdicción sería incorrecto porque la geografía natural de Alberta produce un rango neutral distinto.',
			vocab_mm: '<strong>Diferencia media-mediana.</strong> La brecha entre la proporción de voto del distrito mediano de un partido y su proporción de voto media por distrito. Cuando un partido gana muchas contiendas reñidas, la mediana queda por encima de la media — esos votos se distribuyen eficientemente. Cuando un partido gana muchas contiendas por márgenes amplios, la media queda por encima de la mediana — se están desperdiciando votos. Una brecha media-mediana grande en una dirección señala ineficiencia estructural en cómo se reparten los votos de un lado entre los distritos.',
			vocab_percentile: '<strong>Clasificación por percentil.</strong> En esta auditoría, un "percentil" es un rango dentro de los 1,010,000 mapas neutrales simulados. "p94" significa que el 94% de los mapas neutrales puntúa más bajo — el mapa real es más extremo que el 94% de las extracciones neutrales. "p99.99" significa que menos de 1 de cada 10,000 mapas neutrales alcanza ese nivel.',
			vocab_anchoring: '<strong>Anclaje.</strong> La fracción de un borde electoral que descansa sobre una línea administrativa preexistente — un límite de ciudad, un límite de división escolar, una línea censal de Statistics Canada.',
			closing_p1: 'Las filas inferiores dependen de resultados electorales. La prueba <em>seats@50/50</em> mantiene al electorado en paridad perfecta (el UCP y el NDP ganan exactamente la mitad de los votos cada uno a escala provincial) y pregunta cuántos escaños le otorga el mapa al UCP. Un mapa neutral de Alberta produce una mediana de alrededor del 44.8% de escaños UCP. La geografía de Alberta — votantes del NDP concentrados en los núcleos urbanos, votantes del UCP repartidos por los distritos rurales — le da al NDP una pequeña ventaja de eficiencia en neutralidad. El mapa mayoritario, con 46.1%, se sitúa en el percentil 78 de la simulación de 1,010,000 mapas, bien dentro del rango normal. El mapa minoritario, con 51.7%, se sitúa en el percentil 99.99: menos de 100 de 1,010,000 extracciones neutrales alcanzan ese valor. El número de la <em>brecha de eficiencia</em> mide qué tan desproporcionadamente se traducen en escaños los votos de cada partido. Sobre los shapefiles oficiales de Elections Alberta, la brecha de eficiencia de la minoría es +3.96%, situándola en el percentil 94.4 — justo debajo de la línea de valor atípico del percentil 95 de la auditoría. Las preguntas iniciales en la parte superior de esta página desglosan las consecuencias.',
			closing_p2: 'La última fila es donde el mapa minoritario tiene menos señales de cadena acopladas que el mayoritario en la prueba de drenaje de vecinos: 2 frente a las 6 del mayoritario (y las 5 del mapa promulgado en 2019). La auditoría preregistró esta prueba antes de medir, y el conteo más bajo de la minoría es un APROBADO preregistrado genuino — la minoría no muestra el patrón clásico de adyacencia de empaquetar-y-drenar. Es la única prueba donde la minoría supera numéricamente a la mayoría. El §5.3.5 del informe académico explica por qué: la minoría logra su efecto partidista mediante hibridación (división de ciudades que internaliza el empaquetamiento y la fragmentación dentro de EDs individuales), lo cual es invisible para una prueba de cadenas de adyacencia que solo mide cómo los distritos empaquetados se agrupan junto a los fragmentados.'
		},
		commission_split: {
			heading: '2: Cómo se dividió la comisión',
			intro: 'La Comisión de Límites Electorales de Alberta terminó su trabajo el 23 de marzo de 2026 y no pudo ponerse de acuerdo. Tres comisionados produjeron un mapa; los otros dos produjeron uno distinto. El presidente de la Comisión, el juez Dallas K. Miller, y dos comisionados nominados por la oposición escribieron el informe mayoritario; dos comisionados nominados por el gobierno — el Dr. Julian Martin y John D. Evans — escribieron el informe minoritario. La división se centró en cómo trazar los límites en las comunidades de rápido crecimiento del borde urbano. La mayoría le dio a Airdrie dos distritos; la minoría, cuatro. La mayoría trazó las divisiones del noroeste de Calgary cerca del promedio provincial; la minoría las trazó 11.5% por encima. Ambos mapas siguen el mismo estatuto. Ambos son legales bajo la <em>Electoral Boundaries Commission Act</em> (Ley de la Comisión de Límites Electorales). El desacuerdo era sobre qué configuraciones geográficas específicas servían mejor a las comunidades que se estaban trazando. El partido gobernante de Alberta es el United Conservative Party (UCP); su principal oposición es el New Democratic Party (NDP). Partidos más pequeños — el Alberta Party, el Partido Liberal de Alberta y otros — también compiten por escaños, pero su proporción combinada del voto provincial ha sido lo bastante baja en elecciones recientes como para no afectar materialmente los cálculos de equidad partidista de la auditoría, que se basan en la división UCP–NDP de 2023. Esta auditoría midió ambos mapas con los mismos métodos, aplicados de manera idéntica. Tres hallazgos destacan.',
			finding1: '<strong>Los dos mapas difieren en seis cosas que se pueden medir sin mirar ningún resultado electoral:</strong> qué tan uniformemente está repartida la gente entre los distritos, si los votantes están concentrados, qué tan mal cortadas quedan las ciudades, si los bordes siguen los límites de ciudad, la forma de los distritos, y cuántos límites el propio presidente de la Comisión, el juez Miller, señaló como anómalos por escrito (§5.8.2 del informe mayoritario y Apéndice C). El mapa minoritario difiere del mayoritario en todas y cada una de ellas.',
			finding2: '<strong>Cada diferencia medida se mueve en la misma dirección.</strong> En todos los lugares donde los dos mapas divergen — el noroeste de Calgary, Airdrie, zonas urbanas con límites de ciudad claros — el mapa minoritario traza límites que reparten más delgados los votos del NDP y dejan que los votos del UCP cuenten con más eficiencia. Las comunidades más remodeladas por el mapa minoritario son las mismas comunidades donde el NDP es más fuerte. La auditoría no puede determinar la intención. Puede medir el efecto.',
			finding3: '<strong>El proceso que ahora promueve el mapa minoritario es sin precedentes entre los ciclos canadienses de redistribución que esta auditoría revisó — una valoración que el politólogo Duane Bratt (Mount Royal University) compartió con el autor en correspondencia.</strong> Ninguna de las provincias revisadas permite que un gabinete entregue la redistritación a un comité que su propio partido controla a mitad de un ciclo de redistribución. La mayoría de las provincias o bien exigen que la Legislatura debata primero el mapa de los comisionados, o bien dan al mapa de la comisión efecto automático salvo que sea anulado. Alberta no hace ninguna de las dos. El 16 de abril, el gobierno dejó de lado ambos mapas de la comisión y asignó el trabajo a un comité de MLA cuya mayoría de miembros proviene del gobernante United Conservative Party (UCP); la composición completa y el mandato del comité se detallan en el §7. La <em>Electoral Boundaries Commission Act</em> de Alberta exige que la Legislatura apruebe una Electoral Districts Act aparte para dar efecto legal a un informe de la comisión — el informe de la comisión por sí mismo no cambia nada. La mayoría de las demás provincias hacen que el informe de una comisión sea legalmente efectivo a menos que la Legislatura lo anule activamente; el régimen por defecto de Alberta lo invierte, lo que significa que el partido gobernante controla si algún mapa de comisión llega a ser ley alguna vez. La justificación declarada del gobierno fue implementar la Recomendación 5 del presidente de la Comisión, el juez Miller. Pero Miller había escrito la recomendación específicamente para disuadir a la Legislatura de aceptar el mapa minoritario, y sus colegas de la mayoría no la respaldaron. La Recomendación 5 también era geográficamente específica: un escaño rural adicional al sur de Edmonton, y uno en el condado de Clearwater y el oeste del condado de Mountain View — ambos lejos de las comunidades de rápido crecimiento del borde urbano de Calgary y Edmonton donde la comisión realmente se dividió. No era una invitación a rediseñar esos límites en disputa. El gobierno adoptó el número de escaños mientras le entregaba a un comité que controla la autoridad sobre exactamente las líneas en las que la comisión estuvo en desacuerdo.',
			closing: '<strong>El proceso es un hallazgo en sí mismo, separado de los mapas.</strong>'
		},
		november: {
			heading: '7: El comité Lunty',
			context_label: 'CONTEXTO',
			context_body: ' — Esta sección describe el proceso que reemplazó a la comisión y el marco legal que le aplica. No forma parte de los hallazgos estadísticos. Los hallazgos están en los §3–§6 de arriba.',
			intro: 'Ningún mapa de la comisión está en vigor. El 16 de abril de 2026, la Asamblea Legislativa aprobó la Moción 19, dejando ambos de lado y remitiendo la redistritación a un Comité Especial Selecto de cinco MLA — tres UCP, dos NDP — presidido por Brandon Lunty (UCP, Leduc-Beaumont). El comité en sí no traza el mapa. Supervisa un Panel Asesor Independiente aparte, constituido bajo la Moción Gubernamental 37 (aprobada el 21 de abril de 2026), encargado de producir una propuesta de límites de 91 escaños. La Moción 37 contemplaba cinco miembros del panel — un juez en funciones o jubilado como presidente, dos miembros nominados por el premier y dos por el líder de la oposición — pero la jueza en jefe interina de Alberta declinó nominar a un juez para la presidencia, y el panel opera ahora con los cuatro designados que el comité confirmó: el Hon. Monte Solberg y Darwin Durnie (nominados del premier) y el Dr. Gerard Kennedy y Brent Robinson (nominados de la oposición). El comité debe entregar su informe a la Legislatura antes del 2 de noviembre de 2026. A diferencia de la comisión original, ni el comité ni el panel están obligados a celebrar audiencias públicas; el panel se apoya en las presentaciones que recopiló la comisión original. Cuando se publique el mapa del comité, esta auditoría aplicará la misma metodología para evaluarlo.',
			h_anomalous: 'Por qué el comité es anómalo',
			anomalous_p1:
				'La práctica canadiense de redistritación se ha asentado, desde los años sesenta, en un solo modelo: una comisión independiente, aislada de la dirección del gobierno, produce recomendaciones de límites; la Legislatura puede debatirlas pero no puede anularlas fácilmente sin una votación legislativa formal. El proceso estatutario de Alberta bajo la <em>Electoral Boundaries Commission Act</em> sigue esta plantilla — pero con una diferencia estructural respecto de la mayoría de las provincias: el informe de la comisión de Alberta no tiene efecto legal automático. Bajo la Ley, la Legislatura debe aprobar una Electoral Districts Act aparte para dar fuerza de ley a cualquier mapa de la comisión. Esto significa que el gobierno de turno controla no solo si el mapa de la comisión se debate, sino si llega a ser ley alguna vez. Otras jurisdicciones canadienses adoptan el régimen contrario por defecto: las recomendaciones de la comisión entran en vigor a menos que la Legislatura vote afirmativamente para anularlas.',
			anomalous_p2:
				'Lo que el gobierno hizo en abril de 2026 no tiene precedente registrado en la redistritación posterior a la Confederación: permitió que un proceso de comisión completado y publicado concluyera — con ambos informes, mayoritario y minoritario, presentados — y luego remitió la tarea de redistritación a un comité de cinco MLA cuya mayoría (tres de cinco) pertenece al partido gobernante, sin someter a votación ninguno de los dos informes de la comisión. El comité Lunty no es una comisión. No tiene independencia estatutaria de la dirección legislativa del gobierno. Su mayoría de tres miembros del UCP refleja el control del gobierno sobre la Legislatura. Ninguna otra provincia canadiense ha transferido la autoridad de redistritación, a mitad de ciclo, a un comité legislativo controlado por el gobierno después de que una comisión independiente hubiera completado su trabajo.',
			h_framework: 'El marco constitucional',
			framework_p1:
				'El artículo 3 de la <em>Carta de Derechos y Libertades</em> — "Todo ciudadano de Canadá tiene derecho a votar en una elección de miembros de la Cámara de los Comunes o de una asamblea legislativa" — ha sido interpretado por la Corte Suprema de Canadá como garantía no solo del acto de depositar una boleta sino de la <em>representación efectiva</em>. La autoridad principal es <em>Reference re Provincial Electoral Boundaries (Saskatchewan)</em> [1991] 2 SCR 158, en la que la jueza McLachlin (como era entonces) escribió por la mayoría que el propósito del artículo 3 "no es la igualdad del poder de voto en sí, sino el derecho a una representación efectiva". La paridad poblacional es la consideración primaria; se permiten desviaciones cuando están justificadas por comunidad de interés, geografía, historia u objetivos de representación de minorías.',
			framework_p2:
				'El marco de Saskatchewan no prohíbe categóricamente las consideraciones partidistas en la redistritación. Lo que establece es que los mapas de límites deben, en su conjunto, proporcionar representación efectiva a los votantes — y que el menoscabo sistemático de la capacidad de un grupo identificable para elegir representación proporcionada es el patrón al que apuntan las impugnaciones bajo el artículo 3. Los hallazgos estadísticos y estructurales de la auditoría — la posición del mapa minoritario en el percentil 99.99 de 1,010,000 extracciones neutrales, su cruce de cuatro de los cinco umbrales estructurales (el quinto, el anclaje, es neutral para ambos mapas), las comunidades afectadas identificadas — son el expediente probatorio que un demandante bajo el artículo 3 necesitaría reunir. En el lado de la comunidad de interés de ese expediente, la decisión de la Corte Federal en <em>Raîche v. Canada</em> (2004 FC 679) es la autoridad canadiense principal: la corte exigió allí que la Comisión federal de Límites Electorales revisara límites que habían ignorado la comunidad de interés acadiana en New Brunswick. Las mediciones de anclaje municipal de la auditoría y sus hallazgos comunitarios específicos — Airdrie dividida en cuatro distritos, las anomalías del borde urbano señaladas por el presidente en el noroeste de Calgary — son el mismo tipo de evidencia que la Corte Federal trató como jurídicamente reconocible. Si ese expediente alcanza el umbral constitucional es una pregunta legal que esta auditoría no decide; la auditoría reporta la medición.',
			framework_p3:
				'La legalidad del comité como proceso es una pregunta aparte. La <em>Electoral Boundaries Commission Act</em> de Alberta no prohíbe expresamente que la Legislatura constituya un órgano paralelo de redistritación, porque la Ley contempla que la Legislatura promulgará los límites finales mediante legislación ordinaria de todos modos. Si el proceso del comité, en caso de producir un mapa con el perfil estructural y estadístico de la propuesta minoritaria, podría sobrevivir una impugnación bajo el artículo 3 de la Carta depende de si la representación efectiva es alcanzable bajo los límites resultantes — la misma prueba que se aplicaría a cualquier mapa producido por una comisión.',
			h_quebec: 'El contraste con Quebec',
			quebec_p1:
				'Quebec ofrece la comparación más relevante para la situación de Alberta. La Commission de la représentation électorale (CRE) de Quebec es un órgano permanente e independiente de límites electorales, no una comisión ad hoc constituida por ciclo de redistribución. La CRE opera de forma continua y no puede ser disuelta ni eludida por acción del gabinete. Bajo la <em>Loi électorale</em> de Quebec, la Asamblea Nacional debe adoptar las recomendaciones de la CRE a menos que vote para desviarse — y las desviaciones requieren una mayoría de dos tercios de todos los miembros de la Asamblea, no una mayoría legislativa simple. El efecto práctico es que un partido gobernante no puede, actuando solo con su propia mayoría, sustituir el mapa de la comisión por su mapa preferido. Se requiere constitucionalmente un acuerdo entre partidos para anular el juicio del órgano independiente.',
			quebec_p2:
				'El modelo de Quebec surgió en parte de las lecciones sobre lo que ocurre cuando la redistritación no está aislada del control partidista. El contraste con el proceso actual de Alberta — donde un comité controlado por la mayoría ha reemplazado el trabajo de la comisión antes de que la Legislatura haya votado sobre cualquiera de los dos informes — ilustra la diferencia estructural entre los sistemas de redistritación que asumen la presión partidista y diseñan contra ella, y los sistemas donde esa presión tiene un camino más despejado hacia el resultado.',
			closing:
				'La auditoría aplicará las mismas pruebas al mapa del comité Lunty cuando se publique. Las observaciones constitucionales y comparativas de arriba son contextuales; la metodología no cambia.'
		},
		references: {
			heading: '10: Referencias y metodología',
			heading_aria: 'Enlace a las referencias',
			intro:
				'La metodología subyacente se apoya en literatura establecida de ciencia política, estadística y derecho. Las citas completas siguen el estilo de la American Political Science Association (APSA); los casos judiciales siguen la convención legal canadiense. La lista completa de referencias aparece en el <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/blob/master/reports/academic/report_academic.md" rel="noopener">informe técnico</a>. Las fuentes clave se listan aquí.',
			h_academic: 'Literatura académica',
			h_cases: 'Casos judiciales',
			h_statutes: 'Estatutos'
		},
		resources: {
			heading: '11: Apéndice técnico',
			heading_aria: 'Enlace a lo técnico',
			tag_plain: 'Lenguaje llano',
			plain_label: 'Informe público completo',
			plain_desc: 'De formato largo, con mapas, para lectores generales',
			tag_summary: 'Resumen',
			summary_label: 'Resumen de hallazgos',
			summary_desc: 'Panorama en lenguaje llano, explica cada concepto desde cero',
			tag_academic: 'Académico',
			academic_label: 'Informe técnico',
			academic_desc: 'Métodos completos y citas para investigadores',
			tag_notebook: 'Notebook',
			notebook_label: 'Notebook interactivo',
			notebook_desc: 'Ejecute los gráficos usted mismo en su navegador, sin necesidad de instalar nada',
			tag_code: 'Código'
		},
		about_me: {
			heading: 'Sobre mí',
			p1: 'Soy estudiante de Mount Royal University. Hice esta investigación por mi cuenta — no fue asignada como trabajo de curso y la universidad no la encargó. Mis opiniones son mías y no representan a la universidad. No tengo conexión alguna con Elections Alberta, la comisión ni ningún partido político.',
			p2: 'He votado por distintos partidos en distintas elecciones, a lo largo del espectro político. Se lo cuento porque mi historial político podría afectar cómo miro este asunto. La principal protección contra eso es el método: probé ambos mapas de la misma manera, dejé por escrito mis predicciones antes de mirar los resultados, y puse todo en línea para que cualquiera pueda verificar mi trabajo. Pagué esta investigación de mi propio bolsillo. Si encuentra algo en lo que me equivoqué, genuinamente quiero saberlo.',
			p3: 'Registros de preregistro (escritos antes de examinar los resultados): <a href="https://osf.io/6pt83" rel="noopener">OSF:6pt83</a>, AsPredicted:#289,469, AsPredicted:#289,451.',
			p4: 'Preguntas o correcciones: <a href="mailto:wconn161@mtroyal.ca">wconn161@mtroyal.ca</a>'
		},
		translation_about: {
			heading: 'Sobre esta traducción',
			p1: 'Usted está leyendo una traducción por IA, producida por el modelo Fable 5 de Anthropic y a la espera de revisión por hablantes nativos. La versión en inglés es el texto autoritativo: si algo en esta traducción no queda claro o parece incorrecto, rige el original en inglés.',
			p2: 'La calidad de la traducción importa aquí de una manera en que no importa en la mayoría de los sitios web — esta auditoría hace afirmaciones estadísticas sobre la equidad electoral, y un número mal traducido o una oración con el matiz equivocado engaña de maneras difíciles de detectar para el lector. La traducción automática de prosa cívico-estadística es genuinamente difícil, y es probable que haya errores.',
			p3: 'Si usted es hablante nativo y detecta un error — o quisiera revisar una sección como es debido — por favor %s. Para darle una idea de la escala: la prosa en inglés suma alrededor de {count} palabras. Puede encargarse de todo o solo de una parte, y en la mayoría de los casos el trabajo consiste en corregir errores menores que cometió la máquina más que en traducir desde cero — incluso revisar una sola sección ayuda.',
			p3_link: 'escríbanos'
		},
		retractions: {
			heading: '9: Retractaciones y correcciones',
			heading_aria: 'Enlace a las retractaciones',
			conditions_label: 'CONDICIONES DE RETRACTACIÓN',
			conditions_intro:
				'Cada hallazgo está precomprometido con una condición específica de falsación. Si cualquiera de las condiciones siguientes se materializa, el hallazgo que nombra se retracta públicamente en un plazo de 30 días. La conclusión direccional general — que el mapa minoritario se sitúa fuera del rango neutral en múltiples pruebas independientes — se retracta solo si al menos tres de las cinco pruebas fallan.',
			c1_title: 'Condición 1 — Existe un contramapa',
			c1_what: '<em>Qué se retracta:</em> El hallazgo estructural de que la división en cuatro de Airdrie y los tres límites señalados por el presidente no pueden explicarse por la justificación declarada de comunidad de interés de la minoría.',
			c1_cond:
				'Condición: alguien produce un mapa legal de Alberta que satisface las propias razones declaradas de la minoría — Airdrie, Cochrane, Nolan Hill, Rocky Mountain House–Banff Park — y se ancla a las líneas municipales a tasas comparables a las de la mayoría. Desafío abierto en el <a href="https://github.com/Ixby/alberta-electoral-boundaries-audit/issues/14" rel="noopener">Issue #14</a>.',
			c2_title: 'Condición 2 — Se revierte el APROBADO preregistrado del drenaje de vecinos',
			c2_what: '<em>Qué se retracta:</em> La entrada de la tabla de la Sección 3 que registra el mapa minoritario como un APROBADO preregistrado en la prueba de adyacencia de drenaje de vecinos.',
			c2_cond:
				'Condición: el puntaje continuo de drenaje v2 cae en la cola superior extrema (p &lt; 0.05) de permutaciones aleatorias sobre el grafo de contigüidad fijo, lo que significaría que el aprobado fue un artefacto de medición del método de puntuación binaria v1 y no un resultado nulo genuino.',
			c3_title: 'Condición 3 — Aparece un documento de la comisión anterior a 2026',
			c3_what: '<em>Qué se retracta:</em> La inferencia de que las decisiones de límites de la minoría fueron decisiones de redacción y no respuestas a presentaciones comunitarias documentadas.',
			c3_cond:
				'Condición: un documento interno de la comisión fechado antes de las decisiones finales de límites de la minoría muestra que esas decisiones fueron impulsadas explícitamente por presentaciones comunitarias que la auditoría no ha visto — no por las seis subjustificaciones publicadas que la auditoría puso a prueba.',
			c4_title: 'Condición 4 — El resultado electoral de 2027 contradice la simulación',
			c4_what: '<em>Qué se retracta:</em> El hallazgo de la Vía 1 — que el puntaje seats@50/50 del mapa minoritario se sitúa en el percentil 99.99 de 1,010,000 extracciones neutrales.',
			c4_cond:
				'Condición: si la elección provincial de 2027 se disputa sobre cualquiera de los dos mapas de la comisión y la división partidista real de escaños contradice la proyección direccional a partir de los votos de 2023, los hallazgos de percentil de la Vía 1 se revisan contra los resultados reales.',
			c5_title: 'Condición 5 — Un tribunal de Alberta distingue el fallo de la SCC sobre Quebec',
			c5_what: '<em>Qué se retracta:</em> El argumento procedimental de la Sección 7 de que la moción del 16 de abril para reemplazar la comisión con el comité Lunty pertenece a la misma clase constitucional que el congelamiento de la redistritación de Quebec de 2024.',
			c5_cond:
				'Antecedente: el 22 de abril de 2026 — seis días después de la moción de Alberta del 16 de abril — la Corte Suprema de Canadá confirmó, 7–2 y desde el estrado, un fallo de la Corte de Apelaciones de Quebec según el cual el congelamiento legislativo del gobierno de Legault sobre su comisión de redistritación violaba la garantía de representación democrática del artículo 3 de la Carta. Condición: un tribunal que revise la moción de Alberta la encuentra constitucionalmente distinta — por ejemplo, porque reasignar el trabajo a un comité de MLA difiere estructuralmente de un congelamiento legislativo, o porque el análisis de representación efectiva de Alberta bajo el artículo 3 resulta distinto al de Quebec.',
			corr_label: 'CORRECCIONES DOCUMENTADAS (recomputación canónica, 2026-05-11)',
			corr_intro:
				'El siguiente hallazgo temprano no sobrevivió el reanálisis contra los shapefiles oficiales de Elections Alberta (recibidos el 2026-05-06). Se conserva aquí conforme a la política precomprometida de la auditoría de nunca borrar hallazgos fallidos.',
			corr_municipal:
				'<strong>Anclaje municipal (retractado).</strong> El análisis temprano que usaba límites de mapa provisionales mostraba que el mapa minoritario se anclaba a las líneas municipales solo el 15% del tiempo — 4.9&times; por debajo de la norma canadiense de 70–85%. Esta cifra era un artefacto de las reconstrucciones provisionales de límites (de la era DPG). Sobre los shapefiles canónicos oficiales de Elections Alberta, ambos mapas se anclan dentro de la norma canadiense: mayoritario 80%, minoritario 72%. La <em>divergencia</em> de anclaje municipal entre los dos mapas no es una señal que sobreviva la recomputación canónica. Las tres anomalías de límites señaladas por el presidente de la comisión (Rocky Mountain House–Banff Park, Nolan Hill–Cochrane, Olds–North Airdrie) permanecen y no se ven afectadas por esta corrección.'
		},
		suggestions: {
			heading: '8: Sugerencias',
			heading_aria: 'Enlace a la sección 8',
			intro:
				'Esta auditoría tropezó con dos problemas de datos que no tienen nada que ver con el trabajo de la comisión y todo que ver con cómo está diseñado el sistema electoral de Alberta. Ambos tienen arreglo.',
			advance_p1:
				'<strong>Cerca de la mitad de todos los votos de Alberta llegan ahora antes del día de la elección</strong> — votación anticipada, mesas móviles, boletas especiales. Elections Alberta reporta estos resultados como totales por cada división electoral, no por Área de Votación específica. Esto significa que aproximadamente 395,000 votos del NDP y el UCP emitidos en 2023 no pueden fijarse a ningún vecindario en un mapa. Se cuentan; simplemente no se pueden ubicar. Cada votante anticipado se verifica contra una lista de votantes antes de recibir su boleta, y la lista vincula a cada votante con su Área de Votación específica. Publicar los totales de voto anticipado a nivel de VA no requeriría ningún cambio en el proceso de votación — solo en lo que EA reporta.',
			advance_p2:
				'Esto afecta también a los comisionados, no solo a los analistas externos. Cuando una comisión decide si mantener Airdrie entera o dividirla, si un corredor entre dos comunidades tiene sentido, si un límite propuesto divide una circunscripción natural — esos son juicios que dependen de saber dónde viven los votantes. Los comisionados trabajan con el mismo conjunto de datos publicado que todos los demás. La mitad de la señal geográfica sobre las comunidades alrededor de las cuales están trazando límites les falta también a ellos.',
			lesser_slave_p1:
				'Hay al menos una comunidad en el norte de Alberta donde esta brecha es total. En la parte norte de la división de Lesser Slave Lake <button class="ed-trigger" data-ed-name="Lesser Slave Lake">ver ↗</button>, hay un Área de Votación que cubre 4,832 km&#178; — más grande que la Isla del Príncipe Eduardo — donde absolutamente cada voto en 2023 se emitió a través del equipo de votación móvil de Elections Alberta. Las decisiones de esos 844 residentes se cuentan en el total divisional pero no pueden fijarse a ninguna ubicación en un mapa. La comunidad es enteramente invisible en los resultados electorales publicados.',
			lesser_slave_p2:
				'Cuando la comisión consideró inicialmente eliminar la división de Lesser Slave Lake y fusionarla en un distrito más grande, estaba trabajando sin datos geográficos de voto de esas comunidades. La comisión finalmente preservó la división — tras más de 80 presentaciones públicas, muchas de las comunidades indígenas de la parte norte del distrito — invocando una ley provincial que permite que los distritos con comunidades de Primeras Naciones y M&#233;tis tengan poblaciones menores que el promedio provincial. Llegaron a buen puerto. Pero los datos con los que trabajaban no les mostraban quién votaba en las comunidades que estaban decidiendo proteger.',
			ebca_label: 'ARTÍCULO 15(2) DE LA EBCA',
			ebca_body:
				'El artículo 15(2) de la <em>Electoral Boundaries Commission Act</em> de Alberta es una disposición discrecional que permite a las comisiones proteger distritos por debajo del tamaño — aquellos más de 25% por debajo del promedio poblacional provincial — cuando el distrito cumple al menos tres de cinco criterios específicos: (a) superficie geográfica superior a 20,000 km², (b) distancia de más de 150 km del Edificio de la Legislatura por la ruta de carretera más directa, (c) ausencia de cualquier pueblo con más de 8,000 residentes, (d) presencia de una reserva indígena o un asentamiento Métis, y (e) si el distrito colinda con un límite de la Provincia de Alberta. La disposición no es automática; la comisión debe juzgar si se cumplen los criterios. Lesser Slave Lake cumple de forma independiente cuatro de los cinco.',
			rationale_p1:
				'La justificación provisional para eliminar el distrito era la población: con aproximadamente 27,000 residentes, Lesser Slave Lake está cerca de 45% por debajo del promedio provincial, acercándose al piso legal. Esto se lee como una aplicación directa de las reglas. No lo es. La ley de Alberta da a las comisiones discreción explícita para proteger distritos por debajo del tamaño cuando aplican al menos tres de cinco criterios específicos, y Lesser Slave Lake cumple cuatro de ellos de forma independiente. Su superficie es de 69,566 km² (criterio a, umbral de 20,000 km²). Su límite más cercano está a más de 150 km de la Legislatura por carretera (criterio b). Ningún pueblo del distrito tiene una población superior a 8,000 (criterio c). Y el distrito contiene catorce reservas indígenas y asentamientos M&#233;tis cuyas comunidades comparten una geografía norteña común, una dependencia común de la votación móvil para poder votar siquiera, y un interés colectivo en tener un representante principalmente responsable ante el norte de Alberta (criterio d).',
			rationale_p2:
				'Bajo la fusión propuesta con Mackenzie, la voz colectiva habría quedado absorbida permanentemente en un distrito donde el otro partido gana por más de dos a uno, no porque esas comunidades cambiaran sino porque cambiaron las líneas a su alrededor. Cada uno de esos cuatro criterios es un hecho objetivo sobre la geografía del distrito, no una cuestión de criterio. Juntos describen una circunscripción que la disposición fue escrita para proteger: remota, extensa, escasamente poblada, y con comunidades cuyo interés de representación no puede leerse en los números brutos de población. Se necesitan tres para calificar; Lesser Slave Lake tiene cuatro. Tratar el déficit poblacional como si obligara a la eliminación malinterpreta el estatuto. La reversión de la comisión fue la aplicación correcta de la ley, no una concesión a la presión política.',
			banff_p:
				'Aquí está el otro lado de la historia: mientras las comunidades indígenas de Lesser Slave Lake luchaban por ser contadas, los comisionados disidentes propusieron proteger un distrito distinto trazando su límite a través del Parque Nacional Banff, donde no vive nadie. El propio presidente de la comisión lo llamó "un esfuerzo de mala fe" para reclamar la protección legal. La frase está en el informe final oficial de la comisión. La protección diseñada para comunidades remotas con poblaciones indígenas se usó, en el mapa de la minoría, para defender un límite a través de tierra silvestre deshabitada. Las comunidades para las que fue diseñada tuvieron que pelearla mediante presentaciones públicas. El comité Lunty enfrentará la misma decisión del §&#x2009;15(2) en noviembre — sin obligación estatutaria de celebrar audiencias públicas, y sin garantía de que las 80 presentaciones que revirtieron la posición provisional de la comisión pesen lo mismo una segunda vez.',
			census_p1:
				'<strong>Alberta debería esperar al censo de 2026 antes de trazar el próximo mapa.</strong> Canadá cuenta su población cada diez años. La enumeración del censo de 2026 ocurre en la primavera de 2026; Statistics Canada publica datos subprovinciales utilizables aproximadamente dos años después, en 2027 o 2028. La comisión que trazó los mapas evaluados en esta auditoría tuvo que usar el censo de 2021 — ya con cuatro años de antigüedad cuando se trazaron los mapas, y potencialmente con catorce años cuando esos límites se retiren. Ciudades de rápido crecimiento como Airdrie y Chestermere cambiarán 40% o más en esa ventana. Las comunidades rurales se encogerán. El mapa estará equivocado desde el día en que se use. Un cambio sencillo a la <em>Electoral Boundaries Commission Act</em> podría exigir que cualquier nueva comisión se designe solo después de que Statistics Canada publique los datos de áreas de difusión más actuales del censo precedente. El resultado: mapas que reflejen dónde viven realmente los albertanos, no dónde vivían hace una década.',
			census_p2:
				'El comité Lunty opera bajo el estatuto vigente, que no fija ningún requisito de sincronización con el censo, y no puede aplazar unilateralmente más allá de su fecha límite de noviembre de 2026. Esta recomendación aplica a una futura enmienda a la <em>Electoral Boundaries Commission Act</em>, no al proceso actual. La tensión es real: un comité obligado a entregar un mapa para noviembre trabaja con datos que para entonces ya tendrán cinco años — nombrar la restricción es más útil que fingir que no existe.',
			closing:
				'Ninguna de estas dos es un hallazgo sobre los mapas de la comisión actual. Son observaciones sobre un sistema que hace el análisis electoral preciso más difícil de lo necesario. Se ofrecen aquí como sugerencias prácticas, no como conclusiones. Ambas tienen genuinamente arreglo, y arreglarlas haría que cada comisión futura — y cada auditoría futura — trabaje sobre mejor terreno.'
		}
	},
	editorial_canada: {
		heading: 'Contexto: Canadá es diferente — y parecido',
		p1: 'Canadá pertenece a la misma familia que EE. UU., el Reino Unido y Australia. Elegimos miembros individuales por distritos geográficos bajo el sistema de mayoría simple (first-past-the-post). Redibujamos las líneas periódicamente — a nivel federal después de cada censo decenal, a nivel provincial en calendarios escalonados. Heredamos la maquinaria básica de las mismas raíces de Westminster. Hasta aquí, sin sorpresas.',
		p2: 'Lo que distingue a Canadá es la prueba que las líneas tienen que pasar.',
		p3: 'En el derecho constitucional estadounidense, la regla vinculante es <em>una persona, un voto</em> — los distritos deben tener poblaciones tan iguales como sea practicable, y las desviaciones grandes requieren justificación estricta. En el derecho constitucional canadiense, la regla vinculante es distinta. El artículo 3 de la <em>Carta Canadiense de Derechos y Libertades</em> garantiza a todo ciudadano el derecho al voto. En <em>Reference re Provincial Electoral Boundaries (Sask.)</em> — el Saskatchewan Reference de 1991, el caso de referencia — la Corte Suprema de Canadá interpretó ese derecho como un derecho a la <em>representación efectiva</em>, no un derecho a la igualdad matemática de las poblaciones de los distritos.',
		p4: 'Esa distinción importa. La representación efectiva permite que las poblaciones de los distritos varíen, a veces sustancialmente, cuando hay buenas razones: geografías rurales vastas que un solo MLA no puede atender razonablemente a densidad de población estándar, comunidades de interés que deben mantenerse juntas, representación de minorías que la igualdad matemática diluiría. El Saskatchewan Reference hizo constitucional esa flexibilidad. La variación poblacional del 25% de la EBCA — la regla que protege los escaños rurales de Alberta — fluye directamente de él.',
		p5: 'El problema es que la flexibilidad corta en ambos sentidos. Si una comisión puede apartarse legítimamente de la igualdad poblacional por las razones correctas, también puede apartarse de la igualdad poblacional por las equivocadas. El derecho canadiense no tiene un piso matemático al estilo estadounidense al cual recurrir. Tiene la prueba de la representación efectiva, aplicada por jueces, después de los hechos, en litigio. La mayoría de las jurisdicciones se protegen contra las razones equivocadas con salvaguardas estructurales: las comisiones federales de redistritación están aisladas por estatuto y sus recomendaciones entran en vigor automáticamente si el Parlamento no actúa sobre ellas dentro de un plazo. Quebec usa una comisión independiente permanente cuyo trabajo la Asamblea Nacional solo puede anular con una supermayoría de dos tercios. British Columbia opera bajo una regla similar de adopción por defecto.',
		p6: 'Alberta es la excepción. Bajo la <em>Electoral Boundaries Commission Act</em>, el informe de la comisión es solo una recomendación — la Legislatura debe votar para promulgarlo. La aprobación es normalmente una formalidad. En el ciclo de 2026, la comisión se dividió 3–2 y produjo dos propuestas rivales; la Legislatura creó un comité de MLA aparte, presidido por un MLA designado por el premier, para elegir entre ellas. Nada en el derecho constitucional canadiense exigía que el comité existiera. Nada exige que su elección siga el proceso de la comisión. Esta es la brecha estructural que esta auditoría examina.',
		p7: 'Así que cuando los tribunales canadienses dicen que "gerrymander" no es su vocabulario legal, no están diciendo que el concepto subyacente no aplique aquí. Están diciendo que la prueba es distinta — representación efectiva, no igualdad matemática. Si la propuesta minoritaria pasa esa prueba es exactamente la pregunta contra la cual esta auditoría ha medido la geometría, y exactamente la pregunta que solo un juez puede responder de manera definitiva. El razonamiento completo del <em>Saskatchewan Reference</em>, el contraste con otras provincias, la cuestión de la legitimación procesal y las vías de reforma disponibles se tratan en <a href="#references">la sección de referencias más abajo</a>.'
	},
	chrome: {
		back_to_top: 'Volver arriba',
		license_title: 'Creative Commons Atribución-NoComercial-CompartirIgual 4.0',
		license_alt: 'CC BY-NC-SA 4.0',
		license_aria: 'Creative Commons BY-NC-SA 4.0',
		back_to_stakes: '↑ Volver a Lo que está en juego',
		lightbox: {
			fig_aria: 'Vista ampliada de la figura',
			fig_close_aria: 'Cerrar la figura ampliada (Esc)',
			map_aria: 'Visor de zoom del mapa',
			map_close_aria: 'Cerrar el visor del mapa',
			close_title: 'Cerrar (Esc)'
		},
		participation: {
			heading: 'Ayúdenos a refinar MapExplorer',
			body:
				'Mientras usted explora, registramos qué mapas y distritos visita y enviamos periódicamente los datos a nuestra base de datos de investigación. Compartir una vista también guarda dónde terminó. El objetivo: entender qué es útil y mejorar la herramienta.',
			no_collect:
				'Nunca recopilamos su nombre, dirección IP ni ubicación precisa. Todo se anonimiza en su navegador antes de salir. No podríamos identificarlo a partir de los datos ni aunque nos lo ordenaran.',
			dnt:
				'Su navegador tiene activado No Rastrear (Do Not Track). Se ha preseleccionado "No" en su nombre. Aun así puede elegir "Sí".',
			no_thanks: 'No, gracias',
			yes_help: 'Sí, ayudaré',
			privacy_policy: 'Política de privacidad'
		},
		share: {
			button: 'Compartir',
			button_title: 'Compartir o cargar una configuración del mapa',
			dialog_aria: 'Compartir la configuración del mapa',
			close_aria: 'Cerrar el panel de compartir',
			share_label: 'Compartir esta configuración',
			share_hint:
				'Escriba este código en cualquier navegador que ejecute la auditoría para cargar esta configuración. El código nunca se coloca en una URL.',
			load_label: 'Cargar una configuración',
			load_btn: 'Cargar',
			load_placeholder: 'alpine-eagle-banff',
			copy: 'Copiar',
			copied: '¡Copiado!',
			copy_failed: 'Falló',
			unrecognised: 'Código no reconocido — revise la escritura.'
		},
		map: {
			minority: 'Minoritario',
			majority: 'Mayoritario',
			current: 'Vigente',
			wasted: 'Desperdiciados',
			wasted_title: 'Contribución a la brecha de eficiencia por distrito',
			partisan: 'Partidista',
			partisan_title:
				'Colorear cada distrito según el resultado partidista (UCP azul / NDP naranja)',
			borders: 'Límites',
			flagged: 'Señalados',
			flagged_title:
				'Las 7 configuraciones señaladas por el presidente de la comisión, el juez Miller — cambia automáticamente al mapa minoritario',
			help_aria: 'Ayuda del mapa',
			help_title: 'Cómo usar el mapa',
			pin_aria: 'Fijar el mapa',
			pin_title: 'Fijar el mapa — evita el desplazamiento automático al hacer clic en un distrito',
			search_placeholder: 'Buscar distrito…',
			zoom_aria: 'Zoom del mapa',
			clear_aria: 'Borrar la selección de distrito',
			clear_title: 'Borrar selección',
			va_hint: 'Haga clic dentro de este distrito para ver los resultados por centro de votación',
			va_close_aria: 'Cerrar el detalle del centro de votación',
			va_close_title: 'Cerrar',
			object_title: 'Mapa de distritos electorales de Alberta — resolución completa',
			ea_credit: 'Datos del mapa:',
			cc_title: 'Contenido textual: CC BY-NC-SA 4.0',
			cc_alt: 'Creative Commons BY-NC-SA 4.0',
			// Engine-internal strings (callouts, errors, loading) — injected into
			// the framework-free map engine via setEngineStrings() at init and on
			// every language switch.
			votes_suffix: 'votos',
			total_votes_suffix: 'votos totales',
			pop_prefix: 'Pob.',
			voting_areas_suffix: 'áreas de votación',
			other_maps: 'Otros mapas',
			unique_boundary: 'Límite exclusivo de este mapa',
			in_person_votes: 'votos presenciales (excl. Vote Anywhere)',
			load_error_generic: 'No se pudo cargar el mapa de límites. Intente recargar la página.',
			load_error_map: 'No se pudo cargar el mapa {key} — revise su conexión.',
			context_minority: 'Propuesta minoritaria 2026 · resultados electorales de 2023',
			context_majority: 'Propuesta mayoritaria 2026 · resultados electorales de 2023',
			context_2019: 'Límites promulgados en 2019 · resultados electorales de 2023',
			tag_min: 'Min',
			tag_maj: 'May',
			tag_2019: '2019',
			skel_1: 'Cargando el Explorador de Mapas…',
			skel_2: 'dibujando Alberta…',
			skel_3: 'procesando los números…',
			skel_4: 'contando cada voto…',
			skel_5: 'trazando los límites…',
			skel_6: 'ya casi…'
		},
		map_intro: {
			heading: 'Cómo usar el mapa',
			click_district: 'Haga clic en cualquier distrito',
			click_district_desc: 'vea los resultados electorales de 2023 y céntrese en él',
			click_within: 'Haga clic dentro de un distrito seleccionado',
			click_within_desc:
				'vea los resultados de cada centro de votación (color = división del voto)',
			dblclick: 'Haga doble clic en un distrito',
			dblclick_desc:
				'acerque hasta llenar la pantalla; haga doble clic en un espacio vacío para alejar',
			layers_primary: 'Minoritario / Mayoritario / Vigente',
			layers_primary_desc: 'cambie el mapa de límites activo',
			layers_data: 'Partidista / Desperdiciados / Límites',
			layers_data_desc: 'active o desactive las capas de datos',
			search: 'Buscar distrito',
			search_desc: 'salte por nombre; las flechas desplazan, + / − acercan y alejan',
			escape: 'Escape',
			escape_desc: 'cerrar este visor',
			s4_tip:
				'En el §4, haga clic en <em>Mostrar los distritos señalados en el mapa</em> para resaltar la división de Airdrie y la zona del NO de Calgary.',
			got_it: 'Entendido'
		},
		footer: {
			title: 'Auditoría de los Límites Electorales de Alberta — mayo de 2026',
			copyright: '© Will Conner 2026 —',
			text_label: 'Texto:',
			code_label: 'Código:',
			translation_label: 'Traducciones:',
			translation_credit: 'Anthropic Fable 5 (IA) — a la espera de revisión por hablantes nativos'
		}
	}
} as const;
