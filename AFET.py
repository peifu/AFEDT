"""This module provides a command line tool to encrypt files using AES GCM mode."""

# The name AFET stands for AEAD File Encryption Tool
# This is something I wrote when I was trying to understand GCM mode better
# Dependencies: Python 2.7, pycryptodome(http://pycryptodome.readthedocs.io/en/latest/)
import pickle
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Authenticated encryption on a string using AES GCM with both encryption and MAC

# Key generation
kdf_salt = get_random_bytes(16)
default_passphrase = "I!LIKE!IKE!"
user_passphrase = raw_input("SECRET PASSPHRASE INPUT\nYou will need this to decrypt\nDefault: " + str(default_passphrase) + "\nEnter secret passphrase:")
passphrase = user_passphrase or default_passphrase
print "Passphrase used: " + str(passphrase)
key = PBKDF2(passphrase, kdf_salt)
print "AES Encryption Key: " + str(key)

# Sensitive file to encrypt
user_sensitive_file = raw_input("\n\nFILE INPUT\nEnter file to encrypt:")
input_file_handle = open(user_sensitive_file, 'rb')
sensitive_data = input_file_handle.read()
input_file_handle.close()
print "Sensitive data encrypted: " + str(sensitive_data)

# Additional data to authenticate - won't be encrypted but will be authenticated
default_aad = "Operation Overlord"
user_aad = raw_input("\n\nAAD INPUT\nThis won't be encrypted but it will be authenticated\nDefault: " + str(default_aad) + "\nEnter associated authenticated data:")
aad = user_aad or default_aad
print "Associated authenticated data: " + str(aad)

# Encrypt using AES GCM
cipher = AES.new(key, AES.MODE_GCM)
cipher.update(aad)
ciphertext, tag = cipher.encrypt_and_digest(sensitive_data)
# Nonce is generated randomly if not provided explicitly
nonce = cipher.nonce

# Print all the components of the message
print "\nCOMPONENTS OF TRANSMITTED MESSAGE"
print "AAD: " + str(type(aad))
print aad
print
print "Ciphertext: " + str(type(ciphertext))
print ciphertext
print
print "Authentication tag: " + str(type(tag))
print tag
print
print "Nonce: " + str(type(nonce))
print nonce
print
print "KDF salt: " + str(type(kdf_salt))
print kdf_salt
# Message to transmit/share
transmitted_message = [aad, ciphertext, tag, nonce, kdf_salt]
print "\nTransmitted message: " + str(transmitted_message)
print "Type: " + str(type(transmitted_message))


# Saving message in a file
default_output_filename = "encrypted_file.enc"
user_output_filename = raw_input("\n\nOUTPUT FILENAME INPUT\nDefault: " + str(default_output_filename) + "\nEnter output filename:")
output_filename = user_output_filename or default_output_filename
with open(output_filename, 'wb') as out_file:
    pickle.dump(transmitted_message, out_file)
print "Encrypted output filename: " + str(output_filename)
