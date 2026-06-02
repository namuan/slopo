public class Comments {

    /**
     * Documentation
     */
    public int withComments(int a, int b) {
        // a leading line comment
        int sum = a + b; // a trailing line comment
        /* a block comment
           spanning lines */
        String url = "http://not-a-comment";
        return sum;
    }
}
