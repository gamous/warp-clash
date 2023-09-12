from wireguard import WireGuard
from warpapi import clone_key
import random,os


os.system("warp-yxip.bat")

with open("result.csv","r",encoding="utf-8") as f:
    result=list(map(lambda l:l.split(',')[0].split(':'),f.readlines()[1:7]))

with open("template.yml","r",encoding="utf-8") as f:
    template=f.read()

with open("basekeys.txt","r",encoding="utf-8") as f:
    keys=f.readlines()

srckey=random.choice(keys).strip()
print(f"[succ] choice a source 24PB-key: {srckey}")

pk=WireGuard.genkey()
print(f"[succ] start clone with private key: {pk}")
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
print("[succ] wireguard.conf generated")

template=template.replace("{{private_key}}",pk)\
                 .replace("{{server_A}}",result[0][0]).replace("{{port_A}}",result[0][1])\
                 .replace("{{server_B}}",result[1][0]).replace("{{port_B}}",result[1][1])\
                 .replace("{{server_C}}",result[2][0]).replace("{{port_C}}",result[2][1])\
                 .replace("{{server_D}}",result[3][0]).replace("{{port_D}}",result[3][1])\
                 .replace("{{server_E}}",result[4][0]).replace("{{port_E}}",result[4][1])\
                 .replace("{{server_F}}",result[5][0]).replace("{{port_F}}",result[5][1])

with open("clash.yml","w+",encoding="utf-8") as f:
    f.write(template)
print("[succ] clash.yml generated")