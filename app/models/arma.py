from typing import Optional

from pydantic import BaseModel


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
    elementos: list[Elemento] = None
    slots: list[int] = []  # ex: [2, 0, 0]

     # --- Árvore de progressão (para a feature de seleção via árvore) ---
    anterior_id: Optional[str] = None  # id da arma anterior na árvore
    proximos_ids: list[str] = []  # ids das armas que ramificam a partir desta

    # --- Corpo a corpo ---
    sharpness: Optional[list[Sharpness]] = None

    # --- Chifre de caça ---
    melodias: Optional[list[str]] = None

    # --- Gunlance ---
    tipo_disparo: Optional[str] = None
    nivel_disparo: Optional[int] = None

    # --- Switch Axe / Charge Blade/ Charge Axe ---
    tipo_frasco: Optional[str] = None
    nivel_frasco: Optional[int] = None

    # --- Insect Glaive ---
    bonus_kinsect: Optional[str] = None

    # --- Bow ---
    coatings: Optional[list[str]] = None
    niveis_carga: Optional[list[int]] = None

    # --- Bowgun ---
    municoes: Optional[list[Municao]] = None
    recuo: Optional[int] = None
    velocidade_recarga: Optional[int] = None