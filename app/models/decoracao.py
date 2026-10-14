from pydantic import BaseModel, Field

from app.models.armadura import Skill


class Decoracao(BaseModel):
    id: str
    nome: str
    raridade: int
    tamanho: int
    skills: list[Skill] = Field(default_factory=list)