#!usr/bin/python3

from Crypto.PublicKey import RSA                  # RSA from pycryptodome 
from Crypto import Random                         # Random Number Generator
import hashlib                                    # Optional, To compare hashes of generated keys

KEYS_PATH = 'Keys/'

random_gen = Random.new().read                    # Cryptographically Secure Random Number Generator

new_key = RSA.generate(4096,random_gen,e=65537)   # 4096 Bits Key

private_key = new_key.exportKey('PEM')            # export in PEM Format
public_key = new_key.publickey().exportKey('PEM')  

print("Private Key Hash : {} ".format(hashlib.sha256(private_key).hexdigest()))   # if you want to check hash of keys to see 
print("Public  Key Hash : {} ".format(hashlib.sha256(public_key).hexdigest()))    # performance of random number generator 

fw = open(KEYS_PATH + 'private_key.pem','wb')                 # Write the private Key to a file
#print(private_key.decode('utf-8'))
fw.write(private_key)
fw.close()

fw = open(KEYS_PATH + 'public_key.pem','wb')                  # Write the public key to a file 
#print(public_key.decode('utf-8'))
fw.write(public_key)
fw.close()
