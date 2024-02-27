class Utils:
    def get_channels():
        channels_two = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # fmt: off
        channels_five = [
            36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124,
            128, 132, 136, 140, 144, 149, 153, 157, 161, 165,
        ]
        # fmt: on

        return channels_two, channels_five

    def mbps(n):
        return "{:.2f} Mbs".format(n / 1000 / 1000)
