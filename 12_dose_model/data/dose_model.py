"""Parametric intranasal dose model for Epione.

The one input the dry lab does not have is the expression yield from the first
transfection. Rather than wait for it, this model carries yield as a FREE
variable and solves for everything else, so that when the number arrives the
answer is a substitution rather than a week of work.

WHAT IT COMPUTES
----------------
The chain from a spray actuation to a concentration at the receptor:

    dose of lipoplex
      -> plasmid deposited in the olfactory region        (f_olf)
      -> nuclei transfected                               (eta_tf)
      -> peptide molecules produced per cell per day      (YIELD, free)
      -> peptide delivered to the CNS compartment         (f_cns)
      -> steady-state CNS concentration                   (production / clearance)
      -> compared against the receptor EC50

Steady state is production divided by clearance. Clearance has two routes that
act in parallel: enzymatic degradation, which the siRNA arm is designed to slow,
and bulk CSF turnover, which it cannot touch. That distinction is the reason the
silencing arm appears in the model at all.

WHAT IT DOES NOT DO
-------------------
It is a steady-state compartment model, not a spatially resolved one. It assumes
the peptide that reaches the CNS compartment mixes within it, which overestimates
concentration at a distant target and underestimates it near the site of
production. It says nothing about which receptor the peptide prefers.

HONEST PARAMETER STATUS
-----------------------
Every parameter below carries a range rather than a point value, and the source
field says whether the range is physiological, taken from literature, or an
assumption we are making explicit. The model's purpose is not to produce one
number from numbers we do not have; it is to show which of them the answer is
actually sensitive to, so the wet lab measures the ones that matter.
"""
import numpy as np

AVOGADRO = 6.02214076e23

# name -> (low, high, units, source_class, note)
PARAMS = {
    "spray_volume_uL": (
        100.0, 200.0, "uL per actuation, both nostrils",
        "device",
        "Standard metered nasal spray pumps deliver 50 to 100 uL per nostril."),
    "f_olf": (
        0.005, 0.05, "fraction of dose reaching the olfactory region",
        "literature range",
        "The olfactory region is a small fraction of the nasal surface and is "
        "poorly reached by conventional sprays. Device work aims to raise this."),
    "eta_tf": (
        0.001, 0.05, "fraction of exposed cells productively transfected",
        "assumption",
        "In vivo non-viral transfection of nasal epithelium. Wide because it "
        "depends on formulation and on mucociliary clearance competing with uptake."),
    "cells_exposed": (
        1e6, 1e7, "cells in the exposed olfactory epithelium",
        "physiological",
        "Human olfactory epithelium is roughly 2 to 10 cm2 with ~1e6 cells/cm2."),
    "f_cns": (
        0.05, 0.5, "fraction of secreted peptide entering the CNS compartment",
        "assumption",
        "Peptide secreted at the epithelium partitions between systemic uptake "
        "and direct nose-to-brain routes. Highly uncertain."),
    "cns_volume_mL": (
        140.0, 170.0, "mL",
        "physiological",
        "Adult human CSF volume."),
    "csf_turnover_per_h": (
        0.15, 0.25, "fraction of CSF replaced per hour",
        "physiological",
        "CSF is replaced roughly 3 to 4 times daily."),
    "t_half_min_native": (
        1.0, 5.0, "min",
        "literature range",
        "Enkephalins are degraded within minutes, principally by neprilysin and "
        "aminopeptidase N."),
    "knockdown_fold": (
        1.5, 4.0, "fold increase in peptide half-life",
        "assumption",
        "Effect of the neprilysin siRNA arm. Neprilysin is one of two main "
        "enzymes, so even complete knockdown cannot give an unbounded increase."),
    "ec50_nM": (
        1.0, 50.0, "nM at the delta receptor",
        "literature range",
        "Enkephalin potency at DOR. Spans the range reported across assay formats."),
    "expression_days": (
        3.0, 14.0, "days of useful expression from one dose",
        "assumption",
        "Transient, non-integrating plasmid in a tissue that turns over."),
}

PEPTIDE_MW = 1000.0          # g/mol, order of magnitude for an octapeptide


def sample(n, rng, overrides=None):
    """Latin-hypercube-ish uniform sample over every parameter range."""
    overrides = overrides or {}
    out = {}
    for k, (lo, hi, *_rest) in PARAMS.items():
        if k in overrides:
            v = overrides[k]
            out[k] = np.full(n, float(v)) if np.isscalar(v) else np.asarray(v, float)
        else:
            out[k] = rng.uniform(lo, hi, n)
    return out


def cns_concentration_nM(yield_molecules_cell_day, p):
    """Steady-state CNS concentration for a given per-cell expression yield.

    yield_molecules_cell_day : the FREE parameter, peptide molecules secreted
        per transfected cell per day. This is what the transfection measures.

    A first version of this function declared f_olf and spray_volume_uL in the
    parameter table but never used them, so the sensitivity analysis reported
    them as having no influence. That was a defect in the model rather than a
    property of the system: only cells the formulation actually reaches can be
    transfected, so f_olf scales the exposed population. The spray volume enters
    through the same term, since a larger actuation wets more of the epithelium
    up to the point where the surface is covered.
    """
    # only the fraction of the epithelium the spray reaches is available
    coverage = np.minimum(1.0, p["spray_volume_uL"] / 150.0)
    reached = p["cells_exposed"] * p["f_olf"] * coverage
    transfected = reached * p["eta_tf"]
    produced_per_day = transfected * yield_molecules_cell_day        # molecules/day
    to_cns_per_day = produced_per_day * p["f_cns"]
    per_hour = to_cns_per_day / 24.0

    # two clearance routes in parallel
    t_half_h = (p["t_half_min_native"] * p["knockdown_fold"]) / 60.0
    k_enzyme = np.log(2.0) / t_half_h                                 # per hour
    k_bulk = p["csf_turnover_per_h"]
    k_total = k_enzyme + k_bulk

    molecules_at_steady_state = per_hour / k_total
    litres = p["cns_volume_mL"] / 1000.0
    molar = molecules_at_steady_state / AVOGADRO / litres
    return molar * 1e9                                                # nM


def required_yield_for_ec50(p):
    """Invert the chain: what per-cell yield puts the CNS at the EC50?"""
    unit = cns_concentration_nM(1.0, p)        # nM produced by 1 molecule/cell/day
    return p["ec50_nM"] / unit


def dose_equivalent_ug(yield_molecules_cell_day, p, ug_per_actuation=100.0):
    """How many actuations, if concentration scales linearly with deposited dose.

    Expressed relative to a reference actuation, since the absolute plasmid mass
    per actuation is a formulation choice rather than a biological quantity.
    """
    reached = cns_concentration_nM(yield_molecules_cell_day, p)
    return p["ec50_nM"] / np.maximum(reached, 1e-30) * ug_per_actuation


def dosing_interval_days(p):
    """How often a dose must be repeated.

    expression_days does not affect the steady-state concentration while
    expression lasts; it sets how long that steady state is held, and therefore
    the redosing interval. Reported separately rather than folded into the
    concentration, which is what an earlier version wrongly implied by listing
    it as an unused parameter.
    """
    return p["expression_days"]


def sensitivity(n, rng, yield_fixed):
    """Rank parameters by how much of the spread in the answer they explain.

    Spearman rank correlation between each sampled parameter and the resulting
    concentration. Rank rather than Pearson because the chain is multiplicative.
    """
    from scipy import stats
    p = sample(n, rng)
    y = cns_concentration_nM(yield_fixed, p)
    rows = []
    for k in PARAMS:
        if k in ("ec50_nM",):          # a target, not an input to the concentration
            continue
        rho, pv = stats.spearmanr(p[k], y)
        rows.append((k, float(rho), float(pv)))
    rows.sort(key=lambda r: -abs(r[1]))
    return rows, y, p
