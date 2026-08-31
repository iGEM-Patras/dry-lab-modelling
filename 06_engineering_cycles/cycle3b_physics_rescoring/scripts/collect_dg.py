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
    # Return (avg, sd, sem) for the GB BINDING DELTA.
    #
    # WHY THIS IS FUSSY (bug found 2026-08-31 by the first real rescoring run)
    #   gmx_MMPBSA 1.5.0.3 prints four total rows: Complex, Receptor, Ligand, and the
    #   delta. The delta row is labelled with a UNICODE DELTA GLYPH -- U+0394 followed by
    #   TOTAL -- while the first three are plain "TOTAL". The previous implementation
    #   matched (?:DELTA\s+TOTAL|Delta\s+TOTAL|TOTAL) and took the LAST hit. That pattern
    #   never matches the delta glyph, so the last hit was the LIGAND's absolute energy
    #   (-123.33 kcal/mol) rather than dG_bind (-67.48). It passed the physical-range
    #   guard because a ligand's absolute GB energy happens to fall inside it. That is
    #   exactly the "plausible-looking dG" this module exists to prevent.
    #
    # Rules now enforced:
    #   1. Anchor on the "Delta (Complex - Receptor - Ligand)" header, never on a total row.
    #   2. Stop at the next block header so the search cannot stray into a later section.
    #   3. Accept the total row with or without the leading delta glyph.
    #   4. Require EXACTLY ONE total row in that block.
    #   5. Cross-check that the printed components sum to the printed total.
    txt = open(path, errors="replace").read()

    anchor = re.search(r"^Delta\s*\(\s*Complex\s*-\s*Receptor\s*-\s*Ligand\s*\)",
                       txt, re.M | re.I)
    if not anchor:
        raise SystemExit("FAIL: no 'Delta (Complex - Receptor - Ligand)' block in "
                         + path + "; MM-GBSA may have failed while still exiting 0")
    tail = txt[anchor.end():]

    nxt = re.search(r"^(?:Complex|Receptor|Ligand|Delta)\b", tail, re.M | re.I)
    if nxt:
        tail = tail[:nxt.start()]

    num = r"(-?\d+\.\d+)"
    rows = re.findall(r"^\s*\u0394?TOTAL\s+" + num + r"\s+" + num + r"\s+" + num
                      + r"\s+" + num + r"\s+" + num, tail, re.M)
    if len(rows) != 1:
        raise SystemExit("FAIL: expected exactly one total row in the delta block of "
                         + path + ", found " + str(len(rows))
                         + "; refusing to guess which one is dG_bind")

    avg, sd_prop, sd, sem_prop, sem = (float(x) for x in rows[0])

    # ---- cross-check: components must reproduce the total --------------------
    comps = {}
    for line in tail.splitlines():
        m = re.match(r"^\s*\u0394?([A-Z0-9][A-Z0-9 \-]*?)\s+(-?\d+\.\d+)\s", line)
        if m:
            comps[m.group(1).strip()] = float(m.group(2))
    wanted = ["BOND", "ANGLE", "DIHED", "VDWAALS", "EEL", "1-4 VDW", "1-4 EEL",
              "EGB", "ESURF"]
    missing = [w for w in wanted if w not in comps]
    if missing:
        raise SystemExit("FAIL: delta block of " + path + " is missing components "
                         + repr(missing) + "; cannot verify the total")
    ssum = sum(comps[w] for w in wanted)
    if abs(ssum - avg) > 0.15:
        raise SystemExit("FAIL: delta components sum to %.2f but the total row says %.2f "
                         "in %s. The parse is reading the wrong row -- refusing to emit "
                         "a number." % (ssum, avg, path))

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
