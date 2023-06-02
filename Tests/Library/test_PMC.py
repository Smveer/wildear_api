import ctypes

# Chargement de la bibliothèque dynamique (.so, .dll, etc.)
mlp_lib = ctypes.CDLL(r"../../Library/target/debug/libLibrary.dylib")  # Remplacez "path/to/mlp_lib.so" par le chemin absolu de votre bibliothèque

# Définition des types de données
mlp_lib.create_mlp_model.restype = ctypes.c_void_p

# Appel de la fonction create_mlp_model
neurons_per_layer = [4, 8, 6, 3]  # Exemple de configuration des couches
arr_len = len(neurons_per_layer)
arr_type = ctypes.c_int * arr_len
arr = arr_type(*neurons_per_layer)

model_ptr = mlp_lib.create_mlp_model(arr, arr_len)

# Vérification du modèle créé
if model_ptr is not None:
    print("Modèle MLP créé avec succès !")
else:
    print("Erreur lors de la création du modèle MLP.")

mlp_lib.delete_mlp_model(model_ptr)