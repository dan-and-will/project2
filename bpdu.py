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
        """return True if self is the better BPDU
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        if self.root < other.root:
            return True
        if self.root == other.root and self.cost < other.cost:
            return True
        if self.root == other.root and self.cost == other.cost and self.bid < other.bid:
            return True
        return False

    def create(self, pid):
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'id': pid, 'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)

    def is_timedout(self):
        return datetime.now() - self.time_updated > TIMEOUT

    def reset_timeout(self):
        self.time_updated = datetime.now()
