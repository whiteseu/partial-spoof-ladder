# EXCERPT, not a runnable module. Imports, I/O and the driver are
# omitted. Reproduced verbatim from the working tree so that the rule
# stated in the paper can be checked against the code that produced the
# numbers.
#
# Source: src/build_ladder_corpus.py, the join used for every
# condition and crossfade width. Sec. 2.1 of the paper.
#
# The two properties the paper relies on are visible here: the fade
# weights are complementary (ramp and 1-ramp), and a same-source
# join takes gain exactly 1.0, so the self-rejoin is an identity at
# every width.

def join(left: np.ndarray, right: np.ndarray, cut: int, width_ms: float,
         right_offset: int = 0, force_unit_gain: bool = False):
    """Level-matched crossfade at `cut`; `right` is read from `cut + right_offset`.

    Both sources are indexed by absolute sample position, so mixing a signal
    with itself is exact and the only residual is the level-matching gain.
    """
    total = int(DURATION_S * TARGET_SR)
    # Utterance-level gain, not a local window. Acceptance showed that matching
    # the 200 ms before the cut to the 200 ms after it imposes a large artificial
    # step even when both sides are the SAME continuous signal -- median 1.29 and
    # up to 2.98 on real speech, because speech level is non-stationary. That
    # procedure flattens a source's own dynamics instead of correcting a
    # difference between sources. Comparing whole-utterance levels corrects only
    # what it should: a same-source join gets a gain of exactly 1 and is an
    # identity, while a cross-source join is levelled without erasing the local
    # dynamics that a real splice would carry.
    start = cut + right_offset
    left_rms = float(np.sqrt(np.mean(left[:total] ** 2) + 1e-12))
    right_rms = float(np.sqrt(np.mean(right[start: start + total] ** 2) + 1e-12))
    if force_unit_gain or left is right:
        gain = 1.0
    else:
        limit = 10 ** (GAIN_LIMIT_DB / 20)
        gain = float(np.clip(left_rms / right_rms, 1 / limit, limit))

    shifted = np.zeros(total, dtype=np.float32)
    take = min(total, len(right) - right_offset)
    shifted[:take] = right[right_offset: right_offset + take] * gain

    fade = int(width_ms / 1000 * TARGET_SR)
    out = np.empty(total, dtype=np.float32)
    if fade <= 1:
        out[:cut] = left[:cut]
        out[cut:] = shifted[cut:]
        return out, gain
    half = fade // 2
    lo, hi = cut - half, cut - half + fade
    out[:lo] = left[:lo]
    ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
    out[lo:hi] = left[lo:hi] * (1.0 - ramp) + shifted[lo:hi] * ramp
    out[hi:] = shifted[hi:]
    return out, gain
