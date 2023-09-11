from wireguard import WireGuard
from warpapi import clone_key
import random,os

os.system("warp-yxip.bat")

with open("basekeys.txt","r",encoding="utf-8") as f:
    keys=f.readlines()

srckey=random.choice(keys).strip()
print(srckey)

pk=WireGuard.genkey()
newkey=clone_key(srckey,WireGuard.pubkey(pk))

with open("wireguard.conf","w+",encoding="utf-8") as f:
    lines= ["[Interface]",
            f"PrivateKey = {pk}",
            "Address = 172.16.0.2/32, 2606:4700:110:8a5d:771e:f3c8:3726:5a53/128",
            "DNS = 1.1.1.1, 1.0.0.1",
            "MTU = 1280",
            "[Peer]",
            "PublicKey = bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=",
            "AllowedIPs = 0.0.0.0/0",
            "AllowedIPs = ::/0",
            "Endpoint = engage.cloudflareclient.com:2408"]
    f.write("\n".join(lines))

with open("template.yml","r",encoding="utf-8") as f:
    template=f.read()
with open("result.csv","r",encoding="utf-8") as f:
    result=list(map(lambda l:l.split(',')[0].split(':'),f.readlines()[1:7]))

template=template.replace("{{private_key}}",pk)\
                 .replace("{{server_A}}",result[0][0]).replace("{{port_A}}",result[0][1])\
                 .replace("{{server_B}}",result[0][0]).replace("{{port_B}}",result[0][1])\
                 .replace("{{server_C}}",result[0][0]).replace("{{port_C}}",result[0][1])\
                 .replace("{{server_D}}",result[0][0]).replace("{{port_D}}",result[0][1])\
                 .replace("{{server_E}}",result[0][0]).replace("{{port_E}}",result[0][1])\
                 .replace("{{server_F}}",result[0][0]).replace("{{port_F}}",result[0][1])

with open("clash.yml","w+",encoding="utf-8") as f:
    f.write(template)
