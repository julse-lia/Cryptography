# -------------------- Скрипт прикладу реалізації Лр5 - афінний шифр --------------------------
# ---- файл не викликається, ключ - однаковий за константою, криптоаналіз не реалізовано -------
import sys,  pyperclip, random
import time
SYMBOLS = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгґдеєжзиіїйклмнопрстуфхцчшщьюя1234567890 ,!?.()'

def main():
    # ----------- шифрування -------------------------
    StartTime = time.time()
    myMessage = 'Криптографія — наука про математичні методи забезпечення конфіденційності, цілісності і автентичності інформації.'
    myKey = 3012
    myMode = 'encrypt'
    encrypted_message = encryptMessage(myKey, myMessage)
    print('Key: %s' % (myKey))
    print('%sed text:' % (myMode.title()))
    print(encrypted_message)
    pyperclip.copy(encrypted_message)
    print('Full %sed text copied to clipboard.' % (myMode))
    # ---------- дешифрування ------------------------
    myMessage = encrypted_message
    myMode = 'decrypt'
    decrypted_message = decryptMessage(myKey, myMessage)
    print('Key: %s' % (myKey))
    print('%sed text:' % (myMode.title()))
    print(decrypted_message)
    pyperclip.copy(decrypted_message)
    print('Full %sed text copied to clipboard.' % (myMode))
    totalTime = (time.time() - StartTime)
    print('totalTime for string =', totalTime, 's')
    # ----------------------------- Шифрування файлів ----------------------------
    imputFilename = 'test_file.docx'
    ouputFilename = 'crypt_test_file.docx'
    fileObj = open(imputFilename)
    content = fileObj.read()  # Зчитування інформації з файлу
    fileObj.close()
    # ------------------ Кодування з контролем часу -----------------
    StartTime = time.time()
    myMode = 'encrypt'
    encrypted_text = encryptMessage(myKey, content)  # Кодування
    print('Key: %s' % (myKey))
    print('%sed text:' % (myMode.title()))
    print(encrypted_text)
    pyperclip.copy(encrypted_text)
    print('Full %sed text copied to clipboard.' % (myMode))
    # ------------------ Декодування з контролем часу -----------------
    decrypted_text = decryptMessage(myKey, encrypted_text) # Декодування
    myMode = 'decrypt'
    print('Key: %s' % (myKey))
    print('%sed text:' % (myMode.title()))
    print(decrypted_text)
    pyperclip.copy(decrypted_text)
    print('Full %sed text copied to clipboard.' % (myMode))
    totalTime = (time.time() - StartTime)
    print('totalTime for text =', totalTime, 's')
    # -----------------------------------------------------------------------------
    outputfileObj = open(ouputFilename, 'w')
    outputfileObj.write(decrypted_text)  # Запис інформації у файл
    outputfileObj.close()
    # ---------- взлам ключа ------------------------
    StartTime = time.time()
    myMessage = encrypted_message
    hack(myMessage)
    totalTime = (time.time() - StartTime)
    print('totalTime =', totalTime, 's')
    return

# -------------------------- функції модульної арифметики для афіного шифру --------------------------
def gcd(a, b):               # найбільший загальний дільник a, b за алгоритмом Евкліда (для шифрування)
    while a != 0:
        a, b = b % a, a
    return b
def findModInverse(a, m):    # модульне обертання за алгоритмом  Евкліда (для шифрування)
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
# -----------------------------------------------------------------------------------------------------
# --------------------------------------- визначення значень ключів -----------------------------------
def getKeyParts(key):
    keyA = key // len(SYMBOLS) # ділення без залишку
    keyB = key // len(SYMBOLS)  # ділення без залишку
    # keyB = key % len(SYMBOLS)  # залишок від ділення
    return (keyA, keyB)
# --------------------------- виявлення та видалення слабких ключів 0,1 -------------------------------
def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
    if keyB == 0 and mode == 'encrypt':
        sys.exit('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        sys.exit('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))
    return
# --------------------------------------- АфІнне  шифрування --------------------------------------------
def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol # just append this symbol unencrypted
    return ciphertext
# --------------------------------------- АфІнне  дешифрування ------------------------------------------
def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plaintext = ''
    modInverseOfKeyA = findModInverse(keyA, len(SYMBOLS))
    for symbol in message:
        if symbol in SYMBOLS:
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol # just append this symbol undecrypted
    return plaintext

def hack(message):
    for key in range(len(SYMBOLS)):
        keyA, keyB = (key, key)
        try:
            checkKeys(keyA, keyB, 'decrypt')
            plaintext = ''
            modInverseOfKeyA = findModInverse(keyA, len(SYMBOLS))
            for symbol in message:
                if symbol in SYMBOLS:
                    symIndex = SYMBOLS.find(symbol)
                    plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
                else:
                    plaintext += symbol  # just append this symbol undecrypted
            print('key=', key, ' ', plaintext)
        except:
            continue
    return
main()
# ----------------------------------------------------------------------------------------------------------