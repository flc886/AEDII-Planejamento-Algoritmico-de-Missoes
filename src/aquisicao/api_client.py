
import os
import requests


class ApiClient:
    BASE_URL = "https://api.le-systeme-solaire.net/rest"

    def __init__(self):
        self.api_key = os.getenv("SOLAR_SYSTEM_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Token da API não encontrado. "
                "Configure a variável SOLAR_SYSTEM_API_KEY."
            )

    def _fazer_requisicao(self, endpoint):
        url = f"{self.BASE_URL}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        resposta = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        resposta.raise_for_status()
        return resposta.json()

    def buscar_todos_corpos(self):
        dados = self._fazer_requisicao("bodies/")
        return dados["bodies"]

    def buscar_corpo_por_id(self, identificador):
        return self._fazer_requisicao(
            f"bodies/{identificador}"
        )
