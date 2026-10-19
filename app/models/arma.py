from typing import Optional

from pydantic import BaseModel, Field


class Elemento(BaseModel):
    tipo: str
    valor: int
    oculto: bool = False


class Sharpness(BaseModel):
    vermelho: int = 0
    laranja: int = 0
    amarelo: int = 0
    verde: int = 0
    azul: int = 0
    branco: int = 0
    roxo: int = 0


class Municao(BaseModel):
    tipo: str
    capacidade: int


class Arma(BaseModel):
    id: int
    nome: str
    tipo: str
    raridade: int
    ataque_display: int
    ataque_bruto: int

    afinidade: int = 0
    defesa_bonus: int = 0
    elderseal: Optional[str] = None
    tipo_dano: Optional[str] = None

    elementos: list[Elemento] = Field(default_factory=list)
    slots: list[int] = Field(default_factory=list)

    # Imagens da API mhw-db
    imagem: Optional[str] = None
    icone: Optional[str] = None

    # Árvore de progressão
    anterior_id: Optional[str] = None
    proximos_ids: list[str] = Field(default_factory=list)

    # Corpo a corpo
    sharpness: Optional[list[Sharpness]] = None

    # Hunting Horn
    melodias: Optional[list[str]] = None

    # Gunlance
    tipo_disparo: Optional[str] = None
    nivel_disparo: Optional[int] = None

    # Switch Axe / Charge Blade
    tipo_frasco: Optional[str] = None
    nivel_frasco: Optional[int] = None

    # Insect Glaive
    bonus_kinsect: Optional[str] = None

    # Bow
    coatings: Optional[list[str]] = None
    niveis_carga: Optional[list[int]] = None

    # Bowguns
    municoes: Optional[list[Municao]] = None
    recuo: Optional[int] = None
    velocidade_recarga: Optional[int] = None