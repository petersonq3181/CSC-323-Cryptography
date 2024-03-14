
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
                elif data['type'] == self.BLOCK:
                    valid_block = self.validate_block(data)
                    print('validated block returned: ', valid_block)
                    


    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def validate_block(self, data):
        try:

            # a. check if all required fields are present
            print(f'\tin validate_block a')
            required_block_fields = ["type", "id", "nonce", "pow", "prev", "tx"]
            for field in required_block_fields:
                if field not in data:
                    print('failed check a')
                    return False
            
            # b. check if the type field is 0
            print(f'\tin validate_block b')
            if data["type"] != self.BLOCK:
                print('failed check b')
                return False
            
            # c. verify the block ID
            print(f'\tin validate_block c')
            computed_id = hashlib.sha256(json.dumps(data["tx"], sort_keys=True).encode('utf8')).hexdigest()
            if data["id"] != computed_id:
                print('failed check c')
                return False
            
            # f.i. 
            # i. 
            print(f'\t\tin validate_block f. i')
            tx = data["tx"]
            required_tx_fields = ["type", "input", "sig", "output"]
            for field in required_tx_fields:
                if field not in tx:
                    print('failed check f i')
                    return False
            
            # ----- meta useful info 
            # 1 finding index of current passed in block, in blockchain 
            #   (must find, b/c this is called in function where we can't also pass an index)
            found = False
            for blockchain_idx, b in enumerate(self.blockchain): 
                if b['id'] == data['id']:
                    found = True
                    break 
            if not found or blockchain_idx < 1:
                print('could not find current block in blockchain')
                return False 
            # 2 find prev block 
            prev_block = self.blockchain[blockchain_idx - 1]
            # 3 find current block's tx's input block 
            # (and part of f iii)
            input_block_id = data['tx']['input']['id']
            found = False
            for input_block_idx, b in enumerate(self.blockchain): 
                if b['id'] == input_block_id:
                    found = True
                    break 
            if not found:
                print('failed check f iii, no valid block')
                return False 
            input_block = self.blockchain[input_block_idx]

            # d. check if prev stores the block ID of the preceding block
            if data['prev'] != prev_block['id']:
                print('failed check d')
                return False
            
            # e. validate the proof-of-work
            print(f'\tin validate_block e')
            utx = json.dumps(data["tx"], sort_keys=True).encode('utf8')
            nonce = data["nonce"].encode('utf8')
            prev_id = data["prev"].encode('utf8')
            pow_computed = hashlib.sha256(utx + prev_id + nonce).hexdigest()
            if int(pow_computed, 16) > self.DIFFICULTY:
                print('failed check e')
                return False

            # ----- f. validate the transaction
            print(f'\tin validate_block f')
            
            # ii. 
            print(f'\t\tin validate_block f. ii')
            if tx["type"] != self.TRANSACTION:
                print('failed check f ii')
                return False

            # iii. (part of it's above)
            print(f'\t\tin validate_block f. iii')
            if 'tx' in input_block and 'output' in input_block['tx']:
                if data['tx']['input']['n'] + 1 > len(input_block['tx']['output']):
                    print('failed check f iii, does not refer to valid output')
                    return False 
            
            # iv. there is no other valid transaction referring to the
            # same output currently in the blockchain
            print(f'\t\tin validate_block f. iv')
            out_id = data['tx']['input']['id']
            out_n = data['tx']['input']['n']
            for b in self.blockchain:
                if 'tx' in b and 'input' in b['tx'] and 'id' in b['tx']['input'] and 'n' in b['tx']['input']:
                    if b['tx']['input']['id'] == out_id and b['tx']['input']['id'] == out_n:
                        print('failed check f iv')
                        return False 

            # v. value of the input equals the sum of the outputs 
            # (Assuming input and output both from the given block?)
            print(f'\t\tin validate_block f. v')
            output_sum = sum(out['value'] for out in tx['output'] if out['value'] != 50) # TODO (don't know if i need to exclude coinbase)
            if 'tx' in input_block and 'output' in input_block['tx'] and len(input_block['tx']['output']) >= out_n + 1:
                input_val = input_block['tx']['output'][out_n]['value']

                if input_val != output_sum:
                    print('failed check f v')
                    return False 
                    
            # vi.
            print(f'\t\tin validate_block f. vi')
            nouts = len(tx["output"])
            # "There should be no more than two outputs and no fewer than one output for any unverified transaction (not
            # including the coinbase transaction which is added by the miner, described later)"
            if (not (1 <= nouts <= 3)) or (not (all('value' in item and isinstance(item['value'], int) and item['value'] > 0 for item in tx['output']))): 
                print('failed check f vi')
                return False 
            
            # vii. 
            print(f'\t\tin validate_block f. vii')
            if tx['output'][-1]['value'] != 50: 
                print('failed check f vii')
                return False 
            
            # viii. 
            input_output = None
            if 'tx' in input_block and 'output' in input_block['tx']:
                if len(input_block['tx']['output']) <= out_n + 1:
                    input_output = input_block['tx']['output'][out_n]
            if input_output is None: 
                print('failed check f viii (first part)')
                return False     

            vk = VerifyingKey.from_string(bytes.fromhex(input_output['pub_key']))
            viii = vk.verify(bytes.fromhex(tx['sig']), json.dumps(tx['input'], sort_keys=True).encode('utf8'))
            if not viii: 
                print('failed check f viii (second part)')
                return False
            

            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            print('failed validate_block try()')
            return False


def mine_transaction(utx, prev):
    static_part = json.dumps(utx, sort_keys=True).encode('utf8') + json.dumps(prev, sort_keys=True).encode('utf8')
    
    nonce = Random.new().read(AES.block_size).hex()

    print(f'Mining ... .....')

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
        x = input("\t0: Print keys\n\t1: Print blockchain\n\t2: Print UTX pool\n\t3: Enter UTX\n\t4: Mine\n\nEnter your choice -> ")
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

        elif x == 3:

            # for now, just links a utx to the last block in the block chain
            # and just make the utx for myself 
            last_block = client.blockchain[-1]

            injson = { 'id': last_block['id'], 'n': 2 }
            sig = sk.sign(json.dumps(injson, sort_keys=True).encode('utf8')).hex()
            myutx = {
                'type': 1,
                'input': injson,
                'sig': sig,
                'output': [{
                    'value': 2,
                    'pub_key': my_pub
                }]
            }

            client.send_to_nodes(myutx)

        elif x == 4: 
            # # TODO verify the UTX chosen ? diff verification than entire block verification? 

            # mineutx = client.utx[-1]
            # mineutx['output'].append({'value': ZachCoinClient.COINBASE, 'pub_key': my_pub})        
            # prev = client.blockchain[-1]
            # pow, nonce = mine_transaction(mineutx, json.dumps(prev, sort_keys=True))

            # block_id = hashlib.sha256(json.dumps(mineutx,
            #     sort_keys=True).encode('utf8')).hexdigest()
            # zc_block = {
            #     "type": 0,
            #     "id": block_id,
            #     "nonce": nonce,
            #     "pow": pow,
            #     "prev": prev['id'],
            #     "tx": mineutx
            # }
            # client.send_to_nodes(zc_block)
            
            # print('got here!')

        
            client.send_to_nodes(client.blockchain[-1])


    
            


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

        
        # print(my_pub)



        input()
        
if __name__ == "__main__":
    main()