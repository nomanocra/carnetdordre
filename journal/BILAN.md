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

## Suivi

Le détail de chaque séance est consigné dans `journal/AAAA-MM-JJ.md`. Ce fichier agrège les résultats.

### Journal des séances

| Date | Valeurs retenues | Positions ouvertes | Anomalies |
|---|---|---|---|
| 2026-09-09 | ORLY, VRTX, IDXX | 6 | Push et issue refusés (403) ; limites de données documentées |

### Trades anormaux (positions orphelines rattrapées)

Aucun à ce jour.
