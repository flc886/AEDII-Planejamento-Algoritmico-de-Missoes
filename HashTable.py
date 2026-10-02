class NoExterno:
    # No de lista encadeada alocado dinamicamente (fora do array).
    def __init__(self, id, objeto):
        self.id = id
        self.objeto = objeto
        self.proximo = None


class TabelaHash:
    LIMITE_CARGA = 0.75
    
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho
        self.fatorCarga = 0
        self.colisoes = 0
        self.qtdElementos = 0
        self.qtdRehashings = 0
        
    def _hash(self, string: str, tamanho=None):
        hashCode = 0
        expoente = len(string) - 1
        if tamanho is None:
            tamanho = self.tamanho
        
        for char in string:
            hashCode += (ord(char) * 31 ** expoente)
            
            expoente -= 1
            
        return hashCode % tamanho
        
    def _rehashing(self):
        novoTamanho = self.tamanho * 2
        novaTabela = [None] * novoTamanho
        
        for endereco in range(self.tamanho):
            nodo = self.tabela[endereco]
            while nodo is not None:
                # Percorre a lista do endereço reposicionando os nodos
                proximo = nodo.proximo
                indice = self._hash(nodo.id, novoTamanho)
                nodo.proximo = novaTabela[indice]
                novaTabela[indice] = nodo
                nodo = proximo
                    
        self.tabela = novaTabela
        self.tamanho = novoTamanho
        self.fatorCarga = self.qtdElementos / self.tamanho
        self.qtdRehashings += 1

    def inserir(self, id, objeto):
        indice = self._hash(id)
          
        atual = self.tabela[indice]
        while atual is not None:
            if atual.id == id:
                atual.objeto = objeto
                return
            atual = atual.proximo

        novo = NoExterno(id, objeto)
        if self.tabela[indice] is not None:
            self.colisoes += 1
        novo.proximo = self.tabela[indice]
        self.tabela[indice] = novo

        self.qtdElementos += 1
        self.fatorCarga = self.qtdElementos / self.tamanho

        if self.fatorCarga >= self.LIMITE_CARGA:
            self._rehashing()
            
    def buscar(self, id):
        atual = self.tabela[self._hash(id)]
        
        while atual is not None:
            if atual.id == id:
                return atual.objeto
            
            atual = atual.proximo
            
        return None
        
    def remover(self, id):
        indice = self._hash(id)
        atual = self.tabela[indice]
        anterior = None

        while atual is not None:
            if atual.id == id:
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

    def imprimir(self):
        print("Indice | Array principal -> Lista externa")
        for i in range(self.tamanho):
            cadeia = []
            atual = self.tabela[i]
            while atual is not None:
                cadeia.append(str(atual.id))
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


