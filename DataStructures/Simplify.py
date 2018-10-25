from DataStructures.BlockChain import BlockChain

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

import json
import os
import time
import hashlib

#    Old init function not using config file, but all raw configuration data
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
        self.votes   = {}
        raw_rsa_key  = RSA.import_key(open(PRIVATE_KEY_FILE,'r').read())
        self.privkey = PKCS1_OAEP.new(raw_rsa_key)
        self.infile  = config["outfile"]
        self.next_hash   = None
        self.next_e_hash = None
    
    def show_status(self):
        os.system("clear")
        print(" Results : \n")
        print(" +-------------+-----------------------------+----------------+")
        for key in self.votes:
            print(" | ID : {:6d} | Name : {:20s} | Votes : {:6d} |".format(int(key),self.candidates[key],self.votes[key]))
            print(" +-------------+-----------------------------+----------------+")

    def process(self,DELAY=1):
        raw_data = open(self.infile,'r').read()
        blockchain = json.loads(raw_data)[::-1]
        for i in range(1,len(blockchain)):
            self.show_status()
            perc = (i)*100 / (len(blockchain)-1)
            print("\n\n Progress : {:3.4f}% ".format(perc))
            time.sleep(DELAY)
            self.process_block(blockchain[i])

    def process_block(self,block):
        block_dic = json.loads(block)
  
        aes_key_dic = json.loads(self.privkey.decrypt(bytes.fromhex(block_dic["key"])).decode())
        aes = AES.new(bytes.fromhex(aes_key_dic["key"]),AES.MODE_EAX,nonce=bytes.fromhex(aes_key_dic["nonce"]))
        enc_data = aes.decrypt(bytes.fromhex(block_dic["data"]))
        
        self.curr_e_hash = hashlib.sha256(block_dic["data"].encode()).hexdigest()
        self.curr_hash = hashlib.sha256(enc_data).hexdigest()

        if(self.next_e_hash != None and self.next_hash != None):
            assert (self.curr_e_hash == self.next_e_hash) , "Improper Encrypted Hash Match! Data Modified! Exiting!"
            assert (self.curr_hash == self.next_hash), "Imporoper Hash Match! Data has been Modified! Exiting!"
        

        block_data = json.loads(enc_data.decode())

        self.next_hash = block_data["lasthash"]
        self.next_e_hash = block_data["lastEhash"]


        #print("Hash: {} EHash: {} PrevHash: {} PrevEHash: {}".format(self.curr_hash,self.curr_e_hash,self.next_hash,self.next_e_hash))


        if(block_data["vote"] != 0xFF):
            vote_data = block_data["vote"]
            try:
                voter_id = json.loads(vote_data)
                self.votes[voter_id["vote"]] += 1
            except KeyError:
                self.votes[voter_id["vote"]] = 0x01
        