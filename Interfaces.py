from abc import ABC, abstractmethod

class EstruturaIndice(ABC):
    #Contrato comum: o sistema usa isto sem saber qual estrutura esta por tras."""

    @abstractmethod
    def inserir(self, chave, objeto):
        pass

    @abstractmethod
    def buscar(self, chave):
        # Devolve o objeto associado, ou None se nao existir.
        pass

    @abstractmethod
    def remover(self, chave):
        # Remove e devolve o objeto, ou None se nao existir.
        pass

    @abstractmethod
    def listar(self):
        # Devolve todos os objetos armazenados.
        pass

    @abstractmethod
    def imprimir_metricas(self):
        # Metricas instrumentadas, produzidas pela propria estrutura.
        pass

# Interface da Trie
class IndicePrefixo(EstruturaIndice):
    @abstractmethod
    def buscar_por_prefixo(self, prefixo: str) -> list:
        pass

# Interface da Arvore B
class IndiceOrdenado(EstruturaIndice):
    @abstractmethod
    def buscar_por_intervalo(self, minimo, maximo) -> list:
        pass