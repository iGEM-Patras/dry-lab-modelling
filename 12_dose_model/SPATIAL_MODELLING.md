# Spatial modelling: what CompuCell3D and PhysiCell can answer here, and what they cannot

**22 Nov 2026.** Both are free, open source, and run on a laptop. Both are a good fit for
this project's single largest stated weakness. One of them would give a wrong answer to the
question it looks most obviously suited to, and that is worth knowing before anyone spends
a month on it.

---

## 1 · The weakness they address

`dose_model.py` says this about itself, in its own docstring:

> It is a steady-state compartment model, not a spatially resolved one. It assumes the
> peptide that reaches the CNS compartment mixes within it, which overestimates
> concentration at a distant target and underestimates it near the site of production.

And the model's headline conclusion is that bulk CSF dilution is fatal, so **the therapy has
to act locally**. That conclusion is a statement about space, reached with a model that has
none. Replacing the compartment with a diffusion–reaction field is the natural next step,
and **PhysiCell's BioFVM solver does exactly that**: multiple diffusing substrates on a 3D
domain with cell-based sources and sinks, agents that secrete and take up.

## 2 · The answer in closed form, before anyone writes a simulation

For a point source secreting into a medium with diffusion coefficient `D` and first-order
degradation `k`, the steady-state field is

```
C(r) = Q / (4 π D r) · exp(−r/λ)        with      λ = sqrt(D/k)
```

`λ` is the distance over which the peptide survives, and it is the only length scale in the
problem. Using the dose model's own half-life range of 1–5 minutes and an effective tissue
diffusion coefficient of 50–200 µm²/s for a ~1 kDa peptide:

| | λ |
|---|---|
| fastest degradation, slowest diffusion | **66 µm** |
| central case (D = 100 µm²/s, t½ = 3 min) | **161 µm** |
| slowest degradation, fastest diffusion | **294 µm** |

**This is independently checkable, and it checks out.** Somatostatin-14, a neuropeptide of
comparable size, was released from implanted nanovesicles in mouse neocortex and detected
optically: transmission was reduced but synchronised **within 130 µm**, and markedly smaller
and delayed beyond it (PMID 35723610). A measured neuropeptide volume-transmission scale
sits inside the range our own parameters predict, which is the closest thing to a validation
this project has for any spatial claim.

So the local picture is quantitative now: **our payload acts over roughly a tenth of a
millimetre — about ten cell diameters.** That is what "acts locally" means, and it can be
said with a number instead of a hedge.

## 3 · A result that changes how the silencing arm should be described

Concentration near a source scales linearly with half-life, which is how the dose model
reports the MME knockdown: 2.7-fold at midpoint. But **range** scales as **√(half-life)**,
and the **volume served** scales as **half-life^(3/2)**:

| knockdown | concentration | range | volume served |
|---|---|---|---|
| 1.5× | 1.5× | 1.22× | 1.84× |
| 2.75× (midpoint) | 2.75× | 1.66× | **4.56×** |
| 4× | 4× | 2.00× | 8.00× |

**The siRNA arm buys territory, not just concentration.** At midpoint it extends the radius
of useful signalling by two-thirds and the volume each transfected cell serves by 4.6-fold.
Since the transfected fraction is small and patchy, coverage is plausibly the binding
constraint, which makes this the stronger argument for the second arm — and it is one the
project has never made, because a compartment model cannot express it.

## 4 · The finding that disqualifies a diffusion-only model for the main leg

The nearest CNS target is on the far side of the olfactory epithelium, lamina propria and
cribriform plate — of order **0.5 to 2 mm** from a secreting cell. Over that distance the
field falls by `exp(−r/λ)`:

| distance | surviving fraction |
|---|---|
| 0.5 mm | 4.5 × 10⁻² |
| 1 mm | 2.0 × 10⁻³ |
| 2 mm | 4.1 × 10⁻⁶ |

And the timing is worse than the amplitude. Pure diffusion needs `r²/2D` ≈ **83 minutes** to
cross 1 mm. The measured brain t_max after intranasal dosing is **10 minutes**
(PMID 41901301).

**Diffusion is too slow by an order of magnitude and too lossy by three.** Nose-to-brain
transport is therefore convective — bulk flow along perineural and perivascular channels
following the olfactory and trigeminal nerves — which is exactly what the delivery
literature describes, and what makes a 10-minute t_max possible at all.

**BioFVM solves diffusion and decay. It does not solve advection.** A PhysiCell model of the
nose-to-brain leg would faithfully reproduce a transport mechanism that is not the operative
one, and would conclude the therapy cannot work. That conclusion would be an artefact of the
solver. **Do not model the nose-to-brain leg in PhysiCell as supplied.**

## 5 · Where each tool is the right choice

**PhysiCell / BioFVM — the local field.** Once the peptide has arrived, what does the
concentration look like around sparsely transfected cells? Only a few percent of exposed
cells are transfected, so the field is a superposition of point sources at 10⁴–10⁵ µm²
spacing against a λ of ~161 µm. Whether that sums to a smooth field or isolated spikes
decides whether "local action" means useful tissue coverage or scattered hot spots. This is
genuinely a simulation question — the answer depends on source geometry — and it is squarely
what BioFVM is built for. Parameters needed: D, k, per-cell secretion rate, transfected-cell
density. Three of the four are already in the dose model.

**CompuCell3D — the epithelium under repeated dosing.** The open question in
`OLFACTORY_SAFETY.md` is whether daily cationic-lipid injury outpaces regeneration from
basal cells. That is a cell-level question about death, division and tissue integrity over
weeks, which is what a Cellular Potts model does well and what a PDE cannot represent at
all. It would turn "we don't know if the epithelium recovers" into a testable prediction to
set against the MucilAir result.

## 6 · Priority, stated plainly

These tools are free but not cheap: a usable PhysiCell or CC3D model is weeks of work, and
the parameters it needs — secretion rate per cell, transfected-cell density, the olfactory
diffusion coefficient — are exactly the numbers the wet lab has not measured. **A simulation
built on four assumed parameters is not more trustworthy than the algebra in section 2; it
is the same uncertainty, more expensively packaged, and harder for a judge to audit.**

The order that makes sense:

1. **Use section 2 now.** It is three lines of algebra, it is cross-validated against a
   published in vivo measurement, and it converts the dose model's biggest caveat into a
   quantitative statement. It costs nothing and it is already done.
2. **Run the cheap experiments** in `MPPD_DEPOSITION_PLAN.md` — the actuation-integrity test
   first — because they produce the parameters any simulation would need.
3. **Then build the PhysiCell local-field model**, which answers a real question the algebra
   cannot: whether sparse sources give coverage or hot spots.
4. **CompuCell3D for epithelial regeneration** only if the MucilAir result shows injury
   worth modelling.

Simulation should follow the measurements here, not substitute for them.

## References

| source | used for |
|---|---|
| PMID 35723610 | somatostatin volume transmission measured within 130 µm in vivo — validates the λ estimate |
| PMID 38789677 | review of volume-transmission mechanisms and spatiotemporal scales |
| PMID 41901301 | intranasal brain t_max of 10 min — the timing that rules out diffusion |
| PhysiCell / BioFVM (physicell.org) | agent-based cells with a 3D diffusion–decay substrate solver; no advection |
| CompuCell3D (compucell3d.org) | Cellular Potts tissue model for injury and regeneration |

Full citations with links: [`REFERENCES.md`](REFERENCES.md).

---

## 7 · Added 22 Nov: the PhysiCell question, answered without PhysiCell

Section 5 assigned the coverage-versus-hot-spots question to a simulation. With one
diffusion length and randomly placed sources it has a closed form:

```
coverage = 1 − exp(−ρ · π · λ²)
```

the probability that a point lies within one diffusion length of at least one transfected
cell. Code: `data/coverage_model.py`. Figure: `coverage_map.png`.

At the dose model's midpoint parameters there are **3,857 transfected cells over 6 cm²** —
a density of 6.4 × 10⁻⁶ per µm², which is a **mean spacing of 394 µm against a λ of 161 µm**.
The sources are more than two diffusion lengths apart.

| | tissue within one λ of a source |
|---|---|
| native | **40.8 %** |
| with MME knockdown | **76.4 %** |

**The knockdown arm nearly doubles coverage, 1.87-fold, at the same transfection
efficiency.** That is a different and stronger claim than the 2.7-fold concentration gain
the dose model reports, and it is the argument the second arm has been missing.

### Superposition helps more than the closed form admits

A direct sum of the fields (107 sources over 4 × 4 mm) puts **66.9 %** of the area above the
one-λ level natively and **98.6 %** with knockdown, against the 40.8 % and 76.4 % above. The
difference is real: a point can clear a threshold on the sum of several distant sources
while lying within one diffusion length of none of them. **Treat the closed form as a lower
bound and the superposition as the realistic figure.**

### The result the coverage number hides

The native field is **extremely uneven: peak-to-median 66, CV 1.70.** With knockdown it
falls to **32 and 1.14.** Panels (a) and (b) show why — natively the tissue is a scatter of
bright spots in a dark field; with the longer λ the spots merge.

This matters for safety, not only efficacy. Hot spots are where local concentration is
highest, so they are where receptor over-activation would first occur, and the exposure
ceiling in `dose_model.py` is computed on a **mean**. A field with a peak-to-median of 66
can hold its mean below the ceiling while its hot spots sit far above it. **Halving the
peak-to-median ratio widens the real safety margin at the same average exposure** — so the
silencing arm improves safety as well as coverage, which nothing in the project currently
claims.

### What this does and does not settle

It settles the geometry for a flat epithelium with randomly placed sources, which is the
case section 5 described, and it does so in seconds rather than weeks. It does **not** cover
clustered transfection (lipoplex deposition is patchy, and clustering lowers coverage at the
same density), uptake by receptor-bearing cells acting as sinks, or any tissue mechanics.
Those remain genuine PhysiCell and CompuCell3D questions.

But the headline is now available without either: **at our own midpoint assumptions, under
half the target tissue is within reach of the payload natively, and the silencing arm is
what brings it above three-quarters.**
