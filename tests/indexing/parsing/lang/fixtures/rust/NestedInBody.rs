pub fn outer_function(values: &[i32]) -> i32 {
    fn increment(n: i32) -> i32 {
        n + 1
    }

    values.iter().map(|v| increment(*v)).sum()
}
