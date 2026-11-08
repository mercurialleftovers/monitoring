// == general architecture
//
// === hardware
// - arduino UNO
// - temperature sensors
// - vibration sensor
// - LCD
// - keyboard
// - wifi
//
// === software
// - fastAPI
// - websockets
// - sql (for the history)
// - web technologies (front end)
//   - css
//   - html
//   - js
//
// === how they play together:
// - you install the module in the device to be monitored
// - you enter a unique identifier for the device
// - you connect to the wifi
// - you connect to the server
// - every known period of time, a sample containing the id and the measurements from the sensors is sent as a json to an endpoint e.g.: "localhost:[PORT]/device/[id]/sample"
//

// === Repères Bibliographiques et Textes Réglementaires
//
// Pour approfondir l'étude de l'ADE dans le cadre d'un travail académique ou de recherche, les références suivantes constituent le socle documentaire principal :
// - République Algérienne Démocratique et Populaire. Décret exécutif n° 01-101 du 21 avril 2001 portant création de l'Algérienne des Eaux (ADE). Journal Officiel de la République Algérienne, N° 24.
// - République Algérienne Démocratique et Populaire. Loi n° 05-12 du 4 août 2005 relative à l'eau. Journal Officiel de la République Algérienne, N° 60.
// - Ministère des Ressources en Eau (MRE). Plan National de l'Eau (PNE) - Horizon 2030, Alger.
// - Kettab, A. (2001). Les ressources en eau en Algérie : stratégies, enjeux et réalités. Sécheresse, 12(2), 119-124.
// - Rapport annuel de l'Algérienne des Eaux. Bilan d'activité et statistiques de distribution, Direction Générale de l'ADE, Alger.

#set text(
  font: "Times New Roman",
  size: 12pt,
)

#set par(
  justify: true,
  first-line-indent: 2em,
)

#set heading(numbering: "1.1")
#show heading: set block(above: 1.5em, below: 1.5em)

== intro ADE

L’Algérienne des Eaux (ADE) est un établissement public à caractère industriel et commercial (EPIC) placé sous la tutelle du Ministère des Ressources en Eau. Figure centrale de la politique hydraulique en Algérie, l'entreprise est investie d'une mission de service public visant à assurer la production, le transport, la distribution et la gestion commerciale de l'eau potable sur l'ensemble du territoire national.

=== Contexte Historique et Création
Avant la création de l'ADE, la gestion de l'eau potable en Algérie était fragmentée. Elle relevait principalement de la responsabilité des collectivités locales (les Communes) ou d'unités régionales telles que les EPE/EPEOR (Entreprises Publiques d'Eau) et la régie d'Alger (EPEAL), ce qui entraînait d'importantes disparités techniques, financières et opérationnelles entre les régions.

#figure(image("images/agence_ade.jfif"), caption: [Agence commerciale de l'ADE en Algérie. Source: ADE])

- Cadre Juridique de Création : L'Algérienne des Eaux a été formellement créée par le Décret exécutif n° 01-101 du 21 avril 2001.

- Objectif de Centralisation : Cette création s'inscrit dans la mise en œuvre de la Loi n° 05-12 du 4 août 2005 relative à l'eau (révisant le Code de l'Eau de 1983). L'objectif était d'unifier la gestion de l'Eau Potable et de l'Assainissement (AEP) au sein d'une entité nationale unique capable de péréquater les ressources et de rationaliser les investissements.

- Transfert de Compétences : L'ADE a progressivement pris en charge la gestion du réseau AEP des 58 wilayas via ses directions opérationnelles (Zone et Unité) et à travers des partenariats de gestion déléguée (notamment SEAAL à Alger/Tipaza, SEOR à Oran, SEACO à Constantine dans le cadre de contrats de management conclus dans les années 2000).

=== Missions et Objectifs Stratégiques
L'ADE assure la maîtrise d'ouvrage déléguée et l'exploitation des infrastructures de production et de distribution. Ses principaux objectifs s'articulent autour de quatre axes :

- Sécurité Alimentaire en Eau : Assurer un approvisionnement continu (H24) ou régulier aux populations, même dans les zones soumises au stress hydrique.
- Préservation de la Santé Publique : Garantir la potabilité stricte de l'eau distribuée grâce à un suivi physico-chimique et bactériologique rigoureux.
- Lutte contre le Gaspillage et Réduction des Pertes : Moderniser les réseaux pour réduire le Taux de Rendement du Réseau (TRR) en luttant contre les fuites physiques et les piquages illicites.
- Viabilité Économique : Améliorer le taux de recouvrement des créances, généraliser la comptage individuel (compteurs d'eau) et optimiser les coûts d'exploitation énergétique.

=== Aspects Techniques, Architecturaux et Infrastructures

L'infrastructure gérée par l'ADE repose sur un maillage complexe combinant génie civil, réseaux de transport à haute pression et technologies de traitement de pointe.

#figure(
  image("images/ade_infrastructure.jpg", width: 100%),
  caption: [Infrastructures de traitement et transfert d'eau. @transfer_ade],
)

==== Typologie des Infrastructures:

- Ouvrages de Stockage : Réservoirs d'eau surélevés (châteaux d'eau) et réservoirs semi-enterrés en béton armé, dimensionnés pour équilibrer la pression du réseau et offrir une autonomie de distribution.
- Grands Transferts : Systèmes d'adduction hydraulique reliant les barrages intérieurs ou les stations de dessalement vers les hauts plateaux et les agglomérations urbaines (ex. le transfert Mostaganem-Arzew-Oran MAO, ou le grand transfert de M'daourouch).
- Stations de Traitement : Unités conventionnelles de décantation, filtration sur lit de sable et désinfection au chlore gazeux ou à l'hypochlorite de sodium.

==== Innovations Technologiques et Digitalisation:

- Télégestion et SCADA : Déploiement progressif de systèmes d'acquisition de données et de contrôle à distance (SCADA) pour surveiller en temps réel la pression, le débit et le niveau des réservoirs.
- Sectorisation et Recherche de Fuites : Découpage des réseaux en districts (DMA - District Metered Area) couplé à l'utilisation de corrélateurs acoustiques et de pré-localisateurs de fuites.
- Contrôle Qualité : Réseau de laboratoires centraux et régionaux équipés pour des analyses par spectrophotométrie et chromatographie, accrédités selon les normes de potabilité nationales et internationales (OMS).
- Dessalement de l'Eau de Mer (SDEM) : Intégration accrue dans le réseau de distribution des eaux issues des grandes stations de dessalement par osmose inverse construites le long du littoral algérien.


=== L'Unité ADE de Mila et la Station d'Aïn Tine
L'Unité de l'Algérienne des Eaux (ADE) de la wilaya de Mila représente un maillon névralgique de la gestion hydraulique dans l'Est algérien. En raison de sa position géographique, Mila abrite le complexe de Béni Haroun (le plus grand ouvrage hydraulique du pays, d'une capacité de 960 millions de $m^3$), faisant de cette unité territoriale un centre stratégique de production et de transfert d'eau potable @ade_mila.

== Les procédées de traitement
Pour assurer une production d'eau potable continu la chaîne de traitement qui constituée des étapes suivantes:

#figure(image("images/process.png"), caption: [le process])

=== Brise charge et régulation de débit:

L’alimentation en eau brute se fait gravitarement depuis le réservoir tampon (cote 835          cote 791,68).
Une vane de régulation de pression réduit la pression de 4 bars à 1.1 bars environ.

#figure(image("images/shema_brise_charge.png"), caption: [shema d'operation brise charge])

L’obturateur à disque permet de dissiper l’énergie excédentaire de l’eau brute et de cette facon assurer un équilibre hydroulique d’arrivée d’eau.
Une vanne de régulation de débit(vanne papillon automatique) permet d’ajuster le débit suivant une consigne fixée.

#figure(image("images/bassin_brise_charge.png", width: 50%), caption: [bassin de brise charge])

=== bassin d’aération:

Un bassin d’aération de $270m^3$ a été aménagé en aval du brise charge permettant un temps de contact d’au moins 3 minutes comme spécifié au cahier des charges.
L’aération de l’eau brute à traiter à pour objectifs:

#figure(image("images/shema_bassin_aeration.png", width: 80%), caption: [shema bassin d'aeration])

- D’assurer l’oxygénation de l’eau brut pour permettre une saturation en $O_2$ dissous nécessaire à l’oxydation de certains éléments minéraux et organiques.
- De permettre aux bactéries nitrifiantes de proliférer (bactéries aérobies)

#figure(image("images/bassin_aeration.png", width: 50%), caption: [bassin d'aeration])

=== la préozonation (préoxydation):

L’ozone est un gaz instable (formule chimique $O_3$). C’est un oxydant très puissant et est utilisé en pré-oxydation pour :
- Déstructurer les particules colloïdales et améliorer les performances de la coagulation/floculation et de ce fait le fonctionnement de la décantation
- Oxydation des matières organiques et notamment celles responsables des gouts et odeurs (micro-algues).
- Oxydation du fer et du manganèse

Le gaz ozoné est envoyé dans des cuves de contact (temps de contact de 3 minutes) et est diffusé dans l’eau par des domes poreux, permettant la diffusion en fines bulles et donc une activité supérieure.

#figure(image("images/shema_preozonation.png", width: 80%), caption: [shema de pre-ozonation])

=== Coagulation et floculation:

Les MES et particules en suspension (colloïdes) se repoussent naturellement les unes avec les autres de part leur charge superficielle.
Dans l’objectif de les rapprocher les unes aux autres, on ajoute un coagulant minéral: la sulfate d’alumine qui neutralise les charges de surface des colloïdes.
Pour être efficace, le coagulant doit être immédiatement dispersé dans l’eau pour obtenir une répartition homogène avant la formation d’hydroxydes d’aluminium. Pour cela, on agite fortement le mélange eau-coagulant grâce à un agitateur de vitesse de rotation élevé.
L’injection du sulfat d’alumine a aussi une influence sur le PH de l’eau.
L’agglomération des particules colloïdales neutralisées est appelée la floculation. Les microflocs s’agrègent ensuite en flocons plus volumineux et décontables. Cette floculation est améliorée par l’ajout d’un réactif  «adjuvant de floculation».
Dans le cas de la station d’Ain Tinn, l’adjuvant utilisé est un polymère anionique, injecté après la cuve de coagulation.

#figure(image("images/shema_coagulation.png", width: 60%), caption: [shema de coagulation])

La concentration en sulfate d’alumine et polymère sont déterminées en laboratoire (jar test) afin d’obtenir le meilleur rendement (amélioration de la turbidité).
Le PH joue aussi un rôle très important sur l’efficacité de la Coagulation – Floculation. Le PH optimum est comprise entre 6,5 et 7,4.
Bien que le sulfate d’alumine fasse naturellement baisser le pH. Un ajout d’acide sulfurique (baisse du PH) ou de lait de chaux(augmentation du pH) s’avère nécessaire dans certains cas les concentrations sont déterminées en laboratoire. Suivant la qualité de l’eau brute à traiter.
L’ajout éventuel de permanganate de potassium est aussi nécessaire dans certains cas, notamment pour oxide par l’ozone en pré-ozonation.


#figure(image("images/shema_reactif.png", width: 80%), caption: [shema de reactifs ajoutes])


=== La décantation :

Les flocs obtenus en phase de coagulation/floculation vont naturellement décanter du fait de leur pois plus important. La vitesse de décantation varie en fonction de la taille des flocs ainsi que du type de décanteur prévu (statique ou dynamique).
Les décanteurs sont des ouvrages spécialement conçus pour permettre aux flocs d’être récupérés et concentrés afin d’être ultérieurement évacués.
Sur la station d’Ain Tinn, des décanteurs de type pulsateur ont été mis en place et permettent une vitesse de décantation de 2.46m/h.
Ces décanteurs sont à lit de boue pulsée et permettent des rendements 2 à 3 fois supérieur que pour un décanteur statique.

#figure(
  image("images/shema_decantation.png", width: 80%),
  caption: [Temps nécessaires a la décantation naturel sur 1 mètre de particules de différentes tailles],
)

+ l’eau brute est envoyée dans la cloche à vide
+ Un ventilateur permet au niveau d’eau dans la cloche de monter jusqu’à un certain niveau. Un interrupteur déclanche alors la mise à l’atmosphère de la cloche en dépression.
+ L’eau pénètre avec une grande vitesse dans le décanteur par les tuyaux de répartitions.
+ Les flocs restent au fond du décanteur formant progressivement un lit de boue. Servant de « filtre » à l’eau arrivant progressivement.
+ Le lit de boue augmente jusqu’à un déversoir pour tombes gravitairement dans des concentrateurs.
+ Des purges sont effectuées pour permettre l’évacuation des boues.
+ L’eau décantée est évacuée en surface.


#figure(
  image("images/bassin_decantation.png", width: 80%),
  caption: [bassin de décantation],
)

=== La filtration biologique:

Les filtres biologiques installés sur la station d’Ainn Tinn permettent la nitrification de l’ammonium présent dans l’eau (transformation en nitrates) par voie biologique selon les réaction suivantes:

#figure($N H_4^- + 3/2 O_2 -> N O_2^- + 2H^- + H_2O$, caption: [formation de nitrites], kind: math.equation)

#figure($N O_2^- + ½ O_2 -> N O_3^-$, caption: [formation de nitrates], kind: math.equation)

Cette nitrification se réalise sous l’influence de bactéries spécifiques. Ces bactéries sont aérobies (elles nécessitent de l’oxygène) pour pouvoir se développer. Elles se développent autour de petites billes d’argile expansée (la biolite- 2.7mm de diamètre) de grande superficie spécifique (de l’ordre de 700 m2/m3).
Si la quantité d’oxygène dans l’eau n’est pas suffisante, un apport d’oxygène supplémentaire est apporté. Il faut environ 3.6 ppm d’oxygène dissous dans l’eau pour nitrifier 1ppm d’ammonium
L’oxygène supplémentaire apporté se fait par injection d’air sous le plancher des filtres par des membranes trouées (1.2 mm de diamètre) : les oxazurs.
La cinétique de la nitrification dépend de la température mais:


- Si Tc augmente, l’oxygène dissous diminue
- Si Tc diminue, la réaction de nitrification diminue.

La cinétique de nitrification peut donc être  égale à 2 températures différentes.
La formation de la biomasse permettant une nitrification nécessite cependant un certain temps (de 1 mois à 3 selon les cas)
Ces filtres jouent aussi un rôle de filtre à MES (non décantées). L’eau en sortie des filtres biologiques sera d’une turbidité plus faible que l’eau décantée.
Lorsque les filtres présentent une perte de charge importante, il est nécessaire de procéder à leur lavage. Des lavages à l’air + eau sont réalisés et les eaux sales de lavage sont réintroduites en tête de station.

#figure(image("images/shema_filtration_bio.png", width: 80%), caption: [filtration biologique])

#figure(image("images/bassin_filtration_bio.png", width: 80%), caption: [bassin de filtration biologique])

=== Post ozonation

La post-ozonation est utilisée pour oxyder les matières organiques non oxydées lors des phases précédentes et des odeurs, certains pesticides et autres toxines algales.
Aussi, le temps de contact en post-ozonation est supérieur à celui de la pré-ozonation (10 minutes environ contre 3 minutes en pré-ozonation) afin d’assurer une désinfection quasi –complète de l’eau.
L’efficacité de l’ozone dépend du PH de l’eau (elle diminue si le PH augmente) et de la température.


Les matières organiques contribuent à la demande en ozone et entrent en compétition avec les micro-organismes + bactéries. C’est pourquoi il est nécessaire d’avoir un résiduel d’ozone (entre 0.2 et 0.4 ppm) pour s’assurer d’une bonne désinfection.

#figure(
  image("images/ozonation_diagram_simple.png", width: 30%),
  caption: [ozonation, description simplifiee @article_ozonation],
)
#figure(image("images/ozonation_process.png", width: 60%), caption: [procedure d'ozonation @article_ozonation])

=== Filtration sur charbon actif en grain (CAG) :


La filtration sur charbon CAG permet la rétention des particules fines oxydées en post-ozonation ainsi que les particules (micro-algue) responsables des mauvais goût et odeurs. L’eau ainsi filtrée possède une turbidité plus faible.
Le charbon actif en grain est un matériau qui a subit un traitement thermique spécifique (à plus de 100°C) qui permet à sa structure d’obtenir une grande porosité. Sa taille est d’environ 1.2mm.
Les molécules organiques de tout type se fixent à la surface du charbon, mais aussi d’autres composés comme le charbon et certains métaux lourds.


#figure(image("images/cag.jpg", width: 100%), caption: [diagram de cag 1 @cag])
#figure(image("images/cag_2.jpg", width: 60%), caption: [diagrame de cag 2 @cag_2])
#figure(image("images/cag_shema.png", width: 100%), caption: [mechanisme de fonction de cag @article_cag])


Lorsque le filtre est encrassé par les matières organiques retenues sur le charbon, un lavage à l’air +eau est nécessaire (la fréquence dépend de la perte de charge observée).les eau sales de lavage sont réintroduites en tête de station.
Ces filtres CAG possèdent une vitesse de filtration relativement importante de l’ordre de 7.3m3/m2/h et permettent la filtration d’eau relativement chargée (jusqu’à70 UNT) en effectuant des lavages chaque 48 heure.
La durée de vie du GAC dépend de la charge de l’eau en MO et MES (6 mais à 1 an pour les eaux peu chargées).

=== Désinfection final (chloration):


Bien que l’eau post-ozonée soit stérile (résiduel supérieur à 0.2ppm) l’injection de chlore au niveau du réservoir d’eau traitée est nécessaire pour s’assurer de l’absence totale d’éléments pathogens.
La solution d’eau charge peut être préparée :
- à partir du chlore gaz .
- à partir de l’unité d’électrochloration (fabrication de l’eau de javel).
la quantité de chlore à injecter est obtenu en laboratoire à partir d’un «test de demande en chlore» qui consiste à injecter progressivement du chlore dans l’eau et de mesurer le chlore résiduel (chlore non consommé) donc actif
Le chlore résiduel assure une protection contre des contaminations extérieure et doit être supérieure à 0.3 ppm au niveau de stokage.

Le chlore doit etre introduit dans l’eau très rapidement (ici dans une chambre de contact) pour permettre au chlore injecté de se mélanger de façon homogène. Le temps de contact dépend de la cible visée et est supérieur à 30 minutes.


L’efficacité du chlore dépend du PH et de la température :
- Diminue si PH augmente.
- Augmente si la température augmente.

Des analyseurs de chlore sont installés au niveau des chambres de chloration er des réservoirs pour contrôler en permanence la concentration en chlore résiduel.
Le facteur C × T (concentration × temps de contact) permet d’avoir une idée générale sur la concentration nécessaire à la désinfection de certains éléments pathogènes.

#figure(
  table(
    columns: 5,
    "Espaces", "E.coli", "Poliovirus", "Rotavirus", "Giardia lambia",
    "CT(mg.min/litre)", "0.03", "1.1", "0.01", "15",
  ),
  kind: table,
  caption: [Données à PH 7 et à 25˚c],
)


#figure(
  table(
    columns: 5,
    "Espaces", "E.coli", "Poliovirus", "Rotavirus", "Giardia lambia",
    "CT(mg.min/litre)", "95", "770", "3810", "2200",
  ),
  kind: table,
  caption: [Données à PH 9 et à 20˚c],
)



#figure(image("images/chlore_injection.png", width: 80%), caption: [injection de chlore])

== La problématique

Dans le milieu industriel moderne, la maintenance conditionnelle occupe une place prépondérante au sein des stratégies de maintenance préventive. En permettant de suivre l'évolution de l'état réel des équipements, elle s'avère cruciale pour anticiper les défaillances, maximiser la disponibilité opérationnelle des outils de production et, par conséquent, renforcer la compétitivité de l'entreprise sur le marché.
Cependant, une grande partie de cette surveillance repose encore sur des méthodes « sensorielles », c'est-à-dire l'inspection visuelle, auditive ou tactile réalisée directement par les opérateurs et les techniciens. Bien que précieuse, cette approche humaine montre rapidement ses limites. Les premiers stades d'une défaillance se manifestent souvent par des micro-indicateurs (faibles variations de température, micro-vibrations, anomalies électriques subtiles) imperceptibles par les sens biologiques.
Dès lors, un défi majeur se pose : comment dépasser les limites de la surveillance humaine pour détecter ces signaux faibles avant qu'ils ne provoquent une panne majeure ?
Pour répondre à cet impératif, il devient nécessaire d'introduire des outils technologiques capables de suppléer ou d'automatiser ces tâches d'inspection. L'enjeu est de collecter ces micro-indicateurs, de les interpréter avec précision et, idéalement, de prédire les comportements futurs des machines. Une telle anticipation permettrait non seulement d'ajuster les gammes de maintenance corrective, mais aussi de déclencher automatiquement des protocoles de sauvegarde (tels que la lubrification forcée ou le refroidissement d'urgence).
Face à ce constat, une question centrale guide notre travail de recherche : Comment l'intégration des technologies de l'Internet des Objets (IoT) et de l'intelligence artificielle peut-elle moderniser la maintenance conditionnelle au sein de l'entreprise ?
Pour y répondre, nous posons l'hypothèse qu'un système de surveillance continue basé sur une architecture IoT — combinant des capteurs physiques, un microcontrôleur pour la collecte de données en temps réel, et un serveur centralisé exploitant des algorithmes d'apprentissage automatique (Machine Learning) — constitue une solution robuste et efficace pour traiter les données industrielles et automatiser les diagnostics.



#bibliography("refs.bib")
