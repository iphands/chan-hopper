import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Client:
    def __init__(self, host):
        self.host = host
        self.cookies = {
            "unifises": "W0SkTLVjwkR4fpuX7Wu5hnl8gYzVOCFR",
            "csrf_token": "hSZBMDrKl7wRbOJjEXnwH6OV7RVxdXgC",
        }

        self.headers = {
            "authority": "unifi-controller.noir.lan",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json;charset=utf-8",
            "dnt": "1",
            "origin": "https://unifi-controller.noir.lan",
            "referer": "https://unifi-controller.noir.lan/manage/default/devices/properties/b4:fb:e4:e1:53:11/settings",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-csrf-token": "hSZBMDrKl7wRbOJjEXnwH6OV7RVxdXgC",
        }

    def get_url(self, frag):
        url = f"{self.host}{frag}"
        # print(f"DEBUG: url: {url}")
        return url

    def get_settings_data(self, chan_two, chan_five):
        json_data = {
            "atf_enabled": False,
            "mesh_sta_vap_enabled": False,
            "radio_table": [
                {
                    "name": "ra0",
                    "ht": "20",
                    "channel": chan_two,
                    "tx_power_mode": "high",
                    "vwire_enabled": False,
                    "min_rssi_enabled": False,
                    "hard_noise_floor_enabled": False,
                    "antenna_gain": 6,
                    "sens_level_enabled": False,
                    "radio": "ng",
                },
                {
                    "name": "rai0",
                    "ht": "80",
                    "channel": chan_five,
                    "tx_power_mode": "high",
                    "vwire_enabled": False,
                    "min_rssi_enabled": False,
                    "hard_noise_floor_enabled": True,
                    "antenna_gain": 6,
                    "sens_level_enabled": False,
                    "radio": "na",
                },
            ],
            "mesh_uplink_1": "",
            "mesh_uplink_2": "",
            "name": "",
            "config_network": {
                "type": "dhcp",
                "bonding_enabled": False,
            },
        }

        return json_data

    def put(self, frag, data):
        response = requests.put(
            self.get_url(frag),
            cookies=self.cookies,
            headers=self.headers,
            json=data,
            verify=False,
        )
        return response.json()

    def get(self, frag):
        response = requests.get(
            self.get_url(frag),
            cookies=self.cookies,
            headers=self.headers,
            verify=False,
        )
        return response.json()

    def change_chan(self, chan_two, chan_five):
        return self.put(
            "/api/s/default/rest/device/5de8531246e0fb00f79da35c",
            self.get_settings_data(chan_two, chan_five),
        )
