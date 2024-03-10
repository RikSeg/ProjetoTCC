import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def PLMP_projection(data, target_dimension, num_landmarks):
    # Seleção de Landmarks usando KMeans
    kmeans = KMeans(n_clusters=num_landmarks)
    kmeans.fit(data)
    landmarks = kmeans.cluster_centers_
    
    # Projeção Múltipla usando PCA
    pca_models = []
    for landmark in landmarks:
        # Selecionando amostras próximas ao landmark
        distances = np.linalg.norm(data - landmark, axis=1)
        nearest_samples_indices = np.argsort(distances)[:5]  # 5 amostras mais próximas
        nearest_samples = data[nearest_samples_indices]
        
        # Aplicando PCA nas amostras próximas ao landmark
        pca = PCA(n_components=target_dimension)
        pca.fit(nearest_samples)
        pca_models.append(pca)
    
    # Combinando as matrizes de projeção
    combined_projection_matrix = np.vstack([pca.components_ for pca in pca_models])
    
    # Aplicando a projeção combinada nos dados originais
    projected_data = np.dot(data, combined_projection_matrix.T)
    
    return projected_data

# Exemplo de uso
if __name__ == "__main__":
    # Definindo uma matriz de dados de exemplo (100 amostras, 10 atributos)
    data = np.random.rand(100, 10)
    
    # Definindo os parâmetros do PLMP
    target_dimension = 2  # Dimensão alvo da projeção
    num_landmarks = 5     # Número de landmarks
    
    # Realizando a projeção PLMP
    projected_data = PLMP_projection(data, target_dimension, num_landmarks)
    
    # Exibindo os dados projetados
    print("Dados Projetados:")
    print(projected_data)
