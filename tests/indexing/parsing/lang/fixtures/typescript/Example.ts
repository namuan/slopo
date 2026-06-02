function add(a: number, b: number): number {
  return a + b;
}

const greet = (name: string): string => {
  return `Hello, ${name}!`;
};

async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/users/${id}`);
  return response.json();
}

interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private readonly radius: number) {}

  area(): number {
    return Math.PI * this.radius ** 2;
  }
}
