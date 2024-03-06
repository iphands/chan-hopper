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

        retried = False
        for i in range(0, 100):
            try:
                res = ping(
                    host,
                    count=10,
                    interval=0.250,
                    timeout=0.100,
                    id=None,
                    source=None,
                    family=None,
                    privileged=False,
                )

                if res.packet_loss != 0.0:
                    Say.mid(".")
                    retried = True
                    continue

                if retried:
                    Say.mid(" ")

                Say.end()
                return
            except:
                pass
