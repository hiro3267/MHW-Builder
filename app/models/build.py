from pydantic import BaseModel


class Build(BaseModel):
    arma_id: str | None = None
    kinsect_id: str | None = None  # só relevante se a arma for Insect Glaive
    cabeca_id: str | None = None
    peito_id: str | None = None
    bracos_id: str | None = None
    cintura_id: str | None = None
    pernas_id: str | None = None
    talisma_id: str | None = None