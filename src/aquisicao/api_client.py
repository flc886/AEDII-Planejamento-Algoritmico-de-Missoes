
import os
import requests


class ApiClient:
    # Endpoint base da API pública do Sistema Solar.
    BASE_URL = "https://api.le-systeme-solaire.net/rest"

    def __init__(self):
        # Valida a configuração da credencial antes de permitir chamadas à API.
        self.api_key = os.getenv("SOLAR_SYSTEM_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Token da API não encontrado. "
                "Configure a variável SOLAR_SYSTEM_API_KEY."
            )

    def _fazer_requisicao(self, endpoint):
        # Centraliza a montagem da URL, a chamada HTTP e a validação da resposta.
        url = f"{self.BASE_URL}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        # Erros HTTP são propagados; em caso de sucesso, converte JSON em dados Python.
        resposta.raise_for_status()
        return resposta.json()

    def buscar_todos_corpos(self):
        # A listagem geral retorna um objeto com os corpos dentro da chave "bodies".
        dados = self._fazer_requisicao("bodies/")
        return dados["bodies"]

    def buscar_corpo_por_id(self, identificador):
        # Consulta pontual por identificador, usada para obter um corpo específico.
        return self._fazer_requisicao(
            f"bodies/{identificador}"
        )
