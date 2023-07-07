use rand::Rng;
use super::structs::*;
use super::tools::recompose_2d_vec;
use super::propagate::propagate;

#[no_mangle]
extern "C" fn train_pmc_model(model: &mut PMC, inputs_ptr: *const f32, input_length: i32, inputs_sub: i32,
                              output_ptr: *const f32, output_length: i32, alpha: f32, iteration: i32,
                              is_classification: bool){
    // Recompose Vec<Vec<f32>>
    let inputs = recompose_2d_vec(inputs_ptr, input_length,
                                   inputs_sub);
    let outputs = recompose_2d_vec(output_ptr, output_length,
                                    inputs_sub);

    let mut rng = rand::thread_rng();

    for _ in 0..iteration as usize{
        // pick random data in the dataset
        let random = rng.gen_range(0..inputs.len());
        let random_input = &inputs[random];
        let random_output = &outputs[random];

        // Set neurons inputs with the random dataset
        propagate(model, random_input.as_ptr(), random_input.len() as i32,
                  is_classification);
        println!("---------phase 2----------");
        print_created_model(model);
    }


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