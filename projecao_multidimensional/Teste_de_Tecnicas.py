import csv
import numpy as np
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
from scipy.linalg import lstsq


#import umap.umap_ as umap

epsilon = 1e-7

def default_case():
    print("Erro: operação desconhecida")
    return exit(0)

def isomap(matriz):
    isomap = Isomap(n_components=2)
    matriz_saida = isomap.fit_transform(matriz)
    return matriz_saida

def lsp(matriz,n_components=2,k=5):
    n_samples = matriz.shape[0]
    
    # Etapa 1: Calcular distâncias euclidianas
    distances = euclidean_distances(matriz)
    
    # Etapa 2: Construir grafo de vizinhança (kNN)
    neighbors = np.argsort(distances, axis=1)[:, 1:k+1]
    W = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in neighbors[i]:
            W[i, j] = 1 / (distances[i, j] + 1e-5)  # Evitar divisão por zero
    
    # Normalizar a matriz de pesos
    W = (W + W.T) / 2  # Tornar simétrica
    
    # Etapa 3: Resolver o problema de mínimos quadrados
    # Inicializar a projeção final
    projections = np.zeros((n_samples, n_components))
    
    for d in range(n_components):
        # Inicializar aleatoriamente o vetor de projeção
        initial_projection = np.random.rand(n_samples)
        
        # Resolver Ax = b para mínimos quadrados, usando a inicialização
        A = np.eye(n_samples) - W
        b = initial_projection  # Agora usamos o vetor inicial
        projection, _, _, _ = lstsq(A, b)
        projections[:, d] = projection
    
    return projections


def plmp(matriz, n_segmentos=3, n_components=2):
    """
    Implementação de PLMP (Part-Linear Multidimensional Projection).
    
    Parâmetros:
        matriz (numpy.ndarray): Dados de entrada (amostras x características).
        n_segmentos (int): Número de segmentos nos quais os dados serão divididos.
        n_components (int): Número de componentes principais para a projeção linear (PCA).
        
    Retorna:
        numpy.ndarray: Matriz de dados projetada no espaço de baixa dimensionalidade.
    """
    # Etapa 1: Definir os segmentos usando KMeans
    kmeans = KMeans(n_clusters=n_segmentos, random_state=42)
    labels = kmeans.fit_predict(matriz)
    
    # Etapa 2: Aplicar PCA em cada segmento
    projecoes = []
    for segmento_id in range(n_segmentos):
        segmento = matriz[labels == segmento_id]
        pca = PCA(n_components)
        projecao = pca.fit_transform(segmento)
        projecoes.append(projecao)
    
    # Etapa 3: Combinar as projeções em uma única matriz
    projecao_final = np.vstack(projecoes)
    
    return projecao_final



def t_sne(matriz):
    tsne = TSNE(n_components=2)

    # Ajustar o modelo aos dados e transformá-los
    matriz_saida = tsne.fit_transform(matriz) 

    return matriz_saida

# Dicionário de casos
switch = {
    1: isomap,
    2: lsp,
    3: plmp,
    4: t_sne 
}

# Define a função que será aplicada aos valores associados a cada chave
def funcao_aplicada(matriz,case):
    
    matriz_saida = switch.get(case,default_case)(matriz)
    
    return matriz_saida

def processar_arquivo_entrada(nome_arquivo_entrada):
    print("NOME: "+nome_arquivo_entrada)
    dados_entrada = {}

    if nome_arquivo_entrada == "./input/iris_index.csv":
        with open(nome_arquivo_entrada, 'r', newline='') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            titulo = next(leitor_csv)
            classes = []
            for linha in leitor_csv:
                chave = linha[0]
                classes.append(linha[1])
                valores = linha[2:]
                dados_entrada[chave] = valores
    else:
        # Lê o arquivo de entrada e organiza os dados
        with open(nome_arquivo_entrada, 'r', newline='') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            titulo = next(leitor_csv)
            classes = []
            for linha in leitor_csv:
                chave = linha[0]
                classes.append(linha[4])
                valores = linha[5:]
                dados_entrada[chave] = valores

    return titulo,classes, dados_entrada

def escrever_arquivo_saida(dados_entrada, nome_arquivo_saida):
    
    nome_arquivo_saida = "./output/"+ nome_arquivo_saida
    # Escreve os dados no arquivo de saída
    with open(nome_arquivo_saida, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        for chave, valor in dados_entrada.items():
            #print(valor)
            if len(valor) == 2:
                classe,valor1 = valor
                escritor_csv.writerow([chave,classe,valor1])
            else:
                classe,valor1,valor2 = valor
                escritor_csv.writerow([chave,classe,valor1,valor2])



def main():
    # Nome do arquivo de entrada e saída
    nome_arquivo = "iris_index"
    nome_arquivo_entrada = "./input/" + nome_arquivo + ".csv" #endereço de busca
    
    tecnica = int(input("Técnicas de teste:\n1: ISOMAP - (Isometric Mapping)\n2: LSP\t - (Least Squares Projections)\n3: PLMP\t - (Part-Linear Multidimensional Projection)\n4: t-SNE - (t-distributed Stochastic Neighbor Embedding)\nDigite o número da tecnica: "))

    if tecnica == 1:
        nome_arquivo_saida = "Saida_ISOMAP_"+ nome_arquivo +".csv"
    elif tecnica == 2:
        nome_arquivo_saida = "Saida_LSP_"+ nome_arquivo +".csv"
    elif tecnica == 3:
        nome_arquivo_saida = "Saida_PLMP_"+ nome_arquivo +".csv"
    elif tecnica == 4:
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
    print(type(chave_dos_dados),type(classes),type(matriz))
    for chave, classe, dado in zip(chave_dos_dados,classes,matriz):
            data_ = dado.tolist()
            data_.insert(0, classe)
            dicio[chave] = data_

    
    # Escreve o arquivo de saída recebendo um dicionario
    escrever_arquivo_saida(dicio, nome_arquivo_saida)

    print("Processamento concluído. Verifique o arquivo de saída.")

if __name__ == "__main__":
    main()
