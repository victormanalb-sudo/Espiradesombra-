function encodeByte(byte, figureSeq, startNum=133n, startDen=100n) {
  const bits = byteToBits(byte);
  const n = figureSeq.length; // but we use 8 figures, cycling if needed
  const seq8 = [];
  for (let i = 0; i < 8; i++) seq8.push(BigInt(figureSeq[i % n]));
  
  // Compute suffix products Q_i = seq8[i] * seq8[i+1] * ... * seq8[7]
  const Q = new Array(9);
  Q[8] = 1n;
  for (let i = 7; i >= 0; i--) Q[i] = seq8[i] * Q[i+1];
  
  // num = startNum * Q[0] / startDen - sum d_i * Q[i+1]
  // To avoid fraction, multiply everything by startDen:
  // startDen * x = startNum * Q[0] / startDen ... hmm
  // Actually: x = startNum/startDen - sum d_i/P_i where P_i = seq8[0]*...*seq8[i]
  // P_i = Q[0]/Q[i+1]
  // So sum = sum d_i * Q[i+1] / Q[0]
  // x = startNum/startDen - (sum d_i * Q[i+1]) / Q[0]
  // = (startNum * Q[0] - startDen * sum) / (startDen * Q[0])
  
  let sum = 0n;
  for (let i = 0; i < 8; i++) sum += BigInt(bits[i] + 1) * Q[i+1];
  
  const num = startNum * Q[0] - startDen * sum;
  const den = startDen * Q[0];
  
  // simplify
  const g = gcd(num < 0n ? -num : num, den);
  return {
    bits,
    seq8: seq8.map(Number),
    Q: Q.map(v => v.toString()),
    sum: sum.toString(),
    num: (num / g).toString(),
    den: (den / g).toString(),
    value: Number(num) / Number(den)
  };
}