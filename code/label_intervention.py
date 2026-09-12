# EXCERPT, not a runnable module. Imports, I/O and the driver are
# omitted. Reproduced verbatim from the working tree so that the rule
# stated in the paper can be checked against the code that produced the
# numbers.
#
# Source: analysis/sal_counter.py, the excision shared byte for byte
# by the counter and coupled arms. Sec. 4.5 of the paper.
#
# The cut is a pure function of (seed, utt_id) through crc32, never
# of worker scheduling, so both arms see the same waveform and
# differ only in the label at the join. The asserts are what make
# 'every excised frame was bona fide' a checked claim.

BONA = 1                 # PartialSpoof seglab convention
EXCISE_SAMPLES = 3200    # 200 ms at 16 kHz
MARGIN_FRAMES = 1        # 160 ms of bona fide on each side of the join
SCALE = 2560             # samples per 0.16 s frame


def item_rng(seed, utt_id, salt):
    """Worker-independent generator for one item. crc32, not hash()."""
    key = ("%d:%s:%s" % (seed, utt_id, salt)).encode("utf-8")
    return np.random.default_rng(zlib.crc32(key))


def bona_runs(label):
    """[(start, end)) of maximal runs where label == BONA."""
    lab = np.asarray(label).astype(int)
    runs, s = [], None
    for i, v in enumerate(lab):
        if v == BONA and s is None:
            s = i
        elif v != BONA and s is not None:
            runs.append((s, i))
            s = None
    if s is not None:
        runs.append((s, len(lab)))
    return runs


def choose_cut(label, n_audio_frames, rng):
    """Frame index c at which to excise, or None if no run is long enough.

    Frames [c, c+2) hold the 1.25 excised frames, and MARGIN_FRAMES on each
    side of the resulting join must also be bona fide; all inside the audio.
    The generator is consumed identically whether or not a cut is found.
    """
    need = 2 * MARGIN_FRAMES + 2
    runs = []
    for r0, r1 in bona_runs(label):
        r1 = min(r1, n_audio_frames)          # clip to the audio, never reject for it
        if r1 - r0 >= need:
            runs.append((r0, r1))
    u1, u2 = rng.random(), rng.random()
    if not runs:
        return None
    r = runs[int(u1 * len(runs)) % len(runs)]
    lo = r[0] + MARGIN_FRAMES
    hi = r[1] - MARGIN_FRAMES - 2
    if hi <= lo:
        return None
    return lo + int(u2 * (hi - lo))


def excise(audio, label, c):
    """Remove 3200 samples at frame c and one label frame. The excision and
    its margins must be bona fide; asserted, so a bad cut aborts the run."""
    a = c * SCALE
    b = a + EXCISE_SAMPLES
    assert b <= len(audio), "excision runs off the end of the audio"
    lab = np.asarray(label).astype(int)
    assert (lab[c - MARGIN_FRAMES:c + 2 + MARGIN_FRAMES] == BONA).all(), \
        "excision or its margins touch spoofed material"
    return torch.cat([audio[:a], audio[b:]]), torch.cat([label[:c], label[c + 1:]])


class CounterDataset(PartialSpoofDataset):
