# The World Today — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/cahya23/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/cahya23/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page summing up world news on Wednesday, 25 November 2026.

## What the image shows

Masthead **THE WORLD TODAY**, dated Wednesday, 25 November 2026, above a lead
story on the Houthi attacks on Saudi Arabia, with a drawn chart of Brent
crude at 90.97, and smaller stories on Hormuz, the AI sell-off, the Pacific,
China, Colombia and Spain. Everything is drawn from scratch with Python's
standard library only — a hand-made 5x7 bitmap font and a hand-written PNG
encoder — no photographs or copied images.

## The stories

1. **HOUTHIS HIT SAUDI OIL HEARTLAND** — Yemen's Houthis say they struck
   the Ras Tanura refinery and Riyadh's financial district, and threaten
   Jeddah and every Red Sea port. Air defences downed four drones.
   Brent crude opened at 90.97 in Asia. (Reuters, 25 Nov 2026.)
2. **TWO TANKERS HIT MINES IN HORMUZ** — Two tankers struck naval mines,
   exploded and caught fire in the Strait of Hormuz, Iran's Revolutionary
   Guards said. (Reuters, 25 Nov 2026.)
3. **AI RALLY FADES AS NVIDIA SLIDES** — Nvidia fell 5.9% after Monday's
   31.5% jump on Huang's return. Nikkei down 2.9%, Seoul down 5.3%,
   SoftBank down 15%. (Reuters, 25 Nov 2026.)
4. **SOLOMONS SIGN AUSTRALIA PACT** — Australia and the Solomon Islands
   signed a security pact on Wednesday, making Canberra the defence
   partner of choice. (Reuters, 25 Nov 2026.)
5. **SHANGHAI CHIEF PROBED IN GRAFT SWEEP** — China opened a graft inquiry
   into Politburo member Chen Jining, the fourth such probe since 2025.
   (Reuters, 25 Nov 2026.)
6. **ALL HOSTAGES FREED IN CARTAGENA** — Security forces stormed a
   supermarket in Cartagena, ending a siege. All hostages were freed.
   (Reuters, 25 Nov 2026.)
7. **PUIGDEMONT TO RETURN ON 12 DEC** — Carles Puigdemont said he will
   return to Spain on 12 December, ending nearly a decade in exile.
   (Reuters, 25 Nov 2026.)
8. **ALSO TODAY** — Greeks strike over wages; US shelves Russia
   business-deal plan; Cikande fire toll rises to 26; Pakistan's first
   astronaut reaches China station. (Reuters, 25 Nov 2026.)

## Build

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` paints the page pixel by pixel and encodes the PNG by hand with
`zlib` and `struct`. It reads no files, uses no network and no randomness,
so two runs write identical bytes.
