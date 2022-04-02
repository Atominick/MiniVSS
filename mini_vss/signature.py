
import hashlib
import os

from Crypto.PublicKey import RSA

standart_private_key_name = 'private.pem'
standart_public_key_name = 'public.pem'


def create_keypair(path):
    private_key_path = os.path.join(path, standart_private_key_name)
    public_key_path = os.path.join(path, standart_public_key_name)

    raw_key = RSA.generate(2048)
    public = raw_key.publickey()

    private_key = raw_key.exportKey('PEM')
    public_key = public.exportKey('PEM')

    try:
        with open(private_key_path, 'wb+') as keyfile:
            keyfile.write(private_key)
            keyfile.close()
        print("Successfully created your new RSA private key")
        with open(public_key_path, "wb+") as keyfile:
            keyfile.write(public_key)
            keyfile.close()
        print ("Successfully created your new RSA public key")
    except Exception as e:
        print("Error creating your key: {}".format(e))

def get_hash(filepath):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    # hash = hashlib.md5()
    hash= hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash.update(data)
    int_hash = int.from_bytes(hash.digest(), byteorder='big')
    # print("hash of {} is {}".format(filepath, int_hash))
    return int_hash

def load_key(key_filepath):
    key = None
    with open(key_filepath, mode='rb') as f:
        key_data = f.read()
        return RSA.import_key(key_data)

def generate(filepath, private_key):
    hash = get_hash(filepath)

    if private_key:
        signature = pow(hash, private_key.d, private_key.n)
        return signature

def check(filepath, signature, public_key):
    present_hash = get_hash(filepath)
    hash_from_signature = pow(signature, public_key.e, public_key.n)
    # print("hash from signature is: {}:".format(hash_from_signature))
    if hash_from_signature == present_hash:
        return True
    return False

def key_to_str(key):
    str_key = key.exportKey('PEM')
    return str_key.decode()

def str_to_key(str):
    b_key = str.encode()
    return RSA.import_key(b_key)