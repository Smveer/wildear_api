import ctypes
import numpy as np
import matplotlib.pyplot as plt

# Import la library
wd = ctypes.CDLL(r"../../Library/target/debug/librust_ml.dylib")


# Import la structure
class LinearRegressionModel(ctypes.Structure):
    _fields_ = [
        ('coefficient', ctypes.c_double),
        ('constant', ctypes.c_double)
    ]


class PolynomialRegressionModel(ctypes.Structure):
    _fields_ = [
        ('coefficients', ctypes.POINTER(ctypes.c_double)),
        ('degree', ctypes.c_size_t)
    ]


# Init argument & return of all Rust function
wd.add.argtype = [ctypes.c_int32, ctypes.c_int32]
wd.create_linear_regression_model.restype = LinearRegressionModel
wd.train_linear_regression_model.argtype = [
    LinearRegressionModel,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_size_t
]
wd.predict_linear_regression_model.argtype = [LinearRegressionModel, ctypes.c_double]
wd.predict_linear_regression_model.restype = ctypes.c_double
wd.delete_linear_regression_model.argtype = [LinearRegressionModel]

# Model creation
model: LinearRegressionModel = wd.create_linear_regression_model()
print(f"------ INITIALISATION ------ \nf(x) = {model.coefficient} * x + {model.constant}")

# Set Datas
X = np.array([[3], [7]], dtype=np.float64)
Y = np.array([6, 12], dtype=np.float64)

plt.scatter(X, Y, color='red')

# Convert datas to C for be able to use them in Library
cx = X.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
cy = Y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

# Model training
wd.train_linear_regression_model(ctypes.byref(model), cx, cy, len(X))
print(f"\n------ TRAINING ------ \nf(x) = {model.coefficient} * x + {model.constant}")

# Set variable to predict & convert it in C to use it in our Library
x = 2
c_input = ctypes.c_double(x)
predicted = wd.predict_linear_regression_model(ctypes.byref(model), c_input)
print(f"\n------ PREDICTION ------ \nf({x}) = {predicted}")

l = np.linspace(0, 8, 7)
f = model.coefficient * l + model.constant
plt.plot(l, f)
plt.grid(True)
plt.show()

# Delete model in the memory
wd.delete_linear_regression_model(model)
# wd.delete_polynomial_regression_model(model)

#
