import csv

def ler_csv_para_matriz(nome_arquivo):
    matriz = []
    with open(nome_arquivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            matriz.append(row)
    return matriz

def imprimir_matriz(matriz):
    for row in matriz:
        print(row)

# Exemplo de uso
nome_arquivo = 'Teste.csv'
minha_matriz = ler_csv_para_matriz(nome_arquivo)
"""imprimir_matriz(minha_matriz)"""
