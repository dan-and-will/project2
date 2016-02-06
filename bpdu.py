from datetime import datetime, timedelta
import json

TIMEOUT = timedelta(seconds=.75)

class Bpdu:

    def __init__(self, root, cost, bid):
        self.root = root
        self.cost = cost
        self.bid = bid
        self.time_updated = datetime.now()

    def compare(self, other):
        """return tuple
        first el is self is better than other
        second el is port should be enabled
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        if self.root < other.root:
            return (True, True)
        if self.root == other.root and self.cost < other.cost:
            return (True, False)
        if self.root == other.root and self.cost == other.cost and self.bid < other.bid:
            return (True, False)
        return (False, True)

    def create(self, pid):
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'id': pid, 'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)

    def is_timedout(self):
        return datetime.now() - self.time_updated > TIMEOUT
