import csv
import numpy as np
from sklearn.manifold import TSNE
from sklearn.manifold import Isomap
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


#import umap.umap_ as umap

epsilon = 1e-7

def default_case():
    print("Erro: operação desconhecida")
    return exit(0)

def isomap(matriz):
    isomap = Isomap(n_components=2)
    matriz_saida = isomap.fit_transform(matriz)
    return matriz_saida

def lsp(matriz):
    # Normalizando os dados
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(matriz)
    
    # Aplicando a técnica de projeção LSP
    svd = TruncatedSVD(n_components=2)
    matriz_saida = svd.fit_transform(data_normalized)
    
    return matriz_saida


def plmp(matriz, n_segmentos=2):
    """
    Função para aplicar PLMP (Part-Linear Multidimensional Projection) em uma matriz de dados.

    Parâmetros:
    - matriz: numpy array ou DataFrame contendo os dados de entrada.
    - n_segmentos: número de segmentos nos quais a matriz será dividida.
    - n_componentes: número de componentes principais para a projeção linear (PCA).

    Retorna:
    - Uma matriz com as projeções combinadas.
    """

    # Função para segmentar os dados
    def segmentar_dados(matriz, n_segmentos):
        return np.array_split(matriz, n_segmentos)

    # Função para aplicar PCA em cada segmento
    def aplicar_pca_segmento(segmento, n_componentes=2):
        pca = PCA(n_components=n_componentes)
        pca_projetado = pca.fit_transform(segmento)
        return pca_projetado

    # Segmentar os dados
    segmentos = segmentar_dados(matriz, n_segmentos)

    # Aplicar PCA a cada segmento
    projecoes = [aplicar_pca_segmento(segmento) for segmento in segmentos]

    # Combinar todas as projeções em uma única matriz
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
    dados_entrada = {}

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
    nome_arquivo = "GSI002_col1"
    nome_arquivo_entrada = "./input/" + nome_arquivo + ".csv" #endereço de busca
    
    tecnica = int(input("Técnicas de teste:\n1: ISOMAP - (Isometric Mapping)\n2: LSP\t - (Least Squares Projections)\n3: PLMP\t - (Part-Linear Multidimensional Projection)\n4: t-SNE - (t-distributed Stochastic Neighbor Embedding)\nDigite o número da tecnica: "))

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
