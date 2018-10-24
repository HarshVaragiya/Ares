from DataStructures.Simplify import Results

FOLDER_NAME      = "SampleElection"

PRIVATE_KEY_FILE = FOLDER_NAME + "/Secret/private_key.pem"
CONFIG_FILE_NAME = FOLDER_NAME + "/Config.json"

x = Results(CONFIG_FILE_NAME,PRIVATE_KEY_FILE)
x.process()
