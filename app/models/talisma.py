from pydantic import BaseModel

from app.models.armadura import Skill


class Talisma(BaseModel):
    id: str
    nome: str
    raridade: int
    skills: list[Skill] = []