#!bin/usr/python3

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import hashlib
import datetime
import json
import os


# Block Definition 


class Block:

    def __init__(self,BlockID,LocationID,PrevHash,PrevEHash,Publickey):
        self.id        = BlockID                # Block ID of the Block
        self.loc       = LocationID             # Location ID of Block Creation
        self.lasthash  = PrevHash               # Previous Block Hash
        self.lastEhash = PrevEHash              # Previous Block Encrypted Hash
        self.pubkey    = Publickey              # Public Key Object For Encryption
    
    def insert(self,vote_data):
        self.timestamp = str(datetime.datetime.now())
        self.data = {
            "id":self.id,
            "time":self.timestamp,
            "loc":self.loc,
            "lasthash":self.lasthash,
            "lastEhash":self.lastEhash,
            "vote":vote_data
        }

    def generate_AES_Obj(self):
        self.key = self.generate_AES_key()
        self.AESObj = AES.new(self.key,AES.MODE_EAX)
        self.nonce = self.AESObj.nonce
    
    def export_ENC_AES_Key(self):
        exportkey = {
            'key':self.key.hex(),
            'nonce':self.nonce.hex()
        }
        export_data = json.dumps(exportkey).encode()
        return self.pubkey.encrypt(export_data)
    
    def process_block(self):
        self.generate_AES_Obj()
        data = json.dumps(self.data).encode()
        self.enc_data = self.AESObj.encrypt(data).hex()
        enc_key  = self.export_ENC_AES_Key().hex()
        self.caclulate_hashes()
        block_out = {
            "id":self.id,
            "time":self.timestamp,
            "prevHash":self.lasthash,
            "prevEHash":self.lastEhash,
            "key":enc_key,
            "data":self.enc_data
        }
        self.randomize()
        return json.dumps(block_out)

    def caclulate_hashes(self):
        self.sha256TD = hashlib.sha256(json.dumps(self.data).encode()).hexdigest()
        self.sha256ED = hashlib.sha256(json.dumps(self.enc_data).encode()).hexdigest()

    def get_hashes(self):
        return self.sha256ED , self.sha256TD

    def randomize(self):
        self.key = os.urandom(32)
        self.nonce = os.urandom(16)
        self.data = os.urandom(32)
    
    def generate_AES_key(self):
        return os.urandom(32)
    