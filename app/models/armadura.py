from typing import Optional
from pydantic import BaseModel, Field


class Skill(BaseModel):
    nome: str
    nivel: int


class AssetsArmadura(BaseModel):
    imageMale: Optional[str] = None
    imageFemale: Optional[str] = None


class Armadura(BaseModel):
    id: str
    nome: str
    peca: str
    rank: Optional[str] = None
    raridade: int
    defesa: int
    resistencia_fogo: int = 0
    resistencia_agua: int = 0
    resistencia_trovao: int = 0
    resistencia_gelo: int = 0
    resistencia_dragao: int = 0
    skills: list[Skill] = Field(default_factory=list)
    slots: list[int] = Field(default_factory=list)
    assets: Optional[AssetsArmadura] = None