export function add(a, b) {
  return a + b;
}

const greet = (name) => {
  return `Hello, ${name}!`;
};

async function fetchUser(id) {
  const response = await fetch(`/users/${id}`);
  return response.json();
}

const handlers = {
  reset() {
    this.value = 0;
  },
};

class Counter {
  constructor(start) {
    this.value = start;
  }

  increment(step) {
    this.value += step;
    return this.value;
  }
}
