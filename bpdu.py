from datetime import datetime, timedelta
import json

TIMEOUT = timedelta(seconds=.75)

class Bpdu:

    def __init__(self, root, cost, bid):
        self.root = root
        self.cost = cost
        self.bid = bid
        self.time_updated = datetime.now()

    def __lt__(self, other):
        """compare BPDUs and return whether self is better than other
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        if self.root < other.root:
            return True
        elif self.root == other.root:
            if self.cost < other.cost:
                return True
            elif self.cost == other.cost:
                if self.bid < other.bid:
                    return True
        return False

    def __eq__(self, other):
        """compare BPDUs and return whether self is the same as other
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        return self.root == other.root and self.cost == other.cost and self.bid == other.bid

    def create(self, pid):
        """create BPDU packet and include the port it is sent on
        """
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'id': pid, 'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)

    def is_timedout(self):
        """find out if the BPDU is too old
        """
        return datetime.now() - self.time_updated > TIMEOUT

    def reset_timeout(self):
        """give the BPDU more time to live
        """
        self.time_updated = datetime.now()
