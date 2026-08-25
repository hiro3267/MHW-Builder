"""
Importa charms da API mhw-db.com para app/data/talismas.json.
Cada rank de um charm vira uma linha própria (ex: "Poison Charm 1",
"Poison Charm 2", "Poison Charm 3" viram 3 talismãs distintos).

Rode na sua máquina:
    python -m app.scripts.importar_talismas
"""

import json
from pathlib import Path

import requests

MHW_DB_URL = "https://mhw-db.com/charms"
DATA_PATH = Path("app/data/talismas.json")


def converter_talismas(item: dict) -> list[dict]:
    talismas = []
    for rank in item.get("ranks", []):
        talismas.append({
            "id": f"{item['id']}-{rank['level']}",
            "nome": rank["name"],
            "nivel": rank["level"],
            "raridade": rank["rarity"],
            "skills": [
                {"nome": s.get("skillName", s.get("slug", "?")), "nivel": s["level"]}
                for s in rank.get("skills", [])
            ],
        })
    return talismas


def main():
    resposta = requests.get(MHW_DB_URL, timeout=30)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    talismas = []
    for item in dados_brutos:
        talismas.extend(converter_talismas(item))

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(talismas, f, ensure_ascii=False, indent=2)

    print(f"{len(talismas)} talismãs importados em {DATA_PATH}")


if __name__ == "__main__":
    main()