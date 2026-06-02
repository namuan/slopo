package example

// WithComments sums two numbers.
/* It also demonstrates a block comment. */
func WithComments(a, b int) int {
	// inline line comment
	sum := a + b /* trailing block comment */
	url := "http://not-a-comment"
	_ = url
	return sum
}
