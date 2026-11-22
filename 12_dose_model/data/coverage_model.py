"""Does sparse transfection give tissue coverage, or isolated hot spots?

This is the question SPATIAL_MODELLING.md section 5 assigned to PhysiCell. It
turns out not to need PhysiCell: with a single diffusion length and Poisson-
distributed sources it has a closed form, and a direct superposition confirms it
in seconds.

    coverage = 1 - exp(-rho * pi * lambda^2)

rho is the areal density of transfected cells, lambda = sqrt(D/k) from section 2.
This is the probability that a random point lies within one diffusion length of
at least one source, for sources placed at random.

The superposition below is the same system without the Poisson assumption, and
it also reports what the closed form cannot: how UNEVEN the field is.
"""
import numpy as np

LN2 = np.log(2.0)
# dose_model.py parameter ranges
CELLS_EXPOSED = (1e6, 1e7)
F_OLF = (0.005, 0.05)
ETA_TF = (0.001, 0.05)
AREA_CM2 = (2.0, 10.0)
D_TISSUE = 100.0          # um^2/s, effective for a ~1 kDa peptide
T_HALF_MIN = 3.0          # dose_model t_half_min_native midpoint
KNOCKDOWN = 2.75          # dose_model knockdown_fold midpoint
CELL_RADIUS = 5.0         # um


def diffusion_length(D=D_TISSUE, t_half_min=T_HALF_MIN):
    return np.sqrt(D / (LN2 / (t_half_min * 60.0)))


def source_density(cells_exposed, f_olf, eta_tf, area_cm2):
    """Transfected cells per um^2 of epithelium."""
    return cells_exposed * f_olf * eta_tf / (area_cm2 * 1e8)


def coverage(rho, L):
    """Fraction of tissue within one diffusion length of a transfected cell."""
    return 1.0 - np.exp(-rho * np.pi * L ** 2)


def superpose(rho, L, box_um=4000.0, res_um=5.0, seed=7):
    """Direct sum of point-source fields. Returns (field, xs, ys).

    Each source contributes (r0/r) * exp(-(r-r0)/L), normalised to 1 at the cell
    surface. Superposition matters: a point can exceed a threshold through the
    sum of several distant sources while lying within one diffusion length of
    none of them, so this reads HIGHER than the closed form above.
    """
    rng = np.random.default_rng(seed)
    g = np.arange(res_um / 2, box_um, res_um)
    X, Y = np.meshgrid(g, g)
    n = rng.poisson(rho * box_um ** 2)
    xs, ys = rng.uniform(0, box_um, n), rng.uniform(0, box_um, n)
    C = np.zeros_like(X)
    for a, b in zip(xs, ys):
        d = np.maximum(np.hypot(X - a, Y - b), CELL_RADIUS)
        C += (CELL_RADIUS / d) * np.exp(-(d - CELL_RADIUS) / L)
    return C, xs, ys


if __name__ == "__main__":
    mid = lambda t: (t[0] + t[1]) / 2.0
    rho = source_density(mid(CELLS_EXPOSED), mid(F_OLF), mid(ETA_TF), mid(AREA_CM2))
    Ln, Lk = diffusion_length(), diffusion_length(t_half_min=T_HALF_MIN * KNOCKDOWN)
    print("midpoint density %.2e /um2 (mean spacing %.0f um)" % (rho, 1 / np.sqrt(rho)))
    print("lambda native %.0f um, knockdown %.0f um" % (Ln, Lk))
    print("closed-form coverage: native %.1f %%, knockdown %.1f %%"
          % (coverage(rho, Ln) * 100, coverage(rho, Lk) * 100))
    for name, L in (("native", Ln), ("knockdown", Lk)):
        C, _, _ = superpose(rho, L)
        thr = (CELL_RADIUS / L) * np.exp(-1.0)
        print("%-10s area above the one-lambda level %.1f %% | peak/median %.0f | CV %.2f"
              % (name, 100 * (C > thr).mean(), C.max() / np.median(C), C.std() / C.mean()))
