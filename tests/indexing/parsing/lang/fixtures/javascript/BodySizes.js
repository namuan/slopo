const square = (n) => n * n;

function noop() {}

async function loadAll(ids, limit) {
  const results = [];
  for (const id of ids) {
    if (results.length >= limit) {
      break;
    }
    const item = await fetch(`/items/${id}`);
    results.push(await item.json());
  }
  return results;
}
