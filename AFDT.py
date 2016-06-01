"""This module provides a command line tool to decrypt files encrypted using AES GCM mode."""

# The name AFET stands for AEAD File Encryption Tool
# This is something I wrote when I was trying to understand GCM mode better
# Dependencies: Python 2.7, pycryptodome(http://pycryptodome.readthedocs.io/en/latest/)
import pickle
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES

# Authenticated encryption on a string using AES GCM with both encryption and MAC
# Decryption step
# The receiver code begins here
user_encrypted_file = raw_input("\n\nFILE INPUT\nEnter file to decrypt:")
with open(user_encrypted_file, 'rb') as in_file:
    received_msg = pickle.load(in_file)

# received_msg = transmitted_message
print "Received message: " + str(received_msg)
received_aad, received_ciphertext, received_tag, received_nonce, received_kdf_salt = received_msg[0], received_msg[1], received_msg[2], received_msg[3], received_msg[4]

# Generate decryption key from passphrase and salt
decryption_passphrase = raw_input("Enter decryption passphrase:")
decryption_key = PBKDF2(decryption_passphrase, received_kdf_salt)
print "Decryption Key: " + str(decryption_key)

# Validate MAC and decrypt
# If MAC validation fails, ValueError exception will be thrown
cipher = AES.new(decryption_key, AES.MODE_GCM, received_nonce)
cipher.update(received_aad)
try:
    decrypted_data = cipher.decrypt_and_verify(received_ciphertext, received_tag)
    print "\nMAC validated: Data was encrypted by someone with the shared secret passphrase"
    print "All allies have passphrase - SYMMETRIC encryption!!!"
    print "\nAuthenticated AAD: " + str(received_aad)
    # print "Decrypted sensitive data: " + str(decrypted_data)
except ValueError as mac_mismatch:
    print "\nMAC validation failed during decryption. No authentication gurantees on this ciphertext"
    print "\nUnauthenticated AAD: " + str(received_aad)

user_decrypted_file = raw_input("\n\nDECRYPTED FILE NAME\nChoose name for decrypted file:")
output_file_handle = open(user_decrypted_file, 'wb')
output_file_handle.write(decrypted_data)
output_file_handle.close()
