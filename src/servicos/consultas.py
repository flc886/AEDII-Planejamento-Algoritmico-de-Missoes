
class Consultas:
    def __init__(self, indice):
        self.indice = indice

    def buscar_por_id(self, identificador):
        return self.indice.buscar(identificador)

    def listar_todos(self):
        return self.indice.listar()

    def filtrar_por_tipo(self, tipo):
        tipo = tipo.lower()

        return [
            corpo
            for corpo in self.indice.listar()
            if corpo.tipo and corpo.tipo.lower() == tipo
        ]

    def buscar_por_nome(self, nome):
        nome = nome.lower()

        return [
            corpo
            for corpo in self.indice.listar()
            if nome in corpo.nome.lower()
            or nome in corpo.nome_ingles.lower()
        ]

    def filtrar_por_gravidade(self, gravidade_minima):
        return [
            corpo
            for corpo in self.indice.listar()
            if corpo.gravidade is not None
            and corpo.gravidade >= gravidade_minima
        ]
