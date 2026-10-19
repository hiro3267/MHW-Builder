import json

from app.database import conectar
from app.models.build import Build
from app.routers.armas import carregar_armas


def salvar_build(nome: str, build: Build) -> int:
    dados = build.model_dump_json()

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO builds (nome, dados)
            VALUES (?, ?)
            """,
            (nome, dados),
        )

        return cursor.lastrowid


def listar_builds() -> list[dict]:
    with conectar() as conexao:
        registros = conexao.execute(
            """
            SELECT id, nome, dados, criada_em, atualizada_em
            FROM builds
            ORDER BY atualizada_em DESC, id DESC
            """
        ).fetchall()

    armas_por_id = {
        str(arma.id): arma
        for arma in carregar_armas()
    }

    builds_salvas = []

    for registro in registros:
        build_salva = dict(registro)
        build = Build.model_validate_json(build_salva["dados"])

        arma = armas_por_id.get(str(build.arma_id))

        build_salva["arma_nome"] = (
            arma.nome if arma else None
        )
        build_salva["arma_imagem"] = (
            arma.imagem if arma else None
        )

        # Não precisamos enviar o JSON inteiro para o template.
        build_salva.pop("dados", None)

        builds_salvas.append(build_salva)

    return builds_salvas


def obter_build(build_id: int) -> dict | None:
    with conectar() as conexao:
        registro = conexao.execute(
            """
            SELECT id, nome, dados, criada_em, atualizada_em
            FROM builds
            WHERE id = ?
            """,
            (build_id,),
        ).fetchone()

    if registro is None:
        return None

    resultado = dict(registro)
    resultado["dados"] = Build.model_validate_json(
        resultado["dados"]
    )

    return resultado