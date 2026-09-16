# Carnet d'ordre — expérience ORB à effet de levier vs Nasdaq-100

Journal de bord d'une expérience de trading de 6 mois menée sur **compte DEMO eToro**,
qui mesure si une stratégie *Opening Range Breakout* (ORB) à effet de levier bat le Nasdaq-100.

- `journal/BILAN.md` — cumuls, régénérés chaque soir
- `journal/AAAA-MM-JJ.md` — un fichier par jour de bourse (ouverture le matin, clôture le soir)
- `journal/RAPPORT-AAAA-MM.md` — rapport d'analyse mensuel
- `journal/calcul_bilan.py` — calcul des cumuls, relit les journaux bruts
- `journal/rapport_mensuel.py` — calcul des chiffres mensuels, relit les journaux bruts

---

## ⚠️ Convention de branches — à lire avant toute écriture

**La branche de référence de ce dépôt est `main`. Elle est la seule source de vérité.**

Ce dépôt est alimenté par plusieurs sessions d'agent automatiques (ouverture le matin,
clôture le soir, rapport mensuel). Chaque session se voit attribuer sa propre branche de
travail par son environnement d'exécution. **Une branche de travail n'est jamais une
destination finale** : si le travail y reste, la session suivante — qui démarre depuis
`main` — ne le verra pas, repartira d'un historique incomplet, et la divergence se
reproduira indéfiniment.

### Règle pour toute session travaillant sur ce dépôt

1. **Avant d'écrire quoi que ce soit**, se synchroniser sur `main` :
   ```bash
   git fetch origin main
   git checkout -B <ta-branche-de-travail> origin/main
   ```
   Vérifier que les journaux des séances précédentes sont bien présents.
   S'il en manque, c'est que `main` n'a pas été mis à jour — corriger avant de continuer.

2. **À la fin de la session**, reporter le travail sur `main` :
   ```bash
   git fetch origin main
   git checkout -B main origin/main
   git merge --no-ff <ta-branche-de-travail>
   git push -u origin main
   ```

3. Ne jamais laisser une séance consignée uniquement sur une branche de travail.

### Pourquoi la fusion est sans risque pour `BILAN.md`

`BILAN.md` est intégralement régénéré par `journal/calcul_bilan.py` à partir des fichiers
journaliers bruts, jamais à partir de lui-même. Une fusion ne peut donc pas détruire
d'information : au pire `BILAN.md` est momentanément périmé, et la clôture suivante le
recalcule à l'identique depuis les journaux. **La crainte d'écraser un historique
reconstitué en fusionnant n'est pas fondée** — ce qui compte, ce sont les fichiers
`journal/AAAA-MM-JJ.md`, et une fusion les préserve tous.

### Historique

Les branches `claude/gifted-maxwell-*` et `claude/trusting-archimedes-*` sont les branches
de travail des sessions antérieures à la mise en place de `main` (2026-09-16). Leur contenu
a été intégralement vérifié et repris dans `main` : aucune donnée de trading n'a été perdue.
Elles sont conservées à titre d'archive et ne doivent plus servir de base de travail.
