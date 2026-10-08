
from aquisicao.carregador import Carregador

carregador = Carregador()
corpos = carregador.carregar_corpos()

print(f"Total carregado: {len(corpos)}")

lua = next(
    (corpo for corpo in corpos if corpo.id == "lune"),
    None
)

if lua:
    print("Corpo encontrado:")
    print(lua)
    print("Nome original:", lua.nome)
    print("Massa:", lua.massa)
