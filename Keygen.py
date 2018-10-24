#!usr/bin/python3

from Crypto.PublicKey import RSA                  # RSA from pycryptodome 
from Crypto import Random                         # Random Number Generator
import hashlib,os                                 # Optional, To compare hashes of generated keys

def generate_keys(PublicPath,PrivatePath):

    os.makedirs(os.path.dirname(PublicPath) , exist_ok=True)
    os.makedirs(os.path.dirname(PrivatePath), exist_ok=True)

    random_gen = Random.new().read                    # Cryptographically Secure Random Number Generator
    new_key = RSA.generate(4096,random_gen,e=65537)   # 4096 Bits Key
    private_key = new_key.exportKey('PEM')            # export in PEM Format
    public_key = new_key.publickey().exportKey('PEM')  

    print("Private Key Hash : {} ".format(hashlib.sha256(private_key).hexdigest()))   # if you want to check hash of keys to see 
    print("Public  Key Hash : {} ".format(hashlib.sha256(public_key).hexdigest()))    # performance of random number generator 

    fw = open(PrivatePath,'wb')                 # Write the private Key to a file
    #print(private_key.decode('utf-8'))
    fw.write(private_key)
    fw.close()
    fw = open(PublicPath,'wb')                  # Write the public key to a file 
    #print(public_key.decode('utf-8'))
    fw.write(public_key)
    fw.close()

if __name__ == "__main__":

    PublicPath = "SampleElection/Keys/public_key.pem"
    PrivatePath = "SampleElection/Secret/private_key.pem"

    generate_keys(PublicPath,PrivatePath)