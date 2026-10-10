from pydantic import BaseModel, Field


class Build(BaseModel):
    arma_id: str | None = None
    kinsect_id: str | None = None
    cabeca_id: str | None = None
    peito_id: str | None = None
    bracos_id: str | None = None
    cintura_id: str | None = None
    pernas_id: str | None = None
    talisma_id: str | None = None

    arma_decoracoes: list[int | None] = Field(default_factory=list)
    cabeca_decoracoes: list[int | None] = Field(default_factory=list)
    peito_decoracoes: list[int | None] = Field(default_factory=list)
    bracos_decoracoes: list[int | None] = Field(default_factory=list)
    cintura_decoracoes: list[int | None] = Field(default_factory=list)
    pernas_decoracoes: list[int | None] = Field(default_factory=list)