
class Consultas:
    def __init__(self, tabela):
        # Recebe a tabela hash já montada; as consultas reutilizam esse índice.
        self.tabela = tabela

    def buscar_por_id(self, identificador):
        # 6.1 - Busca direta pela chave do corpo, sem percorrer a coleção toda.
        return self.tabela.buscar(identificador)
    
    def buscar_por_nome(self, nome):
        # 6.2 - Busca parcial nos nomes local e inglês; também exige varrer os corpos: O(n).
        nome = nome.lower()
    
        return [
            corpo
            for corpo in self.tabela.listar()
            if nome in corpo.nome.lower()
            or nome in corpo.nome_ingles.lower()
        ]

    def listar_todos(self):
        # Devolve os valores armazenados no índice para operações de varredura.
        return self.tabela.listar()

    def filtrar_por_tipo(self, tipo):
        # 6.3 - A comparação sem diferenciar maiúsculas/minúsculas facilita a entrada.
        # Como não há índice por tipo, filtrar percorre todos os corpos: O(n).
        tipo = tipo.lower()

        return [
            corpo
            for corpo in self.tabela.listar()
            if corpo.tipo and corpo.tipo.lower() == tipo
        ]

    

    def filtrar_por_gravidade(self, gravidade_minima):
        # 6.3 - Ignora valores desconhecidos e retorna corpos acima do limite informado.
        # A filtragem é linear em relação ao número de corpos: O(n).
        return [
            corpo
            for corpo in self.tabela.listar()
            if corpo.gravidade is not None
            and corpo.gravidade >= gravidade_minima
        ]

    # 6.4 - Operação adicional: luas de um planeta
    def luas_de(self, id_planeta):
        # Primeiro localiza o planeta; depois resolve cada referência de lua no índice.
        planeta = self.tabela.buscar(id_planeta)
        if planeta is None or not planeta.luas:
            return []

        luas = []
        for lua in planeta.luas:
            id_lua = lua["rel"].rstrip("/").split("/")[-1]
            corpo = self.tabela.buscar(id_lua)
            if corpo is not None:
                luas.append(corpo)
        return luas
