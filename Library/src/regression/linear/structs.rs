/* ax + b = y => a = coefficient, b = constant*/
#[repr(C)] // structs in c99 format
pub struct LinearRegressionModel  {
    pub coefficient: f64, // a
    pub constant: f64, // b
}
