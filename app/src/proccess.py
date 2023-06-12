import pandas as pd
import numpy as np
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
import heapq as hq
import math

# Numero de filas a probar
NROWS = 30
THRESHOLD = 1.5 # Umbral de similitud

PATH = "app/data/Dataset_Huaman_Mendoza_Ramirez_500.csv"

# Leer el archivo CSV
df = pd.read_csv(PATH, usecols=[1, 3, 4, 7, 10, 11, 12, 13, 14, 15, 16, 18], header = 0, nrows = NROWS)

# Seleccionamos las características que vamos a utilizar
features = ['Danceability', 'Loudness', 'Speechiness', 'Acousticness', 
            'Instrumentalness', 'Liveness', 'Valence', 'Tempo']

# Normalizamos los valores de las características
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

# Crea un grafo vacío
G = nx.Graph()

# Agrega los nodos al grafo
for i in range(len(df)):
    G.add_node(i, track=df.loc[i, 'Track'])

features = df[['Danceability', 'Loudness', 'Speechiness', 'Acousticness', 
               'Instrumentalness', 'Liveness', 'Valence', 'Tempo']].values

# Agrega las aristas al grafo
for i in range(len(df)):
    for j in range(i+1, len(df)):
        dist = euclidean_distances([features[i]], [features[j]])[0][0]
        dist = 2 - dist
        if dist > THRESHOLD:
            G.add_edge(i, j, weight=round(dist, 3))

def dijkstra(G, s):
  n = len(G)
  visited = [False]*n
  path = [-1]*n
  cost = [math.inf]*n

  cost[s] = 0
  pqueue = [(0, s)]
  while pqueue:
    g, u = hq.heappop(pqueue)
    if not visited[u]:
      visited[u] = True
      for v in range(n):
        if G[u, v] > 0 and not visited[v]:
          f = g + G[u, v]
          if f < cost[v]:
            cost[v] = f
            path[v] = u
            hq.heappush(pqueue, (f, v))

  return path, cost

# Aplicar el algoritmo de Dijkstra
path, cost = dijkstra(nx.to_numpy_array(G), 1)

# Crear un DataFrame con los resultados del algoritmo de Dijkstra
data = []
for i in range(len(path)):
    if not math.isinf(cost[i]):  # Solo considerar las canciones que están conectadas
        data.append({
            'Track': df.loc[i, 'Track'],  # Agregar la columna 'Track' del dataset original
            'Artist': df.loc[i, 'Artist'],  # Agregar la columna 'Artist' del dataset original
            'Url_youtube': df.loc[i, 'Url_youtube'],  # Agregar la columna 'Url_youtube' del dataset original
            'Path': path[i], 
            'Cost': cost[i]
        })

df_result = pd.DataFrame(data)

# Ordenar el DataFrame de acuerdo con el camino encontrado por el algoritmo de Dijkstra
df_result = df_result.sort_values(by=['Cost'])#.reset_index(drop=True)
print(df_result)

df_result = df_result.sort_values(by=['Cost']).reset_index(drop=True)
df_result = df_result.drop(columns=['Cost', 'Path'])
print()
# Imprimir el DataFrame resultante
print(df_result)

