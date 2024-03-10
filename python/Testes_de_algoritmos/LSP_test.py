import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

def LSP_projection(data, target_dimension):
    # Normalizando os dados
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(data)
    
    # Aplicando a técnica de projeção LSP
    svd = TruncatedSVD(n_components=target_dimension)
    projected_data = svd.fit_transform(data_normalized)
    
    return projected_data

# Exemplo de uso
if __name__ == "__main__":
    # Definindo uma matriz de dados de exemplo (10 amostras, 5 atributos)
    data = np.random.rand(10, 5)
    
    # Definindo a dimensionalidade alvo da projeção
    target_dimension = 2
    
    # Realizando a projeção LSP
    projected_data = LSP_projection(data, target_dimension)
    
    # Exibindo os dados projetados
    print("Dados Projetados:")
    print(projected_data)
