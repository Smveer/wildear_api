#[repr(C)]
pub struct MLP {
    pub nb_layer: usize,
    pub nb_neurons_per_layer: Vec<usize>,
    pub weight: Vec<Vec<Vec<f32>>>,
    pub activations: Vec<Vec<f32>>,
    pub deltas: Vec<Vec<f32>>,
}

#[repr(C)]
pub struct PMC {
    pub neurons_per_layer: Vec<usize>,
    pub layer: usize,
    pub weights: Vec<f32>,
    pub neuron_res: Vec<Vec<f32>>,
    pub deltas: Vec<Vec<f32>>
}