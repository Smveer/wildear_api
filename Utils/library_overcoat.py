import ctypes
import numpy as np
from typing import List

# LOAD Rust ML LIBRARY
rml = ctypes.CDLL(r"./Library/target/debug/librust_ml.dylib")

# Initialise RML functions
rml.delete_mlp_model.argtypes = [ctypes.c_void_p]

rml.create_pmc_model.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
rml.create_pmc_model.restype = ctypes.c_void_p

rml.train_pmc_model.argtypes = [ctypes.c_void_p,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int,
                                ctypes.c_double, ctypes.c_int, ctypes.c_bool]

rml.predict_pmc.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double),
                            ctypes.c_int, ctypes.c_bool]
rml.predict_pmc.restype = ctypes.POINTER(ctypes.c_float)

rml.export_pmc.argtypes = [ctypes.c_void_p]
rml.export_pmc.restype = ctypes.c_char_p
rml.load_pmc_json.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
rml.load_pmc_json.restype = ctypes.c_void_p


def del_pmc(ptr: ctypes.c_void_p):
    rml.delete_mlp_model(ptr)


def load_pmc(path: str, init: List[int]) -> ctypes.c_void_p:
    param = np.array(init, dtype=np.int32)
    c_param = param.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    mlp_ptr = rml.create_pmc_model(c_param, ctypes.c_int(len(param)))

    with open(path, "r") as file:
        json_data = file.read()

    ptr = rml.load_pmc_json(json_data.encode("utf-8"), mlp_ptr)
    return ptr


def predict_pmc(mlp_ptr: ctypes.c_void_p, input_x: List[float], is_classification: bool):
    np_input = np.array(input_x, dtype=np.float32)

    input_ptr = np_input.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    c_length = ctypes.c_int(len(np_input))
    c_is_classification = ctypes.c_bool(is_classification)

    output_ptr = rml.predict_pmc(mlp_ptr, input_ptr, c_length, ctypes.c_bool(c_is_classification))
    return output_ptr


def export_pmc_as_json_string(
        mlp_ptr: ctypes.c_void_p
):
    jstring = rml.export_pmc(mlp_ptr)
    return ctypes.cast(jstring, ctypes.c_char_p).value.decode("utf-8")

