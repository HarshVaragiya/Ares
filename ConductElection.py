from DataStructures.Simplify import Election

FOLDER = "SampleElection"
CONFIG_FILE = FOLDER + "/Config.json"

x = Election(CONFIG_FILE)
while(True):
    try:
        x.display_choices_and_cast_vote()
    except KeyboardInterrupt:
        break
    except:
        print("Invalid Input! Try Again!")

size = x.end()
b  = size
kb = b /1024
mb = kb/1024
print("\n\nElection Conducted! Export File Size : {} Bytes | {} KB | {} MB \n".format(b,kb,mb))