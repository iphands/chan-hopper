import subprocess
import time


class NetworkManager:
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    def try_reconnect(self) -> None:
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

    def wait_for_chan(self, chan: int) -> bool:
        print(f"-- Waiting for channel switch: {chan}")
        start = time.time()
        for _ in range(0, 300):
            for _ in range(1, 100):
                out = subprocess.check_output(["iw", "dev"])
                out = str(out)
                if f"channel {chan}" in out:
                    end = time.time()
                    delta = (end - start) * 1000
                    delta = "{:.2f}".format(delta)
                    print(f"   channel switch hit after {delta}ms")
                    return True
                time.sleep(0.1)
                continue
            self.try_reconnect()
            time.sleep(1)
        print("   wait_for_chan failed!")
        return False
