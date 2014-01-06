from ws4py.client.threadedclient import WebSocketClient
from GephiStreamer import Node,Edge,GephiStreamerManager
import json
t = GephiStreamerManager()
class DummyClient(WebSocketClient):
    #Bootstrap to register to websocket
    def opened(self):
        self.send('{"op":"unconfirmed_sub"}')
    def closed(self, code, reason=None):
        print "Closed down", code, reason
    #When we receive a new blockchain
    def received_message(self, m):
        #Loading the data as json
        data = json.loads("%s"%m)
        print "==%s=="%data['x']['hash']
        #Created the node that represent the transaction
        transactionNode = Node(data['x']['hash'],blue=1)
        #With some properties
        for prop in ['vin_sz','vout_sz','lock_time','relayed_by','tx_index','time']:
            transactionNode.property[prop]=data['x'][prop]
        #Hack to avoid "size" of the node
        transactionNode.property['transaction_size'] = data['x']['size']
        #we type our node
        transactionNode.property['type']='Transaction'
        t.add_node(transactionNode)
        #For all incomming flow
        for inp in data['x']['inputs']:
            print inp['prev_out']['addr']
            #Create a Node with properties
            inNode = Node(inp['prev_out']['addr'],red=1)
            inNode.property['type']='Wallet'
            inNode.property['time']=data['x']["time"]
            t.add_node(inNode)
            #Create an edge Wallet-[weight=value of the transaction]->Transaction
            edge = Edge(inNode,transactionNode,True,weight=inp['prev_out']['value'])
            edge.property['type'] = inp['prev_out']['type']
            t.add_edge(edge)
        print "*"
        #For all outgoing flow
        for out in  data['x']['out'] : 
            print out['addr']
            #Create a Node with properties
            outNode = Node(out['addr'],red=1)
            outNode.property['type']='Wallet'
            outNode.property['time']=data['x']["time"]
            t.add_node(outNode)
            #Create an edge Transaction-[weight=value of the transaction]->Wallet
            edge = Edge(transactionNode,outNode,True,weight=out['value'])
            edge.property['type'] = out['type']
            t.add_edge(edge)
                
                
        t.commit()

if __name__ == '__main__':
    try:
        #Using Blockchain websocket service
        #You can change it to specified your request : see https://blockchain.info/fr/api
        ws = DummyClient("wss://ws.blockchain.info/inv", protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
