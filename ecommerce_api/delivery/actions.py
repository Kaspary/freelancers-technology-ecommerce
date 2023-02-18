from delivery.correios.dtos import CorreiosRequest
from delivery.correios.enums import (
    CalcEnum,
    FormatReturnEnum,
    SNBoolEnum,
    ServiceEnum,
    ShapeEnum,
)
from delivery.correios.integracao import calc_price_and_deadline


def calc_delivery_between_ceps(
    cep_origin: str,
    cep_destination: str,
    value: float,
    weight: float,
    length: float,
    height: float,
    width: float,
    diameter: float,
):
    delivery = calc_price_and_deadline(
        CorreiosRequest(
            sCepOrigem=cep_origin,
            sCepDestino=cep_destination,
            nVlPeso=weight,
            nVlComprimento=length,
            nVlAltura=height,
            nVlLargura=width,
            nVlDiametro=diameter,
            nIndicaCalculo=CalcEnum.PRECO_E_PRAZO.value,
            nCdFormato=ShapeEnum.FORMATO_CAIXA_PACOTE.value,
            sCdMaoPropria=SNBoolEnum.N.label,
            nVlValorDeclarado=value,
            sCdAvisoRecebimento=SNBoolEnum.N.label,
            nCdServico=ServiceEnum.SEDEX_VAREJO.value,
            StrRetorno=FormatReturnEnum.XML.value,
        )
    )
