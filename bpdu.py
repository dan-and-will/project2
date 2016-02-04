from datetime import datetime, timedelta
import json

TIMEOUT = timedelta(seconds=.75)
FORMAT = {"source":"02a1", "dest":"ffff", "type": "bpdu",
      "message":{"root":"02a1", "cost":3}}

class Bpdu:

    def __init__(self, root, cost, bid):
        self.root = root
        self.cost = cost
        self.bid = bid
        self.time_created = datetime.now()

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

    def __str__(self):
        packet = {'source': self.bid, 'dest': 'ffff', 'type': 'bpdu',
                    'message': {'root': self.root, 'cost': self.cost}}
        return json.dumps(packet)
