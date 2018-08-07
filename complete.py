from ws4py.client.threadedclient import WebSocketClient
from gephistreamer import graph
from gephistreamer import streamer
import json
import random
t = streamer.Streamer(streamer.GephiREST(port=8080))
class DummyClient(WebSocketClient):
    #Bootstrap to register to websocket
    def opened(self):
        self.send('{"op":"unconfirmed_sub"}')
    def closed(self, code, reason=None):
        print("Closed down", code, reason)
    #When we receive a new blockchain
    def received_message(self, m):
        #Loading the data as json
        data = json.loads(str(m))
        print(json.dumps(data, sort_keys=True, indent=4))

        #Created the node that represent the transaction
        transactionNode = graph.Node(data['x']['hash'],blue=1,x = random.randint(0,500),y= random.randint(0,500))
        #With some properties
        for prop in ['vin_sz','vout_sz','lock_time','relayed_by','tx_index','time']:
            transactionNode.property[prop]=data['x'][prop]
        #Hack to avoid "size" of the node
        transactionNode.property['transaction_size'] = data['x']['size']
        #we type our node
        transactionNode.property['type']='Transaction'

        #For all incomming flow
        inN = [ graph.Node(inp['prev_out']['addr'],red=1, x = random.randint(0,500),y= random.randint(0,500),type="Wallet",time=data['x']["time"]) for inp in data['x']['inputs']]
        inE = [ graph.Edge(inp['prev_out']['addr'],transactionNode,True,weight=inp['prev_out']['value'],type=inp['prev_out']['type']) for inp in data['x']['inputs'] ]

        #For all outgoing flow
        outN = [ graph.Node(out['addr'],red=1,type="Wallet",time=data['x']["time"],x = random.randint(0,500),y= random.randint(0,500)) for out in  data['x']['out'] ] 
        outE = [graph.Edge(transactionNode,out['addr'],True,weight=out['value'],type=out['type']) for out in  data['x']['out']  ]    

        t.add_node(transactionNode,*inN,*outN)
        t.add_edge(*inE,*outE)

if __name__ == '__main__':
    try:
        #Using Blockchain websocket service
        #You can change it to specified your request : see https://blockchain.info/fr/api
        ws = DummyClient("wss://ws.blockchain.info/inv", protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
