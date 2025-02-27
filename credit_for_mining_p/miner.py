import hashlib
import requests
from uuid import uuid4
import os.path

import sys


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        # post_data = {"proof": new_proof}

        if os.path.exists('my_id.txt') == False:
            current_id = open('my_id.txt', 'w+')

            current_id.write(str(uuid4()).replace('-',''))

        else:
            existing_id = []
            with open('my_id.txt', 'r') as myfile:
                for myline in myfile:
                    existing_id.append(myline)

            # current_id = open('my_id.txt', 'r')
        
        # print(current_id.read())
        # existing_id = []
        # existing_id.append(current_id.read())
        print(existing_id)
            

            # current_id.close()
            # if current_id:
            #     print(current_id.read())
            # else:
            # print(current_id.read())
        
        post_data = {"proof": new_proof, "id": existing_id[0]}
        print(post_data)


        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
