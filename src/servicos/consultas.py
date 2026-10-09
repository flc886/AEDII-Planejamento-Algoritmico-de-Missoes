
class Consultas:
    def __init__(self, indice):
        # Recebe a tabela hash já montada; as consultas reutilizam esse índice.
        self.indice = indice

    def buscar_por_id(self, identificador):
        # Busca direta pela chave do corpo, sem percorrer a coleção toda.
        return self.indice.buscar(identificador)

    def listar_todos(self):
        # Devolve os valores armazenados no índice para operações de varredura.
        return self.indice.listar()

    def filtrar_por_tipo(self, tipo):
        # A comparação sem diferenciar maiúsculas/minúsculas facilita a entrada.
        # Como não há índice por tipo, filtrar percorre todos os corpos: O(n).
        tipo = tipo.lower()

        return [
            corpo
            for corpo in self.indice.listar()
            if corpo.tipo and corpo.tipo.lower() == tipo
        ]

    def buscar_por_nome(self, nome):
        # Busca parcial nos nomes local e inglês; também exige varrer os corpos: O(n).
        nome = nome.lower()

        return [
            corpo
            for corpo in self.indice.listar()
            if nome in corpo.nome.lower()
            or nome in corpo.nome_ingles.lower()
        ]

    def filtrar_por_gravidade(self, gravidade_minima):
        # Ignora valores desconhecidos e retorna corpos acima do limite informado.
        # A filtragem é linear em relação ao número de corpos: O(n).
        return [
            corpo
            for corpo in self.indice.listar()
            if corpo.gravidade is not None
            and corpo.gravidade >= gravidade_minima
        ]

    # operacao adicional: luas de um planeta
    # busca o planeta na hash, pega o id de cada lua no fim do link
    # (".../bodies/phobos" -> "phobos") e busca a lua na hash tambem
    # custo O(k), k = numero de luas, sem varrer todos os corpos
    def luas_de(self, id_planeta):
        # Primeiro localiza o planeta; depois resolve cada referência de lua no índice.
        planeta = self.indice.buscar(id_planeta)
        if planeta is None or not planeta.luas:
            return []

        luas = []
        for lua in planeta.luas:
            id_lua = lua["rel"].rstrip("/").split("/")[-1]
            corpo = self.indice.buscar(id_lua)
            if corpo is not None:
                luas.append(corpo)
        return luas
