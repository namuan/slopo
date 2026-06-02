package example

import "strings"

type Greeter struct {
	prefix string
}

func (g Greeter) Greet(name string) string {
	return g.prefix + ", " + name + "!"
}

func Classify(n int) string {
	switch {
	case n < 0:
		return "negative"
	case n == 0:
		return "zero"
	default:
		return "positive"
	}
}

func Normalize(s string) string {
	return strings.ToLower(strings.TrimSpace(s))
}

func SumEvens(nums []int) int {
	total := 0
	for _, n := range nums {
		if n%2 == 0 {
			total += n
		}
	}
	return total
}
