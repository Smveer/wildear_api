use super::structs::*;

pub fn propagate(model:  &mut PMC, arr: *const f32, arr_len: i32, is_classification: bool){
    // Convert arr to slice
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, arr_len as usize) };

    // Set input in neuron res
    for i in 0..model.neurons_per_layer[0]{
        model.neuron_res[0][i + 1] = arr_slice[i];
    }

    // recursive update
    for i in 1..model.layers + 1 {
        for j in 1..model.neurons_per_layer[i] + 1 {
            let mut total = 0.0;
            for x in 0..model.neurons_per_layer[i - 1] + 1 {
                total += model.weights[i][j][x] * model.neuron_res[i - 1][x]
            }

            if i < model.layers || is_classification {
                total = total.tanh();
            }

            model.neuron_res[i][j] = total;
        }
    }
}
