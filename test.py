import unittest
import random

import io
import contextlib


from lib.client import Client
from lib.utils import Utils, Say
from lib.tester import Tester


class TestTester(unittest.TestCase):
    def test_run(self) -> None:
        tester = Tester("example.com", 90, debug=True)
        f = io.StringIO()
        expected = actual = ""
        with contextlib.redirect_stdout(f):
            tester.run(11)
            expected = "-- Running test: done (curr: 12.35 Mbs) best: 12.35 Mbs on 11"
            actual = f.getvalue().strip()
        self.assertEqual(expected, actual)


class TestSay(unittest.TestCase):
    def test_say(self) -> None:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Say.start("foobar")
            self.assertEqual("-- foobar: ", f.getvalue())
            Say.end()
        self.assertEqual("-- foobar: done\n", f.getvalue())


class TestUtils(unittest.TestCase):
    def test_mbps(self) -> None:
        self.assertEqual("12.35 Mbs", Utils.mbps(12345678))


class TestClient(unittest.TestCase):
    def test_get_settings_data(self) -> None:
        c = Client("foobar", "example.com")
        two = random.randrange(1, 1024)
        five = random.randrange(1, 1024)
        data = c.get_settings_data(two, five)
        self.assertEqual(two, data["radio_table"][0]["channel"])
        self.assertEqual(five, data["radio_table"][1]["channel"])

    def test_get_url(self) -> None:
        c = Client("example.com")
        self.assertEqual("https://example.com/foo", c.get_url("foo"))
        self.assertEqual("https://example.com/barfoo", c.get_url("/barfoo"))


if __name__ == "__main__":
    unittest.main()
