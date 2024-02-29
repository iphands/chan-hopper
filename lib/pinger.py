# pyre-ignore[21]:
from icmplib import ping
from .utils import Say


class Pinger:

    @staticmethod
    def wait_for_ping(host: str, debug: bool = False) -> None:
        Say.start("Waiting for ping")
        if debug:
            Say.end()
            return

        for i in range(0, 100):
            try:
                ping(
                    host,
                    count=4,
                    interval=0.250,
                    timeout=2,
                    id=None,
                    source=None,
                    family=None,
                    privileged=False,
                )
                Say.end()
                return
            except:
                pass
