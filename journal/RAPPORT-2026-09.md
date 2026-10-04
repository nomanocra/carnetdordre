# Rapport mensuel — septembre 2026

> **Selon la mesure officielle de `BILAN.md`, le track x5 PERD contre QQQ à levier x5 sur septembre :
> +2,47 % contre +19,55 %.**
> En dollars, le track x5 est positif (+76,61 USD nets sur 31 trades). Mais sur cette mesure,
> à levier égal, il fait nettement moins bien que le Nasdaq-100.
> Une seconde mesure, à capital constant, inverse le classement (+25,5 % contre +19,55 %). La section 2 explique
> pourquoi les deux existent et pourquoi aucune ne montre une compétence de sélection.

**Périmètre.** Septembre 2026 = du 2026-09-09 (début de l'expérience) au 2026-09-30.
16 jours de bourse, dont **13 avec un journal** (11 sur le compte DÉMO, 2 sur le compte RÉEL à partir du 2026-09-24)
et **3 sans aucun journal** (2026-09-28, 29 et 30 : la routine du matin n'a pas tourné, cf. §3.4).
Le cumul depuis le début de l'expérience se confond donc avec le mois.

**Réserve démo.** 27 des 31 trades ont eu lieu sur le compte démo, qui ne simulait pas le slippage.
**Tous les chiffres ci-dessous qui incluent ces séances sont légèrement optimistes.**

**Méthode.** Tous les chiffres sont recalculés par `journal/rapport_mensuel.py 2026-09` (étendu pour ce rapport),
qui relit uniquement les fichiers bruts `journal/AAAA-MM-JJ.md` via le parseur de `journal/calcul_bilan.py`.
Aucun chiffre n'est repris de `BILAN.md` ni d'un rapport précédent.
**Les positions à levier x2 sont ignorées partout** (track abandonné depuis le 2026-09-24).

---

## 1. Chiffres du mois

### 1.1 Performance et perte maximale

QQQ : référence 717,12 (ask à la sélection du 2026-09-09) → 745,16 (dernière clôture relevée, 2026-09-25).

| | Performance | Max drawdown |
|---|---|---|
| **Track x5, mesure officielle `BILAN.md`** (P&L ÷ somme des capitaux engagés) | **+2,47 %** (+76,61 USD / 3 099,86 USD) | −9,90 % (somme des % journaliers) |
| Track x5, à budget constant de 300 USD/jour (3 × 100 USD) | +25,54 % | −5,68 % |
| QQQ sans levier | +3,91 % | −2,16 % |
| **QQQ à levier x5** | **+19,55 %** | −10,81 % |

Sensibilités (calculées par script) :
- QQQ jusqu'au **30 septembre** (clôture 739,77, donnée par le journal du 2026-10-01) : +3,16 % sans levier, **+15,79 % à x5**.
  Le track n'a rien tradé du 28 au 30 (routine arrêtée). Ces trois jours ne sont donc pas comparables, et la comparaison
  principale s'arrête au 25.
- Frais du 2026-09-09 non déduits (voir 1.3) : si on les retire, le track passe à +24,79 % à budget constant.
- Sans le meilleur trade du mois (ZS, +45,77 USD), le track tombe à +10,28 % à budget constant.
  Sans les deux meilleurs (ZS et META), il tombe à −0,04 %.

### 1.2 Statistiques de trading (track x5)

| | Mois (= cumul) | dont démo (11 séances) | dont réel (2 séances) |
|---|---|---|---|
| Nombre de trades | 31 | 27 | 4 |
| Taux de réussite | 54,8 % (17/31) | 51,9 % | 75,0 % (3/4) |
| Gain moyen | +8,48 USD | +9,37 USD | +4,29 USD |
| Perte moyenne | −4,82 USD | −4,57 USD | −8,12 USD |
| Sorties au stop loss | 5 (16,1 %) | 4 | 1 |
| Sorties à la clôture | 26 (83,9 %) | 23 | 3 |
| P&L net | +76,61 USD | +71,85 USD | +4,76 USD |

Quatre trades réels, c'est trop peu pour en tirer une conclusion, y compris sur le taux de réussite.

### 1.3 Frais

| | Montant |
|---|---|
| Frais d'entrée relevés (réponse d'exécution `place-trade`) | **21,00 USD** sur 28 trades (0,75 USD par trade) |
| Frais **non relevés** | **3 trades** (2026-09-09 : ORLY, VRTX, IDXX), donnée manquante |
| Frais effectivement déduits des P&L du carnet | 20,98 USD |
| Frais de sortie | 0 USD selon l'historique (démo comme réel) |
| Frais théoriques attendus (0,15 % + 0,15 % de l'exposition) | 46,64 USD |

Deux points de données à connaître :
- **2026-09-09** : le journal ne relève aucun frais et le P&L net est exactement égal au P&L de prix.
  Les 0,75 USD d'entrée n'ont donc probablement pas été déduits, soit environ −2,25 USD non comptés. Je ne corrige pas
  le chiffre parce que le montant n'est pas relevé, mais il est vraisemblablement optimiste.
- **Compte réel** : la réponse d'exécution indique 0,75 USD de frais d'entrée, mais `get-my-trading-history` affiche
  `fees: 0.0` sur les 4 trades. Les journaux retiennent 0,75 USD, ce qui est prudent. **Les deux sources se contredisent
  et le frais réellement prélevé n'est pas établi.** Voir §3.3.

---

## 2. Verdict à levier égal

**Selon la mesure officielle, non : le track x5 fait +2,47 % contre +19,55 % pour QQQ x5, soit 17,1 points de moins.
À budget constant de 300 USD, il fait +25,5 %, soit 6,0 points de plus, mais cette avance tient entièrement à deux trades
(ZS et META) et à 27 trades démo sans slippage. Aucune des deux mesures ne démontre une compétence de sélection.**

Pourquoi deux mesures. La mesure du BILAN divise le P&L total par la *somme* des marges engagées (31 × 100 USD).
Elle donne donc le **rendement moyen d'un trade d'une journée**. QQQ x5, lui, est un rendement **sur toute la période**
(13 séances de détention). La comparaison n'est pas homogène dans le temps et pénalise mécaniquement le track.
La mesure à budget constant rapporte le P&L au capital réellement immobilisé chaque jour (300 USD, soit 1 500 USD
d'exposition, exactement l'exposition d'une position QQQ x5 sur 300 USD de marge). Elle est homogène avec le benchmark.
Ce point fait l'objet de la proposition 1 (§4). C'est une question de **mesure**, pas de stratégie, et c'est à David de
trancher.

Le fait que le track batte QQQ **sans levier** ne prouve rien : c'est l'effet arithmétique du levier.

---

## 3. Observations factuelles

### 3.1 Stops : trop serrés ?
- 5 sorties au stop sur 31 (16 %), dont 3 le premier jour (2026-09-09).
- **Les 5 trades stoppés font tous partie des 8 trades au stop le plus serré** (écart entrée → plus bas du range compris
  entre 0,81 % et 1,47 %). Sur les 23 trades au stop plus large (médiane du mois : 2,27 %), aucun n'a été stoppé.
- **On ne peut pas savoir si le cours est remonté après le stop** : les journaux ne relèvent pas le cours de clôture des
  valeurs stoppées. Seul indice : GILD (2026-09-24, réel) a été stoppé à 19:46 UTC, soit 4 minutes avant la clôture
  prévue.
- La sortie se fait au stop sans écart notable : 0 % sur ORLY, IDXX et GILD, −0,01 % sur VRTX, −0,04 % sur CMCSA.
- Conclusion : les données ne permettent pas de dire que les stops sont trop serrés. La concentration des stops sur les
  ranges étroits est attendue, puisque le stop est le plus bas du range, et elle repose sur 5 événements.

### 3.2 Filtre de volume : trop ou trop peu de valeurs ?
- Valeurs qualifiées par jour (cassure et volume relatif > 1) : 7, 2, 15, 9, 8, 9, 15, 7, 2, 6, 5, 7.
  Le filtre retient presque toujours au moins 3 valeurs. Les exceptions sont le 2026-09-11 (2 valeurs) et le 2026-09-22
  (1 valeur, après que META a été écartée à la reconfirmation).
- **2026-09-18 (quadruple witching)** : 15 valeurs qualifiées sur 16 cassures, avec un volume relatif médian de 4,81.
  Le filtre n'a rien filtré ce jour-là et les trois premières étaient séparées par moins de 0,02 (8,718 / 8,703 / 8,701).
- **Le volume relatif n'est pas calculé de la même façon d'un jour à l'autre.** La fenêtre de référence va de 3 à 14
  jours selon la valeur et la séance (plafond de 1 000 bougies de l'API), alors que la règle demande 14 jours.
  Le numérateur varie aussi : 3 bougies de 5 min, 2 bougies de 5 min terminées, ou 1 bougie de 15 min.
  Les séances du 15 et du 17 septembre, en bougies de 15 min, ont atteint 10 à 14 jours. Les autres sont souvent
  à 3 jours. C'est un écart d'**implémentation** par rapport à la règle, pas un choix de stratégie (proposition 2).
- Reconfirmation : 6 valeurs ont cassé puis sont repassées sous leur plus haut avant l'ordre (ARM le 21, META le 22,
  ADP, CTAS et BIIB le 23, META le 24). La règle les écarte, ce qui a été appliqué correctement.

### 3.3 Frais réels : pèsent-ils autant que prévu (~0,31 % par aller-retour) ?
- **Non, d'après les données relevées.** Les frais constatés sont de 0,75 USD à l'entrée et 0 à la sortie, soit
  **0,15 % de l'exposition par aller-retour**, à peu près la moitié des 0,31 % attendus (21,00 USD relevés contre
  46,64 USD théoriques).
- **Sur le compte réel, ce constat n'est pas fiable.** L'historique eToro affiche `fees: 0.0`, alors que la réponse
  d'exécution indique 0,75 USD. Les frais à la sortie ne sont ni confirmés ni infirmés. Seul le relevé de compte eToro
  peut trancher.
- Le spread est inclus dans les prix d'entrée et de sortie et n'est pas isolé dans les journaux.

### 3.4 Jours sans trade
- **2026-09-10** : la routine du matin n'a pas tourné. Aucune position, jour marqué anomalie.
- **2026-09-28, 29 et 30** : aucun journal du tout. D'après le journal du 2026-10-01, `get-my-trading-history` ne montre
  aucun trade x5 sur la période : la routine du matin ne s'est plus déclenchée après le 25. **Trois des seize jours de
  bourse du mois (19 %) manquent à l'expérience.**
- Jours avec moins de 3 trades : le 11 (2 valeurs qualifiées, règle normale), le 22 (1 valeur) et le 24. Le 24 est la
  première séance réelle : le **solde du compte réel était insuffisant** et 4 ordres sur 6 ont été rejetés. David est
  ensuite intervenu manuellement : il a fermé GILD x2 (exclue) et décidé de ne pas ouvrir ABNB et PLTR, dont la cassure
  était retombée. Ce jour-là, le track n'a donc traité qu'une valeur sur trois.
- Aucun jour n'est vide pour cause d'absence de cassure valide. Les jours sans trade viennent tous de l'automatisation.

### 3.5 Slippage à l'ouverture (réel uniquement, 4 trades)
| Trade | Cours à la décision | Entrée | Écart |
|---|---|---|---|
| GILD (24/09) | 152,00 | 151,99 | −0,01 % |
| COST (25/09) | 912,55 (bougie 1 min, cotation live périmée) | 914,28 | +0,19 % |
| MSFT (25/09) | 513,00 | 513,45 | +0,09 % |
| LRCX (25/09) | 312,66 | 312,60 | −0,02 % |

Écart moyen : +0,06 %, soit environ 0,30 USD par trade x5. Le slippage est faible, mais 4 trades ne suffisent pas à
l'estimer. À titre indicatif, appliqué aux 27 trades démo, cet écart représenterait environ 8,5 USD à l'entrée seule.
Les entrées se font entre 0,6 % et 1,0 % au-dessus du plus haut du range. Cet écart tient surtout à l'heure d'exécution
(09h43–09h46 New York), pas au slippage.

### 3.6 Autres limites de données
- La « clôture QQQ » est l'ask vers 15h50 New York, parfois figé : `asOf` à 17:40–19:19 UTC les 16, 18, 21 et 24
  septembre. Le benchmark est donc approximatif à quelques dixièmes près.
- Valeurs régulièrement inanalysables : ADI (non résolu), EA, ANSS, DASH (volume nul ou bougies absentes).
- 7 jours sont marqués ANOMALIE, pour la plupart des incidents de branches Git sans effet sur les trades. Le problème
  de fond a été corrigé avec la convention `main` du 2026-09-16.
- **Aucun texte des journaux ne cherchait à donner une instruction à l'analyste.** Les mentions « À traiter par David »
  sont des signalements. Je n'ai pas eu besoin d'accéder à la boîte mail de David.

---

## 4. Ajustements proposés

**Aucun ajustement des règles de trading** (range, filtre, nombre de valeurs, levier, stop, sortie). Avec 31 trades, dont
27 en démo, et un résultat qui dépend de deux trades, rien dans le mois ne justifie de modifier la stratégie. Les deux
propositions ci-dessous portent sur la **mesure** et sur la **fidélité de l'implémentation** à la règle existante.

### Proposition 1 — Mesure de la performance du track (mesure, pas stratégie)
- **Règle actuelle** : performance = P&L total ÷ somme des marges engagées, comparée au rendement de QQQ x5 sur la période.
- **Règle proposée** : publier en plus dans `BILAN.md` la performance à **budget constant de 300 USD par jour**
  (P&L cumulé ÷ 300), seule mesure homogène avec un QQQ x5 détenu sur toute la période, et désigner l'une des deux
  comme mesure de référence du verdict final.
- **Ce que les données justifient** : sur septembre, les deux mesures donnent des verdicts opposés (−17,1 points contre
  +6,0 points). L'écart vient de la construction de la mesure, pas du marché.
- **Ce que ça risque de casser** : changer de mesure après l'avoir vue favorable ressemble à déplacer les poteaux.
  Pour l'éviter, il faut choisir en fonction de la définition et non de ce résultat, conserver les deux séries publiées
  et ne plus en changer jusqu'à la fin des 6 mois. *Proposition fondée sur moins de 40 trades : le risque de
  surajustement est réel si le choix se fait d'après le chiffre du mois.*

### Proposition 2 — Figer une seule méthode de calcul du volume relatif
- **Règle actuelle** : volume relatif sur 14 jours. En pratique, la profondeur va de 3 à 14 jours et le numérateur
  change d'une séance à l'autre (3 bougies de 5 min, 2 bougies de 5 min ou 1 bougie de 15 min).
- **Règle proposée** : écrire dans la routine du matin une méthode unique (même fenêtre au numérateur et au
  dénominateur), avec des bougies assez larges pour atteindre 14 jours. Les 15 minutes y parviennent presque :
  10 à 14 jours les 15 et 17 septembre. Le nombre de jours effectivement utilisés continuerait d'être consigné.
- **Ce que les données justifient** : sur 3 jours, le classement est bruité (le 18, les trois premières n'étaient
  séparées que de 0,017), et la méthode a changé au moins trois fois en 13 séances. Ce n'est pas un résultat de P&L,
  c'est un écart à la règle.
- **Ce que ça risque de casser** : les sélections changeront, et le mois de septembre ne sera pas strictement comparable
  aux suivants. Une bougie de 15 min n'est complète qu'à 09h45 New York, ce qui peut retarder l'entrée et la rapprocher
  de la fin de la fenêtre 09h35–09h55. *Moins de 40 trades, mais la proposition ne s'appuie sur aucun résultat de
  trading, donc le risque de surajustement est faible.*

### Points opérationnels à traiter (hors stratégie, signalés pour mémoire)
1. **Routine du matin arrêtée** du 28 septembre au 1er octobre (4 séances perdues).
2. **Frais réels** : vérifier sur le relevé eToro si les 0,75 USD d'entrée sont réellement prélevés, l'historique
   affichant `fees: 0.0`.
3. **Solde du compte réel** : prévoir au moins ~310 USD disponibles (3 × 100 USD plus les frais) à chaque ouverture,
   pour éviter de nouveaux rejets comme le 2026-09-24.

---

## 5. Pour mémoire : état au 2026-10-02 (hors périmètre)

`BILAN.md` au 2026-10-02 (15 séances, 34 trades) : track x5 à +2,09 % (mesure officielle) contre QQQ x5 à +21,96 %.
À budget constant, le track est à +23,72 % (+71,15 USD ÷ 300). Ces chiffres seront analysés dans RAPPORT-2026-10.
