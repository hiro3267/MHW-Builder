"""
Importa decorations da API mhw-db.com para app/data/decoracoes.json.

Rode na sua máquina:
    python -m app.scripts.importar_decoracoes
"""

import json
from pathlib import Path

import requests

MHW_DB_URL = "https://mhw-db.com/decorations"
DATA_PATH = Path("app/data/decoracoes.json")


def converter_decoracao(item: dict) -> dict:
    return {
        "id": str(item["id"]),
        "nome": item["name"],
        "raridade": item["rarity"],
        "tamanho": item["slot"],
        "skills": [
            {"nome": s.get("skillName", s.get("slug", "?")), "nivel": s["level"]}
            for s in item.get("skills", [])
        ],
    }


def main():
    resposta = requests.get(MHW_DB_URL, timeout=30)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    decoracoes = [converter_decoracao(item) for item in dados_brutos]

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(decoracoes, f, ensure_ascii=False, indent=2)

    print(f"{len(decoracoes)} decorations importadas em {DATA_PATH}")


if __name__ == "__main__":
    main()