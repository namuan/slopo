class Greeter(private val prefix: String) {

    fun greet(name: String) = "$prefix, $name!"

    fun classify(n: Int): String = when {
        n < 0 -> "negative"
        n == 0 -> "zero"
        else -> "positive"
    }

    fun normalize(values: List<Double>): List<Double> {
        val total = values.sum()
        return values.map { it / total }
    }
}

fun List<Int>.sumEvens(): Int =
    filter { it % 2 == 0 }.sum()
