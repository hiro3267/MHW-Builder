from pydantic import BaseModel

from app.models.armadura import Skill


class Decoracao(BaseModel):
    id: str
    nome: str
    raridade: int
    tamanho: int  # tamanho do slot que a joia ocupa (1 a 4)
    skills: list[Skill] = []