import click
import requests
import iperf3
import json
import time
import subprocess

from icmplib import ping

results = {}
best = 0
best_chan = 0

channels_two = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

channels_five = [
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    64,
    100,
    104,
    108,
    112,
    116,
    120,
    124,
    128,
    132,
    136,
    140,
    144,
    149,
    153,
    157,
    161,
    165,
]


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


def mbps(n):
    return "{:.2f} Mbs".format(n / 1000 / 1000)


def run_test(chan):
    global best
    global best_chan

    print("-- Running test")
    client = iperf3.Client()
    client.duration = 90
    client.server_hostname = "noir.lan"
    client.port = 5201
    res = client.run()
    o = json.loads(res.text)
    results[chan] = o
    summary = o["end"]["sum_sent"]["bits_per_second"]

    if summary > best:
        best = summary
        best_chan = chan

    print(f"   done (curr: {mbps(summary)}) best: {mbps(best)} on {best_chan}")


def try_reconnect(uuid):
    print("-- ERROR: trying reconnect!")
    for _ in range(0, 100):
        try:
            subprocess.check_output(["nmcli", "conn", "down", uuid])
            time.sleep(1)
            subprocess.check_output(["nmcli", "conn", "up", uuid])
            time.sleep(1)
            break
        except:
            pass


def wait_for_chan(chan):
    print(f"-- Waiting for channel switch: {chan}")
    for i in range(0, 300):
        out = subprocess.check_output(["iw", "dev"])
        out = str(out)
        if f"channel {chan}" in out:
            print(f"   channel switch hit after {i}s")
            return True
        if i % 2 == 0:
            try_reconnect()
            time.sleep(1)

    # assert False, "wait_for_chan failed!"
    print("   wait_for_chan failed!")
    return False


def wait_for_ping():
    print("-- Waiting for ping:")
    for i in range(0, 100):
        try:
            ping(
                "noir.lan",
                count=4,
                interval=0.250,
                timeout=2,
                id=None,
                source=None,
                family=None,
                privileged=False,
            )
            print("   done")
            return
        except:
            pass


@click.command()
@click.option("--host", help="Base URL for host of unifi controller", required=True)
@click.option(
    "--mode", type=click.Choice(["2", "5"]), help="2.4Ghz or 5Ghz mode", required=True
)
@click.option(
    "--nm-uuid", help="UUID of NetworkManager connection to activate", required=True
)
def main(host, mode, nm_uuid):
    chans = channels_two
    if mode == "5":
        channels_five

    client = Client(host)

    for chan in chans:
        print(f"-- Changing to channel: {chan}")
        client.change_chan(chan, 124)
        if not wait_for_chan(chan):
            results[chan] = False
            continue
        wait_for_ping()
        time.sleep(5)  # settle just a bit
        run_test(chan)

    with open("results.json", "w") as f:
        f.write(json.dumps(results))


if __name__ == "__main__":
    main()
