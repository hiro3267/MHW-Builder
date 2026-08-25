from pydantic import BaseModel


class Skill(BaseModel):
    nome: str
    nivel: int


class Armadura(BaseModel):
    id: str
    nome: str
    peca: str  # "cabeca", "peito", "braco", "cintura", "perna"
    raridade: int
    defesa: int
    resistencia_fogo: int = 0
    resistencia_agua: int = 0
    resistencia_trovao: int = 0
    resistencia_gelo: int = 0
    resistencia_dragao: int = 0
    skills: list[Skill] = []
    slots: list[int] = []  # ex: [2, 0, 0]