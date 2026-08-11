#!/usr/bin/env python3
"""Extract DELTA TOTAL (dG_bind) from a gmx_MMPBSA FINAL_RESULTS .dat file.

Emits ONE csv row: control,receptor,rep,dG_bind  -- the exact schema gate.py reads.

Why a parser and not a grep: the .dat contains several "TOTAL" lines (complex,
receptor, ligand, then the delta). Grepping the wrong one yields a number that is
large, plausible, and meaningless. This anchors on the GENERALIZED BORN delta block
and fails loudly rather than returning the first match.
"""
import re
import sys

TAG2CONTROL = {
    "c3b_dtII": "deltorphin_II",
    "c3b_dtI":  "deltorphin_I",
    "c3b_em1":  "endomorphin_1",
    "c3b_menk": "met_enkephalin",
}


def parse_dat(path):
    txt = open(path, errors="replace").read()

    # Narrow to the GB delta block before matching TOTAL.
    m = re.search(r"GENERALIZED BORN.*?(Delta\s*\(Complex\s*-\s*Receptor\s*-\s*Ligand\)|"
                  r"DELTA\s+TOTAL|Delta TOTAL)", txt, re.S | re.I)
    if not m:
        raise SystemExit(f"FAIL: no GB delta block in {path}; "
                         f"MM-GBSA may have failed while still exiting 0")
    tail = txt[m.start():]

    rows = re.findall(r"^\s*(?:DELTA\s+TOTAL|Delta\s+TOTAL|TOTAL)\s+"
                      r"(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)",
                      tail, re.M)
    if not rows:
        raise SystemExit(f"FAIL: no TOTAL row parsed from the delta block of {path}")

    avg, sd, sem = (float(x) for x in rows[-1])
    return avg, sd, sem


def main():
    dat, tag, rep = sys.argv[1:4]
    avg, sd, sem = parse_dat(dat)

    stem = tag.rsplit("_", 1)[0]          # c3b_dtII_DOR -> c3b_dtII
    recep = tag.rsplit("_", 1)[1]         # -> DOR
    if stem not in TAG2CONTROL:
        raise SystemExit(f"FAIL: unknown control tag {stem!r}; refusing to guess")
    if recep not in ("DOR", "MOR"):
        raise SystemExit(f"FAIL: unknown receptor {recep!r}")

    receptor = {"DOR": "OPRD1", "MOR": "OPRM1"}[recep]

    if not (-200.0 < avg < 50.0):
        raise SystemExit(f"FAIL: dG_bind {avg} kcal/mol is outside any physical "
                         f"range for this system; refusing to emit it")

    print(f"{TAG2CONTROL[stem]},{receptor},{rep},{avg:.3f}")


if __name__ == "__main__":
    main()
