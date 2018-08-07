from ws4py.client.threadedclient import WebSocketClient
from gephistreamer import graph
from gephistreamer import streamer
import json
import random
import itertools

t = streamer.Streamer(streamer.GephiREST(port=8080))
class DummyClient(WebSocketClient):
    def opened(self):
        self.send('{"op":"unconfirmed_sub"}')
    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, m):
        inNode = []
        outNode = []
        data = json.loads(str(m))
        print(json.dumps(data, sort_keys=True, indent=4))
        #Get All in Nodes of the transaction
        inNode = [graph.Node(inp['prev_out']['addr'],x = random.randint(0,500),y= random.randint(0,500)) for inp in data['x']['inputs']]
        #Get All out Nodes of the transaction
        outNode = [ graph.Node(out['addr'],x = random.randint(0,500),y= random.randint(0,500)) for out in  data['x']['out'] ] 
          
        #Graph All the Things !
        t.add_node(*inNode,*outNode)
        t.add_edge(*[ graph.Edge(n,o,True) for n,o in itertools.product(inNode,outNode) ])

if __name__ == '__main__':
    try:
        ws = DummyClient("wss://ws.blockchain.info/inv", protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
