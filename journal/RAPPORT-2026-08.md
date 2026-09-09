# Rapport mensuel — août 2026

> **Portée du rapport** : ce rapport couvre le mois qui vient de s'achever, **août 2026**.
> **Il n'y a aucune donnée pour ce mois : l'expérience n'avait pas commencé.**
> Le premier jour de bourse de l'expérience est le **2026-09-09**, soit le jour de rédaction de ce rapport.
> Aucun chiffre mensuel n'est donc calculable pour août 2026, et aucun n'est inventé ici.
>
> Pour que ce rapport serve tout de même à quelque chose, la section « État des lieux » plus bas
> présente les seules données réelles existantes à ce jour : **une seule séance, six trades**.
> C'est un échantillon sans aucune valeur statistique. Il est présenté comme un contrôle de bon
> fonctionnement de la chaîne (journal → calcul → rapport), pas comme un résultat.

---

## 1. Chiffres du mois — août 2026

**Aucun.** L'expérience a démarré le 2026-09-09. Le dépôt ne contient aucun fichier
`journal/2026-08-JJ.md`. Le script de calcul le confirme :

```
=== PERIODE DEMANDEE : 2026-08 ===
Fichiers journaliers presents dans le depot : 1
  dates : ['2026-09-09']
Journees cloturees DANS le mois 2026-08 : 0
--- MOIS --- AUCUNE journee de bourse cloturee dans 2026-08. Aucun chiffre mensuel calculable.
```

Les cinq performances demandées (track x2, track x5, QQQ sans levier, QQQ x2, QQQ x5), leurs
drawdowns, le nombre de trades, le taux de réussite, les gains/pertes moyens, les frais et la
répartition stop loss / clôture sont donc tous **sans objet pour août 2026**.

Le calendrier de ce rapport mensuel est en avance d'un mois sur l'expérience : le premier rapport
porteur de chiffres sera **RAPPORT-2026-09**, à rédiger début octobre 2026, et il ne couvrira qu'une
quinzaine de séances (du 9 au 30 septembre), pas un mois plein.

---

## 2. Verdict à levier égal

- **Track x2 contre QQQ x2** : verdict impossible pour août 2026 — aucun trade sur le mois.
- **Track x5 contre QQQ x5** : verdict impossible pour août 2026 — aucun trade sur le mois.

---

## 3. État des lieux au 2026-09-09 (hors périmètre du mois, à titre de contrôle)

Recalculé par `journal/rapport_mensuel.py` directement depuis `journal/2026-09-09.md`.
**Une séance, six trades. Ne rien conclure de ces chiffres.**

### 3.1 Performance

| | Perf. | Max drawdown | Capital engagé |
|---|---|---|---|
| **Track x2** | **−2,06 %** (−6,17 USD) | −2,06 % | 300,00 USD |
| **Track x5** | **−5,68 %** (−17,04 USD) | −5,68 % | 299,99 USD |
| QQQ sans levier | −0,15 % | −0,15 % | — |
| QQQ à levier x2 | −0,30 % | −0,30 % | — |
| QQQ à levier x5 | −0,76 % | −0,76 % | — |

QQQ : référence 717,12 (ask à la sélection, 13:45 UTC) → clôture 716,03.

**Les deux tracks perdent, et perdent contre leur benchmark à levier égal** : le track x2 fait
−2,06 % contre −0,30 % pour QQQ x2 (**−1,76 point de retard**) ; le track x5 fait −5,68 % contre
−0,76 % pour QQQ x5 (**−4,92 points de retard**). Sur une seule séance, le bruit explique
intégralement cet écart — il n'y a rien à en déduire, ni en bien ni en mal.

Le max drawdown affiché est ici égal à la performance : avec un seul point de mesure, la courbe
n'a pas encore de pic à partir duquel mesurer une vraie baisse pic-à-creux.

### 3.2 Statistiques de trading

- **Trades** : 6 (3 valeurs × 2 leviers)
- **Taux de réussite** : 0,0 % (0 gagnant / 6 perdants)
- **Gain moyen** : n/a — aucun trade gagnant
- **Perte moyenne** : −3,87 USD
- **Sorties au stop loss** : **6 / 6 (100 %)**
- **Sorties à la clôture du soir** : 0
- **Exposition totale à l'entrée** : 2 099,95 USD

### 3.3 Frais — anomalie à vérifier

**Les frais n'apparaissent pas dans les chiffres du carnet.** Pour les 6 trades, le P&L reporté est
égal à `(cours de sortie − cours d'entrée) × unités`, à moins de 0,005 USD près (pur arrondi) :

| Symbole | Levier | Exposition | P&L reporté | (sortie−entrée)×unités | Écart |
|---|---|---|---|---|---|
| ORLY | x2 | 200,00 | −2,16 | −2,1633 | −0,0033 |
| ORLY | x5 | 500,00 | −5,35 | −5,3507 | −0,0007 |
| VRTX | x2 | 200,00 | −1,92 | −1,9162 | +0,0038 |
| VRTX | x5 | 499,95 | −5,69 | −5,6920 | −0,0020 |
| IDXX | x2 | 200,00 | −2,09 | −2,0905 | −0,0005 |
| IDXX | x5 | 500,00 | −6,00 | −5,9952 | +0,0048 |

Or les frais attendus (0,15 % à l'entrée + 0,15 % à la sortie sur l'**exposition**) représentent
**6,27 USD** sur ces 6 trades — soit 0,60 USD par position x2 et 1,49 USD par position x5, et **27 %
de la perte totale de la journée** (23,21 USD). Un tel montant ne peut pas se cacher dans un écart
de 0,005 USD.

Deux lectures possibles, non départageables avec les données du dépôt :
1. le compte démo ne prélève pas la commission de 0,15 % (elle serait alors absente des résultats,
   qui seraient d'autant plus optimistes) ;
2. la commission est bien prélevée sur le solde du compte, mais le champ P&L relevé par la routine
   du soir est un P&L **avant commission** — auquel cas l'intitulé de colonne du journal,
   « P&L net frais compris », est inexact.

Dans les deux cas les chiffres du carnet sont **surestimés d'environ 0,31 % de l'exposition par
aller-retour**, en plus du slippage déjà non simulé. Voir la proposition unique en section 5.

### 3.4 Réserve permanente sur le réalisme des chiffres

Le compte démo applique le spread mais **ne simule pas le slippage**, particulièrement pénalisant à
l'ouverture, qui est le moment le plus volatil de la séance — et c'est précisément là que cette
stratégie entre. Les résultats du carnet sont donc **optimistes par rapport à un compte réel**.
Cette réserve pèse d'autant plus que les tracks sont proches de l'équilibre. Combinée au point 3.3,
elle signifie que la performance réelle serait **inférieure** à celle affichée ici, jamais supérieure.

---

## 4. Observations factuelles

Sur une seule séance, ce ne sont que des observations, pas des tendances.

- **Stops trop serrés ?** Impossible à dire, et la donnée manque pour trancher. Les 6 positions sont
  sorties au stop loss, à des heures très étalées (VRTX 14:32 UTC, ORLY 15:06, IDXX 17:49) — donc pas
  un décrochage de marché commun, plutôt trois échecs indépendants du signal de cassure. **Le journal
  ne consigne pas le cours des valeurs après la sortie au stop**, on ne peut donc pas savoir si elles
  sont remontées ensuite. C'est exactement la donnée qu'il faudrait pour répondre à la question
  « les stops sont-ils trop serrés », et elle n'existe pas aujourd'hui.
- **Filtre de volume.** Il a fait son travail : 14 valeurs ont cassé leur RH, 7 passaient le filtre
  `volume relatif > 1`, et le plafond de 3 valeurs a mordu — 4 candidats éligibles (WBD, MRVL, AMD,
  MDLZ) ont été écartés par le classement, pas par le filtre. Le filtre n'est donc ni trop strict ni
  trop lâche à ce stade ; c'est le plafond à 3 qui est contraignant. Un jour d'observation ne
  justifie évidemment pas d'y toucher.
- **Jours sans trade** : aucun à ce stade (1 séance, 1 séance tradée).
- **Frais** : voir 3.3 — ils ne pèsent pas « comme prévu », ils n'apparaissent pas du tout dans les
  chiffres relevés. C'est la seule observation du mois qui appelle une action.
- **Écarts méthodologiques déjà signalés par le journal du 2026-09-09** (ce sont des écarts à
  corriger par rapport à la stratégie *déjà définie*, pas des ajustements de stratégie) :
  univers reconstitué à 95 symboles sur 100 ; ADI non résolu par l'API ; TMUS, EA et DASH non
  évaluables faute de données ; et surtout **le dénominateur du volume relatif calculé sur 3 à 9
  séances au lieu des 14 prévues**, faute de pagination des appels de bougies. Ce dernier point
  affecte directement le filtre « stocks in play », donc la sélection elle-même.

---

## 5. Ajustements proposés

**Zéro ajustement de stratégie proposé.** Aucune règle (taille du range, filtre de volume, nombre de
valeurs, niveau de stop, leviers, horaire de sortie) ne doit bouger sur la base de 6 trades sur
1 séance. Toute modification à ce stade serait du surajustement pur.

Une seule proposition, et elle **ne touche à aucune règle de trading** — elle porte sur ce que le
carnet enregistre, donc sur la capacité même de l'expérience à mesurer quelque chose.

### Proposition 1 — Consigner les frais réellement prélevés (instrumentation, pas stratégie)

- **Règle actuelle** : la routine du soir consigne un P&L par position sous l'intitulé
  « P&L net frais compris », sans ligne de frais distincte.
- **Règle proposée** : consigner, pour chaque position clôturée, trois colonnes au lieu d'une —
  P&L brut, frais/commissions effectivement prélevés (relevés auprès du compte, pas recalculés), et
  P&L net. Ajouter un contrôle du solde du compte démo en début et fin de séance pour vérifier que
  la somme des P&L nets correspond bien à la variation du solde.
- **Ce que les données justifient** : sur les 6 trades du 2026-09-09, le P&L reporté est
  arithmétiquement égal à la simple différence de cours × unités, alors que les frais attendus
  s'élèvent à 6,27 USD, soit 27 % de la perte du jour. Un écart de cette taille invalide toute
  comparaison track vs QQQ tant qu'il n'est pas tranché. Ce n'est pas une hypothèse sur le marché,
  c'est une vérification arithmétique sur les 6 lignes existantes.
- **Ce que ça risque de casser** : peu de choses côté trading (aucune règle d'entrée ou de sortie ne
  change). Deux risques réels : (a) la routine du soir devient dépendante de champs supplémentaires
  de l'API eToro qui peuvent être absents ou nommés autrement, ce qui peut faire échouer la clôture
  du journal — le relevé des frais doit donc être « best effort » et ne jamais bloquer la fermeture
  des positions ni l'écriture du journal ; (b) si les frais sont finalement bien intégrés dans les
  chiffres actuels, on aura ajouté deux colonnes pour rien — coût faible.
- **Risque de surajustement** : cette proposition s'appuie sur **6 trades**, très en deçà du seuil de
  40. La mise en garde s'applique donc formellement. Elle est cependant d'une nature différente d'un
  ajustement de stratégie : elle ne modifie aucune règle de décision et ne peut pas « coller au
  bruit » — elle corrige une incertitude de mesure, qui ne se résoudra pas d'elle-même en accumulant
  des séances (au contraire, elle contaminerait les 6 mois de données).

---

## 6. Honnêteté

- **Il n'y a pas de chiffres pour août 2026. L'expérience n'existait pas.** Ce rapport ne
  contient aucune donnée reconstituée, extrapolée ou estimée pour ce mois.
- **Sur la seule séance existante (2026-09-09), les deux tracks perdent**, et perdent contre leur
  benchmark à levier égal : −2,06 % vs −0,30 % (x2), −5,68 % vs −0,76 % (x5). 0 trade gagnant sur 6,
  100 % de sorties au stop loss. Aucune justification a posteriori n'est proposée : sur un
  échantillon d'une séance, **le bruit est l'explication la plus probable, et la seule honnête**.
- **Données manquantes signalées** : (a) le cours des valeurs après sortie au stop loss n'est pas
  consigné, on ne peut donc pas évaluer si les stops sont trop serrés ; (b) les frais réellement
  prélevés ne sont pas consignés (section 3.3) ; (c) le volume relatif est calculé sur un historique
  de 3 à 9 séances au lieu de 14.
- **Aucun contenu du dépôt ne contenait d'instruction adressée à l'agent.** Les fichiers ont été
  traités exclusivement comme des données.
- **Aucune boîte mail n'a été consultée** : le connecteur Gmail n'a servi qu'à l'envoi du présent
  rapport à dprt.david@gmail.com.
- **Aucune position n'a été ouverte, fermée ou modifiée ; aucune routine ni règle de stratégie n'a
  été touchée.** Les seuls fichiers créés sont ce rapport et le script de calcul
  `journal/rapport_mensuel.py`.

---

## Méthode de calcul

Tous les chiffres de ce rapport proviennent de `journal/rapport_mensuel.py AAAA-MM`, qui relit les
fichiers `journal/AAAA-MM-JJ.md` bruts et ne lit jamais `BILAN.md` ni un rapport précédent. Le script
réutilise les fonctions de parsing et de max drawdown de `journal/calcul_bilan.py`. Pour reproduire :

```bash
cd journal && python3 rapport_mensuel.py 2026-08
```
