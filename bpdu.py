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
        first el is use other BPDU
        second el is port should be enabled
        """
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        print 'compare roots'
        print self.create(None)
        print other.create(None)
        if self.root < other.root:
            return (False, True)
        elif self.root == other.root:
            if self.cost < other.cost:
                # other is a child node
                return (False, True)
            elif self.cost == other.cost:
                # other is a sibling node
                if self.bid < other.bid:
                    return (False, True)
                else:
                    return (False, False)
            elif self.cost == other.cost + 1:
                # using other will result in path of same cost
                return (False, False)
        return (True, True)

    def create(self, pid):
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'id': pid, 'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)

    def is_timedout(self):
        return datetime.now() - self.time_updated > TIMEOUT
