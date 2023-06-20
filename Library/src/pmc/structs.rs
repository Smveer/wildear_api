#[repr(C)]
pub struct MLP {
    pub nb_layer: usize,
    pub nb_neurons_per_layer: Vec<usize>,
    pub weight: Vec<Vec<Vec<f32>>>,
    pub x: Vec<Vec<f32>>,
    pub deltas: Vec<Vec<f32>>,
}