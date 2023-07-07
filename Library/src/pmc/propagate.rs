use super::structs::*;

pub fn propagate(model: &mut PMC, inputs: *const f32, inputs_len: i32, is_classification: bool){
    // Convert arr to slice
    let inputs_slice = unsafe { std::slice::from_raw_parts(inputs, inputs_len as usize) };

    // Set input in neuron res
    for i in 0..model.neurons_per_layer[0]{
        model.neuron_data[0][i + 1] = inputs_slice[i];
    }

    // recursive update
    for l in 1..=model.layers{
        for j in 1..=model.neurons_per_layer[l]{
            let mut total = 0.0;
            for i in 0..model.neurons_per_layer[l - 1]{
                total += model.weights[l][i][j] * model.neuron_data[l - 1][i];
            }

            if l < model.layers || is_classification {
                total = total.tanh();
            }
            model.neuron_data[l][j] = total;
        }
    }
}
