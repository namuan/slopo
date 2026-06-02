class Repository<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }
}
