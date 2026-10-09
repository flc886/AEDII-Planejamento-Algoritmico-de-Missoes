from dotenv import load_dotenv

from aquisicao.carregador import Carregador
from aquisicao.armazenamento import Armazenamento
from aquisicao.mapeador import Mapeador
from estruturas.HashTable import TabelaHash
from servicos.consultas import Consultas
from guloso.planejamento_guloso import montar_destinos, planejar_missao


def carregar_corpos():
    # tenta buscar na API; se falhar, usa o ultimo json salvo em dados/
    try:
        return Carregador().carregar_corpos()
    except Exception as erro:
        print(f"Falha na API ({erro}). Usando dados salvos localmente.")
        dados = Armazenamento.carregar()
        if dados is None:
            raise SystemExit("Nenhum dado local encontrado em dados/corpos_celestes.json")
        return Mapeador.mapear_corpos(dados)


def main():
    load_dotenv()  # le a chave da API do arquivo .env

    # 1. aquisicao
    corpos = carregar_corpos()
    print(f"Corpos carregados: {len(corpos)}")

    # 2. tabela hash: indexa cada corpo pelo id
    indice = TabelaHash()
    for corpo in corpos:
        indice.inserir(corpo.id, corpo)

    print("\n=== Métricas da Tabela Hash ===")
    indice.imprimir_metricas()

    # 3. consultas
    consultas = Consultas(indice)

    print("\n=== Consulta por id: 'mars' ===")
    print(consultas.buscar_por_id("mars"))

    print("\n=== Pesquisa por nome: 'jup' ===")
    for corpo in consultas.buscar_por_nome("jup"):
        print(corpo)

    print("\n=== Filtro: planetas anões ===")
    for corpo in consultas.filtrar_por_tipo("Dwarf Planet"):
        print(corpo)

    print("\n=== Operação adicional: luas de Marte ===")
    for lua in consultas.luas_de("mars"):
        print(lua)

    # 4. guloso: planejamento da missao
    print("\n=== Planejamento da missão (guloso) ===")
    destinos = montar_destinos(corpos, indice.buscar)
    planejar_missao(destinos, 100, 5000)


if __name__ == "__main__":
    main()