from datetime import datetime, timedelta

TIMEOUT = timedelta(seconds=5)

class ForwardingTable:

    def __init__(self):
        self.table = {}

    def write_row(self, mac_addr, port):
        """writes new row to table
        """
        self.table[mac_addr] = (port, datetime.now())

    def read_row(self, mac_addr):
        """reads row from table
        returns -1 for nonexistant rowns
        deletes row if a timeout has occurred
        """
        entry = self.table.get(mac_addr)
        if not entry:
            return -1
        if datetime.now() - entry[1] > TIMEOUT:
            del self.table[mac_addr]
            return -1
        return entry[0]

    def flush(self):
        """flushes all entries
        """
        print 'flush mcgoo'
        self.table.clear()
