from enum import Enum

from common.enums import BaseEnum


class SNBoolEnum(BaseEnum):
    S = (True, "S")
    N = (False, "N")


class ServiceEnum(Enum):
    SEDEX_VAREJO = 40010
    SEDEX_A_COBRAR_VAREJO = 40045
    SEDEX_10_VAREJO = 40215
    SEDEX_HOJE_VAREJO = 40290
    PAC_VAREJO = 41106


class ShapeEnum(Enum):
    FORMATO_CAIXA_PACOTE = 1
    FORMATO_ROLO_PRISMA = 2
    ENVELOPE = 3


class CalcEnum(Enum):
    SO_PREÇO = 1
    SO_PRAZO = 2
    PRECO_E_PRAZO = 3


class FormatReturnEnum(Enum):
    XML = "XML"
    POPUP = "Popup"
    URL = "URL"
