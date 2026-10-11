# Porting CABS-dock 0.9.14 from Python 2 to Python 3

The public release (PyPI `CABS` 0.9.14, 2019) is Python 2 only. Nine distinct fixes were
needed. Listed so nobody has to rediscover them.

| # | site | problem | fix |
|---|---|---|---|
| 1 | `__main__.py`, `vector3d.py` | py2 `print` statements | converted to calls |
| 2 | `pdblib.py:302,308` | tuple parameter unpacking `def getStart((x,y,z))` | unpack in the body |
| 3 | `pdblib.py` `szip` | returns a `zip` object, which py3 EXHAUSTS on first use, so the second `filter` over it would silently return nothing | wrap in `list()` |
| 4 | 5 modules | `StringIO`, `pkg_resources`, `matplotlib.ticker.IndexFormatter` | py3 equivalents with fallbacks |
| 5 | 6 modules | py2 `exception.message` | `str(exception)`. This one MASKED a real error for a whole diagnostic round |
| 6 | `pdblib.read()` | `open(...,'rb')` returned `str` in py2, `bytes` in py3 | decode at the read |
| 7 | `pdblib.dssp()` x3 | after fix 6 the body is `str`, so the `'wb'` temp write and the `Popen` pipe both break | text mode and `universal_newlines` |
| 8 | `vector3d.py` | `__div__` / `__idiv__` are py2-only protocols | aliased to `__truediv__` / `__itruediv__` |
| 9 | `cabs.py:114` | `FORTRAN_COMMAND = 'gfortran -O2'` overflows the small code model on this engine's COMMON blocks: `relocation overflow: reference to progress_` | `-mcmodel=medium -std=legacy` |

Fix 9 matters beyond compiling: the default flags DID produce a binary, with `error:` lines
in the link. A binary emitted alongside relocation errors is not trustworthy, so it was
rebuilt rather than used.

## Deviations from the preprint's protocol, carried into any result

1. **No membrane term.** The preprint used a membrane extension (their ref 9, Pulawski 2016).
   It is not in the public release: 0 mentions in source, no `--membrane` among 54 options.
2. **No DSSP.** No binary available and the fallback server is unreachable from our sandbox,
   so the receptor is modelled without assigned secondary structure. CABS degrades gracefully
   but this is not the same calculation.
3. **No D-amino acid or C-terminal amide.** CABS is coarse-grained on L-amino-acid statistics.
   Deltorphin is therefore modelled as L-Ala, free-acid: stripped of exactly the two features
   the Cycle 16 literature attributes its rigidity to.
