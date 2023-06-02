use std::slice;
use std::vec::Vec;

#[no_mangle]
extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[no_mangle]
extern "C" fn sum(arr: *const i32, nb_elems: i32) -> i32 {
    let safe_arr =
        unsafe {
            std::slice::from_raw_parts(arr, nb_elems as usize)
        };

    safe_arr.iter().sum()
}


#[no_mangle]
extern "C" fn count_to_n(n: i32) -> *mut i32 {
    let v: Vec<i32> = (0..n).collect();

    let arr_slice = v.leak();

    arr_slice.as_mut_ptr()
}

#[no_mangle]
extern "C" fn delete_int_array(arr: *mut i32, arr_len: i32) {
    unsafe {
        Vec::from_raw_parts(arr, arr_len as usize, arr_len as usize)
    };
}

fn invert_matrix(matrix: &Vec<Vec<f64>>) -> Option<Vec<Vec<f64>>> {
    let n = matrix.len();
    let m = matrix[0].len();

    let mut augmented_matrix: Vec<Vec<f64>> = matrix.clone();
    let mut inverse_matrix: Vec<Vec<f64>> = vec![vec![0.0; m]; n];

    // Création de la matrice identité de même taille
    for i in 0..n {
        inverse_matrix[i][i] = 1.0;
        augmented_matrix[i].extend_from_slice(&inverse_matrix[i]);
    }

    // Algorithme d'élimination de Gauss-Jordan
    for i in 0..n {
        if augmented_matrix[i][i] == 0.0 {
            return None; // La matrice est singulière, l'inverse n'existe pas
        }

        let pivot = augmented_matrix[i][i];

        // Division de la ligne i par le pivot
        for j in 0..2 * m {
            augmented_matrix[i][j] /= pivot;
        }

        // Soustraction des multiples de la ligne i des autres lignes
        for k in 0..n {
            if k != i {
                let factor = augmented_matrix[k][i];
                for j in 0..2 * m {
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j];
                }
            }
        }
    }

    // Extraction de la matrice inverse
    let mut inverse_matrix: Vec<Vec<f64>> = vec![vec![0.0; m]; n];
    for i in 0..n {
        inverse_matrix[i] = augmented_matrix[i][m..].to_vec();
    }

    Some(inverse_matrix)
}


#[repr(C)]
pub struct PolynomialRegressionModel {
    coefficients: Vec<f64>,
    degree: usize,
}

#[repr(C)]
pub struct LinearRegressionModel  {
    coefficient: f64,
    constant: f64,
}

#[no_mangle]
extern "C" fn create_linear_regression_model() -> *mut LinearRegressionModel{

    let model= Box::new(LinearRegressionModel {
        coefficient: 0.0,
        constant: 0.0,
    });

    let leaked = Box::leak(model);
    leaked
}

#[no_mangle]
extern "C" fn create_polynomial_regression_model() -> *mut PolynomialRegressionModel{

    let model = Box::new(PolynomialRegressionModel {
        coefficients: vec![0.0; 3],
        degree: 2,
    });

    let leaked = Box::leak(model);
    leaked
}

#[no_mangle]
extern "C" fn delete_linear_regression_model(model: *mut LinearRegressionModel) {
    unsafe {
        let _ = Box::from_raw(model);
    }
}

#[no_mangle]
extern "C" fn delete_polynomial_regression_model(model: *mut PolynomialRegressionModel) {
    unsafe {
        let _ = Box::from_raw(model);
    }
}

#[no_mangle]
extern "C" fn train_linear_regression_model(
    model: *mut LinearRegressionModel,
    dataset_input: *const f64,
    predict_output: *const f64,
    len: usize
){
    // ------------ Methode of Ordinary Least Squares : exact answer ------------

    // Create local variable to use in RUST from Python
    let mut model = unsafe { &mut *model };
    let input_slice = unsafe { slice::from_raw_parts(dataset_input,len) };
    let output_slice = unsafe{ slice::from_raw_parts(predict_output, len) };

    // Calc of means
    let mean_input = input_slice.iter().sum::<f64>() / len as f64;
    let mean_output = output_slice.iter().sum::<f64>() / len as f64;

    // Calc of gap
    let mut sum_gap= 0.0;
    let mut sum_squared= 0.0;

    for i in 0..len {
        let deviation_x = input_slice[i] - mean_input;
        let deviation_y = output_slice[i] - mean_output;
        sum_gap += deviation_x * deviation_y;
        sum_squared += deviation_x * deviation_x;
    }

    // Set coefficient & constant of the model
    model.coefficient = sum_gap / sum_squared;
    model.constant = mean_output - model.coefficient * mean_input;


    // ------------ Methode of Stochastic Gradient Descent : approximate answer (good for lot of data) ------------
    // Get the function cost
    // Function Cost : 1/2m x somme(i to m) x (F - Y)
    // Calc the gradient a & b
}

#[no_mangle]
extern "C" fn train_polynomial_regression_model(
    model: *mut PolynomialRegressionModel,
    x: *const f64,
    x_len: usize,
    y: *const f64,
    y_len: usize,
){
    // Convert pointers to slices
    let mut model = unsafe { &mut *model };
    let x_slice = unsafe { std::slice::from_raw_parts(x, x_len) };
    let y_slice = unsafe { std::slice::from_raw_parts(y, y_len) };

    // Convert slices to vec
    let matrix_x = x_slice.to_vec();
    let matrix_y = y_slice.to_vec();

    let n = matrix_x.len();
    let m = model.degree + 1;

    // Creation de la matrice de conception
    let mut matrix_design = vec![vec![0.0; m]; n];
    for (i, &x) in matrix_x.iter().enumerate() {
        for j in 0..m {
            matrix_design[i][j] = x.powf(j as f64);
        }
    }

    // Partie 4: Entraînement du modèle
    let mut x_tx: Vec<Vec<f64>> = vec![vec![0.0; m]; m];
    let mut x_ty: Vec<f64> = vec![0.0; m];
    for (i, row) in matrix_design.iter().enumerate() {
        for j in 0..m {
            for k in 0..m {
                x_tx[j][k] += row[j] * matrix_design[i][k];
            }
            x_ty[j] += row[j] * matrix_y[i];
        }
    }

    // Inversion de la matrice x_tx
    let inverse_x_tx = invert_matrix(&x_tx).expect("Singular matrix");

    // Adjust coefficients
    model.coefficients = vec![0.0; m];
    for j in 0..m {
        for k in 0..m {
            model.coefficients[j] += inverse_x_tx[j][k] * x_ty[k];
        }
    }
}

#[no_mangle]
extern "C" fn predict_linear_regression_model(model: *mut LinearRegressionModel, x: f64) -> f64 {
    let model = unsafe { &mut *model};
    model.coefficient * x + model.constant
}

#[no_mangle]
extern "C" fn predict_polynomial_regression_model(model: *mut PolynomialRegressionModel, x: f64) -> f64 {
    let model = unsafe { &mut *model};

    let mut val = 0.0;
    for (j, &coeff) in model.coefficients.iter().enumerate() {
        val += coeff * x.powf(j as f64);
    }
    val
}

/*
    Multilayer perceptron
*/

//Structure MLP
struct MLP {
    nb_layer: usize, // Nombre de couches (ou layers) du modèle MLP
    nb_neurons_per_layer: Vec<usize>, // Nombre de neurones par couche du modèle MLP
    W: Vec<Vec<Vec<f32>>>,  // Matrices de poids du modèle MLP
    X: Vec<Vec<f32>>,
    deltas: Vec<Vec<f32>>, // Vecteurs de biais du modèle MLP
}


#[no_mangle]
extern "C" fn create_mlp_model(arr: *mut i32, arr_len: i32) -> *mut MLP {

    //Convertir le pointeur brut en slice pour accéder aux données
     let neurons_per_layer = unsafe {
        slice::from_raw_parts(arr, arr_len as usize)
    };

     // Créer une instance de la structure MLP
    let model = Box::new(MLP {
        // Le nombre de couches est déterminé par la longueur de la liste `neurons_per_layer`
        nb_layer: neurons_per_layer.len(),
        // Copier les valeurs de `neurons_per_layer` dans un nouveau vecteur
        nb_neurons_per_layer: neurons_per_layer.to_vec(),
        // Initialiser les matrices de poids et les vecteurs d'entrées et de deltas comme vides
        W: Vec::new(),
        X: Vec::new(),
        deltas: Vec::new(),
    });


    // Initialisation du modèle MLP
    let mut rng = rand::thread_rng(); // Créer un générateur de nombres aléatoires

    // Parcourir chaque couche du modèle
    for layer in 0..neurons_per_layer.len() {
        let num_neurons_curr_layer = neurons_per_layer[layer];
        let num_neurons_prev_layer = if layer > 0 { neurons_per_layer[layer - 1] } else { 0 };

        // Initialisation des poids de la couche
        let mut layer_weights = Vec::new();

        // Pour chaque neurone de la couche actuelle
        for _ in 0..num_neurons_curr_layer {
            let mut neuron_weights = Vec::new();

            // Initialisation des poids des connexions avec la couche précédente
            for _ in 0..=num_neurons_prev_layer {
                let weight = rng.gen::<f32>(); // Générer un poids aléatoire entre 0 et 1
                neuron_weights.push(weight);
            }

            layer_weights.push(neuron_weights);
        }

        // Ajouter les poids de la couche au modèle MLP
        model.W.push(layer_weights);

        // Initialisation des deltas de la couche
        let mut layer_deltas = Vec::new();
        // Pour chaque neurone de la couche
        for _ in 0..num_neurons_curr_layer {
            layer_deltas.push(0.0); // Initialiser les deltas à zéro
        }
        // Ajouter les deltas de la couche au modèle MLP
        model.deltas.push(layer_deltas);
    }

    // Convertir la boîte `model` en pointeur brut
    let leaked = Box::leak(model);
    leaked
}

// We could return losses and metrics too here if needed
// dataset inputs contains all the features of all training samples concatenated
// dataset outputs contains all the expected outputs of all training samples concatenated
#[no_mangle]
extern "C" fn train_mlp_model(model: *mut MLP, dataset_inputs: *const f32, lines: i32, columns: i32,
                              dataset_outputs: *const f32, output_columns: i32, alpha: f32, nb_iter: i32,
                              is_classification: bool) {
    //TODO : training
}

#[no_mangle]
extern "C" fn predict_mlp_model(model: *mut MLP, sample_inputs: *const f32, columns: i32,
                                is_classification: bool) -> *mut f32 {
    //TODO : Predict
    let fake_output = vec![1.0f32];

    fake_output.leak().as_mut_ptr()
}

#[no_mangle]
extern "C" fn delete_mlp_model(model: *mut MLP) {
    unsafe {
        let _ = Box::from_raw(model);
    }
}

#[no_mangle]
extern "C" fn delete_float_array(arr: *mut f32, arr_len: i32) {
    unsafe {
        Vec::from_raw_parts(arr, arr_len as usize, arr_len as usize)
    };
}
