
from aquisicao.api_client import ApiClient
from aquisicao.mapeador import Mapeador
from aquisicao.armazenamento import Armazenamento


class Carregador:
    def __init__(self):
        self.api = ApiClient()

    def carregar_corpos(self):
        dados = self.api.buscar_todos_corpos()

        Armazenamento.salvar(dados)

        corpos = Mapeador.mapear_corpos(dados)

        return corpos
