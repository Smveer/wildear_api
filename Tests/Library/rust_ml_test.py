import ctypes
import json
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
rml.train_pmc_model.argtypes = [ctypes.c_void_p,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.c_double, ctypes.c_int, ctypes.c_bool]
rml.export_pmc.argtypes = [ctypes.c_void_p]
rml.export_pmc.restype = ctypes.c_char_p
rml.load_pmc_json.argtypes = [ctypes.c_char_p, ctypes.c_void_p]

# Test
param = np.array([2, 1])
c_param = param.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

mlp_ptr = rml.create_pmc_model(c_param, ctypes.c_int(len(param)))

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
print("----------inputs-----------")
for i in range(0, len(arr)):
    print(f"arr[{i}] : {arr[i]}")
print("----------ouputs-----------")
for i in range(0, len(arr2)):
    print(f"arr2[{i}] : {arr2[i]}")

i_ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
c_length = ctypes.c_int(len(arr))
c_sub_length = ctypes.c_int(len(i_test[0]))

o_ptr = arr2.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
o_length = ctypes.c_int(len(arr2))
o_sub_length = ctypes.c_int(len(o_test[0]))

alpha = ctypes.c_double(1.0)
iteration = ctypes.c_int(1)
is_classif = ctypes.c_bool(True)

rml.train_pmc_model(mlp_ptr, i_ptr, c_length, c_sub_length, o_ptr, o_length, o_sub_length, alpha, iteration, is_classif)
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

        print("--------------------- Predict ---------------------")
        res_ptr = rml.predict_pmc(mlp_ptr, sample_ptr, sample_length, True)
        res_array = np.ctypeslib.as_array(res_ptr, shape=(len(sample_inputs),)).astype(np.float32)
        print(res_array)


rml.delete_mlp_model(mlp_ptr)
