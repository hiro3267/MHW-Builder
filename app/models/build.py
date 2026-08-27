from pydantic import BaseModel
from typing import List, Optional


class Build(BaseModel):
    arma_id: str | None = None
    kinsect_id: str | None = None  # só relevante se a arma for Insect Glaive
    cabeca_id: str | None = None
    peito_id: str | None = None
    bracos_id: str | None = None
    cintura_id: str | None = None
    pernas_id: str | None = None
    talisma_id: str | None = None

    arma_decoracoes: List[Optional[int]] = []
    cabeca_decoracoes: List[Optional[int]] = []
    peito_decoracoes: List[Optional[int]] = []
    bracos_decoracoes: List[Optional[int]] = []
    cintura_decoracoes: List[Optional[int]] = []
    pernas_decoracoes: List[Optional[int]] = []