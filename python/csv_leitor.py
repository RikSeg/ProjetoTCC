import csv

# Define a função que será aplicada aos valores associados a cada chave
def funcao_aplicada(valores):
    # Exemplo: somar os valores associados
    return sum(map(int, valores))

def processar_arquivo_entrada(nome_arquivo_entrada):
    dados_entrada = {}

    # Lê o arquivo de entrada e organiza os dados
    with open(nome_arquivo_entrada, 'r', newline='') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        for linha in leitor_csv:
            chave = linha[0]
            valores = linha[1:]
            dados_entrada[chave] = valores

    return dados_entrada

def aplicar_funcao_e_escrever_arquivo_saida(dados_entrada, nome_arquivo_saida):
    # Aplica a função a cada valor associado a cada chave
    dados_saida = {chave: funcao_aplicada(valores) for chave, valores in dados_entrada.items()}

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

    # Aplica a função e escreve o arquivo de saída
    aplicar_funcao_e_escrever_arquivo_saida(dados_entrada, nome_arquivo_saida)

    print("Processamento concluído. Verifique o arquivo de saída.")

if __name__ == "__main__":
    main()
