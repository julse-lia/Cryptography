import time
import string
import random
def rc4(data, key):
    """RC4 encryption and decryption method."""

    S, j, out = list(range(256)), 0, [] # Array initialization

    for i in range(256):    # Key Scheduling Algorithm
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0               # Pseudo Random Generation Algorithm
    for ch in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) % 256]))

    return "".join(out)

decrypted = []
def hack_unknownplaintext(knownPlaintext, knownCiphertext, unknownCiphertext):
    for i in range(0, len(unknownCiphertext)):
        p = knownPlaintext[i % len(knownPlaintext)]
        c1 = knownCiphertext[i % len(knownCiphertext)]
        c2 = unknownCiphertext[i]
        decrypted.append(chr(ord(p) ^ ord(c1) ^ ord(c2)))
    print("".join(decrypted))

def rand_digit_key():
    password_characters = string.digits
    return ''.join(random.choice(password_characters) for i in range(12))

if __name__ == "__main__":

    # ------------------- Шифрування повідомлень -----------------------
    key = str(rand_digit_key())
    # print('key =', key)
    key2 = str(rand_digit_key())
    # print('key2 =', key2)
    plaintext = 'A computer would deserve to be called intelligent if it could deceive a human into believing that it was human.'
    # -------------- Виклик функції для шифрування / дешифрування
    print('---------------------------------------------------------------------------------------------------------------------')
    StartTime = time.time()

    print('key =', key)
    encrypted_message = rc4(plaintext, key)  # Кодування
    print('Encrypted message:\n', encrypted_message, '\n')

    print('key2 =', key2)
    encrypted_message2 = rc4(encrypted_message, key2)  # Кодування2
    print('Encrypted2 message:\n', encrypted_message2, '\n')

    print('key2 =', key2)
    decrypted_message = rc4(encrypted_message2, key2)  # Декодування
    print('Decrypted message:\n', decrypted_message, '\n')

    print('key =', key)
    decrypted_message2 = rc4(decrypted_message, key)  # Декодування2
    print('Decrypted2 message:\n', decrypted_message2, '\n')
    totalTime = (time.time() - StartTime)
    print('totalTime_message =', totalTime, 's')
    print('---------------------------------------------------------------------------------------------------------------------')

    # ----------------------------- Шифрування файлів ----------------------------
    inputTXT = 'test_file.txt'
    outputTXT = 'crypt_test_file.txt'

    inputDOCX = 'plain_file.docx'
    outputDOCX = 'crypt_file.docx'

    inputDOCX2 = 'knownplain.docx'
    outputDOCX2 = 'knowncipher.docx'

    fileObj = open(inputDOCX)
    content = fileObj.read()  # Зчитування інформації з файлу
    fileObj.close()
    # ------------------ Кодування / декодування з контролем часу -----------------
    StartTime = time.time()

    print('key =', key)
    encrypted_text = rc4(content, key)  # Кодування1
    print('Encrypted text:\n', encrypted_text, '\n')

    print('key2 =', key2)
    encrypted_text2 = rc4(encrypted_text, key2)  # Кодування2
    print('Encrypted2 text:\n', encrypted_text2, '\n')

    print('key2 =', key2)
    decrypted_text = rc4(encrypted_text2, key2)  # Декодування1
    print('Decrypted text:\n', decrypted_text, '\n')

    print('key =', key)
    decrypted_text2 = rc4(decrypted_text, key)  # Декодування2
    print('Decrypted2 text:\n', decrypted_text2, '\n')

    totalTime = (time.time() - StartTime)
    print('totalTime_text =', totalTime, 's')
    print('---------------------------------------------------------------------------------------------------------------------')
    # -----------------------------------------------------------------------------
    outputfileObj = open(outputDOCX, 'w')
    outputfileObj.write(decrypted_text)  # Запис інформації у файл
    outputfileObj.close()

    #Hacking message
    StartTime = time.time()
    knownPlaintext = "Some known plaintext encrypted with rc4 with the same key, that is secret. In this case we can find plaintext of another same-key encrypted message."
    knownCiphertext = rc4(knownPlaintext, key)
    print("Hacked message:")
    hack_unknownplaintext(knownPlaintext, knownCiphertext, encrypted_message)
    totalTime = (time.time() - StartTime)
    print('totalTime_message =', totalTime, 's')
    print('---------------------------------------------------------------------------------------------------------------------')

    #-----------------------------------------------------------------------------
    # Hacking text
    fileObj2 = open(inputDOCX2)
    content2 = fileObj2.read()  # Зчитування інформації з файлу
    fileObj2.close()

    known_encrypted_text = rc4(content2, key)  # Кодування
    known_decrypted_text = rc4(known_encrypted_text, key)  # Декодування

    StartTime = time.time()
    outputfileObj2 = open(outputDOCX2, 'w')
    outputfileObj2.write(known_encrypted_text)  # Запис інформації у файл
    outputfileObj2.close()
    print("Hacked text:")
    hack_unknownplaintext(content2, known_encrypted_text, encrypted_text)
    totalTime = (time.time() - StartTime)
    print('totalTime_text =', totalTime, 's')

