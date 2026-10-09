
import json
from pathlib import Path


class Armazenamento:
    # O caminho é relativo à raiz do projeto, independentemente do diretório de execução.
    CAMINHO = (
        Path(__file__).resolve().parents[2]
        / "dados"
        / "corpos_celestes.json"
    )

    @staticmethod
    def salvar(dados):
        # Garante que a pasta exista antes de gravar a resposta bruta da API.
        Armazenamento.CAMINHO.parent.mkdir(
            parents=True,   #    permite criar também as pastas intermediárias necessárias.
            exist_ok=True   #    não gera erro se a pasta já existir.
        )

        # Mantém os dados em JSON legível e preserva caracteres acentuados.
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
        # None sinaliza que ainda não há cópia local para usar como alternativa.
        if not Armazenamento.CAMINHO.exists():
            return None

        # Lê o cache local para permitir carregar os corpos sem depender da API.
        with open(
            Armazenamento.CAMINHO,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)
