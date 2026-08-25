"""
Script para importar armas da API pública mhw-db.com e converter para o
formato usado pelo Arma model (app/models/arma.py).

Rode este script na SUA máquina (aqui não tenho acesso à rede):

    python -m app.scripts.importar_armas

Ele salva o resultado em app/data/armas.json, sobrescrevendo o que já existe.
Faça um backup do armas.json atual antes de rodar, se quiser manter os dados
de teste.
"""

import json
from pathlib import Path

import requests

MHW_DB_URL = "https://mhw-db.com/weapons"
DATA_PATH = Path("app/data/armas.json")

# Mapeia o "type" da mhw-db para o nosso "tipo" em português.
# Confira os valores reais retornados pela API caso algum tipo não seja
# mapeado corretamente (ficará com o valor original em inglês).
MAPA_TIPOS = {
    "great-sword": "grande_espada",
    "long-sword": "espada_longa",
    "sword-and-shield": "espada_e_escudo",
    "dual-blades": "laminas_duplas",
    "hammer": "martelo",
    "hunting-horn": "chifre_de_caca",
    "lance": "lanca",
    "gunlance": "lanca_de_fogo",
    "switch-axe": "machado_de_troca",
    "charge-blade": "espada_e_machado_de_carga",
    "insect-glaive": "glaive_insetos",
    "bow": "arco",
    "light-bowgun": "bowgun_leve",
    "heavy-bowgun": "bowgun_pesado",
}

# Mapeia as cores do "durability" da mhw-db para os campos do nosso Sharpness.
MAPA_CORES = {
    "red": "vermelho",
    "orange": "laranja",
    "yellow": "amarelo",
    "green": "verde",
    "blue": "azul",
    "white": "branco",
    "purple": "roxo",
}


def converter_sharpness(durability: list[dict]) -> list[dict] | None:
    if not durability:
        return None
    return [
        {MAPA_CORES[cor]: valor for cor, valor in nivel.items() if cor in MAPA_CORES}
        for nivel in durability
    ]


def converter_arma(item: dict) -> dict:
    arma = {
        "id": str(item["id"]),
        "nome": item["name"],
        "tipo": MAPA_TIPOS.get(item["type"], item["type"]),
        "raridade": item["rarity"],
        "ataque_display": item["attack"]["display"],
        "ataque_bruto": item["attack"]["raw"],
        "afinidade": item.get("attributes", {}).get("affinity", 0),
        "defesa_bonus": item.get("attributes", {}).get("defense", 0),
        "elderseal": item.get("elderseal"),
        "tipo_dano": item.get("damageType"),
        "elementos": [
            {"tipo": e["type"], "valor": e["damage"], "oculto": e.get("hidden", False)}
            for e in item.get("elements", [])
        ],
        "slots": [s["rank"] for s in item.get("slots", [])],
    }

    crafting = item.get("crafting") or {}
    if crafting.get("previous"):
        arma["anterior_id"] = str(crafting["previous"])
    if crafting.get("branches"):
        arma["proximos_ids"] = [str(b) for b in crafting["branches"]]

    sharpness = converter_sharpness(item.get("durability", []))
    if sharpness:
        arma["sharpness"] = sharpness

    # Campos específicos por tipo de arma — a mhw-db pode retornar chaves
    # diferentes dependendo do tipo (ex: "notes" para Chifre de Caça,
    # "coatings" para Arco, "ammo" para Bowguns, "phial"/"phialType" para
    # Machado de Troca / Espada e Machado de Carga, "shelling" para Lança de
    # Fogo). Ajuste os nomes das chaves abaixo conforme o que a API
    # realmente devolver para cada tipo (confira imprimindo um item bruto).
    if "notes" in item:
        arma["melodias"] = item["notes"]
    if "shelling" in item and isinstance(item["shelling"], dict):
        arma["tipo_disparo"] = item["shelling"].get("type")
        arma["nivel_disparo"] = item["shelling"].get("level")
    if "phial" in item and isinstance(item["phial"], dict):
        arma["tipo_frasco"] = item["phial"].get("type")
        arma["nivel_frasco"] = item["phial"].get("damage")
    if "kinsectBonus" in item:
        arma["bonus_kinsect"] = item["kinsectBonus"]
    if "coatings" in item:
        coatings = item["coatings"]
        if coatings and isinstance(coatings[0], dict):
            arma["coatings"] = [c.get("type", str(c)) for c in coatings]
        else:
            arma["coatings"] = coatings
    if "ammo" in item:
        ammo = item["ammo"]
        if isinstance(ammo, dict):
            arma["municoes"] = [
                {"tipo": tipo, "capacidade": capacidade}
                for tipo, capacidade in ammo.items()
            ]
        elif isinstance(ammo, list):
            arma["municoes"] = [
                {
                    "tipo": m.get("type", str(i)),
                    "capacidade": m.get("capacity", m.get("clip", 0)),
                }
                for i, m in enumerate(ammo)
                if isinstance(m, dict)
            ]

    return arma


def main():
    resposta = requests.get(MHW_DB_URL, timeout=30)
    resposta.raise_for_status()
    dados_brutos = resposta.json()

    armas = [converter_arma(item) for item in dados_brutos]

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(armas, f, ensure_ascii=False, indent=2)

    print(f"{len(armas)} armas importadas em {DATA_PATH}")


if __name__ == "__main__":
    main()