# BILAN — Expérience ORB à effet de levier vs Nasdaq-100

## Objet

Mesurer, sur **6 mois**, si une stratégie *Opening Range Breakout* (ORB) appliquée avec effet de levier bat le Nasdaq-100 (benchmark : QQQ).

Stratégie de référence : Zarattini, Barbon & Aziz (2024), *A Profitable Day Trading Strategy For The U.S. Equity Market*.

## Cadre

- **Compte** : DEMO eToro exclusivement (cid 7632001). Aucune position sur le compte réel.
- **Univers** : les 100 valeurs du Nasdaq-100.
- **Range d'ouverture** : première bougie de 5 minutes (09h30–09h35, heure de New York). RH = plus haut, RL = plus bas.
- **Filtre « stocks in play »** : volume relatif depuis l'ouverture > 1 (rapporté à la moyenne du même créneau sur les 14 derniers jours).
- **Signal** : cours actuel strictement supérieur à RH.
- **Sélection** : les 3 plus forts volumes relatifs parmi les candidats.
- **Positions** : pour chaque valeur retenue, deux positions longues de 100 USD, l'une à levier x2, l'autre à levier x5, stop loss placé sur RL.
- **Sortie** : clôture de toutes les positions en fin de séance (routine du soir).

## Début de l'expérience

**2026-09-09** (mercredi).

## Méthodologie de calcul

Ce fichier est intégralement régénéré chaque soir par `journal/calcul_bilan.py`, qui relit tous les fichiers `journal/AAAA-MM-JJ.md` depuis le début et recalcule l'ensemble des chiffres à partir des données brutes (jamais à partir de ce fichier lui-même).

- **Performance cumulée des tracks x2 / x5** : somme des P&L nets (frais compris) de tous les trades du track, rapportée à la somme des capitaux engagés sur ce track (non composé — chaque position est un pari indépendant de ~100 USD, pas un capital qui roule).
- **QQQ sans levier depuis le premier jour** : variation du cours QQQ entre la valeur relevée à l'ouverture du premier jour de l'expérience et la clôture du jour considéré.
- **QQQ à levier x2 / x5** : la performance QQQ sans levier multipliée par 2 ou par 5 (exposition identique aux tracks, sans frais de financement ni rebalancement journalier — approximation volontairement simple). C'est cette comparaison, à levier égal, qui mesure une compétence de sélection — battre QQQ sans levier avec du levier ne prouve rien.
- **Max drawdown** : plus forte baisse pic-à-creux de la courbe cumulée (en points de %), recalculée jour après jour.
- **Jours anormaux** : tout journal contenant la mention `ANOMALIE` (journal du matin manquant, fermeture échouée, position orpheline...). Les trades de ces jours restent inclus dans les cumuls (l'argent gagné/perdu est réel) mais le jour reste identifiable.
- **Séances écourtées** : jours de clôture anticipée (13h00 New York). Incluses dans les cumuls mais isolables — l'amplitude des mouvements y est mécaniquement réduite, donc non comparable aux autres jours.

## Tableau récapitulatif

_Dernière mise à jour : 2026-09-22 19:53 UTC — 10 jour(s) de bourse clôturé(s)._

| | Perf. cumulée | Max drawdown | Capital engagé |
|---|---|---|---|
| **Track x2** | +1.25 % | -2.06 % | 2 399.86 USD |
| **Track x5** | +3.14 % | -5.68 % | 2 399.88 USD |
| QQQ sans levier | +4.29 % | -2.16 % | — |
| QQQ à levier x2 (même exposition que le track x2) | +8.59 % | -4.32 % | — |
| QQQ à levier x5 (même exposition que le track x5) | +21.47 % | -10.81 % | — |

**Comparaison à levier égal** : le track x2 perd contre QQQ x2 (+1.25 % vs +8.59 %) ; le track x5 perd contre QQQ x5 (+3.14 % vs +21.47 %).

## Statistiques de trading

- **Jours de bourse écoulés** : 10
- **Nombre de trades** : 48
- **Taux de réussite** : 54.2 %
- **Gain moyen (trades gagnants)** : 6.94 USD
- **Perte moyenne (trades perdants)** : -3.41 USD
- **Jours anormaux** (journal du matin manquant, fermeture échouée, position orpheline) : 5
- **Séances écourtées** (clôture anticipée) : 0
- **QQQ, référence de départ (J1)** : 717.12
- **QQQ, dernière clôture connue** : 747.91

## Suivi

Le détail de chaque séance est consigné dans `journal/AAAA-MM-JJ.md`. Ce fichier agrège les résultats.

### Journal des séances

| Date | Trades | P&L x2 (USD) | P&L x5 (USD) | QQQ clôture | Anomalie | Écourtée |
|---|---|---|---|---|---|---|
| 2026-09-09 | 6 | -6.17 | -17.04 | 716.03 | non | non |
| 2026-09-10 | 0 | 0.00 | 0.00 | 708.76 | oui | non |
| 2026-09-11 | 4 | 1.90 | 4.45 | 715.15 | non | non |
| 2026-09-14 | 6 | 16.15 | 40.12 | 710.80 | oui | non |
| 2026-09-15 | 6 | 0.28 | 0.79 | 703.86 | non | non |
| 2026-09-16 | 6 | -4.74 | -11.64 | 701.62 | oui | non |
| 2026-09-17 | 6 | -1.16 | -2.52 | 717.73 | oui | non |
| 2026-09-18 | 6 | 4.41 | 11.17 | 717.89 | non | non |
| 2026-09-21 | 6 | 19.47 | 50.61 | 740.43 | non | non |
| 2026-09-22 | 2 | -0.25 | -0.63 | 747.91 | oui | non |

