from datetime import datetime, timedelta
import json

TIMEOUT = timedelta(seconds=.75)

class Bpdu:

    def __init__(self, root, cost, bid, next_hop):
        self.root = root
        self.cost = cost
        self.bid = bid
        self.next_hop = next_hop
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
                # other is direct parent
                if self.next_hop < other.bid:
                    return (False, False)
                elif self.next_hop == other.bid:
                    self.reset_timeout()
        return (True, True)

    def __lt__(self, other):
        if not isinstance(other, Bpdu):
            raise NotImplementedError
        print 'DO COMPARE'
        print self.create(None)
        print other.create(None)
        if self.root < other.root:
            return True
        elif self.root == other.root:
            if self.cost < other.cost:
                return True
            elif self.cost == other.cost:
                if self.bid < other.bid:
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
