import random
import httpx
import os
import time

class WarpApi:
    def __init__(self):
        self.headers = {
            "CF-Client-Version": "a-6.11-2223",
            "Host": "api.cloudflareclient.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
        }
        self.client = httpx.Client(base_url="https://api.cloudflareclient.com/v0a2223", headers=self.headers, timeout=30.0)
        
    def reg(self):
        resp = self.client.post("/reg").json()

        """
        {
	        'id': '',
	        'type': 'a',
	        'name': '',
	        'account': {
	        	'id': '',
	        	'account_type': 'free',
	        	'premium_data': 0,
	        	'quota': 0,
	        	'usage': 0,
	        	'warp_plus': True,
	        	'referral_count': 0,
	        	'referral_renewal_countdown': 0,
	        	'role': 'child',
	        	'license': ''
	        },
	        'token': '5223065a-b221-4753-b243-77394344253e',
	        'warp_enabled': False,
	        'waitlist_enabled': False,
	        'place': 0,
	        'locale': 'zh-CN',
	        'enabled': True,
	        'install_id': ''
        }
        """
        print(resp)
        self.token = resp["token"]
        self.deviceId = resp["id"]
        self.license = resp['account']['license']
        self.headers["Authorization"] = f"Bearer {self.token}"
        self.client = httpx.Client(base_url="https://api.cloudflareclient.com/v0a2223", headers=self.headers, timeout=30.0)
        return resp
    

    def get_device(self):
        return self.client.get(f"reg/{self.deviceId}").json()

    def unreg(self):
        return self.client.delete(f"/reg/{self.deviceId}")

    def get_account(self):
        return self.client.get(f"reg/{self.deviceId}/account").json()
    
    def get_account_devices(self):
        return self.client.get(f"reg/{self.deviceId}/account/devices").json()
    
    def get_client_config(self):
        return self.client.get(f"client_config").json()

    def set_device_active(self):
        payload = {"active": True}
        return self.client.patch(f"reg/{self.deviceId}/account/reg/{self.deviceId}",json=payload)

    def set_device_name(self,name):
        payload = {"name": f"{name}"}
        return self.client.patch(f"reg/{self.deviceId}/account/reg/{self.deviceId}",json=payload)

    def set_license_key(self,license):
        payload = {"license": f"{license}"}
        return self.client.put(f"reg/{self.deviceId}/account",json=payload)

    def set_public_key(self,key):
        payload = {"key": f"{key}"}
        return self.client.patch(f"reg/{self.deviceId}",json=payload)

    def set_referrer(self,referrer):
        #referrer -> license_key
        payload={"referrer": f"{referrer}"}
        return self.client.patch(f"reg/{self.deviceId}/account/license",json=payload)

def clone_key(source_license,pubkey=None):
    target = WarpApi()
    target.reg()
    helper = WarpApi()
    helper.reg()

    target.set_referrer(helper.deviceId)
    helper.unreg()

    target_license = target.license 
    target.set_license_key(source_license)
    target.set_license_key(target_license)
    print(target.get_account())
    if pubkey:
        target.set_public_key(pubkey)
    else:
        target.unreg()
    return target_license
