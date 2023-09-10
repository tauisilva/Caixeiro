import tkinter as tk
import itertools
import time

# Função para calcular a distância entre duas cidades
def distancia(cidade1, cidade2):
    return ((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2) ** 0.5

# Função para calcular a distância total de um caminho
def calcular_distancia_total(caminho, cidades):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]
        distancia_total += distancia(cidades[cidade_atual], cidades[proxima_cidade])
    return distancia_total

# Função para encontrar o menor caminho usando força bruta
def menor_caminho_forca_bruta(cidades):
    num_cidades = len(cidades)
    todas_permutacoes = itertools.permutations(range(num_cidades))
    menor_distancia = float('inf')
    melhor_caminho = None

    for permutacao in todas_permutacoes:
        caminho_com_volta = permutacao + (permutacao[0],)
        distancia_atual = calcular_distancia_total(caminho_com_volta, cidades)

        # Atualize a interface gráfica para mostrar o caminho atual
        atualizar_interface(cidades, caminho_com_volta)
        time.sleep(0.1)

        if distancia_atual < menor_distancia:
            menor_distancia = distancia_atual
            melhor_caminho = caminho_com_volta
        
        #Cria uma linha com o melhor caminho    
        canvas.create_line(cidades, cidades[0], fill="blue", width=2)
    return melhor_caminho


# Função para atualizar a interface gráfica com o caminho atual
def atualizar_interface(cidades, caminho):
    canvas.delete("all")  # Limpe o canvas

    # Desenhe as cidades como círculos
    for cidade in cidades:
        x, y = cidade
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")

    # Desenhe o caminho
    for i in range(len(caminho) - 1):
        cidade_atual = cidades[caminho[i]]
        proxima_cidade = cidades[caminho[i + 1]]
        canvas.create_line(cidade_atual, proxima_cidade, fill="red", width=2)
    
    root.update()  # Atualize a janela

# Crie a janela Tkinter
root = tk.Tk()
root.title("Caixeiro Viajante")

# Crie um canvas para desenhar o mapa
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()

# Defina as coordenadas das cidades
cidades = [(100, 200), (150, 180), (170, 190), (200, 210), (40,400)]
#, (400, 350), (500, 150), (100,200),(200, 250), (300, 280)

# Encontre o melhor caminho usando força bruta
melhor_caminho = menor_caminho_forca_bruta(cidades)

print("Melhor caminho encontrado:", melhor_caminho)

# Mantenha a janela aberta
root.mainloop()
