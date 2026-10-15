# Cycle 18: gates passed, and the result does not survive its own diagnostic

**15 Oct 2026. Gates committed in `cycle18_prereg.json` before the fold ran. They passed.
I am reporting this as NOT INTERPRETABLE anyway, and the reason is a flaw in my gate, not
in the computation.**

---

## What was asked

The construct is already ordered and the payload must be released from the precursor by
proprotein convertases cutting at dibasic sites. Nobody had asked whether recoding all seven
cassettes leaves those sites accessible. If a site is buried, that cassette's payload is
never liberated, and the construct silently under-delivers.

Native preproenkephalin is the control: its twelve sites **are** cleaved in vivo.

## What the gates said

```
G1 control validity : native median RSA 0.404  (needs > 0.40)  -> PASS
G2 reproducibility  : 14 of 24 sites with SD < 0.15            -> PASS
G3 the question     : native 10th percentile RSA = 0.280
   engineered sites below it: KK126 (0.185), RR238 (0.171), KR261 (0.138)
```

Taken at face value that is a wet-lab-actionable result: three of twelve cassettes predicted
less accessible than any native site, and all three separable from the native mean on a
Welch test (p = 0.034, 0.005, 0.001).

**Do not act on it.**

## Why it does not survive

### 1. The structures have no confidence

```
mean pLDDT   natPENK 43.2   engPENK 37.1
```

Both are **below 50**, the conventional "very low, likely disordered" band. This is
biologically unsurprising: preproenkephalin is a secretory precursor without a stable
globular fold. But per-residue solvent accessibility read off a structure the predictor
cannot resolve is not a measurement we can stand behind.

### 2. The control carries no site-level signal

| | between-site SD | within-site SD (5 models) | ratio |
|---|---|---|---|
| native | 0.095 | 0.138 | **0.69** |
| engineered | 0.138 | 0.148 | **0.93** |

**F = 0.47 for the control.** Site-to-site differences in native preproenkephalin are
*smaller* than the scatter between five diffusion samples of the same sequence. The method
cannot tell one native site from another, and every native site is genuinely cleaved, so
there is no reference against which an engineered site can be called anomalous.

The three flagged sites have p < 0.05 only because the test compared one site's five models
against twelve site means treated as precise. They are not.

### 3. My G1 gate was the wrong gate

G1 asked **"are native sites exposed?"** (median RSA > 0.40). A disordered extended chain
satisfies that trivially. It never asked **"can the method distinguish an exposed site from
a buried one?"**, which is the capability G3 entirely depends on.

**This is the Cycle 16 error repeated.** There, the control gate failed loudly and stopped
the cycle. Here a differently-worded gate passed and would have let a meaningless number
through to a wet-lab recommendation. A control gate must test the discriminating capability,
not a property the null case also has.

## What is reportable

**The paired comparison, which needs no per-site resolution:** across all twelve
corresponding sites, mean RSA is 0.411 native versus 0.343 engineered, **difference 0.068,
p = 0.160**. No evidence that recoding the cassettes systematically buries the processing
sites. That is a weak negative, and it is the only statement this calculation supports.

## What would answer it properly

1. **The bench answers it directly.** LC-MS/MS on transfection supernatant shows which
   cassettes were cleaved. One experiment, no modelling assumption.
2. If a computational answer is wanted: molecular dynamics of the precursor with accessibility
   averaged over the ensemble, not over five static predictions. Days, and still a prediction
   about a disordered protein.

## Correction to the pre-registration

`cycle18_prereg.json` G1 is **inadequate as written** and that is recorded here rather than
quietly amended. A correct G1 would require the control to resolve a known buried site from
a known exposed one in the same structure, or require a minimum pLDDT before any RSA is read.
