SEQUENCIA = [10, 17, 24, 31, 5, 12]

# ---------- Parte A: Encadeamento Externo (Hashing Aberto) ----------

class NoExterno:
    # No de lista encadeada alocado dinamicamente (fora do array).
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.proximo = None


class TabelaHash:
    LIMITE_CARGA = 0.75
    """
    Cada posicao do array principal guarda apenas um PONTEIRO para o
    inicio de uma lista encadeada. Os dados ficam fora do array, em
    memoria alocada dinamicamente (heap).
    """
    
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho
        self.fatorCarga = 0
        self.colisoes = 0
        self.qtdElementos = 0
        self.qtsRehashings = 0
        
    def _hash(self, string: str, tamanho: int):
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
                proximo = nodo.proximo
                indice = self._hash(nodo.chave, novoTamanho)
                nodo.proximo = novaTabela[indice]
                novaTabela[indice] = nodo
                nodo = proximo
                    
        self.tabela = novaTabela
        self.tamanho = novoTamanho
        self.fatorCarga = self.qtdElementos / self.tamanho
        self.qtsRehashings += 1

    def inserir(self, chave, valor):
        indice = self._hash(chave)
          
        atual = self.tabela[indice]
        while atual is not None:
            if atual.chave == chave:
                atual.valor = valor
                return
            atual = atual.proximo

        novo = NoExterno(chave, valor)
        if self.tabela[indice] is not None:
            self.colisoes += 1
        novo.proximo = self.tabela[indice]
        self.tabela[indice] = novo

        self.qtdElementos += 1
        self.fatorCarga = self.qtdElementos / self.tamanho

        if self.fatorCarga >= self.LIMITE_CARGA:
            self._rehashing()
        

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


