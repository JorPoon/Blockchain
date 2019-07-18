import hashlib
import requests
import json

import sys


# TODO: Implement functionality to search for a proof 

url = "http://localhost:5000/"
def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 4
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"

def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1

    return proof

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get(f"{url}proof")
        data = response.json()
        request_proof = data['last_proof']
        print(request_proof)
        # print(proof_of_work(request_proof), "hello")
        new_proof = proof_of_work(request_proof)
        # data = {"proof": new_proof}
        print(new_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        post_proof = requests.post(f"{url}mine", json={"proof": new_proof})
        print(post_proof.json())
        # TODO: If the server responds with 'New Block Forged'
        if post_proof.status_code == 201:
            coins_mined += 1
            print(coins_mined)
        else:
            print(post_proof.json())

        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        
