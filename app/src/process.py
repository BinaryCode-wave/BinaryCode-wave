import pandas as pd
import numpy as np
import networkx as nx
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
import math
import src.algorithms.dijkstra as dj
import src.algorithms.kruskal as kr
import src.algorithms.floyd_warshall as fw

def generate_df(data):
    if not data:
        return pd.DataFrame()

    df_result = pd.DataFrame(data)
    df_result = df_result.sort_values(by=['Cost']).reset_index(drop=True)
    df_result = df_result.drop(columns=['Cost', 'Path'])
    return df_result

def find_id(data, track):
    id = data[data['Track'] == track]['index']
    if id.empty:
        return -1
    else:
        return id.values[0]

def process_dataframe(NROWS=30, THRESHOLD=1.5, PATH="app/data/Dataset_Huaman_Mendoza_Ramirez_500.csv", print_info=False, print_processed_df=False, features=['Danceability', 'Loudness', 'Speechiness', 'Acousticness','Instrumentalness', 'Liveness', 'Valence', 'Tempo'], algorithm='dijkstra', song="", filter_artists=[]):
    # Leer el archivo CSV
    df = pd.read_csv(PATH, usecols=[0, 1, 3, 4, 7, 10, 11, 12, 13, 14, 15, 16, 18], header=0, nrows=NROWS)

    # Filtramos las artitas que no se requieran
    if filter_artists:
        new_df = df[~df['Artist'].isin(filter_artists)].copy()
        df = new_df
        
    #Buscamos el id de la cancion
    id = find_id(df, song)

    if id == -1:
        return -1

    # Normalizamos los valores de las características
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])

    # Crea un grafo vacío
    G = nx.Graph()

    # Agrega los nodos al grafo
    for index, row in df.iterrows():
        G.add_node(row['index'], name=row['Track'], artist=row['Artist'])

    # Crea un arreglo con las características de las canciones
    features = df[features].values

    # Agrega las aristas al grafo
    nodes = list(G.nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dist = euclidean_distances([features[i]], [features[j]])[0][0]
            dist = 2 - dist
            if dist > THRESHOLD:
                G.add_edge(nodes[i], nodes[j], weight=round(dist, 3))

    result_df = pd.DataFrame()
    if algorithm == 'dijkstra':
        # Aplicar el algoritmo de Dijkstra
        path, cost = dj.dijkstra(nx.to_numpy_array(G), id)
        if print_info:
            print("Dijkstra Path:", path)
        # Crear un DataFrame con los resultados del algoritmo de Dijkstra
        data = []
        for i in range(len(path)):
            if not math.isinf(cost[i]):  # Solo considerar las canciones que están conectadas
                data.append({
                    'Id': nodes[i],  # Agregar la columna 'Id' del dataset original
                    'Track': df.loc[nodes[i], 'Track'],  # Agregar la columna 'Track' del dataset original
                    'Artist': df.loc[nodes[i], 'Artist'],  # Agregar la columna 'Artist' del dataset original
                    'Url_youtube': df.loc[nodes[i], 'Url_youtube'],  # Agregar la columna 'Url_youtube' del dataset original
                    'Path': path[i],
                    'Cost': cost[i]
                })

        result_df = generate_df(data)
    elif algorithm == 'kruskal':
        # Aplicar el algoritmo de Kruskal
        mst = kr.kruskal(G)
        if print_info:
            print("Kruskal MST Edges:")
            print(list(mst.edges.data()))
            data_kruskal = [{'Edge': str(edge[0]) + '-' + str(edge[1]), 'Weight': edge[2]} for edge in list(mst.edges.data('weight'))]

        # Crear DataFrame para Kruskal
        data_kruskal = []
        for edge in list(mst.edges.data('weight')):
            data_kruskal.append({
                'Id': edge[0], 
                'Track': df.loc[edge[0], 'Track'], 
                'Artist': df.loc[edge[0], 'Artist'], 
                'Url_youtube': df.loc[edge[0], 'Url_youtube'],
                'Path': edge[1],  # Interpreta el nodo final de la arista como el "Path"
                'Cost': edge[2]  # El peso de la arista es interpretado como el "Cost"
            })
        return generate_df(data_kruskal)
    else:
        # Aplicar el algoritmo de Floyd-Warshall
        dist_matrix = fw.floyd_warshall(G)
        if print_info:
            print("Floyd-Warshall Distance Matrix:")
            print(np.array(dist_matrix))
        # Crear DataFrame para Floyd-Warshall
        data_floyd_warshall = []

        for i in range(len(dist_matrix)):
            for j in range(len(dist_matrix[i])):
                if i != j and dist_matrix[i][j] < THRESHOLD * 1.8:  # No considerar la distancia de un nodo a sí mismo
                    data_floyd_warshall.append({
                        'Id': i,
                        'Track': df.loc[i, 'Track'], 
                        'Artist': df.loc[i, 'Artist'], 
                        'Url_youtube': df.loc[i, 'Url_youtube'],
                        'Path': j,  # Interpreta el nodo destino como el "Path"
                        'Cost': dist_matrix[i][j]  # La distancia más corta es interpretada como el "Cost"
                    })
        return generate_df(data_floyd_warshall)

    if print_processed_df:
        print(result_df)
    return result_df 

if __name__ == '__main__':
    process_dataframe()