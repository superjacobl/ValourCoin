import requests, hashlib
from urllib.request import Request, urlopen
from dotenv import load_dotenv

load_dotenv()

PoolURL = os.get("PoolURL")


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

def GetWork():
  data = get_html(f"{PoolURL}/GetWork")
  data = data.split(",")
  start = int(data[0])
  end = int(data[1])
  return (start,end)
