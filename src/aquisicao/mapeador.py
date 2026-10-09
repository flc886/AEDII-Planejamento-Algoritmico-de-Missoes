
from modelos.corpo_celeste import CorpoCeleste


class Mapeador:
    @staticmethod
    def mapear_corpo(dados):
        # Traduz os nomes/campos do JSON externo para os atributos do modelo interno.
        # get() permite que dados opcionais ausentes na API sejam representados por None.
        return CorpoCeleste(
            id=dados["id"],
            nome=dados["name"],
            nome_ingles=dados["englishName"],
            tipo=dados["bodyType"],
            semieixo_maior=dados.get("semimajorAxis"),
            perihelio=dados.get("perihelion"),
            afelio=dados.get("aphelion"),
            massa=dados.get("mass"),
            volume=dados.get("vol"),
            gravidade=dados.get("gravity"),
            velocidade_escape=dados.get("escape"),
            periodo_orbital=dados.get("avgTempo"),
            densidade=dados.get("density"),
            luas=dados.get("moons"),
            ao_redor_de=dados.get("aroundPlanet"),
            temperatura_media=dados.get("avgTemp"),
            raio_medio=dados.get("meanRadius")
        )

    @staticmethod
    def mapear_corpos(lista_dados):
        # Aplica a conversão individual a cada registro recebido da API/cache.
        return [
            Mapeador.mapear_corpo(dados)
            for dados in lista_dados
        ]
