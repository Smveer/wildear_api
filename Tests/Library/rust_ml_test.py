import ctypes

import numpy as np

# LOAD Rust ML LIBRARY
rml = ctypes.CDLL(r"../../Library/target/debug/librust_ml.dylib")

# Initialise RML functions
rml.create_mlp_model.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
rml.create_mlp_model.restype = ctypes.c_void_p
rml.delete_mlp_model.argtypes = [ctypes.c_void_p]

# Test
param = np.array([1, 1])
c_param = param.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

mlp_ptr = rml.create_mlp_model(c_param, ctypes.c_int(2))

print("Test en cour")
if mlp_ptr is not None:
    print(mlp_ptr)

rml.delete_mlp_model(mlp_ptr)
