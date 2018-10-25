# Ares

Just another Blockchain based Election System.

## Specifications:
1. PublicKey Cryptography     : RSA 4096 Bits
2. Symmetric Key Cryptography : AES 256 Bits
3. Hashing Function used      : SHA 256

## Working:
For Each Election, a config file is generated and stored in a folder with other files:

1. Location Identifier of the Election  (in config file)
2. Output File Name to store Data       (in config file)
3. Candidates File to store list of Candidates
4. Public Key File                

For simplicity using JSON Files to store all data

## Elections:
1. Genesis Block Is made with random data. it wont be used for storing any data.
2. Block Data is encrypted with AES Key and data is saved in block.
3. AES Key is encrypted with PublicKey of the Election so that only the Private Key holder can unlock it.
4. Next Block is made and stores Hash of Previous Block and hash of encrypted previous block.
5. This goes onn... And in the end, while exporting the results, the top-block is added (random data)

## Future:
- [x] Basic System Working
- [ ] Signed Candidates List (signed with private key)
- [ ] Distributed System     (on a network working on a single blockchain)