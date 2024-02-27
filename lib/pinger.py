from icmplib import ping


class Pinger:
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
