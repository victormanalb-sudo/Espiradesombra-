function precompute(g, p, maxK) {
  const N = Math.min(maxK, /* period */);
  const table = new Uint32Array(N);
  let cur = 1 % p;  // g^0 = 1
  for (let k = 0; k < N; k++) {
    table[k] = cur;
    cur = (cur * g) % p;
  }
  return table;
}