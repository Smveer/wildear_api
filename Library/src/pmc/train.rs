use rand::Rng;
use super::structs::*;
use super::tools::recompose_2d_vec;
use super::propagate::propagate;

#[no_mangle]
extern "C" fn train_pmc_model(model: &mut PMC,
                              inputs_ptr: *const f32, input_length: i32, inputs_sub: i32,
                              output_ptr: *const f32, output_length: i32, output_sub: i32,
                              learning_rate: f32, iteration: i32, is_classification: bool){
    println!("---------phase 2----------");
    // Recompose Vec<Vec<f32>>
    let inputs = recompose_2d_vec(inputs_ptr, input_length,
                                   inputs_sub);
    let outputs = recompose_2d_vec(output_ptr, output_length,
                                    output_sub);

    let mut rng = rand::thread_rng();

    for _ in 0..iteration as usize{
        // pick random data in the dataset
        let random = rng.gen_range(0..inputs.len());
        let random_input = inputs[random].clone();
        let random_output = outputs[random].clone();
        let input_slice = random_input.as_slice();

        // Set neurons inputs with the random dataset
        propagate(model, input_slice.as_ptr(), random_input.len() as i32,
                  is_classification);

       // Recursive calc of semi-gradients in the last layer
        for i in 1..=model.neurons_per_layer[model.layers] {
            model.deltas[model.layers][i] = model.neuron_data[model.layers][i] - random_output[i - 1];
            if is_classification {
                model.deltas[model.layers][i] *= 1.0 - model.neuron_data[model.layers][i].powi(2);
            }
        }
        // Recursive calc of semi-gradients in the rest
        for l in (1..=model.layers).rev() {
            for i in 1..=model.neurons_per_layer[l - 1] {
                let mut total = 0.0;
                for j in 1..=model.neurons_per_layer[l] {
                    total += model.weights[l][i][j] * model.deltas[l][j];
                }
                model.deltas[l - 1][i] = (1.0 - model.neuron_data[l - 1][i].powf(2.0)) * total;
            }
        }

        // Update Weights
        for l in 1..model.layers {
            for i in 0..=model.neurons_per_layer[l - 1] {
                for j in  1..=model.neurons_per_layer[l] {
                    model.weights[l][i][j] -= learning_rate * model.neuron_data[l - 1][i] * model.deltas[l][j];
                }
            }
        }
    }
    print_created_model(model);
}

fn print_created_model(model : &PMC) {
    // Layers & neurons per layer
    println!("PMC : layers : {}", model.layers);
    println!("PMC : n per layer len : {}", model.neurons_per_layer.len());
    for i in 0..model.neurons_per_layer.len() {
        println!("PMC : layer[{}] : {}", i, model.neurons_per_layer[i]);
    }

    // Weights
    println!("PMC: Weights len : {}", model.weights.len());
    for i in 0..model.weights.len() {
        for j in 0..model.weights[i].len() {
            for x in 0..model.weights[i][j].len() {
                println!("-- weights[{}][{}][{}]: {}", i, j,x,  model.weights[i][j][x]);
            }
        }
    }

    // Neurons res
    println!("PMC: Neuron res :");
    for i in 0..model.neuron_data.len(){
        for j in 0..model.neuron_data[i].len(){
            println!("-- neuronRes[{}][{}]: {}", i, j, model.neuron_data[i][j]);
        }
    }

    // Deltas
    println!("PMC: deltas :");
    for i in 0..model.deltas.len(){
        for j in 0..model.deltas[i].len(){
            println!("- deltas[{}][{}]: {}", i, j, model.deltas[i][j]);
        }
    }
}