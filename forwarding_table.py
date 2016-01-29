from datetime import datetime, timedelta

TIMEOUT = timedelta(seconds=5)
now = datetime.now

class ForwardingTable:

    def __init__(self):
        self.table = {}

    def write_row(self, mac_addr, port):
        self.table[mac_addr] = (port, now())

    def read_row(self, mac_addr):
        entry = self.table.get(mac_addr)
        if not entry:
            return -1
        if now() - entry[1] > TIMEOUT:
            del self.table[mac_addr]
            return -1
        return entry[0]
