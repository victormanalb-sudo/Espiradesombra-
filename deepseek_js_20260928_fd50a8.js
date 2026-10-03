const aesPacket = bitsToBytes(res.bits);

const iv = aesPacket.slice(0, 12);           // Uint8Array
const cipherBytes = aesPacket.slice(12);     // Uint8Array