package example

func OuterFunction(x int) int {
	increment := func(n int) int {
		return n + 1
	}
	return increment(x)
}
