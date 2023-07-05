import ctypes

import numpy as np

# LOAD Rust ML LIBRARY
rml = ctypes.CDLL(r"../../Library/target/debug/librust_ml.dylib")

# Initialise RML functions
rml.delete_mlp_model.argtypes = [ctypes.c_void_p]
# ----------
rml.create_pmc_model.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
rml.create_pmc_model.restype = ctypes.c_void_p

rml.predict_pmc.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
                            ctypes.c_int, ctypes.c_bool]
rml.predict_pmc.restype = ctypes.POINTER(ctypes.c_int)

# Test
param = np.array([2, 1])
c_param = param.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

mlp_ptr = rml.create_pmc_model(c_param, ctypes.c_int(3))

print("Pointer du pmc :")
if mlp_ptr is not None:
    print(mlp_ptr)
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

    for sample_inputs in test_1_all_samples_inputs:
        sample_ptr = (ctypes.c_double * len(sample_inputs))(*sample_inputs)

        res_ptr = rml.predict_pmc(mlp_ptr, sample_ptr, len(sample_inputs),
                                  False)
        output = ctypes.c_double * len(sample_inputs)
        output_ptr = ctypes.cast(res_ptr, ctypes.POINTER(output))

        output_array = list(output_ptr.contents)

        for i in range(0, len(output_array)):
            print(f"res index : {i} : {output_array[i]}")

rml.delete_mlp_model(mlp_ptr)
