# Pre-scoring record: the out-of-domain join-state test

This is the record referred to in Sec. 4.4 of the paper, "the ordering
predicted by P2 was specified before scoring". It is reproduced verbatim from
the project's revision log, including the outcome section written after the
numbers existed and the three caveats recorded at the same time.

Naming: this document numbers the prediction **P5** in its own local sequence.
It is the prediction the paper labels **P2** (the response tracks join state,
in particular whether the join interrupts phonation, more strongly than the
voiced fraction of the excised segment). The out-of-domain test is of the
left-side form of that claim, for the reason given below.

---

## Revision R5 — out-of-domain confirmation of the join-state result
*Recorded 2026-08-27, before the out-of-domain frames were scored.*

The join-state result of §4.2 was **found**, not predicted: the pre-registered
dose hypothesis was that the response tracks the amount of speech removed, and
the cross-tab showed instead that the two dose axes are collinear and that the
governing variable is the state of the signal at the join. That makes §4.2 an
exploratory finding on the in-domain corpus, and it is written as one. This
revision converts it into a prediction and states, before scoring, what would
falsify it.

**Axis.** `cut_voicing_ladder.csv`, the voicing state of the 50 ms ending at the
cut, computed 2026-08-23 for the stratified adjudication runs — before the
two-sided join analysis existed, and never used to select sets or thresholds.
It is one-sided; the out-of-domain audio has since been deleted, so the two-sided
`join_sides` axis cannot be recomputed there. The out-of-domain test is therefore
of the **left-side** form of the claim only, which is the side the in-domain
analysis found to dominate.

**Why the one-sided axis is admissible.** In domain, and on this same file
format, the left-only split already carries the effect: CFPRF Y_f
+103.7 / +30.1 / +5.2 ms per item and the PartialSpoof baseline
+72.2 / +19.6 / +3.1 for voiced / unvoiced / silence. A flat left-only split
would have made the out-of-domain test uninformative; it is not flat.

**Nothing is re-fitted.** Frozen operating points unchanged (CFPRF
0.8817107081413269, PartialSpoof 0.9953510165214539, both estimated in domain on
the stride-20 eval subsample with the control sources removed). δ unchanged
(12.5 ms, 0.0 ms). Region rule, mix-band handling and the four-width average
unchanged. Sets: the 638 in `sets_clean.txt`, the set already reported for this
corpus. Items: the bona-fide line only (`P_BF`, `D_BF_w*`), matching the
in-domain design; the corpus's synthetic line and its `A` family are not used.

**Corpus.** Different source recordings, speakers and generator (LibriSpeech
readings, CosyVoice) from the in-domain corpus (ASVspoof LA / PartialSpoof).
The construction code and the readout are shared, so this is a corpus
replication, not an independent re-implementation, and is reported as such.

**P5, stated before scoring.** `D − P` is largest in the `voiced` stratum and
smallest in `silence`; the `voiced` interval excludes zero for both systems and
the `silence` interval covers zero.

**Falsification.** If the `silence` interval excludes zero, or if `voiced` is
not the largest of the three strata, in either system, the phonation account
does not transfer. In that case §4.2 is restricted to the in-domain corpus by
name, the out-of-domain result is reported as a failure to replicate, and the
central claim is narrowed accordingly. This paragraph is written before the
numbers exist so that outcome cannot be re-described afterwards.

### R5 outcome, recorded 2026-08-27 after scoring

**P5 holds in all four panels** (two systems × two operating points): the
`voiced` stratum is the largest in every panel, its interval excludes zero in
every panel, and the `silence` interval covers zero in every panel.

| | in domain | OOD, frozen point | OOD, recalibrated to FPR 1 % |
|---|---|---|---|
| CFPRF `voiced` | +103.7 * | +420.0 * | +24.6 * |
| CFPRF `unvoiced` | +30.1 | +318.1 * | +21.2 * |
| CFPRF `silence` | +5.2 | +86.4 | −13.6 |
| CFPRF `voiced − silence` | — | +333.7 * | +38.2 * |
| PS `voiced` | +72.2 * | +246.1 * | +8.9 * |
| PS `unvoiced` | +19.6 * | +196.9 * | +4.8 |
| PS `silence` | +3.1 | +83.6 | +3.4 |
| PS `voiced − silence` | — | +162.5 * | +5.4 |

ms per item; `*` marks an interval excluding zero; between-cell contrasts
bootstrapped directly rather than read off overlapping intervals.

**Three things the pass does not license, stated so they cannot be dropped
later.**

*The `silence` interval covers zero for want of data, not for want of an
effect.* The out-of-domain corpus holds 29 clean silent cut points against 204
in domain — LibriSpeech readings contain far less internal silence than ASVspoof
LA — and at the frozen point the `silence` estimate is +86.4 / +83.6 ms, far
from the in-domain +5.2 / +3.1. What replicates is the *ordering* and the
`voiced − silence` contrast, not the in-domain null. The stratum definition
itself did not drift: median level at the cut is −46.08 dB out of domain against
−46.14 in domain.

*The frozen operating point does not transfer in level.* At the in-domain
equal-error threshold these systems flag 36 % (CFPRF) and 55 % (PartialSpoof) of
**unedited** post-cut frames out of domain. Absolute durations are therefore not
comparable across corpora, and the recalibrated panel is the one to read for
magnitude. That the ordering survives recalibration is the load-bearing result;
that the magnitudes do not is expected and is not evidence of anything.

*Recalibration thins the effect until PartialSpoof cannot resolve the
strata.* At FPR 1 % out of domain, the whole response is +24.6 ms (CFPRF) and
+8.9 ms (PartialSpoof); CFPRF still separates `voiced` from `silence`
(+38.2 [+17.7, +67.3]) but PartialSpoof does not (+5.4 [−4.0, +15.0]). The
claim that survives at a strict operating point out of domain is CFPRF's alone.

**A continuous-axis test, added after seeing that the silence cell was small,
and therefore not pre-registered.** `cut_voicing_ladder.csv` records the two
quantities the stratum is thresholded from. Regressing `D − P` on them uses all
638 sets. At the frozen point both axes are positive in both systems — level
+8.24 [+5.70, +10.63] and +4.65 [+2.80, +6.47] ms per dB; voiced fraction
+149.6 [+67.9, +232.0] and +81.5 [+22.4, +142.4] ms per unit. At FPR 1 % no
slope is resolvable. This is the better-powered form of the same directional
prediction; it is reported as a follow-up, not as the test.

---

