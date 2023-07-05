use super::structs::*;
use rand::Rng;

#[no_mangle]
extern "C" fn create_pmc_model(arr: *mut i32, len: i32) -> *mut PMC {
    let mut model = Box::new(PMC {
        layers :  0,
        neurons_per_layer : vec![],
        weights: vec![],
        neuron_data: vec![],
        deltas: vec![],
    });

    // Convert arr to slice
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, len as usize) };

    // Calc layer & neurons per layer
    model.layers = len as usize;
    model.neurons_per_layer = arr_slice.iter().map(|&x| x as usize).collect::<Vec<usize>>();

    // Init weights
    let mut rng = rand::thread_rng();
    for i in 1..model.layers {
        let prev = model.neurons_per_layer[i - 1];
        let curr = model.neurons_per_layer[i];
        let layer_weights = vec![
            vec![rng.gen_range(-1.0..1.0); prev + 1]; curr
        ];
        model.weights.push(layer_weights);
    }

    // Create shape of neuron_res & deltas
    model.neuron_data = vec![vec![0.0; model.neurons_per_layer.iter().max().unwrap_or(&0) + 1]; model.layers];
    model.deltas =  vec![vec![]; model.layers];

    // Init neuron_res : 1.0 / 0.0
    for l in 0..model.layers {
        for j in 0..=model.neurons_per_layer[l] {
            model.neuron_data[l][j] = if j == 0 { 1.0 } else { 0.0 };
        }
    }

    // Init deltas : 0.0
    for l in 0..model.layers {
        let layer_deltas = vec![0.0; model.neurons_per_layer[l] + 1];
        model.deltas[l] = layer_deltas;
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
    for j in 0..model.weights.len() {
        for x in 0..model.weights[j].len() {
            println!("-- Data[{}][{}]: {:?}", j, x, model.weights[j][x]);
        }
    }

    // Neurons res
    println!("PMC: Neuron res :");
    for i in 0..model.neuron_data.len(){
        for j in 0..model.neuron_data[i].len(){
            println!("-- neuronRes[{}][{}]: {:?}", i, j, model.neuron_data[j][i]);
        }
    }

    // Deltas
    println!("PMC: deltas :");
    for i in 0..model.deltas.len(){
        for j in 0..model.deltas[i].len(){
            println!("- deltas[{}][{}]: {:?}", i, j, model.deltas[i][j]);
        }
    }
}