use super::structs::*;

/* LinearRegressionModel delete function */
#[no_mangle]
extern "C" fn delete_linear_regression_model(
    model: *mut LinearRegressionModel
){
    unsafe { // object coming from outside needs to be unsafe to give ownership to rust (no copy)
        let ml = Box::from_raw(model);
        println!("LRM: Before delete: {} and {}", ml.coefficient, ml.constant);
    }
    println!("LRM: Deleted");
}
