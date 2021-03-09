import requests, hashlib
from urllib.request import Request, urlopen
import json
import os
import time
import BasicPoolMiningAPI
from dotenv import load_dotenv

load_dotenv()

MiningAddress = os.getenv("MINING_ADDRESS")

global TotalTimeForMining
global TotalShares
TotalTimeForMining = 0
TotalShares = 0

PoolURL = os.getenv("PoolURL")

def get_html(link):
  try:
    print(link)
    fp = Request(link,headers={'User-Agent': 'Mozilla/5.0'})
    fp = urlopen(fp).read()
    mybytes = fp
    mystr = mybytes.decode("utf8")
    return mystr
  except Exception as e:
    print(e)
    return "Error"

def PoolMine():
  index = int(get_html(f"https://ValourCoin.superjacobl.repl.co/GetCurrentBlockIndex"))
  ShareDifficulty = 2**237
  while True:
    start, end = BasicPoolMiningAPI.GetWork()
    index = get_html("https://ValourCoin.superjacobl.repl.co/GetCurrentBlockIndex")
    for i in range(start, end):
      sha = hashlib.sha256()
      #data = index + str(i)
      data = index + '-' + str(i)
      sha.update(data.encode('utf-8'))
      num = int(sha.hexdigest(),base=16)
      if num < ShareDifficulty:
        print(get_html(f"{PoolURL}/ConfirmShare?address={MiningAddress}&notice={i}"))
        print(data)

PoolMine()
# add solo mine later
