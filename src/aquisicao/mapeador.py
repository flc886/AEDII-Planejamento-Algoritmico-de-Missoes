
from modelos.corpo_celeste import CorpoCeleste


class Mapeador:
    @staticmethod
    def mapear_corpo(dados):
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
            ao_redor_de=dados.get("aroundPlanet")
        )

    @staticmethod
    def mapear_corpos(lista_dados):
        return [
            Mapeador.mapear_corpo(dados)
            for dados in lista_dados
        ]
