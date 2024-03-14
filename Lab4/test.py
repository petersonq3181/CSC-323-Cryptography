import hashlib, json
from ecdsa import VerifyingKey, SigningKey

BLOCK = 0
TRANSACTION = 1
DIFFICULTY = 0x0000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

sk = SigningKey.generate()

blockchain = []


# ----
# b1
b1 = {
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


# ----
# b2 
# note: not making nonce and pow legit for now 

prev_id = b1['id']

input_json = { 'id': prev_id, 'n': 0 }
sig = sk.sign(json.dumps(input_json, sort_keys=True).encode('utf8')).hex()

b2tx = {
    "type": TRANSACTION,
    "input": input_json,
    "sig": sig,
    "output": [
        {
            "value": 50,
            "pub_key": "75fa6f7d6263203194ed9c9111ec07c643fcdd9643507c0fdc39e2fdea6b17dd760cc9822f35688a8fdcdd1bc6c0f6a0"
        }
    ]
}

b2id = hashlib.sha256(json.dumps(b2tx, sort_keys=True).encode('utf8')).hexdigest()

b2 = {
    "type": BLOCK,
    "id": b2id, 
    "nonce": "1950b006f9203221515467fe14765720",
    "pow": "00000027e2eb250f341b05ffe24f43adae3b8181739cd976ea263a4ae0ff8eb7",
    "prev": "b4b9b8f78ab3dc70833a19bf7f2a0226885ae2416d41f4f0f798762560b81b60",
    "tx": b2tx
}



def validate_block(data):
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
        if data["type"] != BLOCK:
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
        for blockchain_idx, b in enumerate(blockchain): 
            if b['id'] == data['id']:
                found = True
                break 
        if not found or blockchain_idx < 1:
            print('could not find current block in blockchain')
            return False 
        # 2 find prev block 
        prev_block = blockchain[blockchain_idx - 1]
        # 3 find current block's tx's input block 
        # (and part of f iii)
        input_block_id = data['tx']['input']['id']
        found = False
        for input_block_idx, b in enumerate(blockchain): 
            if b['id'] == input_block_id:
                found = True
                break 
        if not found:
            print('failed check f iii, no valid block')
            return False 
        input_block = blockchain[input_block_idx]


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
        if int(pow_computed, 16) > DIFFICULTY:
            print('failed check a')
            return False

        # ----- f. validate the transaction
        print(f'\tin validate_block f')
        
            
        # ii. 
        if tx["type"] != TRANSACTION:
            print('failed check f ii')
            return False

        # iii. (part of it's above)
        if 'tx' in input_block and 'output' in input_block['tx']:
            if data['tx']['input']['n'] + 1 > len(input_block['tx']['output']):
                print('failed check f iii, does not refer to valid output')
                return False 
        
        # iv. there is no other valid transaction referring to the
        # same output currently in the blockchain
        out_id = data['tx']['input']['id']
        out_n = data['tx']['input']['n']
        for b in blockchain:
            if 'tx' in b and 'input' in b['tx'] and 'id' in b['tx']['input'] and 'n' in b['tx']['input']:
                if b['tx']['input']['id'] == out_id and b['tx']['input']['id'] == out_n:
                    print('failed check f iv')
                    return False 

        # v. value of the input equals the sum of the outputs 
        # (Assuming input and output both from the given block?)
        output_sum = sum(out['value'] for out in tx['output'] if out['value'] != 50)
        if 'tx' in input_block and 'output' in input_block['tx'] and len(input_block['tx']['output']) >= out_n + 1:
            input_val = input_block['tx']['output'][out_n] 

            if input_val != output_sum:
                print('failed check f v')
                return False 
                
        # vi.
        nouts = len(tx["output"])
        # "There should be no more than two outputs and no fewer than one output for any unverified transaction (not
        # including the coinbase transaction which is added by the miner, described later)"
        if (not (2 <= nouts <= 3)) or (not (all('value' in item and isinstance(item['value'], int) and item['value'] > 0 for item in tx['output']))): 
            print('failed check f vi')
            return False 
        
        # vii. 
        if tx['output'][-1]['value'] != 50: 
            print('failed check f vii')
            return False 
        
        # viii. 
        found = False 
        for o in tx['output']:
            if 'value' in o and o['value'] == 50: 
                found = True
                pub_key = o['pub_key']
                break 
        if not found: 
            print('failed check f viii (first part)')
            return False
        vk = VerifyingKey.from_string(bytes.fromhex(pub_key))
        sig_valid = vk.verify(bytes.fromhex(tx["sig"]), json.dumps(tx["input"], sort_keys=True).encode('utf8'))
        if not sig_valid:
            print('failed check f viii (second part)')
            return False

        return True
    except:
        print('failed validate_block try()')
        return False


