
import sys, time, json, os, hashlib
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from Crypto import Random
from Crypto.Cipher import AES

SERVER_ADDR = "zachcoin.net"
SERVER_PORT = 9067

class ZachCoinClient (Node):
    
    #ZachCoin Constants
    BLOCK = 0
    TRANSACTION = 1
    BLOCKCHAIN = 2
    UTXPOOL = 3
    COINBASE = 50
    DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    #Hardcoded gensis block
    blockchain = [
        {
            "type": BLOCK,
            "id": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "nonce": "1950b006f9203221515467fe14765720",
            "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
            "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
            "tx": {
                "type": TRANSACTION,
                "input": {
                    "id": "0000000000000000000000000000000000000000000000000000000000000000",
                    "n": 0
                },
                "sig": "adf494f10d30814fd26c6f0e1b2893d0fb3d037b341210bf23ef9705479c7e90879f794a29960d3ff13b50ecd780c872",
                "output": [
                    {
                        "value": 50,
                        "pub_key": "c26cfef538dd15b6f52593262403de16fa2dc7acb21284d71bf0a28f5792581b4a6be89d2a7ec1d4f7849832fe7b4daa"
                    }
                ]
            }
        }
    ]
    utx = []
  
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(ZachCoinClient, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("outbound_node_connected: " + connected_node.id)
        
    def inbound_node_connected(self, connected_node):
        print("inbound_node_connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("inbound_node_disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("outbound_node_disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        #print("node_message from " + connected_node.id + ": " + json.dumps(data,indent=2))
        print("node_message from " + connected_node.id)

        if data != None:
            if 'type' in data:
                if data['type'] == self.TRANSACTION:
                    self.utx.append(data)
                    print('in node_message: successfully added tx')
                elif data['type'] == self.BLOCKCHAIN:
                    self.blockchain = data['blockchain']
                    print('in node_message: successfully updated blockchain')
                elif data['type'] == self.UTXPOOL:
                    self.utx = data['utxpool']
                    print('in node_message: successfully updated utxpool')
                #TODO: Validate blocks

    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")


def mine_transaction(utx, prev):
    static_part = json.dumps(utx, sort_keys=True).encode('utf8') + json.dumps(prev, sort_keys=True).encode('utf8')
    
    nonce = Random.new().read(AES.block_size).hex()

    while( int( hashlib.sha256(static_part + nonce.encode('utf-8')).hexdigest(), 16) > ZachCoinClient.DIFFICULTY):
        nonce = Random.new().read(AES.block_size).hex()

    pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') +
    prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest()

    print('Mining successful')
    return pow, nonce

def main():

    if len(sys.argv) < 3:
        print("Usage: python3", sys.argv[0], "CLIENTNAME PORT")
        quit()

    #Load keys, or create them if they do not yet exist
    keypath = './' + sys.argv[1] + '.key'
    if not os.path.exists(keypath):
        sk = SigningKey.generate()
        vk = sk.verifying_key
        with open(keypath, 'w') as f:
            f.write(sk.to_string().hex())
            f.close()
    else:
        with open(keypath) as f:
            try:
                sk = SigningKey.from_string(bytes.fromhex(f.read()))
                vk = sk.verifying_key
            except Exception as e:
                print("Couldn't read key file", e)

    #Create a client object
    client = ZachCoinClient("127.0.0.1", int(sys.argv[2]), sys.argv[1])
    client.debug = False

    time.sleep(1)

    client.start()

    time.sleep(1)

    my_pub = vk.to_string().hex()

    #Connect to server 
    client.connect_with_node(SERVER_ADDR, SERVER_PORT)
    print("Starting ZachCoin™ Client:", sys.argv[1])
    time.sleep(2)

    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        slogan = " You can't spell \"It's a Ponzi scheme!\" without \"ZachCoin\" "
        print("=" * (int(len(slogan)/2) - int(len(' ZachCoin™')/2)), 'ZachCoin™', "=" * (int(len(slogan)/2) - int(len('ZachCoin™ ')/2)))
        print(slogan)
        print("=" * len(slogan),'\n')
        x = input("\t0: Print keys\n\t1: Print blockchain\n\t2: Print UTX pool\n\nEnter your choice -> ")
        try:
            x = int(x)
        except:
            print("Error: Invalid menu option.")
            input()
            continue
        if x == 0:
            print("sk: ", sk.to_string().hex())
            print("vk: ", vk.to_string().hex())
        elif x == 1:
            print(json.dumps(client.blockchain, indent=1))
        elif x == 2:
            print(json.dumps(client.utx, indent=1))
        # TODO: Add options for creating and mining transactions
        # as well as any other additional features

        # # --- scratch for submitting a utx 
        # sig = sk.sign(json.dumps({
        #         'id': '9c03fc018ea43c00cd7d8e9811b08bb11a47e1f6327765912851bffd23bff298',
        #         'n': 2
        #     }, sort_keys=True).encode('utf8')).hex()
        # myutx = {
        #     'type': 1,
        #     'input': {
        #         'id': '9c03fc018ea43c00cd7d8e9811b08bb11a47e1f6327765912851bffd23bff298',
        #         'n': 2
        #     },
        #     'sig': sig,
        #     'output': [
        #         {
        #             'value': 2,
        #             'pub_key': my_pub
        #         }, 
        #     ]
        # }
        # client.send_to_nodes(myutx)

        mineutx = client.utx[-1]
        mineutx['output'].append({'value': ZachCoinClient.COINBASE, 'pub_key': my_pub})        
        prev = client.blockchain[-1]
        pow, nonce = mine_transaction(mineutx, json.dumps(prev, sort_keys=True))

        block_id = hashlib.sha256(json.dumps(mineutx,
            sort_keys=True).encode('utf8')).hexdigest()
        zc_block = {
            "type": 0,
            "id": block_id,
            "nonce": nonce,
            "pow": pow,
            "prev": prev['id'],
            "tx": mineutx
        }
        client.node_message(zc_block)
        
        
        print('got here')
    





        input()
        
if __name__ == "__main__":
    main()