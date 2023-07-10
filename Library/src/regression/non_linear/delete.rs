use super::structs::*;

#[no_mangle]
extern "C" fn delete_polynomial_regression_model(
    model: *mut PolynomialRegressionModel
){
    unsafe {
        let ml = Box::from_raw(model);
        println!("NLRM: Before delete: {}", ml.degree);
    }
    println!("NLRM: Deleted");
}
