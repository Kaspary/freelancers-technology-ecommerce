import requests
from delivery.correios.dtos import CorreiosRequest, CorreiosResponse
from django.conf import settings

"""
http://www.webdesignemfoco.com/img/files/original/Manual-Correios.pdf
http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx?
    nCdEmpresa=09146920
    sDsSenha=123456
    sCepOrigem=70002900
    sCepDestino=71939360
    nVlPeso=1
    nCdFormato=1
    nVlComprimento=30
    nVlAltura=30
    nVlLargura=30
    sCdMaoPropria=n
    nVlValorDeclarado=0
    sCdAvisoRecebimento=n
    nCdServico=40010
    nVlDiametro=0
    StrRetorno=xml
    nIndicaCalculo=3
"""

def calc_price_and_deadline(params: CorreiosRequest) -> CorreiosResponse:
    response = requests.get(
        settings.CORREIOS_URL,
        params=params.to_dict()
    )
    assert response.status_code == 200
    return CorreiosResponse.from_xml(response.text)
