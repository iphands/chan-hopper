# pyre-ignore[21]:
import iperf3
import json

from .utils import Say, Utils
from typing import Any, Dict, Type


class Tester:
    def __init__(self, host: str, t: int, debug: bool = False) -> None:
        self.host = host
        self.time = t
        self.best = 0
        self.best_chan = 0
        self.debug = debug

        # pyre-ignore[4]:
        self.results: Dict[int, Any] = {}

    # pyre-ignore[3]:
    def get_results(self) -> Dict[int, Any]:
        return self.results

    def _run(self, chan: int) -> int:
        if self.debug:
            self.results[chan] = {}
            return 12345678

        client = iperf3.Client()
        client.duration = int(self.time)
        client.server_hostname = self.host
        client.port = 5201

        res = client.run()
        o = json.loads(res.text)
        self.results[chan] = o
        return o["end"]["sum_sent"]["bits_per_second"]

    def run(self, chan: int) -> None:
        Say.start("Running test")
        summary = self._run(chan)

        if summary > self.best:
            self.best = summary
            self.best_chan = chan

        deets = (
            f"done (curr: {Utils.mbps(summary)}) best: {Utils.mbps(self.best)} on {self.best_chan}"
        )
        Say.end(deets)
