
from aquisicao.api_client import ApiClient
from aquisicao.mapeador import Mapeador

api = ApiClient()
dados = api.buscar_todos_corpos()

corpos = Mapeador.mapear_corpos(dados)

print(f"Objetos criados: {len(corpos)}")

for corpo in corpos[:5]:
    print(corpo)
