#!bin/usr/python3

from DataStructures.Block import Block

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
        self.blocks = []
        self.prev_hash = os.urandom(32).hex()
        self.prev_e_hash = os.urandom(32).hex()
        self.make_genesis()

    def make_genesis(self):
        vote_data = 0xFF
        self.add_block(vote_data)
    
    def add_block(self,vote_data):
        blk = Block(self.block_count,self.location,self.prev_hash,self.prev_e_hash,self.pubkey)  # Create Block
        blk.insert(vote_data)                                                                    # Insert Data 
        block_gist = blk.process_block()                                                         # Process the Block 
        self.prev_e_hash , self.prev_hash = blk.get_hashes()                                     # Get Block Hashes to be used in next block
        self.blocks.append(block_gist)
        self.block_count +=1
    
    def export(self,savefile):
        data = json.dumps(self.blocks,indent=4)
        fw = open(savefile,'w')
        size = fw.write(data)
        fw.close()
        return size




