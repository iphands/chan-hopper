import json
import sys
import os


def mbps(n: int) -> str:
    return "{:.2f}".format(n / 1000 / 1000)


# print("chan, sent, recv, max_rtt, min_rtt, mean_rtt, retrans")
def process(fname: str, dt: str) -> None:
    with open(fname, "r") as f:
        o = json.loads(f.read())
        for chan, data in o.items():
            s_bps = data["end"]["sum_sent"]["bits_per_second"]
            r_bps = data["end"]["sum_received"]["bits_per_second"]
            s_mbps = mbps(s_bps)
            r_mbps = mbps(r_bps)

            sender = data["end"]["streams"][0]["sender"]
            max_rtt = sender["max_rtt"]
            min_rtt = sender["min_rtt"]
            mean_rtt = sender["mean_rtt"]
            retrans = sender["retransmits"]

            # print(f'-- {chan}')
            # print(f'  {sent_mbps}')
            if dt:
                print(
                    f"{dt}, {chan}, {s_mbps}, {r_mbps}, {max_rtt}, {min_rtt}, {mean_rtt}, {retrans}"
                )
                continue
            print(f"{chan}, {s_mbps}, {r_mbps}, {max_rtt}, {min_rtt}, {mean_rtt}, {retrans}")


def process_all(path: str) -> None:
    files = [f for f in os.listdir(path) if "json" in f]
    for f in files:
        dt = f.split(".")[1]
        process(f"{path}/{f}", dt=dt)


if __name__ == "__main__":
    if sys.argv[1] == "many":
        process_all(sys.argv[2])
        sys.exit(0)

    process(sys.argv[1])
