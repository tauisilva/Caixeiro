import random
import matplotlib.pyplot as plt

# Função para calcular a distância euclidiana entre duas cidades
def calcular_distancia(cidade1, cidade2):
    return ((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2) ** 0.5

# Função para calcular a distância total de um caminho
def calcular_distancia_total(caminho, cidades):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        distancia_total += calcular_distancia(cidades[cidade_atual], cidades[proxima_cidade])
    return distancia_total

# Função para atualizar o feromônio
def atualizar_feromonio(trilhas_formigas, feromonio, taxa_evaporacao):
    for i in range(len(feromonio)):
        for j in range(len(feromonio[i])):
            if i != j:
                feromonio[i][j] *= (1 - taxa_evaporacao)
                for trilha in trilhas_formigas:
                    if j in trilha and i in trilha:
                        feromonio[i][j] += 1.0 / calcular_distancia_total(trilha, cidades)

# Função para calcular a probabilidade de escolher uma cidade como próxima
def calcular_probabilidade(cidade_atual, cidade_destino, cidades_visitadas, feromonio, alfa, beta):
    if distancias[cidade_atual][cidade_destino] == 0:
        return 0.0  # Evitar divisão por zero

    numerador = (feromonio[cidade_atual][cidade_destino] ** alfa) * ((1.0 / distancias[cidade_atual][cidade_destino]) ** beta)
    
    denominador = sum((feromonio[cidade_atual][cidade] ** alfa) * ((1.0 / (distancias[cidade_atual][cidade] + 1e-10)) ** beta) for cidade in range(n_cidades) if cidade not in cidades_visitadas)
    
    probabilidade = numerador / denominador
    return probabilidade

# Solicitar o número de cidades ao usuário
n_cidades = int(input("Digite o número de cidades: "))

# Gerar coordenadas aleatórias para as cidades
cidades = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n_cidades)]

# Inicializar a matriz de distâncias
distancias = [[calcular_distancia(cidades[i], cidades[j]) for j in range(n_cidades)] for i in range(n_cidades)]

# Parâmetros do algoritmo de colônia de formigas.
n_formigas = 10
n_iteracoes = 100
taxa_evaporacao = 0.5
alfa = 1.0
beta = 1.0

# Inicialize a matriz de feromônio.
feromonio = [[1.0] * n_cidades for _ in range(n_cidades)]

caminho_minimo = None
distancia_minima = float('inf')

for _ in range(n_iteracoes):
    trilhas_formigas = []

    for _ in range(n_formigas):
        cidade_atual = random.randint(0, n_cidades - 1)
        cidades_visitadas = [cidade_atual]
        trilha_formiga = [cidade_atual]
        distancia_total = 0.0

        while len(cidades_visitadas) < n_cidades:
            probabilidades = [calcular_probabilidade(cidade_atual, cidade, cidades_visitadas, feromonio, alfa, beta) for cidade in range(n_cidades)]
            
            # Definir pesos zero para as cidades já visitadas
            for cidade_visitada in cidades_visitadas:
                probabilidades[cidade_visitada] = 0.0
            
            cidade_escolhida = random.choices(range(n_cidades), weights=probabilidades, k=1)[0]
            cidades_visitadas.append(cidade_escolhida)
            trilha_formiga.append(cidade_escolhida)
            distancia_total += distancias[cidade_atual][cidade_escolhida]
            cidade_atual = cidade_escolhida

        distancia_total += distancias[cidades_visitadas[-1]][cidades_visitadas[0]]
        trilha_formiga.append(cidades_visitadas[0])
        trilhas_formigas.append((trilha_formiga, distancia_total))
        trilhas_formigas.sort(key=lambda x: x[1])

        if trilhas_formigas[0][1] < distancia_minima:
            distancia_minima = trilhas_formigas[0][1]
            caminho_minimo = trilhas_formigas[0][0]

        atualizar_feromonio([trilha for trilha, _ in trilhas_formigas], feromonio, taxa_evaporacao)

# Exibição gráfica do caminho mínimo encontrado
x = [cidades[caminho_minimo[i]][0] for i in range(n_cidades)]
y = [cidades[caminho_minimo[i]][1] for i in range(n_cidades)]
x.append(cidades[caminho_minimo[0]][0])
y.append(cidades[caminho_minimo[0]][1])

plt.figure()
plt.plot(x, y, 'ro-')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title('Caminho mais curto encontrado')
plt.grid()
plt.show()

print("Caminho mais curto encontrado:", caminho_minimo)
print("Distância mínima:", distancia_minima)
