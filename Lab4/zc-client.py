
import sys, time, json, os, hashlib
from ecdsa import VerifyingKey, SigningKey
from p2pnetwork.node import Node
from Crypto import Random
from Crypto.Cipher import AES
import time

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
                print(data)
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
                    print('hereeeeee:')
                    print(data)
                    print('validated block returned: ', valid_block)
                    if valid_block:
                        self.blockchain.append(data)
                    


    def node_disconnect_with_outbound_node(self, connected_node):
        print("node wants to disconnect with oher outbound node: " + connected_node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def validate_block(self, data):
        try:

            prev_block = self.blockchain[-1]

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
            print(pow_computed)
            if int(data['pow'], 16) >= self.DIFFICULTY:
                print('failed check e')
                return False

            return self.validate_tx(data['tx'])
        except Exception as e:
            print(f"An error occurred: {e}")
            print('failed validate_block try()')
            return False
        
    def validate_tx(self, tx):
        try:
            # ----- f. validate the transaction
            print(f'\tin validate_tx f')

            # i. 
            print(f'\t\tin validate_block f. i')
            required_tx_fields = ["type", "input", "sig", "output"]
            for field in required_tx_fields:
                if field not in tx:
                    print('failed check f i')
                    return False
                
            # ii. 
            print(f'\t\tin validate_tx f. ii')
            if tx["type"] != self.TRANSACTION:
                print('failed check f ii')
                return False

            # iii 
            input_block_id = tx['input']['id']
            input_block_found = False
            for input_block_idx, b in enumerate(self.blockchain): 
                if b['id'] == input_block_id:
                    input_block_found = True
                    break 
            if not input_block_found:
                print('failed check f iii, no valid input block found')
                return False 
            input_block = self.blockchain[input_block_idx]
            
            # iii. (part of it's above)
            print(f'\t\tin validate_tx f. iii')
            if 'tx' in input_block and 'output' in input_block['tx']:
                if tx['input']['n'] + 1 > len(input_block['tx']['output']):
                    print('failed check f iii, does not refer to valid output')
                    return False 
            
            # iv. there is no other valid transaction referring to the
            # same output currently in the blockchain
            print(f'\t\tin validate_tx f. iv')
            out_id = tx['input']['id']
            out_n = tx['input']['n']
            for b in self.blockchain:
                if 'tx' in b and 'input' in b['tx'] and 'id' in b['tx']['input'] and 'n' in b['tx']['input']:
                    if b['tx']['input']['id'] == out_id and b['tx']['input']['id'] == out_n:
                        print('failed check f iv')
                        return False 

            # v. value of the input equals the sum of the outputs 
            # (Assuming input and output both from the given block?)
            print(f'\t\tin validate_tx f. v')
            # output_sum = sum(out['value'] for out in tx['output'])
            output_sum = 0
            for o in tx['output'][:-1]:
                # if int(o['value']) != 50:
                output_sum += int(o['value'])
            if 'tx' in input_block and 'output' in input_block['tx'] and len(input_block['tx']['output']) >= int(out_n) + 1:
                input_val = input_block['tx']['output'][out_n]['value']

                # print('input val and output sum')
                # print(input_val, output_sum)

                if input_val != output_sum:
                    print('failed check f v')
                    return False 
                    
            # vi.
            print(f'\t\tin validate_tx f. vi')
            nouts = len(tx["output"])
            # "There should be no more than two outputs and no fewer than one output for any unverified transaction (not
            # including the coinbase transaction which is added by the miner, described later)"
            b2 = (not (all('value' in item and int(item['value']) > 0 for item in tx['output'])))
            # print('b2: ', b2)
            # print(nouts)
            if (not (1 <= nouts <= 3)) or (not (all('value' in item and int(item['value']) > 0 for item in tx['output']))): 
                print('failed check f vi')
                return False 
            
            # vii. 
            print(f'\t\tin validate_tx f. vii')
            if tx['output'][-1]['value'] != 50: 
                print('failed check f vii', tx['output'][-1]['value'], type(tx['output'][-1]['value']))
                return False 
            
            # viii. 
            print(f'\t\tin validate_tx f. viii')
            input_output = None
            if 'tx' in input_block and 'output' in input_block['tx']:
                if len(input_block['tx']['output']) <= out_n + 1:
                    input_output = input_block['tx']['output'][out_n]
            if input_output is None: 
                print('failed check f viii (first part)')
                return False     

            # vk = VerifyingKey.from_string(bytes.fromhex(input_output['pub_key']))
            # viii = vk.verify(bytes.fromhex(tx['sig']), json.dumps(tx['input'], sort_keys=True).encode('utf8'))
            # if not viii: 
            #     print('failed check f viii (second part)')
            #     return False
            
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            print('failed validate_tx try()')
            return False



# def mine_transaction(utx, prev):
#     static_part = json.dumps(utx, sort_keys=True).encode('utf8') + json.dumps(prev, sort_keys=True).encode('utf8')
    
#     nonce = Random.new().read(AES.block_size).hex()

#     print(f'Mining ... .....')
#     last_print_time = time.time()

#     while( int( hashlib.sha256(static_part + nonce.encode('utf-8')).hexdigest(), 16) > ZachCoinClient.DIFFICULTY):
#         nonce = Random.new().read(AES.block_size).hex()
        
#         if time.time() - last_print_time >= 30:
#             print('still mining...')
#             last_print_time = time.time()

#     pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') +
#     prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest()

#     print('Mining successful')
#     return pow, nonce
        
def mine_transaction(utx, prev):
    nonce = Random.new().read(AES.block_size).hex()

    static_part = int(hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') + prev.encode('utf-8')), 16)

    i = 0
    while ( int(static_part + nonce.encode('utf-8')).hexdigest(), 16) > ZachCoinClient.DIFFICULTY:
        i += 1
        if i % 100 == 0:
            print('still mining')
        nonce = Random.new().read(AES.block_size).hex()
    pow = hashlib.sha256(json.dumps(utx, sort_keys=True).encode('utf8') +
    prev.encode('utf-8') + nonce.encode('utf-8')).hexdigest()
    return pow, nonce

def mine_transaction(utx, prev):
    constant_part = json.dumps(utx, sort_keys=True).encode('utf8') + json.dumps(prev, sort_keys=True).encode('utf8')
    
    nonce = Random.new().read(AES.block_size).hex()
    
    i = 0
    while True:
        hash_hex = hashlib.sha256(constant_part + nonce.encode('utf-8')).hexdigest()
        
        if int(hash_hex, 16) <= ZachCoinClient.DIFFICULTY:
            break
        
        nonce = Random.new().read(AES.block_size).hex()

        i += 1
        if i % 100000 == 0:
            print('still mining')
    
    pow = hashlib.sha256(constant_part + nonce.encode('utf-8')).hexdigest()
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
            last_output_val = last_block['tx']['output'][-1]['value']
            last_output_n = len(last_block['tx']['output']) - 1

            injson = { 'id': last_block['id'], 'n': last_output_n }
            sig = sk.sign(json.dumps(injson, sort_keys=True).encode('utf8')).hex()
            myutx = {
                'type': 1,
                'input': injson,
                'sig': sig,
                'output': [{
                    'value': str(last_output_val),
                    'pub_key': my_pub
                }]
            }

            client.send_to_nodes(myutx)

        elif x == 4: 

            # submit a valid utx to the pool 
            last_block = client.blockchain[-1]
            last_output_val = last_block['tx']['output'][-1]['value']
            last_output_n = len(last_block['tx']['output']) - 1

            injson = { 'id': last_block['id'], 'n': last_output_n }
            sig = sk.sign(json.dumps(injson, sort_keys=True).encode('utf8')).hex()
            mineutx = {
                'type': 1,
                'input': injson,
                'sig': sig,
                'output': [{
                    'value': str(last_output_val),
                    'pub_key': my_pub
                }]
            }

            client.send_to_nodes(mineutx)

            # mine 
            mineutx['output'].append({'value': ZachCoinClient.COINBASE, 'pub_key': my_pub})        
            print('mineutx:')
            print(mineutx)
            prev = client.blockchain[-1]
            print(type(prev))
            # pow, nonce = mine_transaction(json.dumps(mineutx, sort_keys=True), json.dumps(prev, sort_keys=True))
            pow, nonce = mine_transaction(mineutx, prev)
            print('done mining')
            

            # construct and submit block 
            block_id = hashlib.sha256(json.dumps(mineutx,
                sort_keys=True).encode('utf8')).hexdigest()
            new_block = {
                "type": 0,
                "id": block_id,
                "nonce": nonce,
                "pow": pow,
                "prev": prev['id'],
                "tx": mineutx
            }

            # new_block = {'type': 0, 'id': 'cca4dc8083229c1047a701fe42534724def6fb7cf1b494e3936073e07f9d4cea', 'nonce': '8a5da448a0f4a92d6257bf8826970171', 'pow': '0000002a3c1235c13e5e23777305a8ffbf4a424d625be6b577a93cedd26f0130', 'prev': 'e6f5b54ff5d56bd84ba6a73e7427bd301a00b5ddc617decb447c45e2f2c7ecf9', 'tx': {'type': 1, 'input': {'id': 'e6f5b54ff5d56bd84ba6a73e7427bd301a00b5ddc617decb447c45e2f2c7ecf9', 'n': 2}, 'sig': '40c2f9d30e435ab8d96f186105e06d5580da39da980b18ac0f80312e69a804caa4cd0404ca5c6b231c3f28d296c59a97', 'output': [{'value': '50', 'pub_key': '75fa6f7d6263203194ed9c9111ec07c643fcdd9643507c0fdc39e2fdea6b17dd760cc9822f35688a8fdcdd1bc6c0f6a0'}, {'value': 50, 'pub_key': '75fa6f7d6263203194ed9c9111ec07c643fcdd9643507c0fdc39e2fdea6b17dd760cc9822f35688a8fdcdd1bc6c0f6a0'}]}}

            client.send_to_nodes(new_block)
            
            print('got here!')

        elif x == 5:
            # search for my public key 
            for b in client.blockchain:
                for o in b['tx']['output']:
                    print(f"\t\t {o['pub_key']}")

                    if o['pub_key'] == my_pub:
                        print(b)
                        print('Found my pub in blockchain!')
                        break 
            print('end of searching for my pub')

        
            # client.send_to_nodes(client.blockchain[-1])


    
            



        input()
        
if __name__ == "__main__":
    main()