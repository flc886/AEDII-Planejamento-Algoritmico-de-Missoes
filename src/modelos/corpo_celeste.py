
class CorpoCeleste:
    def __init__(
        self,
        id,
        nome,
        nome_ingles,
        tipo,
        semieixo_maior=None,
        perihelio=None,
        afelio=None,
        massa=None,
        volume=None,
        gravidade=None,
        velocidade_escape=None,
        periodo_orbital=None,
        densidade=None,
        luas=None,
        ao_redor_de=None,
        temperatura_media=None,
        raio_medio=None,
    ):
        self.id = id
        self.nome = nome
        self.nome_ingles = nome_ingles
        self.tipo = tipo

        self.semieixo_maior = semieixo_maior
        self.perihelio = perihelio
        self.afelio = afelio

        self.massa = massa
        self.volume = volume
        self.gravidade = gravidade
        self.velocidade_escape = velocidade_escape
        self.periodo_orbital = periodo_orbital
        self.densidade = densidade

        self.luas = luas
        self.ao_redor_de = ao_redor_de

        self.temperatura_media = temperatura_media
        self.raio_medio = raio_medio

    def __str__(self):
        return (
            f"{self.nome_ingles} ({self.id}) - "
            f"Tipo: {self.tipo}"
        )
