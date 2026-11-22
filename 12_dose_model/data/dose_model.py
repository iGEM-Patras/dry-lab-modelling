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
    "dose_interval_days": (
        1.0, 14.0, "days between repeat actuations",
        "assumption",
        "Set by the dosing schedule, NOT by how long one dose expresses. Held "
        "independent of expression_days so that repeat doses can superpose: if the "
        "interval is shorter than the expression window, doses overlap and the "
        "concentration accumulates. An earlier version returned expression_days as "
        "the interval, which silently forbade accumulation."),
    "tolerated_multiple_of_ec50": (
        3.0, 10.0, "fold over EC50 taken as the upper acceptable exposure",
        "literature range",
        "No convulsant threshold has been measured for this peptide, so this is the "
        "weakest-anchored number in the table and is a placeholder for a measured "
        "one. The range is taken from SNC80 in rhesus monkeys, where a convulsant "
        "dose was 3 to 10 fold above the doses producing other behavioural effects "
        "(PMID 17112570). It is a conservative anchor in the sense that SNC80 is a "
        "high-efficacy non-peptidic delta agonist, the ligand class in which the "
        "seizure liability is established (PMID 37004753)."),
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
    """The longest interval that holds continuous exposure WITHOUT accumulation.

    Dosing exactly at the end of the expression window gives continuous coverage
    with no overlap, so this is the boundary case rather than a recommendation.
    Any shorter interval makes doses superpose; see accumulation_factor.
    """
    return p["expression_days"]


def accumulation_factor(p):
    """How many doses are expressing simultaneously once dosing reaches steady state.

    One dose drives expression for expression_days. Redosing every
    dose_interval_days means that, at steady state, expression_days /
    dose_interval_days doses are active at once and their outputs add. Daily
    dosing against a 3 to 14 day expression window therefore accumulates 3 to
    14 fold over the single-dose concentration.

    This is a square-pulse superposition: it treats expression as constant for
    expression_days and zero afterwards. A real expression profile rises and
    decays, which spreads the accumulation out in time but does not change the
    steady-state multiple, since that depends only on the area under one dose.

    It also assumes each dose deposits into the same compartment with the same
    efficiency. Repeat intranasal dosing need not be linear in this way:
    nasal instillation in mice gave 5 to 17 fold HIGHER brain bioaccumulation
    factors at low dose than at high dose (PMID 42296265), i.e. disproportionate
    retention rather than simple proportionality. A linear superposition is
    therefore the optimistic case for a safety calculation, not a worst case.
    """
    return np.maximum(1.0, p["expression_days"] / p["dose_interval_days"])


def cns_concentration_multidose_nM(yield_molecules_cell_day, p):
    """Steady-state CNS concentration under a repeat-dosing schedule."""
    return cns_concentration_nM(yield_molecules_cell_day, p) * accumulation_factor(p)


def exposure_margin(yield_molecules_cell_day, p):
    """Where the achieved exposure sits relative to EC50 and to the tolerated ceiling.

    Returns (multiple_of_ec50, margin), where margin is the factor by which the
    achieved exposure may still rise before crossing tolerated_multiple_of_ec50.
    A margin below 1 means the ceiling has been passed. This is the arm the model
    previously lacked entirely: it could only answer how much yield was needed to
    reach the EC50, never how much would be too much.
    """
    reached = cns_concentration_multidose_nM(yield_molecules_cell_day, p)
    multiple = reached / p["ec50_nM"]
    return multiple, p["tolerated_multiple_of_ec50"] / np.maximum(multiple, 1e-30)


def max_tolerated_yield(p):
    """The per-cell yield at which exposure reaches the tolerated ceiling.

    The upper counterpart of required_yield_for_ec50. The therapeutic window is
    the interval between the two, and its width is tolerated_multiple_of_ec50
    exactly, since every term in the chain is linear in yield. The window is set
    by that one assumed number and by nothing else in the model, which is the
    honest statement of how little the model constrains safety.
    """
    unit = cns_concentration_multidose_nM(1.0, p)
    return p["ec50_nM"] * p["tolerated_multiple_of_ec50"] / unit


def sensitivity(n, rng, yield_fixed):
    """Rank parameters by how much of the spread in the answer they explain.

    Spearman rank correlation between each sampled parameter and the resulting
    concentration. Rank rather than Pearson because the chain is multiplicative.
    """
    from scipy import stats
    p = sample(n, rng)
    y = cns_concentration_multidose_nM(yield_fixed, p)
    rows = []
    for k in PARAMS:
        if k in ("ec50_nM", "tolerated_multiple_of_ec50"):   # criteria, not inputs
            continue
        rho, pv = stats.spearmanr(p[k], y)
        rows.append((k, float(rho), float(pv)))
    rows.sort(key=lambda r: -abs(r[1]))
    return rows, y, p


# ---------------------------------------------------------------------------
# The wet lab's own bound on the free variable
# ---------------------------------------------------------------------------
# Dot blot, 72 h post-transfection, HEK293T in 6-well format (Results page).
# Grey levels above blank membrane:
DOTBLOT = {
    "lysate_500uL":      [18, 25, 20, 20],
    "lysate_1000uL":     [19, 25, 12, 17],
    "supernatant_500uL":  [6, -1, -3, -5],
    "supernatant_1000uL": [1,  6, -4, -6],
    "negative_control":   [5, -6],
    "positive_control_range": [41, 46],      # purified His-tagged protein
    "positive_control_ug":    [1.5, 3, 15],  # applied masses
}
TAGGED_PRECURSOR_MW_DA = 32126.0   # His6-tagged PENK precursor, 278 aa
CELLS_SEEDED_PER_WELL = 3e5        # Results page, within the 0.25-1e6 6-well range
MEGFP_POSITIVE_FRACTION = 0.90     # best of the four architectures, Table 3


def dotblot_is_quantitative():
    """Test whether the dot blot can be read as a quantity rather than a presence.

    Two internal checks, both from the blot's own data:

    1. Doubling the applied volume should roughly double the signal. It does not:
       the 1000 uL lysate dots average 0.88 times the 500 uL dots, against 2.00
       for a linear response.
    2. The positive control spans a 10 fold mass range (1.5 to 15 ug) for a 1.12
       fold change in signal.

    Both say the readout is saturated. The blot therefore supports presence or
    absence and an upper bound, and no interpolation between the two. This is why
    the ceiling below is a bound and not an estimate.
    """
    lo = np.asarray(DOTBLOT["lysate_500uL"], float)
    hi = np.asarray(DOTBLOT["lysate_1000uL"], float)
    volume_response = float(np.mean(hi / lo))
    pc = DOTBLOT["positive_control_range"]
    pc_ug = DOTBLOT["positive_control_ug"]
    calibrator_response = pc[1] / pc[0]
    calibrator_mass_range = pc_ug[-1] / pc_ug[0]
    return {
        "volume_response_observed": volume_response,
        "volume_response_if_linear": 2.0,
        "calibrator_mass_range_fold": calibrator_mass_range,
        "calibrator_signal_fold": calibrator_response,
        "quantitative": bool(volume_response > 1.5 and calibrator_response > 3.0),
    }


def wetlab_yield_ceiling(lysate_volume_mL, days_of_expression=3.0,
                         cells=CELLS_SEEDED_PER_WELL * MEGFP_POSITIVE_FRACTION,
                         mw_da=TAGGED_PRECURSOR_MW_DA):
    """Upper bound on per-cell yield implied by our own dot blot.

    Every lysate dot sits below the weakest calibrator, 1.5 ug, so the tagged
    precursor in a 500 uL spot is below that mass. Scaling to the whole lysate
    and dividing by transfected cells and by the days of expression gives a
    ceiling on molecules per cell per day.

    The bound is deliberately generous in three ways, so that a conclusion which
    survives it is safe:
      - it uses the SEEDED cell count, not the count at harvest after three days
        of growth, so the per-cell figure is inflated;
      - it treats the entire sub-threshold mass as intact tagged precursor;
      - it ignores losses in harvest and clearing.

    lysate_volume_mL is the one quantity the notebook does not record. It is an
    explicit argument rather than a hidden default for that reason: the answer
    scales linearly with it, so the missing number is worth one line in a
    notebook.
    """
    ug_per_spot_max = DOTBLOT["positive_control_ug"][0]       # 1.5 ug
    spot_volume_mL = 0.5
    ug_per_mL_max = ug_per_spot_max / spot_volume_mL
    grams = ug_per_mL_max * lysate_volume_mL * 1e-6
    molecules = grams / mw_da * AVOGADRO
    return molecules / cells / days_of_expression


def secretion_is_bounded():
    """Whether the blot bounds the SECRETED pool. It does not.

    The supernatant dots span -6 to +6 grey levels and the negative control
    occupies 5 and -6, so the two are indistinguishable and no secreted tagged
    protein was detected. That is not a bound on secreted peptide, because the
    signal peptide is removed on entry to the secretory pathway and takes the
    N-terminal tag with it, so correctly exported precursor is invisible to an
    anti-His antibody by construction. The experiment is diagnostic in the
    lysate and silent in the supernatant.
    """
    sup = DOTBLOT["supernatant_500uL"] + DOTBLOT["supernatant_1000uL"]
    neg = DOTBLOT["negative_control"]
    return {
        "supernatant_range": [min(sup), max(sup)],
        "negative_control_range": [min(neg), max(neg)],
        "distinguishable": bool(min(sup) > max(neg)),
        "bounds_secretion": False,
    }


if __name__ == "__main__":
    import json

    rng = np.random.default_rng(20261016)
    mid = {k: (lo + hi) / 2.0 for k, (lo, hi, *_r) in PARAMS.items()}
    p1 = {k: np.array([v]) for k, v in mid.items()}

    linearity = dotblot_is_quantitative()
    ceiling_1mL = float(wetlab_yield_ceiling(1.0))
    # single dose, for continuity with the result reported in October
    required_single = float(required_yield_for_ec50(p1)[0])
    # under the repeat-dosing schedule, which is what a patient receives
    unit_md = cns_concentration_multidose_nM(1.0, p1)
    required = float((mid["ec50_nM"] / unit_md)[0])
    tolerated = float(max_tolerated_yield(p1)[0])
    # linearity self-check: every term is linear in yield, so the window must
    # equal tolerated_multiple_of_ec50 exactly
    assert abs(tolerated / required - mid["tolerated_multiple_of_ec50"]) < 1e-9
    acc = float(accumulation_factor(p1)[0])
    daily = dict(p1, dose_interval_days=np.array([1.0]))

    out = {
        "free_variable": "peptide molecules secreted per transfected cell per day",
        "required_yield_bulk_csf_155mL_single_dose": required_single,
        "required_yield_bulk_csf_155mL_repeat_dosing": required,
        "max_tolerated_yield_bulk_csf": tolerated,
        "therapeutic_window_fold": tolerated / required,
        "accumulation_factor_at_midpoint_interval": acc,
        "accumulation_factor_daily_dosing": float(accumulation_factor(daily)[0]),
        "wetlab_ceiling_molecules_cell_day_per_mL_lysate": ceiling_1mL,
        "wetlab_ceiling_vs_required_fold": ceiling_1mL / required,
        "wetlab_ceiling_vs_plausible_output_fold": ceiling_1mL / 1e6,
        "plausible_cellular_output": [1e4, 1e6],
        "dotblot_linearity": linearity,
        "secretion_bound": secretion_is_bounded(),
        "status": "bounded above by our own dot blot; still parametric below that",
    }
    with open("dose_model_result_v2.json", "w") as fh:
        json.dump(out, fh, indent=1)

    rows, _y, _p = sensitivity(20000, rng, yield_fixed=1e5)
    with open("dose_model_sensitivity_v2.csv", "w") as fh:
        fh.write("parameter,spearman_rho,p_value,source\n")
        for k, rho, pv in rows:
            fh.write("%s,%.4f,%.3g,%s\n" % (k, rho, pv, PARAMS[k][3]))
    print(json.dumps(out, indent=1))
