import time
import paramiko

from .utils import Say


class Remote:
    def __init__(self, host: str, dev: str, debug: bool = False) -> None:
        self.host = host
        self.dev = dev
        self.debug = debug

    def wait_for_chan(self, desired_chan: int) -> bool:
        Say.start("Waiting for channel switch")
        retried = False
        for i in range(0, 100):
            try:
                client = paramiko.client.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(self.host, username="root")
                cmd = f"iw {self.dev} info | fgrep channel | awk '{{print $2}}'"
                _stdin, _stdout, _stderr = client.exec_command(cmd)
                chan = int(_stdout.read().decode())
                client.close()
                if chan == desired_chan:
                    if retried:
                        Say.mid(" ")
                    Say.end()
                    return True

                Say.mid(".")
                time.sleep(1)
                retried = True
            except Exception as e:
                Say.mid(".")
                time.sleep(1)
                retried = True

        return False
