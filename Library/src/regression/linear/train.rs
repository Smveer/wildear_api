use super::structs::*;
use std::slice;

/* LinearRegressionModel train function */
#[no_mangle]
extern "C" fn train_linear_regression_model(
    model: *mut LinearRegressionModel,
    dataset_input: *const f64,
    predict_output: *const f64,
    len: usize
){
    unsafe { // object coming from outside needs to be unsafe to give ownership to rust (no copy)
        let mut ml = Box::from_raw(model);
        let input_slice = slice::from_raw_parts(dataset_input,len);
        let output_slice = slice::from_raw_parts(predict_output, len);

        println!("LRM: Before train: {} and {}", ml.coefficient, ml.constant);

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
        ml.coefficient = sum_gap / sum_squared;
        ml.constant = mean_output - ml.coefficient * mean_input;
        println!("LRM: Trained: {} and {}", ml.coefficient, ml.constant);
        Box::into_raw(ml);
    }
}
