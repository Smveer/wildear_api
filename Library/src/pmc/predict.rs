use super::structs::*;

#[no_mangle]
extern "C" fn predict_mlp_model(model: *mut MLP, sample_inputs: *const f32, columns: i32,
                                is_classification: bool) -> *mut f32 {
    // Create local variable for all values
    let slice = unsafe { std::slice::from_raw_parts(sample_inputs, columns as usize) };
    let model = unsafe { &mut *model };

    for layer in 0..model.nb_layer{
        let mut layer_activations = vec![];

        for neuron in 0..model.nb_neurons_per_layer[layer]{
            // Bias
            let mut weight_sum = model.weight[layer][neuron][0];

            for prev_neuron in 1..model.nb_neurons_per_layer[layer - 1] + 1 {
                weight_sum += model.weight[layer][neuron][prev_neuron] * slice[prev_neuron - 1];
            }

            let activation = 1.0 / (1.0 + (-weight_sum).exp());

            layer_activations.push(activation);
        }
        model.activations[layer] = layer_activations;
    }

    let output_layer = model.nb_layer - 1;
    let last_layer_activations = &model.activations[output_layer];
    let prediction = if is_classification {
        if last_layer_activations[0] >= 0.5 {
            1.0
        } else {
            0.0
        }
    } else {
        last_layer_activations[0]
    };
    Ò
    Box::leak(Box::new(prediction))
}