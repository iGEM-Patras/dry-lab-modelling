"""Dose-limiting architectures for the Epione spray.

Answers the question raised at the judging session: what stops a patient in pain
from spraying more than the label allows?

The exposure ceiling, the accumulation arithmetic and the EC50 all come from
dose_model.py. This file adds only the transfer functions of the candidate
limiters, so that they can be compared on the one axis that matters: CNS
exposure as a multiple of EC50, against sprays per day.

CALIBRATION
-----------
Everything is expressed relative to the label regimen, which is defined as the
dose that yields exactly 1 x EC50 at steady state. The question is then how far
above the label a patient can go before crossing tolerated_multiple_of_ec50,
which dose_model puts at 6.5 x EC50 at midpoint parameters.

WHAT EACH LIMITER CAN AND CANNOT DO
-----------------------------------
This is the part worth reading before choosing one.

Accumulation has two sources. Spraying more puts more plasmid into each cell it
reaches, AND it reaches more cells. A limiter that senses plasmid copy number
clamps the first and is blind to the second. A limiter that senses the product
clamps both, because the product is shared across the tissue regardless of which
cell made it. Neither is strictly better: they fail in different directions,
which is why layering them multiplies rather than adds.
"""
import numpy as np
from scipy.optimize import brentq

CEILING_X_EC50 = 6.5      # dose_model.max_tolerated_yield / required_yield, midpoint
COPY_SHARE = 0.5          # share of escalation arriving as extra copies per cell
                          # rather than as newly transfected cells. ASSUMED, and
                          # measurable in one plate: see the protocol in
                          # ABUSE_DETERRENCE.md


def open_loop(m):
    """Current design. Exposure is proportional to dose: no limiter at all."""
    return np.asarray(m, float)


def copy_number_clamp(m, copy_share=COPY_SHARE):
    """miRNA incoherent feedforward loop (ComMAND-style, PMID 40300600).

    The transcript carries both the payload and a synthetic miRNA targeting its
    own 3' UTR, so more plasmid per cell produces more repressor in the same
    cell and per-cell output is held in a narrow window. The component of
    escalation that arrives as newly transfected cells is NOT clamped, because
    each new cell starts its own loop at the same set point.
    """
    return np.asarray(m, float) ** (1.0 - copy_share)


def product_feedback(m, hill=2.0, K=CEILING_X_EC50):
    """Transcription driven by a cAMP response element, read by the peptide itself.

    delta and mu receptors are Gi-coupled, so agonist occupancy lowers cAMP,
    lowers CREB phosphorylation and lowers transcription from a CRE promoter.
    The enkephalin gene carries the founding cAMP-inducible DNA element
    (PMID 3020428), CREB binds its enhancer in striatum in vivo (PMID 8346209),
    activation requires CREB phosphorylation at Ser-133 (PMID 10386963), and
    enkephalin biosynthesis is transcriptionally coupled to secretory activity
    (PMID 1364196), so the loop is native regulation restored rather than a
    circuit invented for the purpose. The CMV promoter in pcDNA3.1 is what
    discards it.

    Closed loop: C * (1 + (C/K)^hill) = m * g, with g chosen so the label dose
    gives exactly 1 x EC50. Note this COMPRESSES without capping: a first-order
    loop still reaches the ceiling, just later. Only cooperativity steepens it,
    and no achievable Hill coefficient turns it into a hard cap.
    """
    g = 1.0 + (1.0 / K) ** hill
    f = lambda x: brentq(lambda c: c * (1 + (c / K) ** hill) - x * g, 1e-12, 1e12)
    return np.array([f(x) for x in np.atleast_1d(m)])


def both_layers(m, hill=2.0, copy_share=COPY_SHARE):
    """The two independent limiters in series."""
    return product_feedback(copy_number_clamp(m, copy_share), hill=hill)


def sprays_to_ceiling(fn, limit=1e4):
    """Sprays per day at which an architecture crosses the tolerated ceiling."""
    try:
        return brentq(lambda m: float(np.atleast_1d(fn(m))[0]) - CEILING_X_EC50,
                      1.0, limit)
    except ValueError:
        return float("inf")


if __name__ == "__main__":
    arch = {
        "open loop (current design)": open_loop,
        "copy-number clamp": copy_number_clamp,
        "product feedback h=1": lambda m: product_feedback(m, hill=1.0),
        "product feedback h=2": product_feedback,
        "both layers": both_layers,
    }
    print("%-28s %9s %9s %9s  %s" % ("architecture", "3/day", "6/day", "12/day",
                                     "crosses 6.5x at"))
    for name, fn in arch.items():
        v = [float(np.atleast_1d(fn(x))[0]) for x in (3, 6, 12)]
        c = sprays_to_ceiling(fn)
        print("%-28s %8.2fx %8.2fx %8.2fx  %s"
              % (name, v[0], v[1], v[2],
                 ("%.1f sprays/day" % c) if np.isfinite(c) else "not within 1e4"))
