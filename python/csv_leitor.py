import csv
import numpy as np
from sklearn.manifold import Isomap
import umap

def default_case():
    print("Erro: operação desconhecida")
    return exit(0)

def isomap(matriz):
    isomap = Isomap(n_components=2, n_neighbors=10)
    matriz_saida = isomap.fit_transform(matriz)
    return matriz_saida

def lamp(matriz):
    # Criar uma instância do modelo UMAP com LAMP
    mapper = umap.UMAP(metric='lamp', n_components=2)

    # Ajustar o modelo aos dados e transformá-los
    matriz_saida = mapper.fit_transform(matriz)
    return matriz_saida


def lsp(matriz):

    return matriz


def plmp(matriz):

    return matriz


def t_sne(matriz):

    return matriz

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
    
    
    return switch.get(case, default_case)()

def processar_arquivo_entrada(nome_arquivo_entrada):
    dados_entrada = {}

    # Lê o arquivo de entrada e organiza os dados
    with open(nome_arquivo_entrada, 'r', newline='') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        for linha in leitor_csv:
            chave = linha[0]
            valores = linha[3:]
            dados_entrada[chave] = valores

    return dados_entrada

def escrever_arquivo_saida(dados_entrada, nome_arquivo_saida):
    # Remonta o Dicionario para saida
    dados_saida = {chave: valores for chave, valores in dados_entrada.items()}

    # Escreve os dados no arquivo de saída
    with open(nome_arquivo_saida, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        for chave, valor in dados_saida.items():
            escritor_csv.writerow([chave, valor])

def main():
    # Nome do arquivo de entrada e saída
    nome_arquivo_entrada = input("Digite o nome do arquivo CSV de entrada: ")
    nome_arquivo_saida = input("Digite o nome do arquivo CSV de saída: ")

    # Processa o arquivo de entrada
    dados_entrada = processar_arquivo_entrada(nome_arquivo_entrada)

    # Faz a matriz dos dados
    matriz = np.array(list(dados_entrada.values()))
    
    # Executa a função
    matriz = funcao_aplicada(matriz)

    # Escreve o arquivo de saída
    escrever_arquivo_saida(matriz, nome_arquivo_saida)

    print("Processamento concluído. Verifique o arquivo de saída.")

if __name__ == "__main__":
    main()
