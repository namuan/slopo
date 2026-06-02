public abstract class BodySizes {

    public abstract int abstractMethod(int a);

    public void emptyBody() {}

    @Deprecated
    @SuppressWarnings("unchecked")
    public <T> List<T> annotatedWithLogic(List<T> items, int limit) {
        List<T> result = new ArrayList<>();
        for (T item : items) {
            if (result.size() >= limit) {
                break;
            }
            result.add(item);
        }
        return result;
    }
}
