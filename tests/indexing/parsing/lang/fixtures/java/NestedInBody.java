public class NestedInBody {

    public Runnable makeTask(String label) {
        return new Runnable() {
            public void run() {
                System.out.println(label);
            }
        };
    }
}
