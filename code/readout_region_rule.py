# EXCERPT, not a runnable module. Imports, I/O and the driver are
# omitted. Reproduced verbatim from the working tree so that the rule
# stated in the paper can be checked against the code that produced the
# numbers.
#
# Source: analysis/r7_readout.py, the 160 ms region rule and T(x).
# Sec. 2.2 of the paper.
#
# offset = hop*frame + delta - boundary_ms; frames inside the
# crossfade region |offset| <= width/2 are dropped from BOTH
# conditions; the measured side is offset >= 0. delta is 12.5 ms for
# CFPRF and 0 for the 160 ms heads, as calibrated in Sec. 3.

WIDTHS = [0.0, 20.0, 60.0, 160.0]
HOP = 160.0


def load(fn):
    d = defaultdict(lambda: defaultdict(dict))
    for r in csv.DictReader(io.open(fn, encoding="utf-8-sig")):
        fam = r["family"]
        if fam not in ("P", "D", "S"):
            continue
        w = float(r["width_ms"])
        off = int(r["frame"]) * HOP - float(r["boundary_ms"])
        if (w / 2 > 0 and abs(off) <= w / 2) or off < 0:
            continue
        d[r["set_id"]][fam].setdefault(w, []).append((off, float(r["score"])))
    return d


def T(fr, thr, half):
    return sum(1 for off, sc in fr if (off > half if half > 0 else True) and sc < thr) * HOP
