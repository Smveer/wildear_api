use super::structs::*;

#[no_mangle]
extern "C" fn predict_linear_regression_model(model: *mut LinearRegressionModel, x: f64) -> f64 {
    let model = unsafe { &mut *model};
    model.coefficient * x + model.constant
}