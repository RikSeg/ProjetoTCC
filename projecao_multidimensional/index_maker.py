import pandas as pd

#PARA CASO SEJA PRECISO CRIAR INDICE (Como foi o caso da base iris)

# Lê o arquivo CSV sem cabeçalhos
df = pd.read_csv('./input/Iris.csv', header=None)

# Adicione uma coluna de índice (substitua 'nome_do_indice' pelo nome que você deseja)
df.insert(0, 'nome_do_indice', range(1, len(df) + 1))

# Salve o DataFrame de volta no arquivo CSV (substitua 'novo_arquivo.csv' pelo nome do arquivo que você deseja)
df.to_csv('novo_arquivo.csv', index=False, header=False)  # Defina index=False e header=False para evitar que o índice e cabeçalhos sejam salvos no arquivo
