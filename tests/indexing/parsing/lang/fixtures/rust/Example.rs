pub struct Greeter {
    prefix: String,
}

impl Greeter {
    pub fn greet(&self, name: &str) -> String {
        format!("{}, {}!", self.prefix, name)
    }

    pub fn classify(n: i32) -> &'static str {
        match n {
            i32::MIN..=-1 => "negative",
            0 => "zero",
            _ => "positive",
        }
    }
}

pub fn normalize(values: &[f64]) -> Vec<f64> {
    let total: f64 = values.iter().sum();
    values.iter().map(|v| v / total).collect()
}

pub fn sum_evens(numbers: &[i32]) -> i32 {
    numbers.iter().filter(|n| *n % 2 == 0).sum()
}
