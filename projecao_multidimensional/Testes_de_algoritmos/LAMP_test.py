import umap
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

# Carregar um conjunto de dados de exemplo (por exemplo, dígitos escritos à mão)
digits = load_digits()

# Criar uma instância do modelo UMAP com LAMP
mapper = umap.UMAP(metric='cosine', n_components=2)

# Ajustar o modelo aos dados e transformá-los
embedding = mapper.fit_transform(digits.data)

# Plotar os dados transformados
plt.scatter(embedding[:, 0], embedding[:, 1], c=digits.target, cmap='Spectral', s=5)
plt.gca().set_aspect('equal', 'datalim')
plt.colorbar(boundaries=range(11)).set_ticks(range(10))
plt.title('LAMP')
plt.show()
