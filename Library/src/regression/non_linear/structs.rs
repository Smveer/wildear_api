#[repr(C)] // struct in c99 format
pub struct PolynomialRegressionModel {
    pub coefficients: Vec<f64>,
    pub degree: usize,
}

pub fn invert_matrix(matrix: &Vec<Vec<f64>>) -> Option<Vec<Vec<f64>>> {
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
