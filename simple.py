from ws4py.client.threadedclient import WebSocketClient
from GephiStreamer import Node,Edge,GephiStreamerManager
import json
t = GephiStreamerManager()
class DummyClient(WebSocketClient):
    def opened(self):
        self.send('{"op":"unconfirmed_sub"}')
    def closed(self, code, reason=None):
        print "Closed down", code, reason

    def received_message(self, m):
        print "===="
        inNode = []
        outNode = []
        data = json.loads("%s"%m)
        #Get All in Nodes of the transaction
        for inp in data['x']['inputs']:
            print inp['prev_out']['addr']
            inNode+=[Node(inp['prev_out']['addr'])]
        print "*"
        #Get All out Nodes of the transaction
        for out in  data['x']['out'] : 
            print out['addr']
            outNode += [Node(out['addr'])]
        #Graph All the Things !
        for n in inNode:
            t.add_node(n)
            for o in outNode:
                t.add_node(o)
                t.add_edge(Edge(n,o,True))
        t.commit()
         
if __name__ == '__main__':
    try:
        ws = DummyClient("wss://ws.blockchain.info/inv", protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
