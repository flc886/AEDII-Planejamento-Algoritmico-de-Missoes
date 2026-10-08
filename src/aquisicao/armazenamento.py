
import json
from pathlib import Path


class Armazenamento:
    CAMINHO = (
        Path(__file__).resolve().parents[2]
        / "dados"
        / "corpos_celestes.json"
    )

    @staticmethod
    def salvar(dados):
        Armazenamento.CAMINHO.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            Armazenamento.CAMINHO,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    @staticmethod
    def carregar():
        if not Armazenamento.CAMINHO.exists():
            return None

        with open(
            Armazenamento.CAMINHO,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)
