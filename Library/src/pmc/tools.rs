use super::structs::*;
use serde_json;
use std::ffi::{c_char, CStr, CString};
use std::ptr::null_mut;
use serde_json::from_str;

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

#[no_mangle]
extern "C" fn export_pmc(model: &PMC) -> *mut c_char{
    let json_string = serde_json::to_string(model).unwrap();
    let c_string = CString::new(json_string).expect("Failed to create CString");
    c_string.into_raw()
}

#[no_mangle]
extern "C" fn free_string(ptr: *mut c_char) {
    unsafe {
        if !ptr.is_null() {
            let _ = CString::from_raw(ptr);
        }
    }
}

#[no_mangle]
extern "C" fn load_pmc_json(json_data: *const c_char, model_ptr : Option<&mut PMC>) -> *mut PMC{
    let c_str = unsafe { CStr::from_ptr(json_data) };
    let str_slice = c_str.to_str().expect("Failed to convert C string to Rust str");

    // Upload data into existing model
    if let Some(model) = model_ptr {
        match from_str::<PMC>(str_slice) {
            Ok(pmc) => {
                model.layers = pmc.layers;
                model.neurons_per_layer = pmc.neurons_per_layer.clone();
                model.weights = pmc.weights.clone();
                model.neuron_data = pmc.neuron_data.clone();
                model.deltas = pmc.deltas.clone();
            }
            Err(e) => {
                eprintln!("Error loading PMC from JSON: {}", e);
            }
        }
        model as *mut PMC
    } else {
        // Upload data into new PMC
        let pmc: PMC = match from_str(str_slice) {
            Ok(pmc) => pmc,
            Err(e) => {
                eprintln!("Error loading PMC from JSON: {}", e);
                return null_mut();
            }
        };
        let leaked = Box::into_raw(Box::new(pmc));
        leaked
    }
}