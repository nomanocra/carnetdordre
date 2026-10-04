#!/usr/bin/env python3
"""
Calcule les chiffres d'un rapport mensuel de l'experience ORB a effet de levier
vs QQQ, a partir des fichiers bruts journal/AAAA-MM-JJ.md uniquement.

Ne relit JAMAIS BILAN.md ni un rapport mensuel precedent : tout est recalcule
depuis les journaux quotidiens, pour eviter toute propagation d'erreur.

Le track x2 est abandonne depuis le 2026-09-24 : toutes les positions a levier
x2 (demo comme reel) sont ignorees dans TOUS les calculs ci-dessous.

Usage : python3 journal/rapport_mensuel.py AAAA-MM
Affiche les chiffres du mois demande + le cumul depuis le debut de l'experience.
"""

import os
import re
import sys

from calcul_bilan import fr_num, load_all_days, max_drawdown, missing_weekdays

JOURNAL_DIR = os.path.dirname(os.path.abspath(__file__))

LEVIER = 5
# Budget quotidien prevu par la strategie : 3 positions x 100 USD de marge.
BUDGET_JOUR = 300.0
# Frais eToro annonces : 0,15 % a l'entree et 0,15 % a la sortie,
# calcules sur l'EXPOSITION (marge x levier), pas sur la marge.
FEE_RATE_ONE_WAY = 0.0015


def read(day):
    with open(os.path.join(JOURNAL_DIR, day["date"] + ".md"), encoding="utf-8") as f:
        return f.read()


def table_rows(section):
    """Renvoie les tableaux markdown d'une section : liste de (entete, lignes)."""
    tables, cur = [], None
    for line in section.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cur is None:
                cur = (cells, [])
            elif all(re.match(r"^:?-+:?$", c) for c in cells if c):
                continue
            else:
                cur[1].append(cells)
        else:
            if cur is not None:
                tables.append(cur)
            cur = None
    if cur is not None:
        tables.append(cur)
    return tables


def first_number(cell):
    m = re.search(r"-?\d[\d\s ]*(?:,\d+)?", cell)
    return fr_num(m.group(0)) if m else None


def enrich(day):
    """Ajoute au jour : compte (demo/reel), et a chaque position x5 les frais
    d'entree releves dans le tableau des ordres du matin, le cours de
    reconfirmation (seances reelles) et le stop loss."""
    text = read(day)
    day["reel"] = text.lstrip().startswith("Compte : REEL")
    morning = text.split("## Clôture")[0]
    fees, stops, decision = {}, {}, {}
    for header, rows in table_rows(morning):
        h = [c.lower() for c in header]
        if not h or h[0] != "symbole":
            continue
        i_lev = next((i for i, c in enumerate(h) if c == "levier"), None)
        i_fee = next((i for i, c in enumerate(h) if c.startswith("frais")), None)
        i_sl = next((i for i, c in enumerate(h) if c.startswith("stop loss")), None)
        i_dec = next((i for i, c in enumerate(h)
                      if c.startswith("cours live") or c.startswith("cours de reconfirmation")), None)
        for r in rows:
            if len(r) != len(h):
                continue
            sym = r[0]
            lev = None
            if i_lev is not None:
                m = re.search(r"x(\d)", r[i_lev])
                lev = int(m.group(1)) if m else None
            elif "levier x5" in morning:
                lev = 5
            if i_fee is not None and lev is not None:
                v = first_number(r[i_fee])
                if v is not None:
                    fees[(sym, lev)] = v
            if i_sl is not None and lev is not None:
                v = first_number(r[i_sl])
                if v is not None:
                    stops[(sym, lev)] = v
            if i_dec is not None:
                v = first_number(r[i_dec])
                if v is not None:
                    decision[sym] = v
    day["positions"] = [p for p in day["positions"] if p["levier"] == LEVIER]
    for p in day["positions"]:
        key = (p["symbole"], LEVIER)
        expo = p["investissement"] * LEVIER
        units = expo / p["entree"]
        p["exposition"] = expo
        p["pnl_brut_prix"] = units * (p["sortie"] - p["entree"])
        # Ce que le carnet a effectivement retranche du P&L brut de prix.
        p["frais_deduits"] = p["pnl_brut_prix"] - p["pnl_net"]
        p["frais_entree_releves"] = fees.get(key)  # None = non releve
        p["frais_theoriques"] = FEE_RATE_ONE_WAY * (expo + units * p["sortie"])
        p["stop"] = stops.get(key)
        p["cours_decision"] = decision.get(p["symbole"])
    return day


def curve_constant_budget(days):
    """Courbe cumulee (non composee) en % d'un budget fixe de 300 USD par jour."""
    out, run = [], 0.0
    for d in days:
        run += sum(p["pnl_net"] for p in d["positions"]) / BUDGET_JOUR * 100
        out.append((d["date"], run))
    return out


def curve_bilan(days):
    """Courbe de BILAN.md : somme des % journaliers (P&L du jour / capital du jour)."""
    out, run = [], 0.0
    for d in days:
        cap = sum(p["investissement"] for p in d["positions"])
        pnl = sum(p["pnl_net"] for p in d["positions"])
        run += (pnl / cap * 100) if cap else 0.0
        out.append((d["date"], run))
    return out


def qqq_curve(days, baseline):
    return [(d["date"], (d["qqq_close"] / baseline - 1) * 100)
            for d in days if d["qqq_close"] is not None]


def bloc(label, days, baseline):
    trades = [p for d in days for p in d["positions"]]
    n = len(trades)
    pnl = sum(t["pnl_net"] for t in trades)
    cap = sum(t["investissement"] for t in trades)
    wins = [t["pnl_net"] for t in trades if t["pnl_net"] > 0]
    losses = [t["pnl_net"] for t in trades if t["pnl_net"] <= 0]
    n_stop = sum(1 for t in trades if t["sortie_via"] == "stop loss")
    cb = curve_constant_budget(days)
    cbl = curve_bilan(days)
    q = qqq_curve(days, baseline)
    q_last = q[-1][1] if q else None
    print(f"--- {label} : {days[0]['date']} -> {days[-1]['date']} | {len(days)} seances cloturees "
          f"({sum(1 for d in days if d['reel'])} reelles, {sum(1 for d in days if not d['reel'])} demo) ---")
    print(f"Track x5 : {n} trades | P&L net {pnl:+.2f} USD | capital engage cumule {cap:.2f} USD")
    print(f"  (A) methode BILAN.md  : P&L / capital engage cumule = {pnl / cap * 100:+.2f} % "
          f"| max drawdown (somme des % journaliers) {max_drawdown(cbl):+.2f} %")
    print(f"  (B) budget constant 300 USD/jour : {cb[-1][1]:+.2f} % | max drawdown {max_drawdown(cb):+.2f} %")
    print(f"QQQ base {baseline:.2f} -> derniere cloture {[d['qqq_close'] for d in days if d['qqq_close']][-1]:.2f}")
    print(f"  QQQ sans levier : {q_last:+.2f} % | max drawdown {max_drawdown(q):+.2f} %")
    print(f"  QQQ x5          : {q_last * 5:+.2f} % | max drawdown {max_drawdown([(a, v * 5) for a, v in q]):+.2f} %")
    print(f"Taux de reussite : {len(wins)}/{n} = {len(wins) / n * 100:.1f} % "
          f"| gain moyen {sum(wins) / len(wins):+.2f} | perte moyenne {sum(losses) / len(losses):+.2f} USD")
    print(f"Sorties : stop loss {n_stop}/{n} ({n_stop / n * 100:.1f} %) | cloture {n - n_stop}")
    rel = [t for t in trades if t["frais_entree_releves"] is not None]
    miss = [t for t in trades if t["frais_entree_releves"] is None]
    print(f"Frais d'entree releves (reponse d'execution) : {sum(t['frais_entree_releves'] for t in rel):.2f} USD "
          f"sur {len(rel)} trades | NON RELEVES : {len(miss)} trades "
          f"{[(d['date'], t['symbole']) for d in days for t in d['positions'] if t['frais_entree_releves'] is None]}")
    print(f"Frais effectivement deduits dans les P&L du carnet (brut prix - net) : "
          f"{sum(t['frais_deduits'] for t in trades):.2f} USD")
    print(f"Frais theoriques 0,15 % + 0,15 % sur exposition : {sum(t['frais_theoriques'] for t in trades):.2f} USD "
          f"| exposition totale {sum(t['exposition'] for t in trades):.2f} USD")
    print()


def report(period):
    days = [enrich(d) for d in load_all_days()]
    closed = [d for d in days if d["has_closing"]]
    baseline = next(d["qqq_open"] for d in days if d["qqq_open"] is not None)
    month = [d for d in closed if d["date"][:7] == period]
    upto = [d for d in closed if d["date"][:7] <= period]
    gaps = [g for g in missing_weekdays([d["date"] for d in days]) if g[:7] == period]

    print(f"=== PERIODE : {period} ===")
    print(f"Journaux du mois : {[d['date'] for d in days if d['date'][:7] == period]}")
    print(f"Jours de bourse du mois SANS AUCUN journal (entre 1er et dernier journal du depot) : {gaps}")
    print(f"Jours ANOMALIE du mois : {[d['date'] for d in month if d['anomaly']]}")
    print()

    print("Detail par seance (track x5) :")
    for d in month:
        pnl = sum(p["pnl_net"] for p in d["positions"])
        print(f"  {d['date']} {'REEL' if d['reel'] else 'demo'} trades={len(d['positions'])} "
              f"pnl={pnl:+.2f} qqq_close={d['qqq_close']}")
    print()
    print(f"{'date':<11}{'sym':<6}{'entree':>9}{'sortie':>9}{'net':>8}{'brut':>8}{'deduit':>8}"
          f"{'f.rel':>7}{'f.th':>7}{'stop':>9}  sortie / slippage")
    for d in month:
        for p in d["positions"]:
            fr = "n/r" if p["frais_entree_releves"] is None else f"{p['frais_entree_releves']:.2f}"
            extra = ""
            if p["sortie_via"] == "stop loss" and p["stop"]:
                extra += f" sortie-vs-stop {(p['sortie'] / p['stop'] - 1) * 100:+.3f} %"
            if d["reel"] and p["cours_decision"]:
                extra += f" entree-vs-decision {(p['entree'] / p['cours_decision'] - 1) * 100:+.3f} %"
            print(f"{d['date']:<11}{p['symbole']:<6}{p['entree']:>9.2f}{p['sortie']:>9.2f}"
                  f"{p['pnl_net']:>8.2f}{p['pnl_brut_prix']:>8.2f}{p['frais_deduits']:>8.2f}"
                  f"{fr:>7}{p['frais_theoriques']:>7.2f}{(p['stop'] or 0):>9.2f}  {p['sortie_via']}{extra}")
    print()

    bloc(f"MOIS {period}", month, baseline)
    demo = [d for d in month if not d["reel"]]
    reel = [d for d in month if d["reel"]]
    if demo and reel:
        bloc("MOIS - seances DEMO", demo, baseline)
        prev = [d for d in closed if d["date"] < reel[0]["date"] and d["qqq_close"]]
        bloc("MOIS - seances REELLES (base QQQ = derniere cloture demo)", reel, prev[-1]["qqq_close"])
    bloc(f"CUMUL depuis le debut jusqu'a fin {period}", upto, baseline)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python3 journal/rapport_mensuel.py AAAA-MM")
    report(sys.argv[1])
