from typing import List
from Utils.utilities import *
from Utils.library_overcoat import rml

dataset_directory = "/Resources/Dataset/"

classes = {
    "bear_roar": [[], [1.0, 0.0, 0.0]],
    "royal_eagle": [[], [0.0, 1.0, 0.0]],
    "wolf": [[], [0.0, 0.0, 1.0]]
}

for k in classes.keys():
    path = dataset_directory + k + "/" + k + ".wav"
    files = Path(
        Audio.get_directory_path_from_path(path)
    ).glob(
        Audio.get_filename_from_path(path, False) + "_*" + Audio.get_file_extension_from_path(path)
    )
    classes[k][0] = [str(f) for f in files]


def get_output_inputs_from_dict(
        classiz: dict
):
    outputs = []
    inputs = []
    for key in classiz.keys():
        for f in classiz[key][0]:
            inputs.append(flatten_png_file_into_array(f, greyscale=True))
            outputs.append(np.array(classiz[key][1], dtype=np.float32))
    return inputs, outputs


def train_pmc_model(
    mlp_ptr: ctypes.c_void_p,
    inputs_x: List[float],
    inputs_x_size: int,
    x_size: int,
    outputs_y: List[float],
    outputs_y_size: int,
    y_size: int,
    learning_rate: float,
    epochs: int,
    is_classification: bool
):
    np_inputs = np.array(inputs_x, dtype=np.float32)
    np_outputs = np.array(outputs_y, dtype=np.float32)

    inputs_ptr = np_inputs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    outputs_ptr = np_outputs.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    c_inputs_x_size = ctypes.c_int(inputs_x_size)
    c_x_size = ctypes.c_int(x_size)
    c_outputs_y_size = ctypes.c_int(outputs_y_size)
    c_y_size = ctypes.c_int(y_size)
    c_learning_rate = ctypes.c_double(learning_rate)
    c_epochs = ctypes.c_int(epochs)
    c_is_classification = ctypes.c_bool(is_classification)

    rml.train_pmc_model(
        mlp_ptr,
        inputs_ptr, c_inputs_x_size, c_x_size,
        outputs_ptr, c_outputs_y_size, c_y_size,
        c_learning_rate, c_epochs, c_is_classification
    )

i, o = get_output_inputs_from_dict(classes)
