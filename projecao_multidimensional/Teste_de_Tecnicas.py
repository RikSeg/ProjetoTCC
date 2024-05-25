import csv
import numpy as np
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import umap.umap_ as umap

def default_case():
    print("Erro: operação desconhecida")
    return exit(0)

def isomap(matriz):
    isomap = Isomap(n_components=2)
    matriz_saida = isomap.fit_transform(matriz)
    return matriz_saida

def lamp(matriz):
    # Criar uma instância do modelo UMAP com LAMP
    mapper = umap.UMAP(metric='cosine', n_components=2)

    # Ajustar o modelo aos dados e transformá-los
    matriz_saida = mapper.fit_transform(matriz)
    return matriz_saida


def lsp(matriz):
    # Normalizando os dados
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(matriz)
    
    # Aplicando a técnica de projeção LSP
    svd = TruncatedSVD(n_components=2)
    matriz_saida = svd.fit_transform(data_normalized)
    
    return matriz_saida


def plmp(matriz):
    num_landmarks = 5 # Número de clusters

    # Seleção de Landmarks usando KMeans
    kmeans = KMeans(n_clusters=num_landmarks)
    kmeans.fit(matriz)
    landmarks = kmeans.cluster_centers_
    
    # Lista para armazenar as matrizes de projeção
    pca_models = []
    
    # Lista para armazenar o número de amostras próximas a cada landmark
    num_samples_per_landmark = []
    
    for landmark in landmarks:
        # Selecionando amostras próximas ao landmark
        distances = np.linalg.norm(matriz - landmark, axis=1)
        nearest_samples_indices = np.argsort(distances)[:5]  # 5 amostras mais próximas
        nearest_samples = matriz[nearest_samples_indices]
        num_samples_per_landmark.append(len(nearest_samples))
        
        # Aplicando PCA nas amostras próximas ao landmark
        pca = PCA(n_components=2)
        pca.fit(nearest_samples)
        pca_models.append(pca)
    
    # Calcular as médias ponderadas das matrizes de projeção com base no número de amostras
    combined_projection_matrix = np.zeros((2, matriz.shape[1]))
    total_samples = sum(num_samples_per_landmark)
    for i, pca in enumerate(pca_models):
        weight = num_samples_per_landmark[i] / total_samples
        combined_projection_matrix += weight * pca.components_
    
    # Aplicar a projeção combinada nos dados originais
    projected_data = np.dot(matriz, combined_projection_matrix.T)
    
    return projected_data



def t_sne(matriz):
    tsne = TSNE(n_components=2, random_state=42)

    # Ajustar o modelo aos dados e transformá-los
    matriz_saida = tsne.fit_transform(matriz) 

    return matriz_saida

# Dicionário de casos
switch = {
    1: isomap,
    2: lamp,
    3: lsp,
    4: plmp,
    5: t_sne
}

# Define a função que será aplicada aos valores associados a cada chave
def funcao_aplicada(matriz,case):
    
    matriz_saida = switch.get(case,default_case)(matriz)
    
    return matriz_saida

def processar_arquivo_entrada(nome_arquivo_entrada):
    dados_entrada = {}

    # Lê o arquivo de entrada e organiza os dados
    with open(nome_arquivo_entrada, 'r', newline='') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        titulo = next(leitor_csv)
        classes = []
        for linha in leitor_csv:
            chave = linha[0]
            classes.append(linha[4])
            valores = linha[6:]
            dados_entrada[chave] = valores

    return titulo,classes, dados_entrada

def escrever_arquivo_saida(dados_entrada, nome_arquivo_saida):
    
    nome_arquivo_saida = "./output/"+ nome_arquivo_saida
    # Escreve os dados no arquivo de saída
    with open(nome_arquivo_saida, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        for chave, valor in dados_entrada.items():
            print(valor)
            classe,valor1,valor2 = valor
            escritor_csv.writerow([chave,classe,valor1,valor2])



def main():
    # Nome do arquivo de entrada e saída
    nome_arquivo = "GSI016"
    nome_arquivo_entrada = "./input/" + nome_arquivo + ".csv" #endereço de busca
    
    tecnica = int(input("Técnicas de teste:\n1: ISOMAP - (Isometric Mapping)\n2: LAMP\t - (Linear Aggregation of Multiple Projections)\n3: LSP\t - (Least Squares Projections)\n4: PLMP\t - (Projected Landmark Multi-Projection) - OBS.:Usa KMeans\n5: t-SNE - (t-distributed Stochastic Neighbor Embedding)\nDigite o número da tecnica: "))

    if tecnica == 1:
        nome_arquivo_saida = "Saida_ISOMAP_"+ nome_arquivo +".csv"
    elif tecnica == 2:
        nome_arquivo_saida = "Saida_LAMP_"+ nome_arquivo +".csv"
    elif tecnica == 3:
        nome_arquivo_saida = "Saida_LSP_"+ nome_arquivo +".csv"
    elif tecnica == 4:
        nome_arquivo_saida = "Saida_PLMP_"+ nome_arquivo +".csv"
    elif tecnica == 5:
        nome_arquivo_saida = "Saida_t-SNE_"+ nome_arquivo +".csv"
    else:
        print("ERRO: não foi selecionada uma técnica válida")
        exit(0)

    # Processa o arquivo de entrada
    titulo,classes,dados_entrada = processar_arquivo_entrada(nome_arquivo_entrada)

    # armazenando chaves 
    chave_dos_dados = dados_entrada.keys()

    # Faz a matriz dos dados
    matriz = np.array(list(dados_entrada.values()))
    matriz = matriz.astype(float)
    
    # Executa a função
    matriz = funcao_aplicada(matriz,tecnica)

    # Verificando os dados
    #print(titulo)
    #print(matriz)
    #print(chave_dos_dados)

    
    # adicionando apenas o título
    dicio = {}
    dicio["id"] = ["class","v1","v2"]
    #print(dicio)

    # adiciona as chaves e matriz
    for chave, classe, dado in zip(chave_dos_dados,classes,matriz):
            data_ = dado.tolist()
            data_.insert(0, classe)
            dicio[chave] = data_

    
    # Escreve o arquivo de saída recebendo um dicionario
    escrever_arquivo_saida(dicio, nome_arquivo_saida)

    print("Processamento concluído. Verifique o arquivo de saída.")

if __name__ == "__main__":
    main()
