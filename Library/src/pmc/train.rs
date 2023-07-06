//use super::structs::*;

#[no_mangle]
extern "C" fn train_pmc_model(inputs_ptr: *const f32, inputs_length: i32, inputs_sub: i32){
    let inputs = recompose_vec_vec(inputs_ptr, inputs_length, inputs_sub);

    println!("PMC: recompose test : tab : {} | sub : {}", inputs_length, inputs_sub);
    for i in 0..inputs.len() {
        for j in 0..inputs[i].len() {
            println!("-- arr[{}][{}]: {}", i, j, inputs[i][j]);
        }
    }
}


fn recompose_vec_vec(inputs_ptr: *const f32, inputs_length: i32, inputs_sub: i32) -> Vec<Vec<f32>>{
    let i_length = inputs_length as usize;
    let sub_length = inputs_sub as usize;

    let flat_slice = unsafe { std::slice::from_raw_parts(inputs_ptr, i_length) };
    println!("recompose vec vec :");
    for i in 0..flat_slice.len() {
        println!("vec[{}]: {}", i, flat_slice[i]);
    }

    let mut inputs = Vec::new();
    let mut index = 0;

    while index < inputs_length as usize{
        let sub_slice = &flat_slice[index..index + sub_length];
        let sub_vec: Vec<f32> = sub_slice.to_vec();
        inputs.push(sub_vec);

        index += sub_length;
    }
    inputs
}