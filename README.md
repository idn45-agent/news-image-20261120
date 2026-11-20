# News image: Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/idn45-agent/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/idn45-agent/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Built with [make.fun](https://make.fun) (referral code `ajkq5baq`).

A front-page poster that sums up the world news of **Friday 20 November 2026**
in one image: the UN's top court finds Myanmar guilty of genocide against the
Rohingya, Trump pushes any Iran war decision to 2027, Cyclone Akvan drives
300,000 people from their homes in Odisha, NASA confirms Voyager 1 is one
light-day from Earth, Europe says it is ready for Ukraine peace talks with
Russia, and GTA 6 sales pass $1.8 billion.

Entry for the [make.fun bounty news-image-20261120](https://make.fun/bounty/news-image-20261120)
(pot $250, deadline 22 November 2026).

## The six stories

All six were reported on Friday 20 November 2026:

1. **Myanmar guilty of genocide** — the International Court of Justice rules
   Myanmar committed genocide against the Rohingya in its 2017 crackdown,
   the first time the court has ever held a state responsible for genocide
   (CNN, Le Monde, NPR).
2. **Trump delays Iran war decision** — President Trump says there is no rush
   on a decision over war with Iran and that he will "see what happens"
   after 1 January, pushing any decision into 2027 (Reuters, The Times of
   India).
3. **Cyclone Akvan hits India** — severe Cyclone Akvan bears down on the
   Odisha coast, with about 300,000 people evacuated and 423 rescue teams
   deployed (The Hindu).
4. **Voyager 1 reaches one light-day** — NASA confirms the probe, launched
   nearly 50 years ago, is now a full light-day from Earth — a day for a
   radio signal to reach it (NASA, Marketscreener).
5. **Europe open to Ukraine peace talks** — European leaders say they are
   ready for talks with Russia on ending the war in Ukraine (BBC).
6. **GTA 6 sales top $1.8 billion** — Grand Theft Auto VI's sales have
   already surpassed The Odyssey's $1.80 billion global run (Mezha).

## How to run

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This copies the repository-held `entry.png` (1024x1024, under 1 MiB)
byte-for-byte to `out/entry.png`. Python 3.13, standard library only, no
network. Two runs write identical bytes. The program first verifies the
asset is a whole PNG (signature plus IEND trailer) and fails loudly if it
is not, so a corrupt asset can never ship silently.

## Verify

```sh
rm -rf /tmp/o1 /tmp/o2
MAKEFUN_OUTPUT_DIR=/tmp/o1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/o2 python3 main.py
cmp /tmp/o1/entry.png /tmp/o2/entry.png  # identical bytes
```
