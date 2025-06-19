def encrypt_xor_repeating_key(message: str, key: str) -> str:
    """
    Encrypt the message using the repeating-key XOR algorithm.
    Algorithm: Repeating-key XOR (a simplified version of the Vigenère cipher using XOR)
    @param message: string of the message to encrypt
    @param key: string representing the encryption key (much smaller than the message)
    @return: hex string representing the encrypted message
    """
    encrypted_bytes = bytearray()
    for i, ch in enumerate(message):
        key_ch = key[i % len(key)]
        encrypted_byte = ord(ch) ^ ord(key_ch)
        encrypted_bytes.append(encrypted_byte)
    # Return the encrypted message as a hex string for readability.
    return encrypted_bytes.hex()

def decrypt_xor_repeating_key(encrypted_message: str, key: str) -> str:
    """
    Decrypt the message using the repeating-key XOR algorithm.
    Algorithm: Repeating-key XOR (a simplified version of the Vigenère cipher using XOR)
    @param encrypted_message: hex string representing the encrypted message
    @param key: string representing the encryption key (much smaller than the message)
    @return: decrypted message string
    """
    # Convert hex back to bytes.
    encrypted_bytes = bytes.fromhex(encrypted_message)
    decrypted_chars = []
    for i, byte in enumerate(encrypted_bytes):
        key_ch = key[i % len(key)]
        decrypted_char = chr(byte ^ ord(key_ch))
        decrypted_chars.append(decrypted_char)
    return "".join(decrypted_chars)


def encrypt_caesar_cipher(message: str, key: str) -> str:
    """
    Encrypt the message with a Caesar cipher.
    Only letters are shifted; other characters remain unchanged.
    The key is provided as a binary string (e.g., '010110111').
    @param message: message to encrypt
    @param key: binary string representing the encryption key
    @return: encrypted message
    """
    # Convert the binary key to an integer shift value.
    shift = int(key, 2)
    result = []
    for ch in message:
        if ch.isupper():
            # A-Z: shift and wrap-around (using modulo 26)
            shifted = (ord(ch) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(shifted))
        elif ch.islower():
            # a-z: shift and wrap-around
            shifted = (ord(ch) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(shifted))
        else:
            result.append(ch)
    return "".join(result)


def decrypt_caesar_cipher(encrypted_message: str, key: str) -> str:
    """
    Decrypt the message encrypted with a Caesar cipher.
    Only letters are shifted; other characters remain unchanged.
    The key is provided as a binary string (e.g., '010110111').
    @param encrypted_message: encrypted message
    @param key: binary string representing the encryption key used for encryption
    @return: decrypted message
    """
    # Convert the binary key to an integer shift value.
    shift = int(key, 2)
    result = []
    for ch in encrypted_message:
        if ch.isupper():
            shifted = (ord(ch) - ord('A') - shift) % 26 + ord('A')
            result.append(chr(shifted))
        elif ch.islower():
            shifted = (ord(ch) - ord('a') - shift) % 26 + ord('a')
            result.append(chr(shifted))
        else:
            result.append(ch)
    return "".join(result)


def encrypt_vigenere_cipher(message: str, key: str) -> str:
    """
    Encrypt the message using the Vigenère cipher.
    Only letters are shifted; other characters remain unchanged.
    @param message: message to encrypt
    @param key: string key used for shifting letters (non-letter characters in key will be ignored)
    @return: encrypted message
    """
    result = []
    key = key.lower()
    key_index = 0
    for ch in message:
        if ch.isalpha():
            # Determine the shift from the key letter.
            shift = ord(key[key_index % len(key)]) - ord('a')
            if ch.isupper():
                shifted = (ord(ch) - ord('A') + shift) % 26 + ord('A')
                result.append(chr(shifted))
            else:
                shifted = (ord(ch) - ord('a') + shift) % 26 + ord('a')
                result.append(chr(shifted))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


def decrypt_vigenere_cipher(encrypted_message: str, key: str) -> str:
    """
    Decrypt a message encrypted using the Vigenère cipher.
    Only letters are shifted; other characters remain unchanged.
    @param encrypted_message: the encrypted message
    @param key: string key used for the encryption (non-letter characters in key will be ignored)
    @return: decrypted message
    """
    result = []
    key = key.lower()
    key_index = 0
    for ch in encrypted_message:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if ch.isupper():
                shifted = (ord(ch) - ord('A') - shift) % 26 + ord('A')
                result.append(chr(shifted))
            else:
                shifted = (ord(ch) - ord('a') - shift) % 26 + ord('a')
                result.append(chr(shifted))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


# test message 1:
message_test1 = "Hello Bob! Hello, World! This is a test message."
message_test2 = "The best way to predict the future is to create it."
message_test3 = "Hope is the light that guides us through the darkest times."
message_test4 = "Every new day is a chance to make a positive impact."

list_messages = [message_test1, message_test2, message_test3, message_test4]
