// Emisor y receptor comparten el mismo secreto (por papel, Signal, etc.)
const secret = "secreto_compartido_2025_muy_seguro_32b";
const salt = "a1b2c3d4...";

// Ambos derivan la misma clave AES-256
const keyAES = PBKDF2(secret, salt, 100000 iteraciones, SHA-256);