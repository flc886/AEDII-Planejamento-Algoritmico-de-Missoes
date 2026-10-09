from estruturas.Interfaces import EstruturaIndice

class NoExterno:
    # No de lista encadeada alocado dinamicamente (fora do array).
    def __init__(self, chave, objeto):
        self.chave = chave
        self.objeto = objeto
        self.proximo = None


class TabelaHash(EstruturaIndice):
    LIMITE_CARGA = 0.75
    
    def __init__(self, tamanho=53):
        
        if tamanho <= 0:
            raise ValueError("O tamanho inicial deve ser maior que zero.")
        self.tamanho = tamanho
        self.tabela = [None] * tamanho
        self.fatorCarga = 0
        self.colisoes = 0
        self.qtdElementos = 0
        self.qtdRehashings = 0
        self.qtdInsercoes = 0
        self.custoRehashing = 0
        
    def _hash(self, string: str, tamanho=None):
        hashCode = 0
        if tamanho is None:
            tamanho = self.tamanho
        
        for char in string:
            hashCode = (hashCode * 31 + ord(char))
            
        return hashCode % tamanho
        
    def _rehashing(self):
        novoTamanho = self.tamanho * 2
        novaTabela = [None] * novoTamanho
        
        for endereco in range(self.tamanho):
            nodo = self.tabela[endereco]
            while nodo is not None:
                # Percorre a lista do endereço reposicionando os nodos
                proximo = nodo.proximo
                indice = self._hash(nodo.chave, novoTamanho)
                nodo.proximo = novaTabela[indice]
                novaTabela[indice] = nodo
                self.custoRehashing += 1
                nodo = proximo
                    
        self.tabela = novaTabela
        self.tamanho = novoTamanho
        self.fatorCarga = self.qtdElementos / self.tamanho
        self.qtdRehashings += 1

    def inserir(self, chave, objeto):
        indice = self._hash(chave)
          
        atual = self.tabela[indice]
        while atual is not None:
            if atual.chave == chave:
                atual.objeto = objeto
                return
            atual = atual.proximo

        novo = NoExterno(chave, objeto)
        if self.tabela[indice] is not None:
            self.colisoes += 1
        novo.proximo = self.tabela[indice]
        self.tabela[indice] = novo

        self.qtdElementos += 1
        self.qtdInsercoes += 1
        self.fatorCarga = self.qtdElementos / self.tamanho

        if self.fatorCarga >= self.LIMITE_CARGA:
            self._rehashing()
            
    def buscar(self, chave):
        atual = self.tabela[self._hash(chave)]
        
        while atual is not None:
            if atual.chave == chave:
                return atual.objeto
            
            atual = atual.proximo
            
        return None
        
    def remover(self, chave):
        indice = self._hash(chave)
        atual = self.tabela[indice]
        anterior = None

        while atual is not None:
            if atual.chave == chave:
                if anterior is None:
                    # Se for a cabeça da lista
                    self.tabela[indice] = atual.proximo
                else:
                    # Se for no meio ou fim
                    anterior.proximo = atual.proximo
                
                atual.proximo = None
                self.qtdElementos -= 1
                self.fatorCarga = self.qtdElementos / self.tamanho
            
                return atual.objeto
        
            anterior = atual
            atual = atual.proximo
        
        return None
    
    def listar(self):
        lista = []
        for endereco in self.tabela:
            nodo = endereco
            while nodo is not None:
                lista.append(nodo.objeto)
                nodo = nodo.proximo
        
        return lista
                
            

    def imprimir(self):
        print("Indice | Array principal -> Lista externa")
        for i in range(self.tamanho):
            cadeia = []
            atual = self.tabela[i]
            while atual is not None:
                cadeia.append(str(atual.chave))
                atual = atual.proximo
            if cadeia:
                print(f"  [{i}]   ->  " + " -> ".join(cadeia) + " -> NULL")
            else:
                print(f"  [{i}]   ->  NULL")
                
    def imprimir_metricas(self):
        print(f"Elementos: {self.qtdElementos}")
        print(f"Capacidade: {self.tamanho}")
        print(f"Colisões: {self.colisoes}")
        print(f"Fator de carga: {self.fatorCarga:.3f}")
        print(f"Rehashings: {self.qtdRehashings}")

