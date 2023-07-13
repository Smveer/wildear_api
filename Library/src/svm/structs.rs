use ndarray::{Array1, Array2};


#[repr(C)]
struct SVM {
    alpha: Array1<i32>,                      // Field to store alpha values of support vectors
    bias: i32,                               // Field to store the bias term
    support_vectors: Array2<i32>,            // Field to store the support vectors
    labels: Array1<i32>,                     // Field to store the labels of support vectors
}