from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64

def encrypt(text: str, passphrase: str) -> str:
    salt = get_random_bytes(16)
    key = PBKDF2(passphrase, salt, dkLen=32, count=1000000)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    return base64.b64encode(salt + cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt(enc_text: str, passphrase: str) -> str:
    enc_data = base64.b64decode(enc_text)
    salt, nonce, tag, ciphertext = enc_data[:16], enc_data[16:32], enc_data[32:48], enc_data[48:]
    key = PBKDF2(passphrase, salt, dkLen=32, count=1000000)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

if __name__ == "__main__":
    print("running example")
    # Example usage
    passphrase = "your-passphrase"
    original_text = "Hello, World!"

    encrypted_text = encrypt(original_text, passphrase)
    print(f"Encrypted: {encrypted_text}")

    decrypted_text = decrypt(encrypted_text, passphrase)
    print(f"Decrypted: {decrypted_text}")

