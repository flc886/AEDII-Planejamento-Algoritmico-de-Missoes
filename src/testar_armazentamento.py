
from aquisicao.carregador import Carregador
from aquisicao.armazenamento import Armazenamento


carregador = Carregador()
corpos = carregador.carregar_corpos()

print("Corpos carregados:", len(corpos))

dados_salvos = Armazenamento.carregar()

if dados_salvos is not None:
    print("Corpos salvos:", len(dados_salvos))

    if len(dados_salvos) > 0:
        print("Primeiro corpo:", dados_salvos[0]["englishName"])
else:
    print("Nenhum dado encontrado no arquivo.")

print("Arquivo:", Armazenamento.CAMINHO)
