function encodeWithThalesDeduction(bytes, figureSeq, startValue) {
  const startNum = 133n, startDen = 100n; // 1.33
  const results = [];
  
  for (const byte of bytes) {
    const bits = byteToBits(byte);
    let S_num = startNum, S_den = startDen;
    let P_num = 1n, P_den = 1n; // product of figures
    const steps = [];
    
    for (let i = 0; i < 8; i++) {
      const f = BigInt(figureSeq[i % figureSeq.length]);
      P_num *= f; // P_i = product of f_0..f_i
      const d = BigInt(bits[i] + 1);
      
      // piece = d / P_num
      // S_new = S_old - d/P_num = (S_num * P_num - d * S_den) / (S_den * P_num)
      const newNum = S_num * P_num - d * S_den;
      const newDen = S_den * P_num;
      
      // simplify
      const g = gcd(newNum < 0n ? -newNum : newNum, newDen);
      S_num = newNum / g;
      S_den = newDen / g;
      
      steps.push({
        figure: Number(f),
        d: Number(d),
        bit: bits[i],
        segment: { num: S_num, den: S_den }
      });
    }
    results.push({ byte, bits, steps, finalSegment: { num: S_num, den: S_den } });
  }
  return results;
}