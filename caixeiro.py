import itertools
import matplotlib.pyplot as plt
import time
import random

# Solicitar a quantidade de cidades ao usuário
num_cidades = int(input("Digite a quantidade de cidades: "))

# Gere coordenadas aleatórias para as cidades
cidades = [(random.randint(0, 10), random.randint(0, 10))
           for _ in range(num_cidades)]

# Criar coordenadas das cidades
x_cidades = [cidade[0] for cidade in cidades]
y_cidades = [cidade[1] for cidade in cidades]

# Distância euclidiana para calcular a distância entre dois pontos


def distancia(cidade1, cidade2):
    return ((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2) ** 0.5

# Calcular a distância total do caminho, considerando uma cidade após a outra


def calcular_distancia_total(caminho, cidades):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        distancia_total += distancia(cidades[cidade_atual],
                                     cidades[proxima_cidade])
    return distancia_total

# Abordagem de força bruta permutando todos os caminhos


def menor_caminho_forca_bruta(cidades):
    num_cidades = len(cidades)
    todas_permutacoes = itertools.permutations(range(num_cidades))
    menor_distancia = float('inf')
    melhor_caminho = None

    todos_caminhos = []
    num_execucoes = 0  # Contador de execuções

    plt.figure(figsize=(10, 6))
    plt.plot(x_cidades, y_cidades, "bo", label="Cidades")

    for permutacao in todas_permutacoes:
        volta_caixeiro = permutacao + (permutacao[0],)
        distancia_atual = calcular_distancia_total(volta_caixeiro, cidades)
        todos_caminhos.append((volta_caixeiro, distancia_atual))
        num_execucoes += 1

        # Atualizar o gráfico para mostrar o caminho atual
        plt.clf()  # Limpar o gráfico
        plt.plot(x_cidades, y_cidades, "bo", label="Cidades")

        for i in range(len(volta_caixeiro) - 1):
            plt.plot([x_cidades[volta_caixeiro[i]], x_cidades[volta_caixeiro[i + 1]]],
                     [y_cidades[volta_caixeiro[i]], y_cidades[volta_caixeiro[i + 1]]], "r-", linewidth=2)

        plt.pause(0.01)  # Pausa para atualizar o gráfico
        plt.draw()  # Redesenhar o gráfico

        # Atualizar o menor caminho encontrado
        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual
            melhor_caminho = volta_caixeiro

    plt.show()  # Mostrar o gráfico final

    return melhor_caminho, menor_distancia, num_execucoes


# Medir o tempo de execução
start_time = time.time()

# Encontrar o menor caminho usando força bruta
melhor_caminho, menor_distancia, num_execucoes = menor_caminho_forca_bruta(
    cidades)

# Calcular o tempo de execução
end_time = time.time()
tempo_execucao = end_time - start_time

# Criar um gráfico
plt.figure(figsize=(10, 6))
plt.plot(x_cidades, y_cidades, "bo", label="Cidades")

for i in range(len(cidades)):
    for j in range(i + 1, len(cidades)):
        plt.plot([x_cidades[i], x_cidades[j]], [y_cidades[i],
                 y_cidades[j]], "k-", linewidth=0.5, alpha=0.3)

for i in range(len(melhor_caminho) - 1):
    plt.plot([x_cidades[melhor_caminho[i]], x_cidades[melhor_caminho[i + 1]]],
             [y_cidades[melhor_caminho[i]], y_cidades[melhor_caminho[i + 1]]], "r-", linewidth=2)


# Personalizar o gráfico com as métricas
titulo = f"Problema do Caixeiro Viajante - {num_cidades} Cidades\n"
titulo += f"Distância Total: {menor_distancia:.2f}\n"
titulo += f"Número de Execuções: {num_execucoes}\n"
titulo += f"Tempo de Execução: {tempo_execucao:.4f} segundos"
plt.title(titulo)
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.legend()

# Mostrar o gráfico
plt.tight_layout()
plt.show()
