function encodeWithThales(bytes, figureSeq, startValue) {
  // figureSeq = [3,5,4,6,...]
  // startValue = 1.33
  const rationals = [];
  for (const byte of bytes) {
    const bits = byteToBits(byte);
    let num = 0n, den = 1n;
    let startNum = 133n, startDen = 100n; // 1.33
    // We work with remainder = startValue - sum
    let remNum = startNum, remDen = startDen;
    for (let i = 0; i < 8; i++) {
      const base = BigInt(figureSeq[i % figureSeq.length]);
      const d = BigInt(bits[i] + 1);
      // subtract d/(prod of bases up to i+1)
      // rem = rem - d / (b1*b2*...*b_{i+1})
      // easier: multiply through by den
      // We'll track x directly
      ...
    }
  }
}