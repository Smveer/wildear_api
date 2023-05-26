use std::slice;
use rand::Rng;

#[no_mangle]
extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
extern "C" fn sum(arr: *const i32, nb_elems: i32) -> i32 {
    let safe_arr =
        unsafe {
            std::slice::from_raw_parts(arr, nb_elems as usize)
        };

    safe_arr.iter().sum()
}


#[no_mangle]
extern "C" fn count_to_n(n: i32) -> *mut i32 {
    let mut v: Vec<i32> = (0..n).collect();

    let arr_slice = v.leak();

    arr_slice.as_mut_ptr()
}

#[no_mangle]
extern "C" fn delete_int_array(arr: *mut i32, arr_len: i32) {
    unsafe {
        Vec::from_raw_parts(arr, arr_len as usize, arr_len as usize)
    };
}

struct MLP {
    nb_layer: usize,
    nb_neurons_per_layer: Vec<usize>,
    W: Vec<Vec<Vec<f32>>>,
    X: Vec<Vec<f32>>,
    deltas: Vec<Vec<f32>>,
}

#[repr(C)]
pub struct LinearRegressionModel  {
    coefficient: f64,
    constant: f64,
}

#[no_mangle]
extern "C" fn create_linear_regression_model() -> *mut LinearRegressionModel{
    let mut rng = rand::thread_rng();

    let model= Box::new(LinearRegressionModel {
        coefficient: 0.0,
        constant: 0.0,
    });

    let leaked = Box::leak(model);
    leaked
}
#[no_mangle]
extern "C" fn delete_linear_regression_model(model: *mut LinearRegressionModel) {
    unsafe {
        let _ = Box::from_raw(model);
    }
}

#[no_mangle]
extern "C" fn train_linear_regression_model(
    model: *mut LinearRegressionModel,
    dataset_input: *const f64,
    predict_output: *const f64,
    len: usize
){
    // ------------ Methode of Ordinary Least Squares : exact answer ------------

    // Create local variable to use in RUST from Python
    let mut model = unsafe { &mut *model };
    let input_slice = unsafe { slice::from_raw_parts(dataset_input,len) };
    let output_slice = unsafe{ slice::from_raw_parts(predict_output, len) };

    // Calc of means
    let mean_input = input_slice.iter().sum::<f64>() / len as f64;
    let mean_output = output_slice.iter().sum::<f64>() / len as f64;

    // Calc of gap
    let mut sum_gap= 0.0;
    let mut sum_squared= 0.0;

    for i in 0..len {
        let deviation_x = input_slice[i] - mean_input;
        let deviation_y = output_slice[i] - mean_output;
        sum_gap += deviation_x * deviation_y;
        sum_squared += deviation_x * deviation_x;
    }

    // Set coefficient & constant of the model
    model.coefficient = sum_gap / sum_squared;
    model.constant = mean_output - model.coefficient * mean_input;


    // ------------ Methode of Stochastic Gradient Descent : approximate answer (good for lot of data) ------------
    // Get the function cost
    // Function Cost : 1/2m x somme(i to m) x (F - Y)
    // Calc the gradient a & b
}

#[no_mangle]
extern "C" fn predict_linear_regression_model(model: *mut LinearRegressionModel, x: f64) -> f64 {
    let model = unsafe { &mut *model};
    model.coefficient * x + model.constant
}

#[no_mangle]
extern "C" fn create_mlp_model(arr: *mut i32, arr_len: i32) -> *mut MLP {
    let model = Box::new(MLP {
        nb_layer: 0,   //TODO
        nb_neurons_per_layer: vec![], //TODO
        W: vec![], //TODO
        X: vec![], //TODO
        deltas: vec![], //TODO
    });
    //TODO : Initialization

    let leaked = Box::leak(model);
    leaked
}

// We could return losses and metrics too here if needed
// dataset inputs contains all the features of all training samples concatenated
// dataset outputs contains all the expected outputs of all training samples concatenated
#[no_mangle]
extern "C" fn train_mlp_model(model: *mut MLP, dataset_inputs: *const f32, lines: i32, columns: i32,
                              dataset_outputs: *const f32, output_columns: i32, alpha: f32, nb_iter: i32,
                              is_classification: bool) {
    //TODO : training
}

#[no_mangle]
extern "C" fn predict_mlp_model(model: *mut MLP, sample_inputs: *const f32, columns: i32,
                                is_classification: bool) -> *mut f32 {
    //TODO : Predict
    let fake_output = vec![1.0f32];

    fake_output.leak().as_mut_ptr()
}

#[no_mangle]
extern "C" fn delete_mlp_model(model: *mut MLP) {
    unsafe {
        Box::from_raw(model);
    }
}

#[no_mangle]
extern "C" fn delete_float_array(arr: *mut f32, arr_len: i32) {
    unsafe {
        Vec::from_raw_parts(arr, arr_len as usize, arr_len as usize)
    };
}
