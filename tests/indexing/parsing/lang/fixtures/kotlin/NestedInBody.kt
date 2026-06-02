fun outerFunction(items: List<Int>): List<Int> {
    fun localFunction(x: Int): Int {
        return x + 1
    }
    return items.map { localFunction(it) }
}
