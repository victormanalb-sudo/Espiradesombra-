function bitsToBytes(bits) {
  const out = new Uint8Array(Math.ceil(bits.length / 8));  // ← Uint8Array
  for (let i = 0; i < bits.length; i += 8) {
    let b = 0;
    for (let j = 0; j < 8; j++) b = (b << 1) | (bits[i+j] || 0);
    out[i/8] = b;
  }
  return out;
}