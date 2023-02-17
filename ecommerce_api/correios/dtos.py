from dataclasses import dataclass, asdict
import xml.etree.ElementTree as ET


class BaseDataclass:
    def to_dict(self):
        return asdict(self)


@dataclass
class CorreiosRequest(BaseDataclass):
    nCdEmpresa: str # Seu código administrativo junto à ECT. O código está disponível no corpo do contrato firmado com os Correios.
    sDsSenha: str # Senha para acesso ao serviço, associada ao seu código administrativo. A senha inicial corresponde aos 8 primeiros dígitos do CNPJ informado no contrato. A qualquer momento, é possível alterar a senha no endereço
    nCdServico: str # 40010 SEDEX Varejo | 40045 SEDEX a Cobrar Varejo | 40215 SEDEX 10 Varejo | 40290 SEDEX Hoje Varejo | 41106 PAC Varejo
    sCepOrigem: str # CEP de Origem sem hífen.Exemplo: 05311900
    sCepDestino: str # CEP de Destino Sem hífem
    nVlPeso: str # Peso da encomenda, incluindo sua embalagem. O peso deve ser informado em quilogramas. Se o formato for Envelope, o valor máximo permitido será 1 kg.
    nCdFormato: int # Formato da encomenda (incluindo embalagem). Valores possíveis: 1, 2 ou 3 | 1 – Formato caixa/pacote | 2 – Formato rolo/prisma | 3 - Envelope
    nVlComprimento: float # Comprimento da encomenda (incluindo embalagem), em centímetros.
    nVlAltura: float # Altura da encomenda (incluindo embalagem), em centímetros. Se o formato for envelope, informar zero (0).
    nVlLargura: float # Largura da encomenda (incluindo embalagem), em centímetros.
    nVlDiametro: float # Diâmetro da encomenda (incluindo embalagem), em centímetros.
    sCdMaoPropria: str # Indica se a encomenda será entregue com o serviço adicional mão própria. Valores possíveis: S ou N (S – Sim, N – Não)
    nVlValorDeclarado: float # Indica se a encomenda será entregue com o serviço adicional valor declarado. Neste campo deve ser apresentado o valor declarado desejado, em Reais.
    sCdAvisoRecebimento: str # Indica se a encomenda será entregue com o serviço adicional aviso de recebimento. Valores possíveis: S ou N (S – Sim, N – Não)
    StrRetorno: str # Indica a forma de retorno da consulta. XML => Resultado em XML | Popup => Resultado em uma janela popup | <URL> => Resultado via post em uma página do requisitante
    nIndicaCalculo: str # Tipo de informação que será retornada. Valores possíveis: 1, 2 ou 3 | 1 - Só preço | 2 - Só prazo | 3 - Preço e Prazo


@dataclass
class CorreiosResponse(BaseDataclass):
    Codigo: str # Código do Serviço de Entrega.
    Valor: float # Preço total da encomenda, em Reais, incluindo os preços dos serviços opcionais
    ValorMaoPropria: float # Preço do serviço adicional Mão Própria
    ValorAvisoRecebimento: float # Preço do serviço adicional Aviso de Recebimento
    ValorValorDeclarado: float # Preço do serviço adicional Valor Declarado
    PrazoEntrega: int 
    ValorSemAdicionais: float
    EntregaDomiciliar: str
    EntregaSabado: str
    Erro: str =None # <Códigos de Erros retornados pelo calculador> + o código 7 (Serviço indisponível, tente mais tarde)
    MsgErro: str =None # Retorna a descrição do erro gerado.
    obsFim: str = None

    @classmethod
    def from_xml(cls, xml):
        """
        <?xml version="1.0" encoding="ISO-8859-1" ?>\n
        <Servicos>
            <cServico>
                <Codigo>40010</Codigo>
                <Valor>22,50</Valor>
                <PrazoEntrega>1</PrazoEntrega>
                <ValorSemAdicionais>22,50</ValorSemAdicionais>
                <ValorMaoPropria>0,00</ValorMaoPropria>
                <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
                <ValorValorDeclarado>0,00</ValorValorDeclarado>
                <EntregaDomiciliar>S</EntregaDomiciliar>
                <EntregaSabado>S</EntregaSabado>
                <obsFim></obsFim>
                <Erro>0</Erro>
                <MsgErro></MsgErro>
            </cServico>
        </Servicos>
        """
        dict_obj = {}
        for element in next(iter(ET.fromstring(xml)), []):
            dict_obj[element.tag] = element.text
        return cls(**dict_obj)