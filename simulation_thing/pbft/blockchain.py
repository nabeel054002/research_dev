#to implement a blockchain with miners and consensus as pbft
import hashlib
import time
import random

class PBFTNode:
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.blockchain = []
        self.prepare_msgs = {}
        self.commit_msgs = {}
        self.view = 0
        self.last_committed = -1
        self.valid_requests = []
        #so the whole system keeps track of how many nodes recieved the msg, so self does not refer to individual nodes but the entire system

    def broadcast_prepare(self, block):
        self.prepare_msgs[block.block_hash] = 1
        for node_id in range(self.num_nodes):
            if node_id != self.node_id:
                send_prepare(node_id, block)#sending prepare msg to all the other nodes, i.e. broadcasting prepare msgs

    def receive_prepare(self, block):
        if block.block_hash in self.prepare_msgs:
            self.prepare_msgs[block.block_hash] += 1
            if self.prepare_msgs[block.block_hash] > self.num_nodes // 2:#this step is kinda hazy
                self.broadcast_commit(block)

    def broadcast_commit(self, block):
        self.commit_msgs[block.block_hash] = 1
        for node_id in range(self.num_nodes):
            if node_id != self.node_id:
                send_commit(node_id, block)#sending commit msg 

    def receive_commit(self, block):
        if block.block_hash in self.commit_msgs:
            self.commit_msgs[block.block_hash] += 1
            if self.commit_msgs[block.block_hash] > self.num_nodes // 2:
                self.last_committed += 1
                self.blockchain.append(block)
                self.commit_msgs = {}
                self.prepare_msgs = {}
                self.valid_requests = []

class Block:
    def __init__(self, data, prev_block_hash, block_num):
        self.timestamp = time.time()
        self.data = data
        self.prev_block_hash = prev_block_hash
        self.block_num = block_num
        self.block_hash = self.get_hash()

    def get_hash(self):
        block_string = f"{self.timestamp}{self.data}{self.prev_block_hash}{self.block_num}"
        return hashlib.sha256(block_string.encode()).hexdigest()

##simulate the actual pbft consensus mechanism

def simulate_pbft(num_nodes, num_requests):
    nodes = []
    for node_id in range(num_nodes):
        nodes.append(PBFTNode(node_id, num_nodes))
        #making a set of nodes, indexed by whole number, 0 to num_nodes

    for request_num in range(num_requests):#all the requests are the same here
        request = f"request {request_num}"
        #make the requests, each iteration includes dealing with single request
        for node in nodes:
            node.valid_requests.append(request)
            #addition to each node`s ongoing requests to be validated

        random_node = random.choice(nodes)#random selection
        block = Block(random_node.valid_requests, random_node.blockchain[-1].block_hash, random_node.blockchain[-1].block_num+1)
        #random_node.valdiate_requests == data, prev_block_hash = block_hash of the blockchain as stored in the random node, block_num is an additino to what it was before, these things are extracted from the values as chosen by the random parameter, if a random_node, misses then the blockchain would change rgt?
        random_node.broadcast_prepare(block)

        for node in nodes:
            if node != random_node:
                node.receive_prepare(block)#node sends a commit msg regarding the block, particularly to those that have the 

        for node in nodes:
            if node != random_node:
                node.receive_commit(block)#node sends its commit msg to all of the other nodes

# Run the simulation with 5 nodes and 10 requests
simulate_pbft(5, 10)
