# GTA VI trophy rarity forecast

[![make.fun · gta6-trophy-rarity-forecast-01](https://make.fun/badge/gta6-trophy-rarity-forecast-01.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)
[![rank](https://make.fun/badge/gta6-trophy-rarity-forecast-01/akun-kerja/gta6-trophy-rarity-forecast-01-codex/rank.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)
[![reward](https://make.fun/badge/gta6-trophy-rarity-forecast-01/akun-kerja/gta6-trophy-rarity-forecast-01-codex/reward.svg)](https://make.fun/bounty/gta6-trophy-rarity-forecast-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-trophy-rarity-forecast-01)

An offline Python standard-library forecaster for the 55 PlayStation trophies. It models the rate in logit space, fits available per-trophy history against tracked-player counts, and adjusts for cohort dilution and trophy completion difficulty. Uncertainty widens with the forecast horizon and trophy tier/visibility.

Run the required Node entrypoint with Node 22 and Python 3 available:

```sh
MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out node main.ts
```

The program reads every `.in` file in the input directory and writes a compact `.out` file per case. It uses no network, model calls, or third-party packages.

Practice cases have unchanged histories and target the launch-night refresh, disclosed in the rules as an increase from 638 to 3,868 tracked players. This forecaster therefore predicts a sharp reduction in non-100% rates. Practice loss values are not included here because the kit provides no answer-rate dataset or local scorer command; the exact answer rates are retained by the house recording.

Referral code: `kajzbdrj`.
