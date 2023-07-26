import requests
from bs4 import BeautifulSoup

url = 'https://www.tcharter.ir/tickets/tickets/VEhSLUlGTi0xNDAyLzA2LzIw/?airplane='
#url = "https://www.tcharter.ir/tickets/get_agency/%5B1477%5D/THR/IFN/1690398000/"
payload = {"tab": "airplane"}
req = requests.post(url, data=payload)

if req.content == b"error":
    soup = BeautifulSoup(req.content, 'html5lib')
    print(soup.prettify())
else:
    print(req.content)
