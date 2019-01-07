"""
This example shows how to train an RNN on a set of smiles and how to predict new smiles with the trained model.
"""

from models import smiles_generator, data_processing
import os
import random
import numpy as np

# Reading the data
current_dir = os.path.dirname(os.path.realpath(__file__))
in_d = open(current_dir + "/../data/bioactivity_PPARg_filtered.csv", 'r')

# Parsing the data
molecules = []

for line in in_d:
    line_split = line.split(",")
    molecule_raw = line_split[-3]
    molecule = molecule_raw[1:-1]
    if molecule == "CANONICAL_SMILES":
        pass
    else:
        molecules.append(molecule)
random.shuffle(molecules)
print("The total number of molecules is: %i \n" % (len(molecules)))

# One-hot encode the molecules
dp = data_processing.Molecules_processing()
X = dp.onehot_encode(molecules)
# y is just the same as X just shifted by one
y = np.zeros(X.shape)
y[:, :-1, :] = X[:, 1:, :]

# Creating the model
estimator = smiles_generator.Smiles_generator(epochs=20, batch_size=100, tensorboard=False, hidden_neurons_1=100,
                                              hidden_neurons_2=100, dropout_1=0.3, dropout_2=0.5, learning_rate=0.001)

# Training the model on the one-hot encoded molecules
estimator.fit(X, y)

# Predicting 10 new molecules from the fitted model at a temperature of 0.75
X_pred = ["G"]*10
X_pred_hot = dp.onehot_encode(X_pred)
pred_hot = estimator.predict(X_pred_hot, temperature=0.75)
pred = dp.onehot_decode(pred_hot)

print(pred)

# Saving the estimator for later re-use
estimator.save("example-save")

