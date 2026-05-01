from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import sklearn
import numpy as np
from utilities import process_data

inputs, outputs = process_data("Data/SaveFiles/saved_data.pkl", 20, 20)

x = np.array(inputs)
y = np.array(outputs)

scaler_fn = sklearn.preprocessing.StandardScaler()

x_scaled = scaler_fn.fit_transform(x)

pca = sklearn.decomposition.PCA(2)
x_pca = pca.fit_transform(x_scaled)

plt.scatter(x_pca[:, 0], x_pca[:, 1], c=y)
plt.colorbar()
plt.show()
