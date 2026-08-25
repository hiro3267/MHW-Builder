from pydantic import BaseModel


class Kinsect(BaseModel):
    id: str
    nome: str
    raridade: int
    tipo: str  # ex: "corte", "impacto", "perfurante" (afeta o efeito de extração)
    velocidade: int
    poder: int
    alcance: int
    resistencia: int
    bonus_extracao: str  # ex: "afinidade", "defesa", "velocidade", "veneno"
    elemento: str | None = None