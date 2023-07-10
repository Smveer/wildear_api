import ctypes
import json
import numpy as np
from typing import List


class MyMLP:
    # Constructeur
    # npl : Neurons Per Layer - représentant la structure du PMC choisie par l'utilisateur
    # (nombre d'entrées, nombre de neurones par couches cachées, nombre de sorties)
    def __init__(self, npl: List[int]):
        self.d = npl
        self.L = len(npl) - 1
        self.W = []

        # Initialisation des poids du modèles entre -1 et 1 (sauf pour les poids inutiles que l'on laissera à 0)
        for l in range(self.L + 1):
            self.W.append([])

            if l == 0:
                continue
            for i in range(npl[l - 1] + 1):
                self.W[l].append([])
                for j in range(npl[l] + 1):
                    self.W[l][i].append(0.0 if j == 0 else np.random.uniform(-1.0, 1.0))

        # Création de l'espace mémoire pour 'stocker' plus tard les valeurs de sorties de chaque neurone
        self.X = []
        for l in range(self.L + 1):
            self.X.append([])
            for j in range(npl[l] + 1):
                self.X[l].append(1.0 if j == 0 else 0.0)

        # Création de l'espace mémoire pour 'stocker' plus tard les semi-gradient associés à chaque neurone
        self.deltas = []
        for l in range(self.L + 1):
            self.deltas.append([])
            for j in range(npl[l] + 1):
                self.deltas[l].append(0.0)

    # Propagation et mise à jour des valeurs de sorties de chaque neurone à partir des entrées d'un exemple
    def _propagate(self, inputs: List[float], is_classification: bool):
        # copie des entrées dans la 'couche d'entrée' du modèle
        for j in range(self.d[0]):
            self.X[0][j + 1] = inputs[j]

        # mise à jour récursive des valeurs de sorties des neurones, couche après couche
        for l in range(1, self.L + 1):
            for j in range(1, self.d[l] + 1):
                total = 0.0
                for i in range(0, self.d[l - 1] + 1):
                    total += self.W[l][i][j] * self.X[l - 1][i]

                if l < self.L or is_classification:
                    total = np.tanh(total)

                self.X[l][j] = total

    # Méthode à utiliser pour interroger le modèle (inférence)
    def predict(self, inputs: List[float], is_classification: bool):
        self._propagate(inputs, is_classification)
        return self.X[self.L][1:]

    # Méthode à utiliser pour entrainer le modèle à partir d'un dataset étiqueté
    def train(self, all_samples_inputs: List[List[float]], all_samples_expected_outputs: List[List[float]],
              is_classification: bool, iteration_count: int, alpha: float):
        # Pour un certain nombre d'itération
        for it in range(iteration_count):
            # Choix d'un exemple étiqueté au hasard dans le dataset
            k = np.random.randint(0, len(all_samples_inputs))
            inputs_k = all_samples_inputs[k]
            y_k = all_samples_expected_outputs[k]

            # Mise à jour des valeurs de sorties des neurones du modèle à partir des entrées de l'exemple sélectionné
            self._propagate(inputs_k, is_classification)

            # Calcul des semi gradients des neurones de la dernière couche
            for j in range(1, self.d[self.L] + 1):
                self.deltas[self.L][j] = (self.X[self.L][j] - y_k[j - 1])
                if is_classification:
                    self.deltas[self.L][j] *= (1 - self.X[self.L][j] ** 2)

            # Calcul de manière récursive des semi gradients des neurones des couches précédentes
            for l in reversed(range(1, self.L + 1)):
                for i in range(1, self.d[l - 1] + 1):
                    total = 0.0
                    for j in range(1, self.d[l] + 1):
                        total += self.W[l][i][j] * self.deltas[l][j]
                    self.deltas[l - 1][i] = (1 - self.X[l - 1][i] ** 2) * total

            # Correction des poids du modèle
            for l in range(1, self.L + 1):
                for i in range(0, self.d[l - 1] + 1):
                    for j in range(1, self.d[l] + 1):
                        self.W[l][i][j] -= alpha * self.X[l - 1][i] * self.deltas[l][j]


# LOAD Rust ML LIBRARY
rml = ctypes.CDLL(r"../../Library/target/debug/librust_ml.dylib")

# Initialise RML functions
rml.delete_mlp_model.argtypes = [ctypes.c_void_p]
# ----------
rml.create_pmc_model.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
rml.create_pmc_model.restype = ctypes.c_void_p

rml.predict_pmc.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
                            ctypes.c_int, ctypes.c_bool]
rml.predict_pmc.restype = ctypes.POINTER(ctypes.c_float)
rml.train_pmc_model.argtypes = [ctypes.c_void_p,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.c_double, ctypes.c_int, ctypes.c_bool]
rml.export_pmc.argtypes = [ctypes.c_void_p]
rml.export_pmc.restype = ctypes.c_char_p
rml.load_pmc_json.argtypes = [ctypes.c_char_p, ctypes.c_void_p]

# Test
param = np.array([2, 1], dtype=np.int32)
c_param = param.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

mlp_ptr = rml.create_pmc_model(c_param, ctypes.c_int(len(param)))

python_mlp = MyMLP(param)

"""pmc_data_c_string = rml.export_pmc(mlp_ptr)
pmc_data_str = ctypes.cast(pmc_data_c_string, ctypes.c_char_p).value.decode("utf-8")

print("test string :")
print(pmc_data_str)
pmc_data_json = json.loads(pmc_data_str)

with open("pmc_data.json", "w") as file:
    json.dump(pmc_data_json, file)

with open("pmc_data.json", "r") as file:
    json_data = file.read()

rml.load_pmc_json(json_data.encode("utf-8"), mlp_ptr)"""

i_test = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0]], dtype=np.float32)
arr = i_test.flatten()
o_test = np.array([[1.0], [-1.0], [-1.0]], dtype=np.float32)
arr2 = o_test.flatten()
"""print("----------inputs-----------")
for i in range(0, len(arr)):
    print(f"arr[{i}] : {arr[i]}")
print("----------ouputs-----------")
for i in range(0, len(arr2)):
    print(f"arr2[{i}] : {arr2[i]}")"""

i_ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
c_length = ctypes.c_int(len(arr))
c_sub_length = ctypes.c_int(len(i_test[0]))

o_ptr = arr2.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
o_length = ctypes.c_int(len(arr2))
o_sub_length = ctypes.c_int(len(o_test[0]))

alpha = ctypes.c_double(0.01)
iteration = ctypes.c_int(100000)
is_classification = ctypes.c_bool(True)

rml.train_pmc_model(mlp_ptr, i_ptr, c_length, c_sub_length, o_ptr, o_length, o_sub_length, alpha, iteration,
                    is_classification)
print("---------------------")

print("Pointer du pmc :")
if mlp_ptr is not None:
    print(mlp_ptr)
    test_1_all_samples_inputs = np.array([
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0]
    ], dtype=np.float32)
    test_1_all_samples_expected_outputs = np.array([
        [1.0],
        [-1.0],
        [-1.0]
    ], dtype=np.float32)

    res = []
    for sample_inputs in test_1_all_samples_inputs:
        sample_ptr = sample_inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        sample_length = ctypes.c_int(len(sample_inputs))

        res_ptr = rml.predict_pmc(mlp_ptr, sample_ptr, sample_length, ctypes.c_bool(True))
        res_array = np.zeros(len(sample_inputs), dtype=np.float32)
        for i in range(len(sample_inputs)):
            res_array[i] = res_ptr[i]
        res.append([res_array[0]])

    print("--------------------- Predict ---------------------")
    print(res)


def print_python_mlp(model: MyMLP):
    print(f"Layers : {model.L}")
    print(f"n per layer len : {len(model.d)}")
    for i in range(len(model.d)):
        print(f"layer[{i}] : {model.d[i]}")

    print(f"Weights len : {len(model.W)}")
    for l in range(len(model.W)):
        for i in range(len(model.W[l])):
            for j in range(len(model.W[l][i])):
                print(f"-- weights[{l}][{i}][{j}]: {model.W[l][i][j]}")

    print(f"Neuron data len : {len(model.X)}")
    for i in range(len(model.X)):
        for j in range(len(model.X[i])):
            print(f"-- Neuron data[{i}][{j}]: {model.X[i][j]}")

    print(f"deltas len : {len(model.deltas)}")
    for i in range(len(model.deltas)):
        for j in range(len(model.deltas[i])):
            print(f"-- deltas[{i}][{j}]: {model.deltas[i][j]}")


print("-------------- PYTHON MLP ------------")
print_python_mlp(python_mlp)

test_1_all_samples_inputs = [
    [0, 0],
    [0, 1],
    [1, 0]
]
test_1_all_samples_expected_outputs = [
    [1],
    [-1],
    [-1]
]

python_mlp.train(test_1_all_samples_inputs, test_1_all_samples_expected_outputs, True, 100000, 0.01)
print("-------------- PYTHON After Train ------------")
print_python_mlp(python_mlp)

print("-------------- PYTHON Predict ------------")
for sample_inputs in test_1_all_samples_inputs:
    print(python_mlp.predict(sample_inputs, True))

rml.delete_mlp_model(mlp_ptr)
