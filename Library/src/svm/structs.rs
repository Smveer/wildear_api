#[repr(C)]
pub struct SVM {
    alpha: *mut i32,
    bias: i32,
    support_vectors: *mut i32,
    labels: *mut i32,
}
