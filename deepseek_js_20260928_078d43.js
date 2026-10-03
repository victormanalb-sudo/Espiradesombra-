const N = 59n ** BigInt(k);
const sqrtN = bigintSqrt(N);
const entries = Number(sqrtN) - 1;
for (let i = 2; i <= Number(sqrtN); i++) {
  const r = Number(N % BigInt(i));
  // ...
}