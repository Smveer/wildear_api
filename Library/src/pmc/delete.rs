use super::structs::*;

#[no_mangle]
extern "C" fn delete_mlp_model(model: &mut PMC) {
    unsafe {
        let _ = Box::from_raw(model);
    }
    println!("Model deleted")
}