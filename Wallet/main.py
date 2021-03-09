import requests
import time
import base64
import ecdsa
import json
import time

def GetBalance(id):
  balance = 0
  for item in check_transactions():
    for tx in item['transactions']:
      if tx['from'] == id:
        balance -= float(tx['amount'])
      if tx['to'] == id:
        balance += float(tx['amount'])
      if item['finder'] == id:
        if not "fee" in tx:
          continue
        balance += float(tx['fee'])
  return balance

#replace this with your public key
ADDRESS = ""

def wallet():
    response = None
    while response not in ["1", "2", "3", "4"]:
        response = input("""What do you want to do?
        1. Generate new wallet
        2. Check transactions
        3. Check Balance\n""")
    if response == "1":
        # Generate new wallet
        print("""=========================================\n
IMPORTANT: save this credentials or you won't be able to recover your wallet\n
=========================================\n""")
        generate_ECDSA_keys()
    elif response == "2":
        print(check_transactions())
    elif response == "3":
        print(GetBalance(ADDRESS))


def send_transaction(addr_from, private_key, addr_to, amount):
    if len(private_key) == 64:
        signature, message = sign_ECDSA_msg(private_key)
        url = 'https://ValourCoin.superjacobl.repl.co/NewTx'
        payload = {"from": addr_from,
                   "to": addr_to,
                   "amount": amount,
                   "signature": signature.decode(),
                   "message": message,
                   "fee": 0.01}
        headers = {"Content-Type": "application/json"}

        res = requests.post(url, json=payload, headers=headers)
        print(res.text)
    else:
        print("Wrong address or key length! Verify and try again.")


def check_transactions():
    res = requests.get('https://ValourCoin.superjacobl.repl.co/blocks')
    data = json.loads(res.text)
    return data


def generate_ECDSA_keys():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
    private_key = sk.to_string().hex() #convert your private key to hex
    vk = sk.get_verifying_key() #this is your verification key (public key)
    public_key = vk.to_string().hex()
    #we are going to encode the public key to make it shorter

    filename = input("Write the name of your new address: ") + ".txt"
    with open(filename, "w") as f:
        f.write("Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key))
    print("Your new address and private key are now in the file {0}".format(filename))

def sign_ECDSA_msg(private_key):
    message = str(round(time.time()))
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))
    return signature, message


def Begin():
    print("""       =========================================\n
        ValourCoin v1.0.0 - BLOCKCHAIN SYSTEM\n
       =========================================\n\n\n\n\n""")
    while True:
      wallet()
Begin()