class Outer {

    fun outerMethod() = println("outer")

    companion object {
        fun innerMethod() = println("inner")
    }
}
