import requests
import urllib3

from typing import Any, Dict, Tuple

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Client:
    def __init__(self, ap_id: str, host: str, debug: bool = False) -> None:
        self.ap_id = ap_id
        self.host = f"https://{host}"
        self.debug = debug

        self.cookies = {
            "unifises": "rGerhmyDYhUVkRaggzfBBzzKn0vCfSAl",
            "csrf_token": "hSZBMDrKl7wRbOJjEXnwH6OV7RVxdXgC",
        }

        self.headers: Dict[str, str] = {
            "authority": self.host,
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json;charset=utf-8",
            "dnt": "1",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-csrf-token": "hSZBMDrKl7wRbOJjEXnwH6OV7RVxdXgC",
        }

    def get_url(self, frag: str) -> str:
        sep = ""
        if not frag.startswith("/"):
            sep = "/"
        return f"{self.host}{sep}{frag}"

    def get_settings_data(self, chan_two: int, chan_five: int) -> Dict[str, Any]:
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

    def put(self, frag: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(
            self.get_url(frag),
            cookies=self.cookies,
            headers=self.headers,
            json=data,
            verify=False,
        )
        return response.json()

    def get(self, frag: str) -> Dict[str, Any]:
        response = requests.get(
            self.get_url(frag),
            cookies=self.cookies,
            headers=self.headers,
            verify=False,
        )
        return response.json()

    def get_current_chans(self) -> Tuple[int, int]:
        # if self.debug:
        #    return 2, 124

        o = self.get(f"/api/s/default/stat/device")
        for d in o["data"]:
            if d["_id"] == self.ap_id:
                return int(d["radio_table"][0]["channel"]), int(d["radio_table"][1]["channel"])
        raise Exception("Could not get current channels!")

    def change_chan(self, chan_two: int, chan_five: int) -> None:
        if self.debug:
            return

        # TODO fail on bad return!

        self.put(
            f"/api/s/default/rest/device/{self.ap_id}",
            self.get_settings_data(chan_two, chan_five),
        )
