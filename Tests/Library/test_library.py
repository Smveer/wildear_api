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
# Polynomial Regression Model
wd.create_polynomial_regression_model.restype = PolynomialRegressionModel
wd.delete_polynomial_regression_model.argtype = [PolynomialRegressionModel]

# Model creation
# model: LinearRegressionModel = wd.create_linear_regression_model()
# print(f"------ INITIALISATION ------ \nf(x) = {model.coefficient} * x + {model.constant}")

model = wd.create_polynomial_regression_model()
print(f"Degrée : {model.degree}")


# Set Datas
#X = np.array([[3], [7]], dtype=np.float64)
#Y = np.array([6, 10], dtype=np.float64)

# Convert datas to C for be able to use them in Library
#cx = X.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
#cy = Y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

# Model training
#wd.train_linear_regression_model(ctypes.byref(model), cx, cy, len(X))
#print(f"\n------ TRAINING ------ \nf(x) = {model.coefficient} * x + {model.constant}")

# Set variable to predict & convert it in C to use it in our Library
#x = 5
#c_input = ctypes.c_double(x)
#predicted = wd.predict_linear_regression_model(ctypes.byref(model), c_input)
#rint(f"\n------ PREDICTION ------ \nf({x}) = {predicted}")

# Delete model in the memory
#wd.delete_linear_regression_model(model)
wd.delete_polynomial_regression_model(model)

#
