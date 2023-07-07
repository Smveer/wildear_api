use super::structs::*;
use rand::Rng;

#[no_mangle]
extern "C" fn create_pmc_model(arr: *mut i32, len: i32) -> *mut PMC {
    let mut model = Box::new(PMC {
        layers :  0, // L
        neurons_per_layer : vec![], // d
        weights: vec![], // W
        neuron_data: vec![], // X
        deltas: vec![],
    });

    // Convert arr to slice
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, len as usize) };

    // Calc layer & neurons per layer
    model.layers = (len - 1) as usize;
    model.neurons_per_layer = arr_slice.iter().map(|&x| x as usize).collect::<Vec<usize>>();

    // Init weights
    let mut rng = rand::thread_rng();
    for l in 1..=model.layers {
        let mut layer_weights = Vec::new();

        for _ in 0..=model.neurons_per_layer[l - 1]{
            let mut neuron_weights = Vec::new();

            for j in 0..=model.neurons_per_layer[l]{
                let weight = if j == 0 { 0.0 } else { rng.gen_range(-1.0..1.0) };
                neuron_weights.push(weight);
            }
            layer_weights.push(neuron_weights);
        }
        model.weights.push(layer_weights);
    }

    // Init neuron_data : 1.0 / 0.0
    for l in 0..=model.layers {
        let mut layer = Vec::new();
        for i in 0..=model.neurons_per_layer[l] {
            let value = if i == 0 { 1.0 } else { 0.0 };
            layer.push(value);
        }
        model.neuron_data.push(layer);
    }

    // Init deltas : 0.0
    for l in 0..=model.layers {
        //let layer_deltas = vec![0.0; model.neurons_per_layer[l] + 1];
        let mut layer_deltas = Vec::new();
        for _ in 0..=model.neurons_per_layer[l]{
            layer_deltas.push(0.0);
        }
        model.deltas.push(layer_deltas);
    }

    print_created_model(&model);

    let leaked = Box::leak(model);
    leaked
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
    println!("PMC: Neuron data :");
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