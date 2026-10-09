from dotenv import load_dotenv

from aquisicao.carregador import Carregador
from aquisicao.armazenamento import Armazenamento
from aquisicao.mapeador import Mapeador
from estruturas.HashTable import TabelaHash
from servicos.consultas import Consultas
from guloso.planejamento_guloso import montar_destinos, planejar_missao

LIMITE_LISTAGEM = 30          # evita despejar centenas de linhas no terminal
COMBUSTIVEL_PADRAO = 100      # toneladas
ORCAMENTO_PADRAO = 5000       # US$ milhoes


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


# ---------- entrada e saida ----------

def ler_texto(prompt):
    return input(prompt).strip()


def ler_numero(prompt, padrao=None):
    # aceita virgula decimal; Enter usa o valor padrao (se houver)
    while True:
        texto = ler_texto(prompt).replace(",", ".")
        if texto == "" and padrao is not None:
            return padrao
        try:
            return float(texto)
        except ValueError:
            print("Valor inválido. Digite um número.")


def valor(v, unidade=""):
    return "n/d" if v is None else f"{v}{unidade}"


def detalhar(corpo):
    ao_redor = corpo.ao_redor_de["planet"] if corpo.ao_redor_de else None
    qtd_luas = len(corpo.luas) if corpo.luas else 0
    print(f"  Nome:              {corpo.nome_ingles} ({corpo.nome})")
    print(f"  Id:                {corpo.id}")
    print(f"  Tipo:              {corpo.tipo}")
    print(f"  Orbita ao redor de:{' ' + valor(ao_redor)}")
    print(f"  Semieixo maior:    {valor(corpo.semieixo_maior, ' km')}")
    print(f"  Gravidade:         {valor(corpo.gravidade, ' m/s²')}")
    print(f"  Raio médio:        {valor(corpo.raio_medio, ' km')}")
    print(f"  Temperatura média: {valor(corpo.temperatura_media, ' K')}")
    print(f"  Luas:              {qtd_luas}")


def mostrar_lista(corpos):
    if not corpos:
        print("Nenhum resultado.")
        return
    for corpo in corpos[:LIMITE_LISTAGEM]:
        print(f"  {corpo}")
    if len(corpos) > LIMITE_LISTAGEM:
        print(f"  ... e mais {len(corpos) - LIMITE_LISTAGEM}")
    print(f"Total: {len(corpos)}")


# ---------- Opções do menu ----------

# Opção 1
def opcao_consultar(consultas):
    # os ids da API sao minusculos (ex.: "terre", "lune")
    identificador = ler_texto("Id do corpo (ex.: mars, terre): ").lower()
    corpo = consultas.buscar_por_id(identificador)
    if corpo is None:
        print("Corpo não encontrado.")
    else:
        detalhar(corpo)

# Opção 2
def opcao_pesquisar_nome(consultas):
    nome = ler_texto("Nome (ou parte dele): ")
    if not nome:
        print("Digite ao menos uma letra.")
        return
    mostrar_lista(consultas.buscar_por_nome(nome))

# Opção 3
def opcao_filtrar_tipo(consultas):
    tipos = sorted({c.tipo for c in consultas.listar_todos() if c.tipo})
    print("Tipos disponíveis: " + ", ".join(tipos))
    tipo = ler_texto("Tipo: ")
    mostrar_lista(consultas.filtrar_por_tipo(tipo))

# Opção 4
def opcao_filtrar_gravidade(consultas):
    minima = ler_numero("Gravidade mínima em m/s² (ex.: 5): ")
    resultado = consultas.filtrar_por_gravidade(minima)
    resultado.sort(key=lambda c: c.gravidade, reverse=True)
    
    if not resultado:
        print("Nenhum resultado.")
        return
    for corpo in resultado[:LIMITE_LISTAGEM]:
        print(f"  {corpo} - Gravidade: {corpo.gravidade} m/s^2")
    if len(resultado) > LIMITE_LISTAGEM:
        print(f"  ... e mais {len(resultado) - LIMITE_LISTAGEM}")
    print(f"Total: {len(resultado)}")

# Opção 5
def opcao_luas(consultas):
    identificador = ler_texto("Id do planeta (ex.: mars, jupiter): ").lower()
    if consultas.buscar_por_id(identificador) is None:
        print("Planeta não encontrado.")
        return
    luas = consultas.luas_de(identificador)
    if not luas:
        print("Nenhuma lua registrada para esse corpo.")
        return
    mostrar_lista(luas)

# Opção 6
def opcao_missao(destinos):
    combustivel = ler_numero(
        f"Combustível máximo em t [Enter = {COMBUSTIVEL_PADRAO}]: ", COMBUSTIVEL_PADRAO)
    orcamento = ler_numero(
        f"Orçamento máximo em US$ mi [Enter = {ORCAMENTO_PADRAO}]: ", ORCAMENTO_PADRAO)
    planejar_missao(destinos, combustivel, orcamento)


MENU = """
===== Crônicas do Espaço =====
 1) Consultar corpo por id
 2) Pesquisar por nome
 3) Filtrar por tipo
 4) Filtrar por gravidade mínima
 5) Luas de um planeta
 6) Planejar missão (guloso)
 7) Métricas da Tabela Hash
 0) Sair"""


def main():
    load_dotenv()  # le a chave da API do arquivo .env

    # 1. Aquisição
    corpos = carregar_corpos()
    print(f"Corpos carregados: {len(corpos)}")

    # 2. Tabela Hash: indexa cada corpo pelo id
    tabela = TabelaHash()
    for corpo in corpos:
        tabela.inserir(corpo.id, corpo)

    print("\n=== Métricas da Tabela Hash ===")
    tabela.imprimir_metricas()

    consultas = Consultas(tabela)
    destinos = montar_destinos(corpos, tabela.buscar)

    # 3. Menu interativo
    while True:
        print(MENU)
        try:
            escolha = ler_texto("Opção: ")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if escolha == "0":
            print("Encerrando.")
            break

        print()
        try:
            if escolha == "1":
                opcao_consultar(consultas)
            elif escolha == "2":
                opcao_pesquisar_nome(consultas)
            elif escolha == "3":
                opcao_filtrar_tipo(consultas)
            elif escolha == "4":
                opcao_filtrar_gravidade(consultas)
            elif escolha == "5":
                opcao_luas(consultas)
            elif escolha == "6":
                opcao_missao(destinos)
            elif escolha == "7":
                tabela.imprimir_metricas()
            else:
                print("Opção inválida.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperação cancelada.")


if __name__ == "__main__":
    main()