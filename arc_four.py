from arc4 import ARC4
import pyperclip
import time

def encrypt_decrypt(message, key, mode):
    global outtranslated
    translated = ''
    if mode == 'encrypt':
        arc4 = ARC4(key)
        translated = arc4.encrypt(message)
    elif mode == 'decrypt':
        arc4 = ARC4(key)
        translated = arc4.decrypt(message)
    if mode == "encrypt":
        print(mode, '=', translated)
    else:
        print(mode, '=', translated.decode("utf-8") )
    # pyperclip.copy(translated)
    outtranslated = translated
    return outtranslated


# ------------------- Шифрування повідомлень -----------------------
message = b'New secret notification'
my_key = b'My Secret Keyword'
# -------------- Виклик функції для шифрування / дешифрування
StartTime=time.time()
encrypt_decrypt(message, my_key, 'encrypt')        #Кодування
encrypt_decrypt(outtranslated, my_key, 'decrypt')  #Декодування
totalTime = (time.time()-StartTime)
print ('totalTime =',  totalTime, 's')
# ----------------------------- Шифрування файлів ----------------------------
imputFilename='test_file.txt'
ouputFilename='crypt_test_file.txt'
fileObj=open(imputFilename)
content=fileObj.read()                        # Зчитування інформації з файлу
fileObj.close()
# ------------------ Кодування / декодування з контролем часу -----------------
StartTime=time.time()

encrypt_decrypt(content, my_key, 'encrypt')         # Кодування
encrypt_decrypt(outtranslated, my_key, 'decrypt')   # Декодування

totalTime = (time.time()-StartTime)
print ('totalTime =',  totalTime, 's')
#-----------------------------------------------------------------------------
outputfileObj=open(ouputFilename, 'w')
outputfileObj.write(outtranslated.decode("utf-8") )                    # Запис інформації у файл
outputfileObj.close()
