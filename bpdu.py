from datetime import datetime, timedelta
import json

TIMEOUT = timedelta(seconds=.75)

class Bpdu:

    def __init__(self, root, cost, bid, pid):
        self.root = root
        self.cost = cost
        self.bid = bid
        self.pid = pid
        self.time_updated = datetime.now()

    def compare(self, other):
        """return tuple
        first el is self is better than other
        second el is port should be enabled
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        if self.root < other.root:
            return (False, True)
        elif self.root == other.root:
            if self.cost < other.cost:
                return (False, True)
            elif self.cost == other.cost:
                if self.bid > other.bid:
                    return (False, False)
                elif self.bid == other.bid and self.pid < other.pid:
                    return (False, False)
        return (True, False)

    def create(self, pid):
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'id': pid, 'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)

    def is_timedout(self):
        return datetime.now() - self.time_updated > TIMEOUT
