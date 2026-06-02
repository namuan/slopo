public class Outer {

    public void outerMethod() {
        System.out.println("outer");
    }

    public class Inner {
        public void innerMethod() {
            System.out.println("inner");
        }
    }
}
