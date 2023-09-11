from wireguard import WireGuard
private_key=WireGuard.genkey()
print(private_key)
print(WireGuard.pubkey(private_key))