struct Worker {
    on_complete: Box<dyn Fn()>,
}

pub fn run(values: &[i32]) -> Vec<i32> {
    let doubler = |x: i32| x * 2;

    let mut worker = Worker {
        on_complete: Box::new(|| {}),
    };
    worker.on_complete = || {
        println!("done");
    };

    values
        .iter()
        .map(|v| {
            let scaled = doubler(*v);
            scaled + 1
        })
        .collect()
}
