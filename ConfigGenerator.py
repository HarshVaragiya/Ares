from Keygen import generate_keys
import json,os

CREATE_KEYS = False


LOCATION_IDENTIFIER  = input("Enter Location Identifier                   : ")
FOLDER_NAME          = input("Election Folder Name                        : ")
OUT_FILE_NAME        = input("Output File Name                            : ")



try:
    PUBLIC_KEY_FILE = input("Public Key File (Ctrl+C to generate Keys)  : ")
except KeyboardInterrupt:
    CREATE_KEYS = True



CANDIDATES_FILE_NAME = "Candidates.json"
CONFIG_FILE_NAME     = "Config.json"


if(CREATE_KEYS == True):
    PUBLICPATH  = FOLDER_NAME + "/Keys/public_key.pem"
    PUBLIC_KEY_FILE = PUBLICPATH 
    PRIVATEPATH = FOLDER_NAME + "/Secret/private_key.pem"
    generate_keys(PUBLICPATH,PRIVATEPATH)


i = 1
dic = {}

print("ENTER CANDIDATES NOW : \nCtrl + C to Quit.\n")

while(i>0):
    try:
        dic[i] = input("Choice {} : ".format(i))
        i+=1
    except KeyboardInterrupt:
        break


os.makedirs(os.path.dirname(FOLDER_NAME + "/" + CANDIDATES_FILE_NAME), exist_ok=True)

open(FOLDER_NAME + "/" + CANDIDATES_FILE_NAME,'w').write(json.dumps(dic))

config = {
    "key":"/Keys/public_key.pem",
    "choices":CANDIDATES_FILE_NAME,
    "location":LOCATION_IDENTIFIER,
    "outfile":OUT_FILE_NAME
}

os.makedirs(os.path.dirname(FOLDER_NAME + "/" + CONFIG_FILE_NAME), exist_ok=True)

open(FOLDER_NAME + "/" + CONFIG_FILE_NAME,'w').write(json.dumps(config))

print("\nConfiguration Exported Sucessfully! \n")