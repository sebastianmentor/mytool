# mytool


Ett minimalt men komplett exempel på ett Python-CLI med `argparse` och `logging`.


## Kom igång


```bash
# 1) (valfritt) skapa och aktivera virtuell miljö
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate


# 2) Installera i utvecklingsläge
pip install -e .[dev]


# 3) Kör verktyget
mytool greet Ada --times 2 -vv
mytool sum 1 2 3 4


# 4) Kör tester
pytest -q