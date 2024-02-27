import iperf3
import json

from .utils import Utils
from typing import Any, Dict

class Tester:
    def __init__(self, host: str, t: int) -> None:
        self.host = host
        self.time = t
        self.best = 0
        self.best_chan = 0

        # pyre-ignore[4]:
        self.results: Dict[int, Any] = {}


    # pyre-ignore[3]:
    def get_results(self) -> Dict[int, Any]:
        return self.results

    def run(self, chan: int) -> None:
        print("-- Running test")
        client = iperf3.Client()
        client.duration = int(self.time)
        client.server_hostname = self.host
        client.port = 5201
        res = client.run()
        o = json.loads(res.text)
        self.results[chan] = o
        summary = o["end"]["sum_sent"]["bits_per_second"]

        if summary > self.best:
            self.best = summary
            self.best_chan = chan

        print(
            f"   done (curr: {Utils.mbps(summary)}) best: {Utils.mbps(self.best)} on {self.best_chan}"
        )
