from DataStructures.BlockChain import BlockChain

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

import json
import os

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
