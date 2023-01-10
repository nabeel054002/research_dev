import random
import hashlib

prepare_counter=0
class Block:
    def __init__(self, valid_requests, prev_block_hash, block_num):
        self.valid_requests = valid_requests
        self.prev_block_hash = prev_block_hash
        self.block_num = block_num
        self.block_hash = self.calculate_hash()

    def calculate_hash(self):
        # Calculate the hash of the block using its attributes
        block_string = str(self.valid_requests) + self.prev_block_hash + str(self.block_num)
        return hashlib.sha256(block_string.encode()).hexdigest()

class PBFTNode:
    def __init__(self, node_id, num_nodes):
        global genesis_block
        self.node_id = node_id
        self.num_nodes = num_nodes
        self.blockchain = []
        #def __init__(self, valid_requests, prev_block_hash, block_num):
        self.blockchain.append(genesis_block)
        self.valid_requests = []
        self.prepare_msgs = {}
        self.commit_msgs = {}

    def broadcast_prepare(self, block):
        global prepare_counter
        prepare_counter += 1
        for node_id in range(self.num_nodes):
            if node_id != self.node_id:
                send_prepare(node_id, block)

    def receive_prepare(self, block):
        global commit_counter
        # global prepare_counter
        # prepare_counter += 1 # becayse it was already decided to have 
        if block.block_hash in self.prepare_msgs:
            self.prepare_msgs[block.block_hash] += 1
            if prepare_counter > self.num_nodes // 2:
                self.broadcast_commit(block)
        else: 
            self.prepare_msgs[block.block_hash]=1
            if prepare_counter>self.num_nodes//2:
                self.broadcast_commit(block)

    def broadcast_commit(self, block):
        for node_id in range(self.num_nodes):
            if node_id != self.node_id:
                self.commit_msgs[block.block_hash]=1
                send_commit(node_id, block)

    def receive_commit(self, block):
        if commit_counter > self.num_nodes // 2:
            self.blockchain.append(block)
            print(self.blockchain)
            self.valid_requests = []
            self.prepare_msgs = {}
            self.commit_msgs = {}

def simulate_pbft(num_nodes, num_requests):
    global prepare_counter
    global commit_counter
    nodes = []
    for node_id in range(num_nodes):
        nodes.append(PBFTNode(node_id, num_nodes))
        #print(nodes[-1])

    for request_num in range(num_requests):
        request = f"request {request_num}"
        #print(request)
        for node in nodes:
            node.valid_requests.append(request)

        random_node = random.choice(nodes)
        block = Block(random_node.valid_requests, random_node.blockchain[-1].block_hash, random_node.blockchain[-1].block_num+1)
        random_node.broadcast_prepare(block)
        #print(random_node)

        for node in nodes:
            if node != random_node:
                node.receive_prepare(block)
        print("random_node is", random_node, random_node.commit_msgs)
        for node in nodes: 
            print(node, node.commit_msgs)
            if node!=random_node and node.commit_msgs[block.block_hash]==1:
                commit_counter+=1

        for node in nodes:
            if node != random_node:
                node.receive_commit(block)
        random_node.blockchain.append(block)
        random_node.commit_msgs[block.block_hash]=1
        print(random_node.blockchain)
        #print(prepare_counter)
        prepare_counter = 0
        commit_counter=0

def send_prepare(node_id, block):
    # Send the prepare message to the specified node, based on networks communication, or can even include this in the pbftnode class using a stack like data structure
    global prepare_counter
    prepare_counter+=1

def send_commit(node_id, block):
    # Send the commit message to the specified node
    pass

if __name__ == "__main__":
    prepare_counter=0
    commit_counter = 0
    genesis_block = Block(["0"],"0",0)
    simulate_pbft(5, 1)

