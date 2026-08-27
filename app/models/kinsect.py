from pydantic import BaseModel


class Kinsect(BaseModel):
    id: str
    nome: str
    linhagem: str
    tipo_ataque: str
    efeito_poeira: str
    nivel_elemento: int
    nivel_poder: int
    nivel_velocidade: int
    nivel_cura: int