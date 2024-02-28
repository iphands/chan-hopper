import unittest

from lib.client import Client


class TestClient(unittest.TestCase):
    def test_get_url(self) -> None:
        c = Client("foobar", "example.com")
        self.assertEqual("https://example.com/foo", c.get_url("foo"))


if __name__ == "__main__":
    unittest.main()
