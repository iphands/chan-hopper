import click
import json
import time
import sys
import getpass

from lib.tester import Tester
from lib.client import Client
from lib.pinger import Pinger
from lib.nm import NetworkManager
from lib.utils import Utils


@click.group("cli")
def cli() -> None:
    pass


@click.command()
@click.option("--unifi-host", help="Hostname of the Unifi controller", required=True)
@click.option("--user", help="Username", required=True)
def auth(unifi_host: str, user: str) -> None:
    client = Client(unifi_host)
    passw = getpass.getpass()
    client.auth(user, passw)
    pass


@click.command()
@click.option("--ap-id", help="The ID of the AP in Unif controller", required=True)
@click.option("--unifi-host", help="Hostname of the Unifi controller", required=True)
@click.option("--iperf-host", help="Hostname of the iperf3 server", required=True)
@click.option("--mode", type=click.Choice(["2", "5"]), help="2.4Ghz or 5Ghz mode", required=True)
@click.option("--nm-uuid", help="UUID of NetworkManager connection to activate", required=True)
@click.option("--time", "t", default=90, help="Time in seconds to run each iperf3 test")
@click.option("--debug", "debug", default=False, help="Dry run with mock calls")
def test(
    ap_id: str,
    unifi_host: str,
    iperf_host: str,
    mode: int,
    nm_uuid: str,
    t: int = 90,
    debug: bool = False,
) -> None:
    start = time.time()
    channels_two, channels_five = Utils.get_channels()
    chans = channels_two
    if mode == "5":
        chans = channels_five

    # chans = [1]

    client = Client(unifi_host, ap_id=ap_id, debug=debug)
    if not client.init():
        sys.exit(1)

    nm = NetworkManager(nm_uuid, debug=debug)
    tester = Tester(iperf_host, t, debug=debug)

    chan_two = chan_five = 0

    try:
        chan_two, chan_five = client.get_current_chans()
    except:
        return

    for chan in chans:
        print(f"\n#### Testing channel: {chan}")

        if mode == "5":
            chan_five = chan
        else:
            chan_two = chan

        client.change_chan(chan_two, chan_five)

        if not nm.wait_for_chan(chan):
            continue

        Pinger.wait_for_ping(iperf_host, debug)
        if not debug:
            time.sleep(5)  # settle just a bit
            tester.run(chan)

    end = time.time()
    delta = end - start
    print("\nDone!")
    print("Run took {:.2f}s".format(delta))
    out_file = f"results.{int(start)}.json"
    with open(out_file, "w") as f:
        if not debug:
            f.write(json.dumps(tester.get_results()))
            print(f"Wrote results to: {out_file}")


if __name__ == "__main__":
    cli.add_command(auth)
    cli.add_command(test)
    cli()
