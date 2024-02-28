import click
import json
import time

from lib.tester import Tester
from lib.client import Client
from lib.pinger import Pinger
from lib.nm import NetworkManager
from lib.utils import Say, Utils


@click.command()
@click.option("--ap-id", help="The ID of the AP in Unif controller", required=True)
@click.option("--unifi-host", help="Hostname of the Unifi controller", required=True)
@click.option("--iperf-host", help="Hostname of the iperf3 server", required=True)
@click.option("--mode", type=click.Choice(["2", "5"]), help="2.4Ghz or 5Ghz mode", required=True)
@click.option("--nm-uuid", help="UUID of NetworkManager connection to activate", required=True)
@click.option("--time", "t", default=90, help="Time in seconds to run each iperf3 test")
def main(
    ap_id: str, unifi_host: str, iperf_host: str, mode: int, nm_uuid: str, t: int = 90
) -> None:
    start = time.time()
    channels_two, channels_five = Utils.get_channels()
    chans = channels_two
    if mode == "5":
        channels_five

    # chans = [1]

    client = Client(ap_id, unifi_host)
    nm = NetworkManager(nm_uuid)
    tester = Tester(iperf_host, t)

    for chan in chans:
        Say.start("Changing to channel: {chan}\n")
        client.change_chan(chan, 124)
        if not nm.wait_for_chan(chan):
            continue
        Pinger.wait_for_ping(iperf_host)
        time.sleep(5)  # settle just a bit
        tester.run(chan)

    end = time.time()
    delta = end - start
    Say.start("\nDone!\n")
    print("Run took {:.2f}s".format(delta))
    out_file = f"results.{int(start)}.json"
    with open(out_file, "w") as f:
        f.write(json.dumps(tester.get_results()))
        print(f"Wrote results to: {out_file}")


if __name__ == "__main__":
    main()
