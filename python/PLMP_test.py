from sklearn.cross_decomposition import PLSCanonical
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# Carregar um conjunto de dados de exemplo (por exemplo, Iris dataset)
iris = load_iris()
X = iris.data
y = iris.target

# Criar uma instância do modelo PLSCanonical
plsc = PLSCanonical(n_components=2)

# Ajustar o modelo aos dados
plsc.fit(X, y)

# Transformar os dados
X_pls = plsc.transform(X)

# Plotar os dados transformados
plt.scatter(X_pls[:, 0], X_pls[:, 1], c=y, cmap='viridis')
plt.xlabel('PLS Component 1')
plt.ylabel('PLS Component 2')
plt.title('PLMP')
plt.colorbar(label='Target Class')
plt.show()
