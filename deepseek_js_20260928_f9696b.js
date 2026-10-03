async function precomputarK(k, entryCap) {
  let N, N_is_number;
  if (k <= 9) {
    N = Math.pow(59, k);
    N_is_number = true;
  } else {
    N = 59n ** BigInt(k);
    N_is_number = false;
  }
  
  const sqrtN = N_is_number ? Math.floor(Math.sqrt(N)) : Number(bigintSqrt(N));
  const entries = Math.min(sqrtN - 1, entryCap);
  
  const seq_r = new Uint32Array(entries);
  let zeros = [];
  let minR = Infinity, maxR = 0;
  
  const t0 = performance.now();
  for (let idx = 0; idx < entries; idx++) {
    const i = idx + 2;
    let r;
    if (N_is_number) {
      r = N % i;
    } else {
      r = Number(N % BigInt(i));
    }
    seq_r[idx] = r;
    if (r === 0) zeros.push(i);
    if (r < minR) minR = r;
    if (r > maxR) maxR = r;
    
    if (idx % 100000 === 0) await new Promise(res => setTimeout(res, 0));
  }
  
  const t1 = performance.now();
  return { k, N, sqrtN, entries, seq_r, zeros, minR, maxR, time: (t1-t0)/1000 };
}