/// Adds two numbers together.
/** Block doc comment describing the function. */
pub fn with_comments(a: i32, b: i32) -> i32 {
    // line comment
    let sum = a + b; /* trailing block comment */
    let url = "http://not-a-comment";
    let _ = url;
    sum
}
