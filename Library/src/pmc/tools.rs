pub fn recompose_2d_vec(ptr: *const f32, array_length: i32, sub_array: i32) -> Vec<Vec<f32>>{
    let columns = array_length as usize;
    let lines = sub_array as usize;

    let flat_slice = unsafe { std::slice::from_raw_parts(ptr, columns) };

    let mut array = Vec::new();
    let mut index = 0;

    while index < array_length as usize{
        let sub_slice = &flat_slice[index..index + lines];
        let sub_vec: Vec<f32> = sub_slice.to_vec();
        array.push(sub_vec);

        index += lines;
    }
    array
}