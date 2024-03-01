import json

def mbps(n):
    return '{:.2f}'.format(n / 1000 / 1000)

print('chan, sent, recv, max_rtt, min_rtt, mean_rtt, retrans')
with open('results.json', 'r') as f:
    o = json.loads(f.read())
    for chan, data in o.items():
        s_bps  = data["end"]["sum_sent"]["bits_per_second"]
        r_bps  = data["end"]["sum_received"]["bits_per_second"]
        s_mbps = mbps(s_bps)
        r_mbps = mbps(r_bps)

        sender = data["end"]["streams"][0]["sender"]
        max_rtt  = sender["max_rtt"]
        min_rtt  = sender["min_rtt"]
        mean_rtt = sender["mean_rtt"]
        retrans  = sender["retransmits"]

        # print(f'-- {chan}')
        # print(f'  {sent_mbps}')
        print(f'{chan}, {s_mbps}, {r_mbps}, {max_rtt}, {min_rtt}, {mean_rtt}, {retrans}')
