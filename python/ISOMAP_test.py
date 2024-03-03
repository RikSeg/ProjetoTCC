from sklearn.datasets import make_swiss_roll
from sklearn.manifold import Isomap
import matplotlib.pyplot as plt




# Gerar dados de exemplo (Swiss Roll dataset)
X, _ = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)

#Leitura dos dados do csv
def main():
    # Gerar dados de exemplo (Swiss Roll dataset)
    X, _ = make_swiss_roll(n_samples=1000, noise=0.2, random_state=42)

# Criar uma instância do modelo ISOMAP
    isomap = Isomap(n_components=2, n_neighbors=10)

# Ajustar o modelo aos dados e transformá-los
    X_iso = isomap.fit_transform(X)

# Plotar os dados originais e os dados transformados pelo ISOMAP
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(X[:, 0], X[:, 1], c=X[:, 2], cmap=plt.cm.Spectral)
    plt.title('Original Data')

    plt.subplot(1, 2, 2)
    plt.scatter(X_iso[:, 0], X_iso[:, 1], c=X[:, 2], cmap=plt.cm.Spectral)
    plt.title('ISOMAP')

    plt.show()

if __name__== "__main__":
    main()