import unittest
import random

from lib.client import Client


class TestClient(unittest.TestCase):
    def test_get_settings_data(self) -> None:
        c = Client("foobar", "example.com")
        two = random.randrange(1, 1024)
        five = random.randrange(1, 1024)
        data = c.get_settings_data(two, five)
        self.assertEqual(two, data["radio_table"][0]["channel"])
        self.assertEqual(five, data["radio_table"][1]["channel"])

    def test_get_url(self) -> None:
        c = Client("foobar", "example.com")
        self.assertEqual("https://example.com/foo", c.get_url("foo"))
        self.assertEqual("https://example.com/barfoo", c.get_url("/barfoo"))


if __name__ == "__main__":
    unittest.main()
