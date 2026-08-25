from pydantic import BaseModel

from app.models.armadura import Skill


class Talisma(BaseModel):
    id: str
    nome: str
    nivel: int
    raridade: int
    skills: list[Skill] = []