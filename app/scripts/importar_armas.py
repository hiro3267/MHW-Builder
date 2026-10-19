import json
import os
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

URL_API = "https://mhw-db.com/weapons"

DIRETORIO_PROJETO = Path(__file__).resolve().parents[2]
ARQUIVO_DESTINO = DIRETORIO_PROJETO / "app" / "data" / "armas.json"

TIPOS = {
    "great-sword": "grande_espada",
    "long-sword": "espada_longa",
    "sword-and-shield": "espada_e_escudo",
    "dual-blades": "laminas_duplas",
    "hammer": "martelo",
    "hunting-horn": "corneta_de_caca",
    "lance": "lanca",
    "gunlance": "lanca_arma",
    "switch-axe": "machado_espada",
    "charge-blade": "lamina_carregada",
    "insect-glaive": "glaive_insetos",
    "light-bowgun": "fuzil_leve",
    "heavy-bowgun": "fuzil_pesado",
    "bow": "arco",
}

CORES_AFIAÇÃO = {
    "red": "vermelho",
    "orange": "laranja",
    "yellow": "amarelo",
    "green": "verde",
    "blue": "azul",
    "white": "branco",
    "purple": "roxo",
}


def converter_arma(dado: dict) -> dict:
    ataque = dado.get("attack") or {}
    atributos = dado.get("attributes") or {}
    crafting = dado.get("crafting") or {}
    assets = dado.get("assets") or {}
    phial = dado.get("phial") or {}
    shelling = dado.get("shelling") or {}

    elementos = [
        {
            "tipo": elemento["type"],
            "valor": elemento.get("damage", 0) or 0,
            "oculto": elemento.get("hidden", False),
        }
        for elemento in dado.get("elements", [])
    ]

    sharpness = []
    for nivel in dado.get("durability") or []:
        sharpness.append({
            CORES_AFIAÇÃO[cor]: nivel.get(cor, 0)
            for cor in CORES_AFIAÇÃO
        })

    slots = [
        slot.get("rank", 0)
        for slot in dado.get("slots", [])
    ]

    municoes = []
    for municao in dado.get("ammo") or []:
        capacidades = municao.get("capacities") or [0]

        # O modelo atual suporta uma capacidade por tipo.
        # Guardamos a maior capacidade disponível entre os níveis.
        municoes.append({
            "tipo": municao.get("type", "desconhecido"),
            "capacidade": max(capacidades, default=0),
        })

    coatings = dado.get("coatings")
    if isinstance(coatings, dict):
        coatings = [
            nome
            for nome, habilitado in coatings.items()
            if habilitado
        ]

    return {
        "id": str(dado["id"]),
        "nome": dado["name"],
        "tipo": TIPOS.get(dado["type"], dado["type"]),
        "raridade": dado.get("rarity", 0),
        "ataque_display": ataque.get("display", 0),
        "ataque_bruto": ataque.get("raw", 0),
        "afinidade": atributos.get("affinity", 0) or 0,
        "defesa_bonus": atributos.get("defense", 0) or 0,
        "elderseal": dado.get("elderseal"),
        "tipo_dano": dado.get("damageType"),
        "elementos": elementos,
        "slots": slots,
        "imagem": assets.get("image"),
        "icone": assets.get("icon"),
        "anterior_id": (
            str(crafting["previous"])
            if crafting.get("previous") is not None
            else None
        ),
        "proximos_ids": [
            str(id_)
            for id_ in crafting.get("branches", [])
        ],
        "sharpness": sharpness or None,
        "melodias": dado.get("melodies"),
        "tipo_disparo": shelling.get("type"),
        "nivel_disparo": shelling.get("level"),
        "tipo_frasco": phial.get("type"),
        "nivel_frasco": phial.get("damage"),
        "bonus_kinsect": dado.get("boostType"),
        "coatings": coatings,
        "niveis_carga": dado.get("chargeLevels"),
        "municoes": municoes or None,
        "recuo": dado.get("recoil"),
        "velocidade_recarga": dado.get("reload"),
    }


def main():
    print("Baixando dados das armas...")

    requisicao = Request(
        URL_API,
        headers={"User-Agent": "MHW-Build-Planner/1.0"},
    )

    with urlopen(requisicao, timeout=60) as resposta:
        dados_api = json.load(resposta)

    if not isinstance(dados_api, list) or not dados_api:
        raise ValueError("A API não retornou uma lista válida de armas.")

    armas = [converter_arma(arma) for arma in dados_api]

    # Valida os dados antes de substituir o JSON existente.
    ids = set()
    for arma in armas:
        if arma["id"] in ids:
            raise ValueError(f"ID duplicado encontrado: {arma['id']}")
        ids.add(arma["id"])

        if not arma["nome"] or not arma["tipo"]:
            raise ValueError("Arma sem nome ou tipo.")

    # Valida cada registro usando o modelo Pydantic do projeto.
    from app.models.arma import Arma

    for arma in armas:
        Arma.model_validate(arma)

    ARQUIVO_DESTINO.parent.mkdir(parents=True, exist_ok=True)

    # Grava em arquivo temporário e só depois substitui o destino.
    arquivo_temporario = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=ARQUIVO_DESTINO.parent,
            suffix=".tmp",
            delete=False,
        ) as arquivo:
            arquivo_temporario = Path(arquivo.name)
            json.dump(
                armas,
                arquivo,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(arquivo_temporario, ARQUIVO_DESTINO)
    finally:
        if arquivo_temporario and arquivo_temporario.exists():
            arquivo_temporario.unlink()

    print(f"Importação concluída: {len(armas)} armas.")
    print(f"Arquivo atualizado: {ARQUIVO_DESTINO}")


if __name__ == "__main__":
    main()