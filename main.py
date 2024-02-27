import click
import json
import time
import subprocess

from lib.tester import Tester
from lib.client import Client

from icmplib import ping

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




class NetworkManager:
    def __init__(self, uuid):
        self.uuid = uuid

    def try_reconnect(self):
        print("-- ERROR: trying reconnect!")
        for _ in range(0, 100):
            try:
                try:
                    # Note this will fail if not already active
                    # in that case its okay to continue with up
                    subprocess.check_output(["nmcli", "conn", "down", self.uuid])
                except:
                    pass
                time.sleep(1)
                subprocess.check_output(["nmcli", "conn", "up", self.uuid])
                time.sleep(1)
                break
            except:
                pass

    def wait_for_chan(self, chan):
        print(f"-- Waiting for channel switch: {chan}")
        start = time.time()
        for _ in range(0, 300):
            for _ in range(1, 100):
                out = subprocess.check_output(["iw", "dev"])
                out = str(out)
                if f"channel {chan}" in out:
                    end = time.time()
                    delta = (end - start) * 1000
                    delta = '{:.2f}'.format(delta)
                    print(f"   channel switch hit after {delta}ms")
                    return True
                time.sleep(0.1)
                continue
            self.try_reconnect()
            time.sleep(1)
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
@click.option("--ap-id", help="The ID of the AP in Unif controller", required=True)
@click.option("--unifi-host", help="Hostname of the Unifi controller", required=True)
@click.option("--iperf-host", help="Hostname of the iperf3 server", required=True)
@click.option(
    "--mode", type=click.Choice(["2", "5"]), help="2.4Ghz or 5Ghz mode", required=True
)
@click.option(
    "--nm-uuid", help="UUID of NetworkManager connection to activate", required=True
)
@click.option("--time", "t", default=90, help="Time in seconds to run each iperf3 test")
def main(ap_id, unifi_host, iperf_host, mode, nm_uuid, t=90):
    start = time.time()
    chans = channels_two
    if mode == "5":
        channels_five

    # chans = [1]

    client = Client(f"https://{unifi_host}")
    nm = NetworkManager(nm_uuid)
    tester = Tester(unifi_host, t)

    for chan in chans:
        print(f"-- Changing to channel: {chan}")
        client.change_chan(chan, 124)
        if not nm.wait_for_chan(chan):
            continue
        wait_for_ping()
        time.sleep(5)  # settle just a bit
        tester.run(chan)

    end = time.time()
    delta = end - start
    print('\nDone!')
    print('Run took {:.2f}s'.format(delta))
    out_file = f'results.{int(start)}.json'
    with open(out_file, "w") as f:
        f.write(json.dumps(tester.get_results()))
        print(f'Wrote results to: {out_file}')


if __name__ == "__main__":
    main()
