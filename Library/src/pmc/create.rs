use super::structs::*;
use rand::Rng;

#[no_mangle]
extern "C" fn create_mlp_model(arr: *mut i32, arr_len: i32) -> *mut MLP {
    // Convert arr to slice
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, arr_len as usize) };

    // Calc layer & neurons per layer
    let layers = arr_len as usize;
    let n_per_layer = arr_slice.iter().map(|&x| x as usize).collect::<Vec<usize>>();

    // Init W randomly
    let mut rng = rand::thread_rng();
    let mut weights = vec![];
    for i in 1..layers {
        let prev = n_per_layer[i - 1];
        let curr = n_per_layer[i];
        let layer_weights = vec![
            vec![rng.gen_range(-1.0..1.0); prev + 1]; curr
        ];
        weights.push(layer_weights);

    }

    let model = Box::new(MLP {
        nb_layer: layers,
        nb_neurons_per_layer: n_per_layer,
        weight: weights,
        activations: vec![vec![]; layers],
        deltas: vec![vec![]; layers],
    });

    let leaked = Box::leak(model);
    leaked
}

#[no_mangle]
extern "C" fn create_pmc(arr: *mut i32, len: i32) -> *mut PMC {
    // Get data
    let arr_slice = unsafe { std::slice::from_raw_parts(arr, len as usize) };

    let layers = len as usize;
    let neurons_per_layer = arr_slice.iter().map(|&x| x as usize).collect::<Vec<usize>>();

    // Init weights
    let mut rng = rand::thread_rng();
    let mut weights = vec![];
    for i in 1..layers {
        let prev = neurons_per_layer[i - 1];
        let curr = neurons_per_layer[i];
        let layer_weights = vec![
            vec![rng.gen_range(-1.0..1.0); prev + 1]; curr
        ];
        weights.push(layer_weights);
    }

    println!("PMC: Weights len : {}", weights.len());
    for j in 0..weights.len() {
        for x in 0..weights[j].len() {
            println!("Data[{}][{}]: {:?}", j, x, weights[j][x]);
        }
    }

    let model = Box::new(PMC {
        layer: layers,
        neurons_per_layer: vec![],
        weights: vec![],
        neuron_res: vec![],
        deltas: vec![],
    });

    let leaked = Box::leak(model);
    leaked
}