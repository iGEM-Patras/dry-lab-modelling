# Nasal deposition CFD — OpenFOAM case

**Purpose: measure `f_olf` for our own device instead of assuming it.** The dose model's
third-strongest driver is the fraction of dose reaching the olfactory region, and it is
currently an assumption spanning a ten-fold range (0.5–5 %). This case computes it.

MPPD cannot do this — it handles the head with empirical filtration efficiency functions
and has no olfactory compartment. See `../12_dose_model/MPPD_DEPOSITION_PLAN.md`.

## What makes this possible

The [iLADDER](https://github.com/UCSD-Darquenne-Lab/iLADDER) `human02.2021` geometry
(Corley et al. 2021, [doi:10.1093/toxsci/kfab062](https://doi.org/10.1093/toxsci/kfab062))
is a CT-segmented human nasal airway, male 35 yr, published as an ASCII STL **in metres**
with **named surface patches** — including `Olf`. Verified with `surfaceCheck`:
300,490 triangles in 9 regions, no illegal triangles. Measured patch areas are in
`../12_dose_model/OLFACTORY_SAFETY.md` section 9; the olfactory patch is **21.60 cm²**.

The STL is not redistributed here — `Allrun` downloads it. Please cite Corley et al. 2021
if you publish anything derived from it. **The repository has no licence file**; its README
grants download and use with citation, which should be confirmed with the authors before a
derived figure goes into a journal submission.

## Running it

```sh
./Allrun 8          # 8 MPI ranks
```

Software: OpenFOAM v2412, installable free from conda-forge (`conda install -c conda-forge
openfoam`). Verified working: `blockMesh`, `snappyHexMesh`, `simpleFoam` and
`icoUncoupledKinematicParcelFoam` all present and reading this geometry.

## Resources — read before starting

**This will not run in a small container.** The published mesh for this geometry is
2.85 M elements; `snappyHexMesh` needs roughly 1.25 GB per million cells at peak, so budget
**4 GB for meshing and ~1 GB for the solver**, plus hours of wall time on 8 cores.
`maxGlobalCells` in `snappyHexMeshDict` is set to 2 M as a conservative default — **raise it
on a cluster.**

Under-resolving is not a neutral economy. The olfactory cleft is a narrow slit, deposition
there is a near-wall process, and a coarse mesh gives a confidently wrong `f_olf`. The case
therefore sets `Olf` to refinement level 4 and adds three boundary layers. If you must cut
cost, cut the number of particle sizes, not the mesh.

## The parameters that decide the answer

| parameter | where | note |
|---|---|---|
| **MMAD** | `constant/kinematicCloudProperties` | the dominant determinant of olfactory deposition. Sweep 1–10 µm; currently 4 µm |
| inlet flow | `0/U` | 15 L/min is the literature standard for deposition studies; Corley used a 7.4 L/min minute volume at 20 breaths/min |
| droplet density | `constantProperties.rho0` | 1000 kg/m³ assumes a water-like suspension. Check against the actual formulation |
| `locationInMesh` | `system/snappyHexMeshDict` | (3.7085, 4.8700, 3.5500) — **verified inside the lumen** by ray casting (odd crossing count against all 300,490 triangles). Re-verify if the geometry is swapped |

## Reading the result

`f_olf` = parcels stuck on `Olf` ÷ parcels injected. Every airway wall is a `stick` patch,
`outlet` and `inlets` are `escape`. Per-patch counts land in `log.parcel` and
`postProcessing/`.

Substitute the result into `../12_dose_model/dose_model.py` as `f_olf` — it is a point value
replacing an assumed range, which is the single largest reduction in that model's uncertainty
available to us.

## Honest status

**Not yet run.** The case is written and the toolchain and geometry are verified; no
deposition number has been produced. Anyone running it should treat the flow and particle
settings above as starting points to be justified, not as validated choices.

Cross-species work is possible with the same pipeline — iLADDER also publishes rat, monkey
and rabbit airways, which is the route to an animal-to-human deposition comparison if one is
ever needed.
