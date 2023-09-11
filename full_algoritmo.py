import itertools
import matplotlib.pyplot as plt
import time
import random

# Solicitar a quantidade de cidades ao usuário
num_cidades = int(input("Digite a quantidade de cidades: "))

# Gere coordenadas aleatórias para as cidades
cidades = [(random.randint(0, 200), random.randint(0, 200)) for _ in range(num_cidades)]

# Criar coordenadas das cidades
x_cidades = [cidade[0] for cidade in cidades]
y_cidades = [cidade[1] for cidade in cidades]

# Distância euclidiana para calcular a distância entre dois pontos
def calcular_distancia(cidade1, cidade2):
    return ((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2) ** 0.5

# Calcular a distância total do caminho, considerando uma cidade após a outra
def calcular_distancia_total(caminho, cidades):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        distancia_total += calcular_distancia(cidades[cidade_atual], cidades[proxima_cidade])
    return distancia_total

# Abordagem de força bruta permutando todos os caminhos
def menor_caminho_forca_bruta(cidades):
    num_cidades = len(cidades)
    todas_permutacoes = itertools.permutations(range(num_cidades))
    menor_distancia = float('inf')
    melhor_caminho = None

    todos_caminhos = []
    num_execucoes = 0  # Contador de execuções

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x_cidades, y_cidades, c='blue', label="Cidades")

    for permutacao in todas_permutacoes:
        volta_caixeiro = permutacao + (permutacao[0],)
        distancia_atual = calcular_distancia_total(volta_caixeiro, cidades)
        todos_caminhos.append((volta_caixeiro, distancia_atual))
        num_execucoes += 1

        # Atualizar o gráfico para mostrar o caminho atual
        ax.clear()  # Limpar o gráfico
        ax.scatter(x_cidades, y_cidades, c='blue', label="Cidades")

        for i in range(len(volta_caixeiro) - 1):
            ax.plot([x_cidades[volta_caixeiro[i]], x_cidades[volta_caixeiro[i + 1]]],
                    [y_cidades[volta_caixeiro[i]], y_cidades[volta_caixeiro[i + 1]]], 'r-', linewidth=2)
        
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.set_title(f"Distância: {distancia_atual:.2f}, Tentativas: {num_execucoes}")
        ax.grid()
        plt.pause(0.01)  # Pausa para atualizar o gráfico
        plt.draw()  # Redesenhar o gráfico

        # Atualizar o menor caminho encontrado
        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual
            melhor_caminho = volta_caixeiro
    
    plt.show()  # Mostrar o gráfico final

    return melhor_caminho, menor_distancia, num_execucoes

# Função para atualizar o feromônio
def atualizar_feromonio(trilhas_formigas, feromonio, taxa_evaporacao):
    for i in range(len(feromonio)):
        for j in range(len(feromonio[i])):
            if i != j:
                feromonio[i][j] *= (1 - taxa_evaporacao)
                for trilha in trilhas_formigas:
                    if j in trilha and i in trilha:
                        distancia_trilha = calcular_distancia_total(trilha, cidades)
                        feromonio[i][j] += 1.0 / (distancia_trilha + 1e-10)

# Função para calcular a probabilidade de escolher uma cidade como próxima
def calcular_probabilidade(cidade_atual, cidade_destino, cidades_visitadas, feromonio, alfa, beta):
    if cidade_atual == cidade_destino:
        return 0.0  # Evitar divisão por zero

    numerador = (feromonio[cidade_atual][cidade_destino] ** alfa) * ((1.0 / calcular_distancia(cidades[cidade_atual], cidades[cidade_destino])) ** beta)
    
    denominador = sum((feromonio[cidade_atual][cidade] ** alfa) * ((1.0 / (calcular_distancia(cidades[cidade_atual], cidades[cidade]) + 1e-10)) ** beta) for cidade in range(num_cidades) if cidade not in cidades_visitadas)
    
    probabilidade = numerador / denominador
    return probabilidade

# Parâmetros do algoritmo de colônia de formigas.
n_formigas = 10
n_iteracoes = 100
taxa_evaporacao = 0.5
alfa = 1.0
beta = 1.0

# Inicialize a matriz de feromônio.
feromonio = [[1.0] * num_cidades for _ in range(num_cidades)]

# Armazenar os resultados da colônia de formigas
caminho_minimo_formigas = None
distancia_minima_formigas = float('inf')

# Armazenar os resultados da força bruta
melhor_caminho_bruto = None
menor_distancia_bruta = float('inf')

# Medir o tempo de execução da colônia de formigas
start_time = time.time()

for _ in range(n_iteracoes):
    trilhas_formigas = []

    for _ in range(n_formigas):
        cidade_atual = random.randint(0, num_cidades - 1)
        cidades_visitadas = [cidade_atual]
        trilha_formiga = [cidade_atual]
        distancia_total = 0.0

        while len(cidades_visitadas) < num_cidades:
            probabilidades = [calcular_probabilidade(cidade_atual, cidade, cidades_visitadas, feromonio, alfa, beta) for cidade in range(num_cidades)]
            
            # Definir pesos zero para as cidades já visitadas
            for cidade_visitada in cidades_visitadas:
                probabilidades[cidade_visitada] = 0.0
            
            cidade_escolhida = random.choices(range(num_cidades), weights=probabilidades, k=1)[0]
            cidades_visitadas.append(cidade_escolhida)
            trilha_formiga.append(cidade_escolhida)
            distancia_total += calcular_distancia(cidades[cidade_atual], cidades[cidade_escolhida])
            cidade_atual = cidade_escolhida

        distancia_total += calcular_distancia(cidades[cidades_visitadas[-1]], cidades[cidades_visitadas[0]])
        trilha_formiga.append(cidades_visitadas[0])
        trilhas_formigas.append((trilha_formiga, distancia_total))
        trilhas_formigas.sort(key=lambda x: x[1])

        if trilhas_formigas[0][1] < distancia_minima_formigas:
            distancia_minima_formigas = trilhas_formigas[0][1]
            caminho_minimo_formigas = trilhas_formigas[0][0]

        atualizar_feromonio([trilha for trilha, _ in trilhas_formigas], feromonio, taxa_evaporacao)

# Calcular o tempo de execução da colônia de formigas
end_time = time.time()
tempo_execucao_formigas = end_time - start_time

# Medir o tempo de execução da força bruta
start_time = time.time()

# Encontrar o menor caminho usando força bruta
melhor_caminho_bruto, menor_distancia_bruta, num_execucoes = menor_caminho_forca_bruta(cidades)

# Calcular o tempo de execução da força bruta
end_time = time.time()
tempo_execucao_bruta = end_time - start_time

# Exibição gráfica do caminho mínimo encontrado pela colônia de formigas
x_formigas = [cidades[caminho_minimo_formigas[i]][0] for i in range(num_cidades)]
y_formigas = [cidades[caminho_minimo_formigas[i]][1] for i in range(num_cidades)]
x_formigas.append(cidades[caminho_minimo_formigas[0]][0])
y_formigas.append(cidades[caminho_minimo_formigas[0]][1])

plt.figure(figsize=(12, 6))

# Gráfico para Colônia de Formigas
plt.subplot(1, 2, 1)
plt.plot(x_cidades, y_cidades, "bo", label="Cidades")
plt.plot(x_formigas, y_formigas, 'ro-')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title(f"Colônia de Formigas - Distância: {distancia_minima_formigas:.2f}, Tempo: {tempo_execucao_formigas:.4f} s")
plt.grid()
plt.legend()

# Exibição gráfica do caminho mínimo encontrado pela força bruta
x_bruta = [cidades[melhor_caminho_bruto[i]][0] for i in range(num_cidades)]
y_bruta = [cidades[melhor_caminho_bruto[i]][1] for i in range(num_cidades)]
x_bruta.append(cidades[melhor_caminho_bruto[0]][0])
y_bruta.append(cidades[melhor_caminho_bruto[0]][1])

# Gráfico para Força Bruta
plt.subplot(1, 2, 2)
plt.plot(x_cidades, y_cidades, "bo", label="Cidades")
plt.plot(x_bruta, y_bruta, 'ro-')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title(f"Força Bruta - Distância: {menor_distancia_bruta:.2f}, Tempo: {tempo_execucao_bruta:.4f} s")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

# Exibir resultados finais
print("Resultados da Colônia de Formigas:")
print("Caminho mais curto encontrado:", caminho_minimo_formigas)
print("Distância mínima:", distancia_minima_formigas)
print("Tempo de execução:", tempo_execucao_formigas)

print("\nResultados da Força Bruta:")
print("Caminho mais curto encontrado:", melhor_caminho_bruto)
print("Distância mínima:", menor_distancia_bruta)
print("Tempo de execução:", tempo_execucao_bruta)
