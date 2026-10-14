
import json
import shutil
from pathlib import Path
from urllib.request import Request, urlopen

ARQUIVO = Path("app/data/armaduras.json")
BACKUP = Path("app/data/armaduras.json.bak")
URL_API = "https://mhw-db.com/armor"


def baixar_armaduras():
    requisicao = Request(
        URL_API,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    with urlopen(requisicao, timeout=30) as resposta:
        dados = json.load(resposta)

    if not isinstance(dados, list) or not dados:
        raise ValueError("A API retornou uma lista vazia ou inválida.")

    return dados


def main():
    if not ARQUIVO.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {ARQUIVO}"
        )

    # Baixa e valida a resposta antes de alterar qualquer arquivo.
    armaduras_api = baixar_armaduras()

    armaduras_por_id = {
        str(item["id"]): item
        for item in armaduras_api
        if "id" in item
    }

    with ARQUIVO.open(encoding="utf-8") as arquivo:
        armaduras_locais = json.load(arquivo)

    if not isinstance(armaduras_locais, list):
        raise ValueError(
            "O JSON local não contém uma lista de armaduras."
        )

    atualizadas = 0
    nao_encontradas = []
    dados_invalidos = []

    campos_resistencia = {
        "resistencia_fogo": "fire",
        "resistencia_agua": "water",
        "resistencia_trovao": "thunder",
        "resistencia_gelo": "ice",
        "resistencia_dragao": "dragon",
    }

    for armadura in armaduras_locais:
        original = armaduras_por_id.get(
            str(armadura.get("id"))
        )

        if original is None:
            nao_encontradas.append(armadura.get("id"))
            continue

        defesa = original.get("defense")
        resistencias = original.get("resistances")

        if not isinstance(defesa, dict):
            dados_invalidos.append(armadura["id"])
            continue

        if not isinstance(resistencias, dict):
            dados_invalidos.append(armadura["id"])
            continue

        valores = {"defesa": defesa.get("base")}

        for campo_local, campo_api in campos_resistencia.items():
            valores[campo_local] = resistencias.get(campo_api)

        # Não grava zeros silenciosamente quando faltam dados.
        if any(
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            for valor in valores.values()
        ):
            dados_invalidos.append(armadura["id"])
            continue

        armadura.update(valores)
        atualizadas += 1

    # Só cria o backup se ainda não existir.
    if not BACKUP.exists():
        shutil.copy2(ARQUIVO, BACKUP)

    # Salva as alterações depois do processamento.
    temporario = ARQUIVO.with_suffix(".json.tmp")

    try:
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(
                armaduras_locais,
                arquivo,
                ensure_ascii=False,
                indent=2,
            )
            arquivo.write("\n")

        temporario.replace(ARQUIVO)

    finally:
        if temporario.exists():
            temporario.unlink()

    print(f"Armaduras atualizadas: {atualizadas}")
    print(f"IDs não encontrados na API: {nao_encontradas}")
    print(f"Armaduras com dados inválidos: {dados_invalidos}")
    print(f"Backup: {BACKUP}")


if __name__ == "__main__":
    main()
