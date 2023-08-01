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


# url = unquote(r'https://www.tcharter.ir//tickets/search/0/%D9%85%D8%B4%D9%87%D8%AF-%D8%AA%D9%87%D8%B1%D8%A7')
# print(url)

req1 = requests.get(
    "https://ipv4.webshare.io/",
    proxies={
        "http": "http://doxfansx-rotate:f33565lbl412@p.webshare.io:80/",
        "https": "http://doxfansx-rotate:f33565lbl412@p.webshare.io:80/"
    }
)

req = requests.get(
    "https://ipv4.webshare.io/",
    proxies={
        "http": "http://doxfansx:f33565lbl412@2.56.119.93:5074/",
        "https": "http://doxfansx:f33565lbl412@2.56.119.93:5074/",
    }
)

print(req)
