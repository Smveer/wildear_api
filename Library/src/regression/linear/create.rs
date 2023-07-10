use super::structs::*;

/* LinearRegressionModel init function */
#[no_mangle] // Helps to not let modify name of functions while usage
extern "C" fn create_linear_regression_model() -> *mut LinearRegressionModel {
    Box::leak(// Leak "model" memory out of the Box
        Box::new( // Box helps to alloc memory for the model
            LinearRegressionModel {
                coefficient: 3.0,
                constant: 2.0
            }
        )
    )
}
