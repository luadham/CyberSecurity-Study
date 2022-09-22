from subprocess import check_output
import re

# This script get all of your Connected wifi and display Wifi name and Password
# >>> Work only for windows

def get_networks():
    command = f"netsh wlan show profile"
    ans = check_output(command, shell=True)
    networks = re.findall("(?:Profile\s*:\s)(.*)", ans.decode())
    networks = [i.replace('\r', '') for i in networks]
    return networks

def get_pwd():
    networks = get_networks()
    res = []
    for i in networks:
        command = f"netsh wlan show profile \"{i}\" key=clear"
        ans = check_output(command, shell=True)
        pwd = re.findall("(?:Key Content\s*:\s)(.*)", ans.decode())
        if len(pwd) == 0:
            res.append((i, "Open Network"))
            continue
        res.append((i, pwd[0].replace('\r', '')))
    return res

networks = get_pwd()
print("="*100)
for i in networks:
    print(f"-> [+] {i[0]} >>>> {i[1]}")
print("="*100)