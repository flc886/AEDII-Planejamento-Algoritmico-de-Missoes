from aquisicao.api_client import ApiClient

api = ApiClient()

corpos = api.buscar_todos_corpos()

print(f"Total de corpos: {len(corpos)}")

for corpo in corpos[:5]:
    print(corpo["id"], "-", corpo["englishName"])