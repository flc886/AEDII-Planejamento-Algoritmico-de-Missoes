A_TERRA = 149_598_023 #distancia sol terra em km

class Destino:
  def __init__(self, nome, combustivel, orcamento, beneficio):
    #nome  identificao
    #combustivel qnt gasta
    #orcamento qnt din gasta
    #beneficio qnt rende

    self.nome = nome
    self.combustivel = combustivel #ton
    self.orcamento = orcamento #mi u$$
    self.beneficio = beneficio

#custo

def calcular_custo(corpo, buscar_corpo):
  #vejo se o corpo é uma lua
  #se o corpo é uma lua, uso a tabela hash (buscar_corpo) pra achar
  # o planeta mae pelo id e uso a orbita dele
  pai = buscar_corpo(corpo.ao_redor_de["planet"]) if corpo.ao_redor_de else None

  #corrijo a orbita usando o pai do corpo ou o proprio corpo
  orbita = (pai or corpo).semieixo_maior or 0

  #distancia ate a orbita da terra em UA abs pra tirar o sinal
  distancia = abs(orbita - A_TERRA) / A_TERRA

  #mais longe = mais combustivel. mais gravidade = mais combustivel pra pousar
  #puxo pela api a gravidade (or 0 caso a api nao tenha o valor)
  combustivel = 2 + 3 * distancia + 0.5 * (corpo.gravidade or 0)

  #custo fixo da sonda + mais longe = viagem mais longe q e mais caro
  orcamento = 150 + 50 * distancia
  return combustivel, orcamento

#calcular beneficio, uso um dicionario

PONTOS_TIPO = {"Planet": 30, "Dwarf Planet": 25, "Moon": 20, "Asteroid": 15}

def calcular_beneficio(corpo):
  #se nao achar retorna 10, tipo "Comet"
  pontos = PONTOS_TIPO.get(corpo.tipo, 10)
  #pego o a temperatura e o raio (or 0 caso a api nao tenha o valor)
  temp, raio = corpo.temperatura_media or 0, corpo.raio_medio or 0

  solido = raio < 10_000 #gasosos tem raio > 10.000 km

  if solido:
    pontos += 10 #aumento os pontos pq da pra pousar
  if 180 <= temp <= 320: #temperatura pra existencia de agua em K
    pontos += 20
  elif 0 < temp < 130 and solido and raio > 200:
    pontos += 25 #gelado e grande: pode ter oceanos

  pontos += min(len(corpo.luas or []), 20) # +1 ponto por lua max 20
  return pontos


#monto uma lista com cada corpo, com combustivel, orcamento e beneficio
def montar_destinos(corpos, buscar_corpo):
  destinos = []
  for corpo in corpos:
    if corpo.id == "terre":
      continue
    comb, orc = calcular_custo(corpo, buscar_corpo)
    destinos.append(Destino(corpo.nome_ingles, comb, orc, calcular_beneficio(corpo)))

  return destinos

#guloso

def planejar_missao(destinos, comb_max, orc_max):
  #criterio do guloso: benenifio / custo normalizado
  #custo normalizado = divido cada recurso pela capacidade

  def razao(d):
    #faco a proporcao de quanto cada um vai gastar do max, e divido pelo beneficio
    return d.beneficio / (d.combustivel / comb_max + d.orcamento / orc_max)

  #ordeno conforme a pontucao (O (n log n))
  ordenados = sorted(destinos, key=razao, reverse=True)

  selecionados = []
  comb_usado = 0
  orc_usado = 0

  print(f"\nCombustível: {comb_max} t | Orçamento: US$ {orc_max} mi")
  print(f"{'Destino':<12}{'Razão':>8}{'Benef':>7}{'Comb(t)':>9}{'Orç(mi)':>9}  Decisão")

  for d in ordenados: # O(n)

    #d = destino atual da lista ordenada
    if comb_usado + d.combustivel <= comb_max and orc_usado + d.orcamento <= orc_max:
      selecionados.append(d)
      #incremento com o total usado os gastos p ir p planeta
      comb_usado += d.combustivel
      orc_usado += d.orcamento
      decisao = "Viagem aceita"
    else:
      decisao = "Viagem rejeitada"
    print(f"{d.nome:<12}{razao(d):>8.2f}{d.beneficio:>7}{d.combustivel:>9.2f}{d.orcamento:>9.0f}  {decisao}")

  total = sum(d.beneficio for d in selecionados)

  #prints mostrando oq foi usado e corpos viajados

  print(f"\nSelecionados: {', '.join(d.nome for d in selecionados)}")
  print(f"Benefício total: {total}")
  print(f"Combustível usado: {comb_usado:.2f} / {comb_max} t")
  print(f"Orçamento usado:   {orc_usado:.0f} / {orc_max} mi")
  return selecionados, total