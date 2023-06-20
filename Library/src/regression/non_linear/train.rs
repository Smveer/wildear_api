use super::structs::*;

#[no_mangle]
extern "C" fn train_polynomial_regression_model(
    model: *mut PolynomialRegressionModel,
    x: *const f64,
    x_len: usize,
    y: *const f64,
    y_len: usize,
){
    unsafe {
        // Convert pointers to slices
        let mut ml = Box::from_raw(model);
        let x_slice = std::slice::from_raw_parts(x, x_len);
        let y_slice = std::slice::from_raw_parts(y, y_len);

        println!("NLRM: Before train: {}", ml.degree);

        // Convert slices to vec
        let matrix_x = x_slice.to_vec();
        let matrix_y = y_slice.to_vec();

        let n = matrix_x.len();
        let m = ml.degree + 1;

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
        ml.coefficients = vec![0.0; m];
        for j in 0..m {
            for k in 0..m {
                ml.coefficients[j] += inverse_x_tx[j][k] * x_ty[k];
            }
        }

        println!("NLRM: Trained: {}", ml.degree);
        Box::into_raw(ml);
    }
}