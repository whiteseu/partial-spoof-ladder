# partial-spoof-ladder

Companion material for *Auditing Partial-Spoof Localization with
Authenticity-Preserving Edits*.

The paper asks whether a frame-level partial-spoof localizer responds to
source authenticity or to the splicing edit that a splice-built corpus uses to
create it. It edits bona fide audio in ways that leave every mask label
unchanged, and moves training labels while holding the training waveform
byte-identical.

`code/` holds excerpts of the routines the paper's claims rest on, with
imports, I/O and drivers removed; they are for reading against the paper, not
for execution. Audio and model weights are not redistributed here: PartialSpoof
and LlamaPartialSpoof carry their own licences, and all four audited outputs
are released checkpoints from their original authors.

## `code/`

| file | source | what it backs |
|---|---|---|
| `construction_join.py` | `src/build_ladder_corpus.py` | Sec. 2.1. The join used for every condition and crossfade width. The fade weights are complementary and a same-source join takes gain exactly 1.0, which is why the self-rejoin is an identity at every width and scores bit-identically. |
| `readout_region_rule.py` | `analysis/r7_readout.py` | Sec. 2.2. `offset = hop*frame + delta - boundary_ms`; frames inside the crossfade region `abs(offset) <= width/2` are dropped from **both** conditions; the measured side is `offset >= 0`. `T(x)` is flagged duration on that side. |
| `label_intervention.py` | `analysis/sal_counter.py` | Sec. 4.5. The excision shared byte for byte by the `counter` and `coupled` arms. The cut is a pure function of `(seed, utt_id)` through `crc32`, never of worker scheduling, so the two arms differ only in the label at the join. The assertions make "every excised frame was bona fide" a checked claim rather than an assumption. |

## `manifests/`

`indomain_manifest.csv` lists all 9,750 scored items: 750 construction sets by
13 items each (the unedited recording, and the self-rejoin, deletion and
same-speaker splice at four crossfade widths). Each row carries the cut
position in samples and in ms, the crossfade width, the speaker, the source
keys on both sides of the join, and the level-matching gain, which is exactly
1.0 wherever the join is same-source.

`cut_voicing_indomain.csv` is the signal state measured at the cut, and
`sets_voiced.txt`, `sets_unvoiced.txt` and `sets_silence.txt` are the
resulting stratum memberships used in Sec. 4.2 and Sec. 4.4.
`control_sources.txt` lists the source recordings removed from the calibration
subsample before any threshold was frozen.

## `results/`

**`reported/`** — the paper's own tables as CSV. `table1_response.csv` is
Table 1 with the bootstrap interval endpoints as columns, `table2_join_state.csv`
is Table 2 with the significance stars as a `*_excludes_zero` flag,
`table3_training_arms.csv` is Table 3, and `sal_finetune_per_seed.csv` is the
released-system fine-tuning of Sec. 4.5 per seed and arm, carried at two
decimals rather than the one the paper prints.

**`thresholds/`** — the frozen operating points of Sec. 3 and the equal-error
rates they were estimated from. Thresholds are fixed on a stride-20 subsample
of the evaluation list with every control source recording removed, and frozen
before any control item is scored. `*_excl.json` are the ones used for the
reported numbers; the others are the calibration variants they were checked
against.

**`reference_cues/`** — the sign-consistency statistics of Sec. 4.3 for CFPRF's
boundary head `Y_b` and a frozen WavLM codec-round-trip distance, with
bootstrap intervals. `adjudication_indomain*` are the in-domain values;
`adjudication_*_clean_with_m*` are the crossfade sweep, over which both cues
collapse to near zero (0.53 -> 0.00 and 0.74 -> 0.03) while CFPRF's response
grows.

**`training_arms/`** — per-seed outputs, one file per arm per seed, no
aggregation. `localizer_5seed/` is the localizer we train (frozen WavLM front
end, BiLSTM head) over five seeds, arms `original`, `counter` and `coupled` at
four requested label spans: the rows of Table 3 and the dose slope of Fig. 3.
`sal_finetune/` is SAL fine-tuned from its released weights over three seeds,
arms `plain`, `counter` and `coupled`: the +50.5 / +44.2 / +122.9 to
+8.6 / -4.8 / +24.2 figures of Sec. 4.5 and the 51% / 77% / 37% recoveries.
File names carry the seed itself (`20260802`-`20260806`).

## Citation

<!-- Replace before publishing the repository. -->

    <authors>, "Auditing Partial-Spoof Localization with
    Authenticity-Preserving Edits", in Proc. IEEE Int. Conf. Acoustics, Speech
    and Signal Processing (ICASSP), 2027.
