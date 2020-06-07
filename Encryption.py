from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Util import Counter
import sys, os , struct
from Crypto.Hash import SHA 
import hashlib


def encrypt(key, infile, block_zise = 4096):
    originalHashFile = hashFile(infile)
    if len(key)<24:
        key = key + (24-len(key))*'a'
    elif len(key) > 24:
        key = key[:24]
    originalHashKey = hashPassword(key)

    iv = Random.new().read(8)
    cipher = DES3.new(key.encode('utf-8'), DES3.MODE_CFB, iv)

    fsz = os.path.getsize(infile)

    outfile = infile + '.cyp'
    count = 0
    with open(infile, 'rb') as fin:
        with open(outfile, 'wb') as fout:
            fout.write(struct.pack('<Q', fsz))
            fout.write(originalHashKey)
            fout.write(originalHashFile)
            fout.write(iv)
            while True:
                data = fin.read(block_zise)
                count += 1
                n = len(data)
                if n == 0:
                    break
                elif n % 16 != 0:
                    data += b' ' * (16 - n % 16) # <- padded with spaces
                encd = cipher.encrypt(data)
                fout.write(encd)
    return (fsz, block_zise, outfile, count)


def decrypt(key, infile, block_zise = 4096):
    #Adjust file name
    leng = len(infile)
    x = infile.split('/')[-1]
    outfile = infile[:leng-len(x)]
    outfile = outfile + 'decyp_' + x
    leng = len(outfile)
    outfile = outfile[:leng-4]
    
    if len(key)<24:
        key = key + (24-len(key))*'a'
    elif len(key) > 24:
        key = key[:24]
    
    count = 0
    size_file = 0
    with open(infile, 'rb') as fin:
        fsz = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
        hashFile = fin.read(16)
        if not verifyPassword(hashFile, key):
            return (False, None, None, None, None)
        hashFile = fin.read(20)
        iv = fin.read(8)
        decipher = DES3.new(key.encode('utf-8'), DES3.MODE_CFB, iv)   
        with open(outfile, 'wb') as fout:
            while True:
                data = fin.read(block_zise)
                n = len(data)
                if n == 0:
                    break
                decd = decipher.decrypt(data)
                n = len(decd)
                if fsz > n:
                    fout.write(decd)
                else:
                    fout.write(decd[:fsz])

                count += 1
                fsz -= n
                size_file += n
                
    verifyFile(infile, outfile)
    return (True , size_file, block_zise, outfile, count)
        

def hashFile(infile):
    sha1 = hashlib.sha1()
    BUF_SIZE = 65536
    with open(infile, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    sha1Hashed = sha1.hexdigest()

    return sha1.digest()


def verifyFile(originalFile, outfile):
    hashOriginalFile = hashFile(originalFile)
    hashOutFile = hashFile(outfile)
    check = True if hashOriginalFile == hashOutFile else False
    return (check, hashOriginalFile, hashOutFile)


def hashPassword(key):
    hashKey = hashlib.md5()
    hashKey.update(key.encode('utf-8'))
    return hashKey.digest()

def verifyPassword(hashOriginalKey, newKey):
    hashNewKey = hashPassword(newKey)
    if hashOriginalKey == hashNewKey: return True
    else: return False
