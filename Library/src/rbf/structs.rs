#[repr(C)]
struct MyRBF {
    centers: Vec<Vec<f32>>,
    widths: Vec<f32>,
    weights: Vec<f32>,
}
