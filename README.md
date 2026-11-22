# One image: 21 November 2026 world news

A newspaper front page summing up Saturday 21 November 2026's world news,
built for the make.fun bounty `news-image-20261121`.

- `entry.png` — the image (1024x1024 PNG)
- `generate_image.py` — the Pillow script that draws it (deterministic)
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`

## The stories

The front page leads with the day's biggest story and then covers six more
across regions and fields, plus a footer strip of three further items.

Lead — GTA VI (culture / gaming, global). Rockstar's Grand Theft Auto VI
took $3.79bn in retail sales on its first day, the biggest launch for any
entertainment product in history, after 32.5 million pre-orders. The figure
was reported on 21 November by Rockstar and carried by AFP, the Daily Star,
the Times of India, CNA and the Malay Mail.

Markets (economy, global). An AI stock sell-off dragged world markets
lower: the S&P 500 fell 3.7% and Japan's Nikkei fell 5.06%.

Anthropic (technology / business, US). Anthropic opened trading on Wall
Street as a roughly $2 trillion company, the biggest stock-market debut in
history, after raising $81.3bn.

The Hague (justice, Netherlands). The International Court of Justice found
Myanmar responsible for genocide against the Rohingya people — the first
time any international court has found a state guilty of genocide.

Mexico (crime / justice). Mexican forces captured Fausto Isidro Meza Flores,
known as "El Chapo Isidro", an FBI most-wanted cartel boss, in Guasave,
Sinaloa.

Ukraine (conflict). A Russian ballistic missile struck Kryvyi Rih,
President Zelenskyy's hometown, killing two people and wounding 60.

Climate (Antalya, Turkey). The COP31 climate talks ran past their Friday
deadline, divided over fossil fuels.

Also in the news (footer). Researchers in Brazil reported that mosquitoes
carrying a bacterium cut dengue cases by 69%. About 700,000 people were
displaced in southern Ethiopia. UN talks in Geneva agreed to continue work
on rules for AI weapons.

## How the image is made

`generate_image.py` draws the whole front page with Pillow shapes and
DejaVu text: a masthead with the date, a large lead illustration (a Vice
City sunset skyline for the GTA VI story) with its headline and deck, a
grid of six panels each with a small drawn illustration, a kicker, a
headline and a one-line deck, and a footer strip. No network is used and
the output is fully deterministic — running the script twice writes the
same bytes.

`main.py` is the entry program. It needs only the Python standard library
and copies `entry.png` beside it to the output directory (the
`MAKEFUN_OUTPUT_DIR` environment variable, or `/output` by default), so
both of the grader's runs write the same bytes.
