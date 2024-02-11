import numpy as np

# Dados originais (matriz X)
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

# Variável alvo (vetor y)
y = np.array([1, 2, 3])

# Calcular os coeficientes da projeção de mínimos quadrados
coefficients = np.linalg.lstsq(X, y, rcond=None)[0]

# Projeto de mínimos quadrados dos dados originais
projection = np.dot(X, coefficients)

print("Coeficientes da projeção de mínimos quadrados:", coefficients)
print("Projeção de mínimos quadrados:", projection)
