
from aquisicao.api_client import ApiClient
from aquisicao.mapeador import Mapeador
from aquisicao.armazenamento import Armazenamento


class Carregador:
    def __init__(self):
        # O carregador delega a comunicação HTTP ao cliente especializado.
        self.api = ApiClient()

    def carregar_corpos(self):
        # Fluxo de aquisição: buscar os dados, guardá-los em disco e convertê-los
        # para os objetos de domínio usados pelo restante do programa.
        dados = self.api.buscar_todos_corpos()

        Armazenamento.salvar(dados)

        corpos = Mapeador.mapear_corpos(dados)

        return corpos
