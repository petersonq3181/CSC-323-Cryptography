import time
import base64
import random


class MersenneTwister:
    def __init__(self, seed=5489):
        self.MT = [0] * 624
        self.index = 0
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = 0xFFFFFFFF & (1812433253 * (self.MT[i - 1] ^ self.MT[i - 1] >> 30) + i)

    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()
        
        y = self.MT[self.index]
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18

        self.index = (self.index + 1) % 624
        return y

    def generate_numbers(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7FFFFFFF)
            self.MT[i] = self.MT[(i + 397) % 624] ^ y >> 1
            if y % 2 != 0:
                self.MT[i] ^= 0x9908B0DF

# should be 5 and 60 
time1 = 5
time2 = 10

def oracle():
    time.sleep(random.randint(time1, time2))

    current_timestamp = int(time.time())
    print('Seed used: ', current_timestamp)
    mt = MersenneTwister(current_timestamp)

    time.sleep(random.randint(time1, time2))

    first_output = mt.extract_number()
    encoded_output = base64.b64encode(first_output.to_bytes(4, 'big'))
    return encoded_output

def oracleAndBreak(): 
    encoded_value = oracle()
    print(encoded_value)

    decoded_encoded_value = base64.b64decode(encoded_value)
    decoded_value = int.from_bytes(decoded_encoded_value, 'big')

    current_time = int(time.time())

    time_range = 2 * time2

    found_seed = None
    for possible_seed in range(current_time - time_range, current_time):
        mt = MersenneTwister(possible_seed)
        if mt.extract_number() == decoded_value:
            found_seed = possible_seed
            break

    if found_seed is not None:
        print(f'Found seed: {found_seed}')
    else:
        print('Seed not found') 


mt = MersenneTwister(3) 
random_number = mt.extract_number()


oracleAndBreak()
