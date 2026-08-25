"""
Importa armaduras da API mhw-db.com para app/data/armaduras.json.

Rode na sua máquina:
    python -m app.scripts.importar_armaduras
"""

import json
from pathlib import Path

import requests

MHW_DB_URL = "https://mhw-db.com/armor"
DATA_PATH = Path("app/data/armaduras.json")

MAPA_PECA = {
    "head": "cabeca",
    "chest": "peito",
    "arms": "braco",
    "waist": "cintura",
    "legs": "perna",
}


def converter_armadura(item: dict) -> dict:
    attrs = item.get("attributes", {})
    return {
        "id": str(item["id"]),
        "nome": item["name"],
        "peca": MAPA_PECA.get(item["type"], item["type"]),
        "rank": item.get("rank"),
        "raridade": item["rarity"],
        "defesa": attrs.get("defense", 0),
        "resistencia_fogo": attrs.get("resistFire", 0),
        "resistencia_agua": attrs.get("resistWater", 0),
        "resistencia_trovao": attrs.get("resistThunder", 0),
        "resistencia_gelo": attrs.get("resistIce", 0),
        "resistencia_dragao": attrs.get("resistDragon", 0),
        "skills": [
            {"nome": s.get("skillName", s.get("slug", "?")), "nivel": s["level"]}
            for s in item.get("skills", [])
        ],
        "slots": [s["rank"] for s in item.get("slots", [])],
    }


def main():
    resposta = requests.get(MHW_DB_URL, timeout=30)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    armaduras = [converter_armadura(item) for item in dados_brutos]

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(armaduras, f, ensure_ascii=False, indent=2)

    print(f"{len(armaduras)} armaduras importadas em {DATA_PATH}")


if __name__ == "__main__":
    main()