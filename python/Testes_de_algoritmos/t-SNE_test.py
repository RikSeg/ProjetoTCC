from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Carregar um conjunto de dados de exemplo (por exemplo, dígitos escritos à mão)
digits = load_digits()
X = digits.data
y = digits.target

print(y)

# Criar uma instância do modelo t-SNE
tsne = TSNE(n_components=2, random_state=42)

# Ajustar o modelo aos dados e transformá-los
X_tsne = tsne.fit_transform(X)

# Plotar os dados transformados
plt.figure(figsize=(10, 8))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='tab10', s=10)
plt.colorbar(label='Digit Label')
plt.title('t-SNE Visualization of Digits Dataset')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.show()
