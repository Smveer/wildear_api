use super::structs::*;

/* PolynomialRegressionModel init function */
#[no_mangle]
extern "C" fn create_polynomial_regression_model() -> *mut PolynomialRegressionModel{
    Box::leak(
        Box::new(
            PolynomialRegressionModel {
                coefficients: vec![0.0; 3],
                degree: 2
            }
        )
    )
}
