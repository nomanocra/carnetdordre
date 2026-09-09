#!/usr/bin/env python3
"""
Calcule les chiffres d'un rapport mensuel de l'experience ORB a effet de levier
vs QQQ, a partir des fichiers bruts journal/AAAA-MM-JJ.md uniquement.

Ne relit JAMAIS BILAN.md ni un rapport mensuel precedent : tout est recalcule
depuis les journaux quotidiens, pour eviter toute propagation d'erreur.

Usage : python3 journal/rapport_mensuel.py AAAA-MM
Affiche les chiffres du mois demande + le cumul depuis le debut de l'experience.
"""

import sys

from calcul_bilan import load_all_days, max_drawdown

# Frais eToro annonces : 0,15 % a l'entree et 0,15 % a la sortie,
# calcules sur l'EXPOSITION (marge x levier), pas sur la marge.
FEE_RATE_ONE_WAY = 0.0015


def enrich_positions(days):
    """Ajoute a chaque position l'exposition, les unites, le P&L brut theorique
    et les frais theoriques. Les unites sont rededuites de l'investissement et
    du levier (exposition / cours d'entree), coherentes avec les tableaux
    d'ouverture des journaux."""
    for d in days:
        for p in d["positions"]:
            exposure = p["investissement"] * p["levier"]
            units = exposure / p["entree"] if p["entree"] else 0.0
            p["exposition"] = exposure
            p["unites"] = units
            p["pnl_brut_prix"] = units * (p["sortie"] - p["entree"])
            p["frais_theoriques"] = FEE_RATE_ONE_WAY * (exposure + units * p["sortie"])
            # Ecart entre le P&L reporte et la simple difference de prix :
            # c'est ce que le carnet impute implicitement aux frais/spread.
            p["frais_implicites"] = p["pnl_brut_prix"] - p["pnl_net"]
    return days


def month_of(day):
    return day["date"][:7]


def track_curve(entries):
    """entries : liste de (date, pnl_jour, capital_jour).
    Renvoie (pnl_total, capital_total, perf_%, max_drawdown_%)."""
    total_pnl = sum(pnl for _, pnl, _ in entries)
    total_cap = sum(cap for _, _, cap in entries if cap > 0)
    perf = (total_pnl / total_cap * 100) if total_cap else 0.0
    curve, running = [], 0.0
    for date, pnl, cap in entries:
        running += (pnl / cap * 100) if cap else 0.0
        curve.append((date, running))
    return total_pnl, total_cap, perf, max_drawdown(curve)


def track_entries(closed_days, levier):
    out = []
    for d in closed_days:
        pnl = sum(p["pnl_net"] for p in d["positions"] if p["levier"] == levier)
        cap = sum(p["investissement"] for p in d["positions"] if p["levier"] == levier)
        out.append((d["date"], pnl, cap))
    return out


def qqq_stats(closed_days, baseline):
    """Performance QQQ sur la periode : baseline -> derniere cloture connue,
    plus le max drawdown de la courbe des clotures rapportee a la baseline."""
    if baseline is None:
        return None
    curve = [
        (d["date"], (d["qqq_close"] / baseline - 1) * 100)
        for d in closed_days
        if d["qqq_close"] is not None
    ]
    if not curve:
        return None
    perf = curve[-1][1]
    return {
        "unlev": perf,
        "x2": perf * 2,
        "x5": perf * 5,
        "mdd_unlev": max_drawdown(curve),
        "mdd_x2": max_drawdown([(dt, v * 2) for dt, v in curve]),
        "mdd_x5": max_drawdown([(dt, v * 5) for dt, v in curve]),
        "baseline": baseline,
        "last_close": [d["qqq_close"] for d in closed_days if d["qqq_close"] is not None][-1],
    }


def trade_stats(days):
    trades = [p for d in days for p in d["positions"]]
    n = len(trades)
    wins = [t["pnl_net"] for t in trades if t["pnl_net"] > 0]
    losses = [t["pnl_net"] for t in trades if t["pnl_net"] <= 0]
    n_stop = sum(1 for t in trades if t["sortie_via"] == "stop loss")
    return {
        "n_trades": n,
        "win_rate": (len(wins) / n * 100) if n else None,
        "avg_gain": (sum(wins) / len(wins)) if wins else None,
        "avg_loss": (sum(losses) / len(losses)) if losses else None,
        "n_wins": len(wins),
        "n_losses": len(losses),
        "n_stop": n_stop,
        "n_close": n - n_stop,
        "pct_stop": (n_stop / n * 100) if n else None,
        "frais_theoriques": sum(t["frais_theoriques"] for t in trades),
        "frais_implicites": sum(t["frais_implicites"] for t in trades),
        "exposition_totale": sum(t["exposition"] for t in trades),
    }


def report(period):
    days = enrich_positions(load_all_days())
    closed = [d for d in days if d["has_closing"]]

    # Baseline QQQ de l'experience : premier cours d'ouverture releve.
    baseline_global = next((d["qqq_open"] for d in days if d["qqq_open"] is not None), None)

    month_days = [d for d in closed if month_of(d) == period]
    prior_days = [d for d in closed if month_of(d) < period]

    print(f"=== PERIODE DEMANDEE : {period} ===")
    print(f"Fichiers journaliers presents dans le depot : {len(days)}")
    print(f"  dont journees cloturees : {len(closed)}")
    print(f"  dates : {[d['date'] for d in days]}")
    print(f"Journees cloturees DANS le mois {period} : {len(month_days)}")
    print(f"Journees cloturees AVANT le mois {period} : {len(prior_days)}")
    print()

    if month_days:
        # Baseline QQQ du mois : derniere cloture du mois precedent si
        # disponible, sinon premier cours d'ouverture releve dans le mois.
        prior_closes = [d["qqq_close"] for d in prior_days if d["qqq_close"] is not None]
        if prior_closes:
            base_month = prior_closes[-1]
            base_src = "derniere cloture QQQ du mois precedent"
        else:
            base_month = next((d["qqq_open"] for d in month_days if d["qqq_open"] is not None), None)
            base_src = "premier cours QQQ releve dans le mois (pas de mois anterieur)"

        print("--- MOIS ---")
        for lev in (2, 5):
            pnl, cap, perf, mdd = track_curve(track_entries(month_days, lev))
            print(f"Track x{lev} : P&L {pnl:+.2f} USD sur {cap:.2f} USD engages "
                  f"-> {perf:+.2f} % | max drawdown {mdd:+.2f} %")
        q = qqq_stats(month_days, base_month)
        if q:
            print(f"QQQ baseline {q['baseline']:.2f} ({base_src}) -> derniere cloture {q['last_close']:.2f}")
            print(f"QQQ sans levier : {q['unlev']:+.2f} % | max drawdown {q['mdd_unlev']:+.2f} %")
            print(f"QQQ x2          : {q['x2']:+.2f} % | max drawdown {q['mdd_x2']:+.2f} %")
            print(f"QQQ x5          : {q['x5']:+.2f} % | max drawdown {q['mdd_x5']:+.2f} %")
        else:
            print("QQQ : donnees insuffisantes dans les journaux du mois.")
        s = trade_stats(month_days)
        print(f"Trades : {s['n_trades']} | gagnants {s['n_wins']} | perdants {s['n_losses']} "
              f"| taux de reussite {s['win_rate'] if s['win_rate'] is None else round(s['win_rate'], 1)} %")
        print(f"Gain moyen : {s['avg_gain']} | Perte moyenne : {s['avg_loss']}")
        print(f"Sorties au stop loss : {s['n_stop']}/{s['n_trades']} "
              f"({s['pct_stop'] if s['pct_stop'] is None else round(s['pct_stop'], 1)} %) "
              f"| sorties a la cloture : {s['n_close']}")
        print(f"Exposition totale (marge x levier, entree) : {s['exposition_totale']:.2f} USD")
        print(f"Frais THEORIQUES (0,15 % entree + 0,15 % sortie sur exposition) : "
              f"{s['frais_theoriques']:.2f} USD")
        print(f"Ecart P&L(difference de prix x unites) - P&L(reporte au carnet) : "
              f"{s['frais_implicites']:+.4f} USD  <- frais reellement visibles dans le carnet")
        print()
        print("Detail par trade :")
        print(f"{'date':<12}{'sym':<6}{'lev':<5}{'entree':>10}{'sortie':>10}"
              f"{'expo':>9}{'net':>8}{'brut_prix':>11}{'frais_th':>10}{'ecart':>9}  sortie")
        for d in month_days:
            for p in d["positions"]:
                print(f"{d['date']:<12}{p['symbole']:<6}x{p['levier']:<4}"
                      f"{p['entree']:>10.2f}{p['sortie']:>10.2f}{p['exposition']:>9.2f}"
                      f"{p['pnl_net']:>8.2f}{p['pnl_brut_prix']:>11.4f}"
                      f"{p['frais_theoriques']:>10.2f}{p['frais_implicites']:>9.4f}  {p['sortie_via']}")
        print()
    else:
        print(f"--- MOIS --- AUCUNE journee de bourse cloturee dans {period}. "
              f"Aucun chiffre mensuel calculable.")
        print()

    print("--- CUMUL DEPUIS LE DEBUT DE L'EXPERIENCE ---")
    if not closed:
        print("Aucune journee cloturee. Rien a cumuler.")
        return
    print(f"Premiere journee : {closed[0]['date']} | derniere : {closed[-1]['date']} "
          f"| {len(closed)} jour(s)")
    for lev in (2, 5):
        pnl, cap, perf, mdd = track_curve(track_entries(closed, lev))
        print(f"Track x{lev} : P&L {pnl:+.2f} USD sur {cap:.2f} USD engages "
              f"-> {perf:+.2f} % | max drawdown {mdd:+.2f} %")
    q = qqq_stats(closed, baseline_global)
    if q:
        print(f"QQQ baseline (J1) {q['baseline']:.2f} -> derniere cloture {q['last_close']:.2f}")
        print(f"QQQ sans levier : {q['unlev']:+.2f} % | max drawdown {q['mdd_unlev']:+.2f} %")
        print(f"QQQ x2          : {q['x2']:+.2f} % | max drawdown {q['mdd_x2']:+.2f} %")
        print(f"QQQ x5          : {q['x5']:+.2f} % | max drawdown {q['mdd_x5']:+.2f} %")
    s = trade_stats(closed)
    print(f"Trades : {s['n_trades']} | taux de reussite "
          f"{s['win_rate'] if s['win_rate'] is None else round(s['win_rate'], 1)} % "
          f"| gain moyen {s['avg_gain']} | perte moyenne {s['avg_loss']}")
    print(f"Sorties au stop loss : {s['n_stop']}/{s['n_trades']} | a la cloture : {s['n_close']}")
    print(f"Frais theoriques cumules : {s['frais_theoriques']:.2f} USD "
          f"| ecart visible au carnet : {s['frais_implicites']:+.4f} USD")
    print(f"Jours marques ANOMALIE : {sum(1 for d in days if d['anomaly'])} "
          f"| seances ecourtees : {sum(1 for d in days if d['shortened'])}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python3 journal/rapport_mensuel.py AAAA-MM")
    report(sys.argv[1])
