import requests
from bs4 import BeautifulSoup

url = "https://www.tcharter.ir/tickets/tickets/VEhSLUtJSC0xNDAyLzA1LzA5/?airplane"
#url = "https://www.tcharter.ir/tickets/get_agency/%5B1477%5D/THR/IFN/1690398000/"
payload = {"tab": "airplane"}
req = requests.post(url, data=payload)

if req.status_code == 200:
    soup = BeautifulSoup(req.content, 'html5lib')
    print(soup.prettify())
