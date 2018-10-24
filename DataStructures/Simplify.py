from DataStructures.BlockChain import BlockChain

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

import json
import os
import time

#    Old init function not using config file
#
#    def __init__(self,candidates,LOCATION,PublicKeyFile,savefile):
#        self.candidates = candidates
#        self.location   = LOCATION
#        self.PublicKeyFile = PublicKeyFile
#        self.generate_RSA_Object()
#        self.blockchain = BlockChain(self.pubkey,self.location)
#        self.savefile = savefile
#



class Election:

    def __init__(self,CONFIG_FILE_NAME="Config.json"):
        config = json.loads(open(CONFIG_FILE_NAME,'r').read())
        self.candidates = json.loads(open(config["choices"],'r').read())
        self.location   = config["location"]
        self.PublicKeyFile = config["key"]
        self.__generate_RSA_Object()
        self.blockchain = BlockChain(self.pubkey,self.location)
        self.savefile   = config["outfile"]

    def __generate_RSA_Object(self):
        raw_rsa_key = RSA.import_key(open(self.PublicKeyFile,'r').read())
        padded_key  = PKCS1_OAEP.new(raw_rsa_key)
        self.pubkey = padded_key

    def display_choices_and_cast_vote(self):
        print("Ctrl + C To Quit.")
        for key in self.candidates:
            print("{} : {} ".format(key,self.candidates[key]))
        ch  = input(" Enter Your Choice  : ")
        vid = input(" Enter Your VoterID : ")
        voter_data = {
            "vote":ch,
            "choice":self.candidates[ch],
            "voterID":vid
        }
        self.blockchain.add_block(json.dumps(voter_data))
    
    def end(self):
        try:
            size = self.blockchain.export(self.savefile)
            return size
        except AttributeError:
            pass

    def __del__(self):
        self.end()





class Results:
    def __init__(self,CONFIG_FILE_NAME,PRIVATE_KEY_FILE):
        config = json.loads(open(CONFIG_FILE_NAME,'r').read())
        self.candidates = json.loads(open(config["choices"],'r').read())
        self.votes = {}
        raw_rsa_key = RSA.import_key(open(PRIVATE_KEY_FILE,'r').read())
        self.privkey = PKCS1_OAEP.new(raw_rsa_key)
        self.infile  = config["outfile"]
    
    def process(self):
        raw_data = open(self.infile,'r').read()
        blockchain = json.loads(raw_data)
        for block in blockchain:
            print(self.votes,end = '\r')
            time.sleep(0.5)
            self.process_block(block)

    def process_block(self,block):
        block_dic = json.loads(block)
        aes_key_dic = json.loads(self.privkey.decrypt(bytes.fromhex(block_dic["key"])).decode())
        aes = AES.new(bytes.fromhex(aes_key_dic["key"]),AES.MODE_EAX)
        aes.nonce = bytes.fromhex(aes_key_dic["nonce"])
        enc_data  = aes.decrypt(bytes.fromhex(block_dic["data"])).decode()
        print(enc_data)
        vote_data = enc_data["vote"]
        voter_id = json.loads(vote_data)
        try:
            self.votes[voter_id["vote"]] += 1
        except KeyError:
            self.votes[voter_id["vote"]] = 0x00
    



