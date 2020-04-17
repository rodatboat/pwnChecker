import sys, requests, json
from bs4 import BeautifulSoup as soup


email = ''
domain = '%'
password = ''

choice = str(int(input("[1] E-mail search\n[2] Password search "))-1)
if choice == '1' or choice == '0':
    #0==exact 1==like
    if choice == '0':
        email = input("[*] Enter your e-mail username: ")
        if '@' in email:
            username = email.split('@')[0]
            domain = email.split('@')[1]
        else:
            username = email

        data = {
            "luser": username,
            "domain": domain,
            "luseropr": 1,
            "domainopr": 1,
            "submitform": 'em'
        }
    elif choice == '1':
        password = input("[*] Enter your password: ")
        data = {
            "password": password,
            "submitform": 'pw'
        }

results = []
proxy = json.loads(open('proxy.json').read())
sproxy = proxy['proxy']

url = 'http://pwndb2am4tzkvold.onion/'
session = requests.session()

proxies = {
    "http": f"socks5h://{sproxy}",
    "https": f"socks5h://{sproxy}"
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
}

r = session.post(url, headers=headers, proxies=proxies, data=data)

content = soup(r.content, 'html.parser')
content = content.find('pre')

print()
pwnData = content.text.split("Array")[1:]
for accinfo in pwnData:
    user = accinfo.split("[luser] =>")[1].split("[")[0].strip()
    dom = accinfo.split("[domain] =>")[1].split("[")[0].strip()
    if accinfo == pwnData[len(pwnData)-1]:
        password = accinfo.split("[password] =>")[1].split("[")[0].strip().replace(")", '').replace("\n", '')
    else:
        password = accinfo.split("[password] =>")[1].split("[")[0].strip().replace(")", '').replace("\n", '')[:-1]
    leakEmail = user + '@' + dom
    userInfo = {
        'email': leakEmail,
        'password': password
    }
    results.append(userInfo)
    print(f"{leakEmail} : {password}")

file = open('results.json', 'w')
json.dump(results, file)
file.close()