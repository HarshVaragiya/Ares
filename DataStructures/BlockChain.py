#!bin/usr/python3

from Block import Block

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

import datetime
import json
import os

# Blockchain Definition

class BlockChain:
    def __init__(self,Publickkey,LOCATION):
        self.location = LOCATION
        self.pubkey = Publickkey
        self.block_count = 0
        self.make_genesis()
    
    def make_genesis(self):
        pass

