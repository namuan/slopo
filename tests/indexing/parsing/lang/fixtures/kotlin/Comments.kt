class Comments {

    /**
     * Documentation
     */
    fun withComments(a: Int, b: Int): Int {
        // a leading line comment
        val sum = a + b // a trailing line comment
        /* a block comment
           spanning lines */
        val url = "http://not-a-comment"
        return sum
    }
}
