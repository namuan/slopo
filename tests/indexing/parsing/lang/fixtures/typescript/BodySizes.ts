const square = (n: number): number => n * n;

const noop = (): void => {};

function buildConfig(env: string): Config {
  const base: Config = { env, retries: 3, timeout: 30 };
  const overrides = env === "prod" ? { retries: 5 } : {};
  const merged = { ...base, ...overrides };
  if (merged.timeout < 0) {
    throw new Error("invalid timeout");
  }
  return merged;
}
