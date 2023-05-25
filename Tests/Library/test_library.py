import ctypes
import numpy as np

# Import la library
wd = ctypes.CDLL(r"../../Library/target/debug/libLibrary.dylib")


# Import la structure
class LinearRegressionModel(ctypes.Structure):
    _fields_ = [
        ('coefficient', ctypes.c_double),
        ('constant', ctypes.c_double)
    ]


# Init library
wd.add.argtype = [ctypes.c_int32, ctypes.c_int32]
wd.create_linear_regression_model.restype = LinearRegressionModel
wd.train_linear_regression_model.argtype = [
    LinearRegressionModel,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t
]
wd.delete_linear_regression_model.argtype = [LinearRegressionModel]

a = wd.add(2, 3)
print(f"LIBRARY : {a}")

model: LinearRegressionModel = wd.create_linear_regression_model()
print(f"MODEL Coeff: {model.coefficient} | constant : {model.constant}")

X = np.array([[1.0], [2]], dtype=np.float64)
Y = np.array([2.0, 3.0], dtype=np.float64)
# conversion en c
# c_X = (ctypes.c_double * len(X))(*X)
# c_Y = (ctypes.c_double * len(Y))(*Y)

cx = X.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
cy = Y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

wd.train_linear_regression_model(ctypes.byref(model), cx, cy, len(X))
print(f"Après entrainement \nModel Coeff: {model.coefficient} | constant : {model.constant}")

predicted = wd.predict_linear_regression_model(ctypes.byref(model), ctypes.c_double(1.0))
print(f"Predict : {predicted}")

wd.delete_linear_regression_model(model)
