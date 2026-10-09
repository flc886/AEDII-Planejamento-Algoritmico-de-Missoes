# Crônicas do Espaço: Planejamento Algorítmico de Missões

Sistema em Python que consome a **Solar System OpenData API**, indexa os corpos celestes em uma **Tabela Hash** própria e planeja uma missão com uma **estratégia gulosa** (Opção A).

**Grupo:** João Falcão (aquisição de dados), Gustavo Bergmann (Tabela Hash), Théo Chatkin (algoritmo guloso). 

## Como executar

```bash
pip install -r requirements.txt
# na raiz, criar o arquivo .env com:  SOLAR_SYSTEM_API_KEY=<sua chave>
cd src
python main.py
```

A chave é gratuita em https://api.le-systeme-solaire.net/generatekey.html. Se a API falhar, o programa usa a última cópia salva em `dados/corpos_celestes.json`.

## 1. Fonte de dados

| | |
|---|---|
| API | Solar System OpenData |
| Endereço | `https://api.le-systeme-solaire.net/rest` |
| Endpoint usado | `GET /bodies/` (todos os corpos) |
| Autenticação | header `Authorization: Bearer <chave>` |
| Data da consulta | 08/10/2026 (554 corpos) |
| Modalidade | Nível 1 — consumo dinâmico, com cópia local |

**Justificativa:** dados reais e variados (planetas, luas, asteroides, cometas) com atributos físicos e orbitais, suficientes para consultas, filtros e para calcular custo e benefício de cada destino.

**Exemplo de requisição** (`src/aquisicao/api_client.py`):

```python
requests.get("https://api.le-systeme-solaire.net/rest/bodies/",
             headers={"Authorization": f"Bearer {chave}"}, timeout=30)
```

**Estrutura retornada** (campos usados, exemplo de Marte):

```json
{
  "id": "mars", "name": "Mars", "englishName": "Mars", "bodyType": "Planet",
  "semimajorAxis": 227939200, "gravity": 3.71, "meanRadius": 3389.5, "avgTemp": 210,
  "moons": [{"moon": "Phobos", "rel": "..."}, {"moon": "Deïmos", "rel": "..."}],
  "aroundPlanet": null
}
```

## 2. Modelagem

Cada corpo vira um objeto `CorpoCeleste` (`src/modelos/corpo_celeste.py`), criado pelo `Mapeador`.

| Atributo | Campo da API | Uso |
|---|---|---|
| `id` | `id` | chave da Tabela Hash |
| `nome`, `nome_ingles` | `name`, `englishName` | pesquisa por nome |
| `tipo` | `bodyType` | filtro e benefício |
| `semieixo_maior` | `semimajorAxis` | distância (custo) |
| `gravidade` | `gravity` | filtro e custo |
| `raio_medio`, `temperatura_media` | `meanRadius`, `avgTemp` | benefício |
| `luas`, `ao_redor_de` | `moons`, `aroundPlanet` | benefício e planeta-mãe das luas |

**Organização:** `aquisicao/` (API, mapeamento e arquivo local), `modelos/`, `estruturas/` (Hash e interfaces), `servicos/` (consultas) e `guloso/`. O `main.py` liga tudo.

**Operações** (`src/servicos/consultas.py`): buscar por id (Hash, O(1)), pesquisar por nome, filtrar por tipo e filtrar por gravidade mínima (varredura com `listar()`).

**Operação adicional: luas de um planeta** (`luas_de(id)`). Para planejar uma missão a um sistema planetário, a agência precisa saber quais luas existem nele. O método busca o planeta na Hash, extrai o `id` de cada lua do link em `moons` (`.../bodies/phobos` → `phobos`) e busca cada lua na Hash. Custo O(k), onde k é o número de luas, sem varrer os 554 corpos.

## 3. Estrutura de dados: Tabela Hash

**Escolha:** a operação central é localizar um corpo pelo `id` (ex.: achar o planeta-mãe de uma lua). A Hash faz isso em O(1) no caso médio. Prefixo de nome (Trie) e faixa de valores (Árvore B) ficam para a Parte 2, com interfaces já definidas em `Interfaces.py` (`IndicePrefixo` e `IndiceOrdenado`).

**Implementação** (`src/estruturas/HashTable.py`, sem `dict` nem `hash()` nativo):
- encadeamento externo: cada posição aponta para uma lista ligada de nós;
- função hash polinomial base 31 (Horner) com módulo pela capacidade;
- capacidade inicial 53; ao atingir fator de carga 0,75, a capacidade dobra (rehashing);
- chave repetida atualiza o objeto, sem criar nó.

| Operação | Médio | Pior |
|---|---|---|
| `inserir` | O(1) amortizado | O(n) |
| `buscar` / `remover` | O(1) | O(n) |
| `listar` | O(m + n) | O(m + n) |
| `_rehashing` | O(n) | O(n) |

**Instrumentação:** a própria estrutura conta colisões (chave nova em bucket ocupado), fator de carga, rehashings e nós movidos. Resultado com os 554 corpos:

```
Elementos: 554 | Capacidade: 848 | Colisões: 228 | Fator de carga: 0.653 | Rehashings: 4
```

## 4. Análise amortizada do rehashing

Um rehashing move todos os elementos, custo O(n). Tomar esse pior caso para toda inserção daria O(n²) para n inserções, o que é pessimista: como a capacidade dobra, os rehashings ficam cada vez mais espaçados.

**Método contábil.** Logo após um rehashing para capacidade m, há 0,375·m elementos (0,75 da capacidade anterior m/2).
1. O próximo rehashing ocorre em 0,75·m elementos, ou seja, após 0,375·m inserções.
2. Ele move 0,75·m nós.
3. Cobrando **3 unidades por inserção** (1 paga a inserção, 2 ficam de crédito), as 0,375·m inserções acumulam 0,75·m créditos, exatamente o custo do rehashing.
4. O saldo nunca fica negativo, então o custo amortizado por inserção é **O(1)**.

**Confirmação nos dados:** os 4 rehashings moveram 40 + 80 + 159 + 318 = **597 nós** em 554 inserções, cerca de 1,08 movimento por inserção, longe do O(n) do pior caso.

## 5. Algoritmo guloso: planejamento de missão

**Problema.** Escolher destinos para sondas lançadas da Terra, maximizando o benefício científico com **dois recursos limitados**: combustível (100 t) e orçamento (US$ 5.000 mi). É uma mochila 0/1 com duas restrições (NP-difícil).

**Custo** (`distância = |órbita − órbita da Terra| / órbita da Terra`, em UA; luas usam a órbita do planeta-mãe, achado na Hash):
- combustível = 2 + 3·distância + 0,5·gravidade
- orçamento = 150 + 50·distância

**Benefício:** pontos por tipo (planeta 30, planeta anão 25, lua 20, asteroide 15, outros 10), +10 se sólido (raio < 10.000 km), +20 se a temperatura média está entre 180 e 320 K, +25 se é gelado e grande (possível oceano), +1 por lua (máx. 20).

**Critério guloso:** ordenar por `benefício / (combustível/100 + orçamento/5000)` e aceitar cada destino se couber nos dois recursos. Dividir pela capacidade põe toneladas e dólares na mesma escala. Escolher só pelo maior benefício gastaria tudo em poucos alvos caros (Plutão, Éris); só pelo menor custo pegaria alvos baratos e pouco interessantes. Complexidade: O(n log n).

**Resultado** (552 destinos): 24 aceitos, benefício **698**, combustível 97,4/100 t, orçamento 4.274/5.000 mi.

**Limitação.** O guloso nunca desfaz uma escolha, então não garante o ótimo. Nos dados reais, trocar **8 Flora** (25 pontos, 5,6 t) por **(243) Ida I Dactyl** (30 pontos, 7,6 t) ainda cabe nos dois recursos e daria **703**. O Flora tinha razão melhor e entrou antes, e quando o Ida chegou não havia mais combustível. A solução exata exigiria testar combinações (exponencial), por isso o guloso troca garantia de ótimo por velocidade.
