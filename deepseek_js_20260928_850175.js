const aesPacket = new Uint8Array(bitsToBytes(res.bits));  // ← conversión

const iv = aesPacket.slice(0, 12);
const cipherBytes = aesPacket.slice(12);