# Authenticated file encryption and decryption tool
### Description
This module provides two python scipts for encryption and decription of files using AES GCM mode <https://en.wikipedia.org/wiki/Galois/Counter_Mode>  
### How to run
#### Install dependencies
It requires Python and Pycryptodome<http://pycryptodome.readthedocs.io/en/latest/src/introduction.html>  
You can get Pycryptodome by running "pip install pycryptodome"  
You should do it in a virtual enviorment if you already have pycrypto as it is a fork of pycrypto and they might interfeare with each other in unexpted ways
#### Encryption step
* Download the files
* From terminal, run "python AFET.py"
* It will guide you through the process
* You have to remember the passpharase you use to encrypt the file in order to decrypt it later  
#### Decryption step
* From terminal, run "python AFDT.py"
* It will guide you through the process
