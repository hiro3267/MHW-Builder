import json
from functools import lru_cache
from pathlib import Path

DATA_PATH = Path("app/data/skills.json")


@lru_cache
def carregar_niveis_maximos() -> dict[str, int]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)

    return {
        skill["name"]: max(rank["level"] for rank in skill["ranks"])
        for skill in dados
        if skill.get("ranks")
    }

@lru_cache
def carregar_skills() -> dict[str, dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        dados = json.load(f)

    return {
        skill["name"]: skill
        for skill in dados
        if skill.get("ranks")
    }