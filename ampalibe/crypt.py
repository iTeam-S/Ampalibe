def encode(text, key):
    encoded_text = ""
    for i in range(len(text)):
        key_char = key[i % len(key)]
        encoded_char = chr((ord(text[i]) + ord(key_char)) % 256)
        encoded_text += encoded_char
    return encoded_text


def decode(encoded_text, key):
    decoded_text = ""
    for i in range(len(encoded_text)):
        key_char = key[i % len(key)]
        decoded_char = chr((ord(encoded_text[i]) - ord(key_char) + 256) % 256)
        decoded_text += decoded_char
    return decoded_text