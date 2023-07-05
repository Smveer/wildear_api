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
    pub layers: usize,
    pub neurons_per_layer: Vec<usize>,
    pub weights: Vec<Vec<Vec<f32>>>,
    pub neuron_data: Vec<Vec<f32>>,
    pub deltas: Vec<Vec<f32>>
}