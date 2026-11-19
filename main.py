#!/usr/bin/env python3
"""Offline GTA VI trophy rate forecast using cohort dilution and history trends."""
import json
import math
import os
from pathlib import Path

IN = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
Z = (-1.645, -0.674, 0.0, 0.674, 1.645)


def clamp(x):
    return min(99.99, max(0.01, x))


def logit(p):
    p = clamp(p)
    return math.log(p / (100.0 - p))


def logistic(x):
    return 100.0 / (1.0 + math.exp(-max(-40.0, min(40.0, x))))


def predict(case):
    hist = case["history"]
    last = hist[-1]
    tracks = [max(1, r["players_tracked"]) for r in hist]
    # Estimate the next observed cohort size. The rules disclose the first
    # refresh at 04:30Z (3,868 tracked); later forecasts use a conservative
    # exponential audience-growth prior from the release timestamp.
    at_hours = ( __import__("datetime").datetime.fromisoformat(case["at"].replace("Z", "+00:00")) -
                 __import__("datetime").datetime.fromisoformat(case["game"]["release_date"] + "T00:00:00+00:00")).total_seconds() / 3600
    target_hours = at_hours + case["horizon_minutes"] / 60.0
    if tracks[-1] < 3868 and target_hours <= 6:
        expected = 3868.0
    else:
        expected = tracks[-1] * math.exp(min(4.2, max(0.0, (case["horizon_minutes"] / 1440.0) * 0.55)))
    ratio = tracks[-1] / expected
    # Exophase's observed launch refresh expanded the tracked cohort 6.06x.
    # The main level follows the learned cohort change, tempered for new cohort
    # members who have already earned popular trophies.
    cohort_shift = math.log(ratio)
    rows = []
    for i, t in enumerate(case["trophies"]):
        rate = last["rates"][i]
        if rate is None:
            rate = 0.01
        base = logit(rate)
        valid = [(j, r["rates"][i]) for j, r in enumerate(hist) if r["rates"][i] is not None]
        # Fit the full history in logit space against log tracked players. Shrink
        # noisy two-decimal increments toward a common cohort-dilution slope.
        slope = 0.0
        if len(valid) >= 2:
            xs = [math.log(tracks[j]) for j, _ in valid]
            ys = [logit(v) for _, v in valid]
            xm, ym = sum(xs) / len(xs), sum(ys) / len(ys)
            denom = sum((x-xm)**2 for x in xs)
            if denom > 1e-9:
                slope = sum((x-xm)*(y-ym) for x, y in zip(xs, ys)) / denom
        # More tracked players generally dilutes earned-rate percentages. A
        # floor on trend strength avoids treating quantization as true decline.
        dilution = min(1.0, max(0.45, -slope)) if slope < 0 else 0.72
        med = base + cohort_shift * dilution
        # Story trophies are earned early; optional and high-tier trophies have
        # much slower discovery among newly tracked players.
        tier = t.get("tier", "bronze")
        story = (t.get("secret", False) and i + 1 in range(2, 14))
        growth = (0.22 if story else 0.09) * (case["horizon_minutes"] / 90.0)
        if tier in ("gold", "silver"):
            growth *= 0.35
        if rate >= 99.99:
            rows.append({"id": t["id"], "q": [100, 100, 100, 100, 100]})
            continue
        else:
            med += min(0.55, growth)
        # Refresh timing dominates the 90-minute practice horizon. For longer
        # forecasts uncertainty grows with time and trophy optionality.
        spread = 0.58 + 0.12 * math.sqrt(case["horizon_minutes"] / 90.0)
        if tier in ("gold", "silver") or not t.get("secret", False):
            spread += 0.12
        qs = [round(logistic(med + z * spread), 4) for z in Z]
        rows.append({"id": t["id"], "q": qs})
    return {"trophies": rows}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(IN.glob("*.in")):
        c = json.loads(f.read_text(encoding="utf-8"))
        (OUT / (f.stem + ".out")).write_text(json.dumps(predict(c), separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
