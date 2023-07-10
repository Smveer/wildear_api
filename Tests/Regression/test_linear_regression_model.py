import ctypes
import numpy as np

# Load library
rml = ctypes.CDLL("../../Library/target/debug/librust_ml.dylib")

# Init functions
rml.create_linear_regression_model.restype = ctypes.c_void_p
rml.train_linear_regression_model.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t
]
rml.delete_linear_regression_model.argtypes = [
    ctypes.c_void_p
]


# Create model
model = rml.create_linear_regression_model()

# Train model
X = np.array([[3], [7]], dtype=np.float64)
Y = np.array([6, 10], dtype=np.float64)

# Convert datas to C for be able to use them in Library
cx = X.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
cy = Y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

# Train model
rml.train_linear_regression_model(model, cx, cy, len(X))

# Delete model
rml.delete_linear_regression_model(model)