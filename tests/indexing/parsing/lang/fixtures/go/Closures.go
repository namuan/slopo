package example

type Worker struct {
	onComplete func()
}

func Transform(nums []int) []int {
	doubler := func(x int) int { return x * 2 }

	w := Worker{}
	w.onComplete = func() {
		println("done")
	}

	register(func(v int) int {
		scaled := doubler(v)
		return scaled + 1
	})

	result := make([]int, 0, len(nums))
	for _, n := range nums {
		result = append(result, doubler(n))
	}
	return result
}
