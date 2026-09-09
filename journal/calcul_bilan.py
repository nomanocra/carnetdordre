#!/usr/bin/env python3
"""
Recalcule le bilan cumule de l'experience ORB a effet de levier vs QQQ
a partir des fichiers bruts journal/AAAA-MM-JJ.md (jamais a partir d'un
BILAN.md precedent, pour eviter toute propagation d'erreur).

Usage : python3 journal/calcul_bilan.py
Ecrit journal/BILAN.md en entier (section statique + section calculee).
"""

import glob
import os
import re
from datetime import datetime

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))
BILAN_PATH = os.path.join(JOURNAL_DIR, "BILAN.md")


def fr_num(s):
    """Convertit un nombre au format francais ('716,03' ou '-2,16') en float."""
    s = s.strip().replace("−", "-")  # signe moins typographique eventuel
    s = s.replace(" ", "").replace(" ", "")  # espaces insecables (milliers)
    s = s.replace(",", ".")
    return float(s)


def parse_journal_file(path):
    """Extrait les donnees brutes d'un fichier journal/AAAA-MM-JJ.md."""
    with open(path, encoding="utf-8") as f:
        text = f.read()

    date_str = os.path.basename(path)[:-3]

    data = {
        "date": date_str,
        "has_morning": "# Journal d'ouverture" in text,
        "has_closing": "## Clôture" in text,
        "anomaly": "ANOMALIE" in text,
        "shortened": bool(
            re.search(r"S[ée]ance [ée]court[ée]e\*?\*?\s*:\s*oui", text, re.IGNORECASE)
        ),
        "qqq_open": None,
        "qqq_close": None,
        "positions": [],
    }

    # QQQ a l'ouverture (benchmark du matin), format : "ask **717,12**"
    m = re.search(r"##\s*Benchmark.*?ask\s*\*\*([\d.,\s ]+)\*\*", text, re.DOTALL)
    if m:
        data["qqq_open"] = fr_num(m.group(1))

    # QQQ a la cloture, format : "**QQQ clôture** : 716,03"
    m = re.search(r"\*\*QQQ cl[ôo]ture\*\*\s*:\s*([\d.,\s ]+)", text)
    if m:
        data["qqq_close"] = fr_num(m.group(1))

    # Table des positions de la section Cloture : on cherche les lignes
    # "| Symbole | Levier | Entree | Sortie | Investissement | P&L net ... | ... | Sortie via |"
    closing_idx = text.find("## Clôture")
    section = text[closing_idx:] if closing_idx != -1 else ""
    rows = re.findall(r"^\|(.+)\|\s*$", section, re.MULTILINE)
    for row in rows:
        cells = [c.strip() for c in row.split("|")]
        if len(cells) < 8:
            continue
        symbole, levier = cells[0], cells[1]
        if symbole in ("Symbole", "---") or re.match(r"^-+$", symbole):
            continue
        m_lev = re.match(r"x(\d+)", levier)
        if not m_lev:
            continue
        try:
            entree = fr_num(cells[2])
            sortie = fr_num(cells[3])
            invest = fr_num(cells[4])
            pnl = fr_num(cells[5])
        except ValueError:
            continue
        sortie_via = cells[7].lower()
        data["positions"].append(
            {
                "symbole": symbole,
                "levier": int(m_lev.group(1)),
                "entree": entree,
                "sortie": sortie,
                "investissement": invest,
                "pnl_net": pnl,
                "sortie_via": "stop loss" if "stop" in sortie_via else "clôture",
            }
        )

    return data


def load_all_days():
    files = sorted(glob.glob(os.path.join(JOURNAL_DIR, "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].md")))
    return [parse_journal_file(f) for f in files]


def max_drawdown(cumulative_series):
    """cumulative_series : liste de (date, valeur cumulee en %). Renvoie le max drawdown (%, negatif ou 0).
    Le point de depart (avant le premier trade) vaut 0 % et compte comme pic potentiel."""
    peak = 0.0
    mdd = 0.0
    for _, val in cumulative_series:
        if val > peak:
            peak = val
        dd = val - peak
        if dd < mdd:
            mdd = dd
    return mdd


def build_bilan(days):
    closed_days = [d for d in days if d["has_closing"]]

    qqq_baseline = None
    for d in days:
        if d["qqq_open"] is not None:
            qqq_baseline = d["qqq_open"]
            break

    # --- Tracks x2 / x5 : P&L journalier, capital engage, courbe cumulee ---
    tracks = {2: [], 5: []}  # liste de (date, pnl_jour, capital_jour)
    all_trades = []
    for d in closed_days:
        pnl_by_lev = {2: 0.0, 5: 0.0}
        cap_by_lev = {2: 0.0, 5: 0.0}
        for p in d["positions"]:
            lev = p["levier"]
            if lev not in pnl_by_lev:
                continue
            pnl_by_lev[lev] += p["pnl_net"]
            cap_by_lev[lev] += p["investissement"]
            all_trades.append(p)
        for lev in (2, 5):
            tracks[lev].append((d["date"], pnl_by_lev[lev], cap_by_lev[lev]))

    def track_stats(entries):
        total_pnl = sum(pnl for _, pnl, _ in entries)
        total_cap = sum(cap for _, _, cap in entries if cap > 0)
        cum_pct = (total_pnl / total_cap * 100) if total_cap else 0.0
        # courbe cumulee (points de % arithmetique, un point par jour)
        curve = []
        running = 0.0
        for date, pnl, cap in entries:
            day_pct = (pnl / cap * 100) if cap else 0.0
            running += day_pct
            curve.append((date, running))
        mdd = max_drawdown(curve)
        return total_pnl, total_cap, cum_pct, mdd

    pnl_x2, cap_x2, cum_x2, mdd_x2 = track_stats(tracks[2])
    pnl_x5, cap_x5, cum_x5, mdd_x5 = track_stats(tracks[5])

    # --- QQQ : sans levier / x2 / x5 (meme exposition, sans frais de financement) ---
    qqq_curve_unlev, qqq_curve_x2, qqq_curve_x5 = [], [], []
    qqq_last_close = None
    for d in closed_days:
        if d["qqq_close"] is None or qqq_baseline is None:
            continue
        ret_pct = (d["qqq_close"] / qqq_baseline - 1) * 100
        qqq_curve_unlev.append((d["date"], ret_pct))
        qqq_curve_x2.append((d["date"], ret_pct * 2))
        qqq_curve_x5.append((d["date"], ret_pct * 5))
        qqq_last_close = d["qqq_close"]

    qqq_cum_unlev = qqq_curve_unlev[-1][1] if qqq_curve_unlev else 0.0
    qqq_cum_x2 = qqq_curve_x2[-1][1] if qqq_curve_x2 else 0.0
    qqq_cum_x5 = qqq_curve_x5[-1][1] if qqq_curve_x5 else 0.0
    qqq_mdd_unlev = max_drawdown(qqq_curve_unlev)
    qqq_mdd_x2 = max_drawdown(qqq_curve_x2)
    qqq_mdd_x5 = max_drawdown(qqq_curve_x5)

    # --- Stats de trading (tous leviers confondus) ---
    n_trades = len(all_trades)
    wins = [t["pnl_net"] for t in all_trades if t["pnl_net"] > 0]
    losses = [t["pnl_net"] for t in all_trades if t["pnl_net"] <= 0]
    win_rate = (len(wins) / n_trades * 100) if n_trades else 0.0
    avg_gain = (sum(wins) / len(wins)) if wins else None
    avg_loss = (sum(losses) / len(losses)) if losses else None

    n_days = len(closed_days)
    n_anomalies = sum(1 for d in days if d["anomaly"])
    n_shortened = sum(1 for d in days if d["shortened"])

    return {
        "n_days": n_days,
        "n_trades": n_trades,
        "win_rate": win_rate,
        "avg_gain": avg_gain,
        "avg_loss": avg_loss,
        "n_anomalies": n_anomalies,
        "n_shortened": n_shortened,
        "pnl_x2": pnl_x2,
        "cap_x2": cap_x2,
        "cum_x2": cum_x2,
        "mdd_x2": mdd_x2,
        "pnl_x5": pnl_x5,
        "cap_x5": cap_x5,
        "cum_x5": cum_x5,
        "mdd_x5": mdd_x5,
        "qqq_baseline": qqq_baseline,
        "qqq_last_close": qqq_last_close,
        "qqq_cum_unlev": qqq_cum_unlev,
        "qqq_cum_x2": qqq_cum_x2,
        "qqq_cum_x5": qqq_cum_x5,
        "qqq_mdd_unlev": qqq_mdd_unlev,
        "qqq_mdd_x2": qqq_mdd_x2,
        "qqq_mdd_x5": qqq_mdd_x5,
        "closed_days": closed_days,
    }


def fmt(x, decimals=2, suffix=""):
    if x is None:
        return "n/a"
    return f"{x:,.{decimals}f}{suffix}".replace(",", " ")


def fmt_pct(x, decimals=2):
    if x is None:
        return "n/a"
    sign = "+" if x > 0 else ""
    return f"{sign}{x:.{decimals}f} %"


def render_bilan(stats):
    lines = []
    lines.append("# BILAN — Expérience ORB à effet de levier vs Nasdaq-100")
    lines.append("")
    lines.append("## Objet")
    lines.append("")
    lines.append(
        "Mesurer, sur **6 mois**, si une stratégie *Opening Range Breakout* (ORB) "
        "appliquée avec effet de levier bat le Nasdaq-100 (benchmark : QQQ)."
    )
    lines.append("")
    lines.append(
        "Stratégie de référence : Zarattini, Barbon & Aziz (2024), "
        "*A Profitable Day Trading Strategy For The U.S. Equity Market*."
    )
    lines.append("")
    lines.append("## Cadre")
    lines.append("")
    lines.append("- **Compte** : DEMO eToro exclusivement (cid 7632001). Aucune position sur le compte réel.")
    lines.append("- **Univers** : les 100 valeurs du Nasdaq-100.")
    lines.append(
        "- **Range d'ouverture** : première bougie de 5 minutes (09h30–09h35, heure de New York). "
        "RH = plus haut, RL = plus bas."
    )
    lines.append(
        "- **Filtre « stocks in play »** : volume relatif depuis l'ouverture > 1 "
        "(rapporté à la moyenne du même créneau sur les 14 derniers jours)."
    )
    lines.append("- **Signal** : cours actuel strictement supérieur à RH.")
    lines.append("- **Sélection** : les 3 plus forts volumes relatifs parmi les candidats.")
    lines.append(
        "- **Positions** : pour chaque valeur retenue, deux positions longues de 100 USD, "
        "l'une à levier x2, l'autre à levier x5, stop loss placé sur RL."
    )
    lines.append("- **Sortie** : clôture de toutes les positions en fin de séance (routine du soir).")
    lines.append("")
    lines.append("## Début de l'expérience")
    lines.append("")
    lines.append("**2026-09-09** (mercredi).")
    lines.append("")
    lines.append("## Méthodologie de calcul")
    lines.append("")
    lines.append(
        "Ce fichier est intégralement régénéré chaque soir par `journal/calcul_bilan.py`, "
        "qui relit tous les fichiers `journal/AAAA-MM-JJ.md` depuis le début et recalcule "
        "l'ensemble des chiffres à partir des données brutes (jamais à partir de ce fichier lui-même)."
    )
    lines.append("")
    lines.append(
        "- **Performance cumulée des tracks x2 / x5** : somme des P&L nets (frais compris) de tous "
        "les trades du track, rapportée à la somme des capitaux engagés sur ce track (non composé — "
        "chaque position est un pari indépendant de ~100 USD, pas un capital qui roule)."
    )
    lines.append(
        "- **QQQ sans levier depuis le premier jour** : variation du cours QQQ entre la valeur relevée "
        "à l'ouverture du premier jour de l'expérience et la clôture du jour considéré."
    )
    lines.append(
        "- **QQQ à levier x2 / x5** : la performance QQQ sans levier multipliée par 2 ou par 5 "
        "(exposition identique aux tracks, sans frais de financement ni rebalancement journalier — "
        "approximation volontairement simple). C'est cette comparaison, à levier égal, qui mesure "
        "une compétence de sélection — battre QQQ sans levier avec du levier ne prouve rien."
    )
    lines.append(
        "- **Max drawdown** : plus forte baisse pic-à-creux de la courbe cumulée (en points de %), "
        "recalculée jour après jour."
    )
    lines.append(
        "- **Jours anormaux** : tout journal contenant la mention `ANOMALIE` (journal du matin manquant, "
        "fermeture échouée, position orpheline...). Les trades de ces jours restent inclus dans les "
        "cumuls (l'argent gagné/perdu est réel) mais le jour reste identifiable."
    )
    lines.append(
        "- **Séances écourtées** : jours de clôture anticipée (13h00 New York). Incluses dans les cumuls "
        "mais isolables — l'amplitude des mouvements y est mécaniquement réduite, donc non comparable "
        "aux autres jours."
    )
    lines.append("")
    lines.append("## Tableau récapitulatif")
    lines.append("")
    lines.append(f"_Dernière mise à jour : {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} — {stats['n_days']} jour(s) de bourse clôturé(s)._")
    lines.append("")
    lines.append("| | Perf. cumulée | Max drawdown | Capital engagé |")
    lines.append("|---|---|---|---|")
    lines.append(f"| **Track x2** | {fmt_pct(stats['cum_x2'])} | {fmt_pct(stats['mdd_x2'])} | {fmt(stats['cap_x2'])} USD |")
    lines.append(f"| **Track x5** | {fmt_pct(stats['cum_x5'])} | {fmt_pct(stats['mdd_x5'])} | {fmt(stats['cap_x5'])} USD |")
    lines.append(f"| QQQ sans levier | {fmt_pct(stats['qqq_cum_unlev'])} | {fmt_pct(stats['qqq_mdd_unlev'])} | — |")
    lines.append(f"| QQQ à levier x2 (même exposition que le track x2) | {fmt_pct(stats['qqq_cum_x2'])} | {fmt_pct(stats['qqq_mdd_x2'])} | — |")
    lines.append(f"| QQQ à levier x5 (même exposition que le track x5) | {fmt_pct(stats['qqq_cum_x5'])} | {fmt_pct(stats['qqq_mdd_x5'])} | — |")
    lines.append("")
    verdict_x2 = "bat" if stats["cum_x2"] > stats["qqq_cum_x2"] else ("égale" if stats["cum_x2"] == stats["qqq_cum_x2"] else "perd contre")
    verdict_x5 = "bat" if stats["cum_x5"] > stats["qqq_cum_x5"] else ("égale" if stats["cum_x5"] == stats["qqq_cum_x5"] else "perd contre")
    lines.append(
        f"**Comparaison à levier égal** : le track x2 {verdict_x2} QQQ x2 "
        f"({fmt_pct(stats['cum_x2'])} vs {fmt_pct(stats['qqq_cum_x2'])}) ; "
        f"le track x5 {verdict_x5} QQQ x5 "
        f"({fmt_pct(stats['cum_x5'])} vs {fmt_pct(stats['qqq_cum_x5'])})."
    )
    lines.append("")
    lines.append("## Statistiques de trading")
    lines.append("")
    lines.append(f"- **Jours de bourse écoulés** : {stats['n_days']}")
    lines.append(f"- **Nombre de trades** : {stats['n_trades']}")
    lines.append(f"- **Taux de réussite** : {fmt(stats['win_rate'], 1)} %")
    lines.append(f"- **Gain moyen (trades gagnants)** : {fmt(stats['avg_gain'])} USD" if stats['avg_gain'] is not None else "- **Gain moyen (trades gagnants)** : n/a (aucun trade gagnant à ce jour)")
    lines.append(f"- **Perte moyenne (trades perdants)** : {fmt(stats['avg_loss'])} USD" if stats['avg_loss'] is not None else "- **Perte moyenne (trades perdants)** : n/a")
    lines.append(f"- **Jours anormaux** (journal du matin manquant, fermeture échouée, position orpheline) : {stats['n_anomalies']}")
    lines.append(f"- **Séances écourtées** (clôture anticipée) : {stats['n_shortened']}")
    if stats["qqq_baseline"] is not None:
        lines.append(f"- **QQQ, référence de départ (J1)** : {fmt(stats['qqq_baseline'])}")
    if stats["qqq_last_close"] is not None:
        lines.append(f"- **QQQ, dernière clôture connue** : {fmt(stats['qqq_last_close'])}")
    lines.append("")
    lines.append("## Suivi")
    lines.append("")
    lines.append("Le détail de chaque séance est consigné dans `journal/AAAA-MM-JJ.md`. Ce fichier agrège les résultats.")
    lines.append("")
    lines.append("### Journal des séances")
    lines.append("")
    lines.append("| Date | Trades | P&L x2 (USD) | P&L x5 (USD) | QQQ clôture | Anomalie | Écourtée |")
    lines.append("|---|---|---|---|---|---|---|")
    for d in stats["closed_days"]:
        n_tr = len(d["positions"])
        pnl2 = sum(p["pnl_net"] for p in d["positions"] if p["levier"] == 2)
        pnl5 = sum(p["pnl_net"] for p in d["positions"] if p["levier"] == 5)
        qqq_c = fmt(d["qqq_close"]) if d["qqq_close"] is not None else "n/a"
        lines.append(
            f"| {d['date']} | {n_tr} | {fmt(pnl2)} | {fmt(pnl5)} | {qqq_c} | "
            f"{'oui' if d['anomaly'] else 'non'} | {'oui' if d['shortened'] else 'non'} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main():
    days = load_all_days()
    stats = build_bilan(days)
    content = render_bilan(stats)
    with open(BILAN_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(content)


if __name__ == "__main__":
    main()
