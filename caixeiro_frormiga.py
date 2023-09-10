# Este algoritmo resolve o problema do caixeiro viajante usando o algoritmo da formiga.
# O problema do caixeiro viajante é encontrar o caminho mais curto que visita todas as cidades uma vez e retorna à cidade de partida.

# Importamos as bibliotecas necessárias.
import random

# Definimos os parâmetros do algoritmo.
n_cidades = 5  # Número de cidades
distancias = [[1, 3, 4, 6, 5], [3, 1, 2, 5, 4], [4, 2, 1, 3, 5], [6, 5, 3, 1, 2], [5, 4, 5, 2, 1]]  # Matriz de distâncias entre as cidades
n_formigas = 10  # Número de formigas

# Criamos uma lista vazia para armazenar os caminhos encontrados pelas formigas.
caminhos = []

def calcular_probabilidade(cidade_atual, cidade_proxima):
    # Calculamos a distância entre as duas cidades.
    distancia = distancias[cidade_atual][cidade_proxima]

    # Calculamos a quantidade de feromônio presente no caminho entre as duas cidades.
    quantidade_feromonio = calcular_quantidade_feromonio(cidade_atual, cidade_proxima)

    # Calculamos a probabilidade.
    probabilidade = distancia / quantidade_feromonio

    return probabilidade

# Função para encontrar o caminho mais curto entre os caminhos encontrados.
def encontrar_caminho_minimo(caminhos):
    # Definimos o caminho mínimo como o primeiro caminho da lista.
    caminho_minimo = caminhos[0]

    # Criamos um loop para iterar sobre os outros caminhos.
    for caminho in caminhos:
        # Se o caminho for menor que o caminho mínimo, atualizamos o caminho mínimo.
        if len(caminho) < len(caminho_minimo):
            caminho_minimo = caminho

    return caminho_minimo


# Criamos um loop para iterar sobre as formigas.
for formiga in range(n_formigas):
    # Criamos uma lista vazia para armazenar o caminho da formiga.
    caminho = []

    # A formiga começa na primeira cidade.
    cidade_atual = 0

    # Criamos um loop para iterar sobre as outras cidades.
    for cidade_proxima in range(1, n_cidades):
        # Calculamos a probabilidade de a formiga ir para a cidade próxima.
        probabilidade = calcular_probabilidade(cidade_atual, cidade_proxima)

        # Se a probabilidade for maior que 0, a formiga vai para a cidade próxima.
        if probabilidade > 0:
            caminho.append(cidade_proxima)
            cidade_atual = cidade_proxima

    # Adicionamos o caminho da formiga à lista de caminhos encontrados.
    caminhos.append(caminho)

# Encontramos o caminho mais curto entre os caminhos encontrados.
caminho_minimo = encontrar_caminho_minimo(caminhos)

# Imprimimos o caminho mais curto.
print("O caminho mais curto é:", caminho_minimo)
