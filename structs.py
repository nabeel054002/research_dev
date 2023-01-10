from enum import Enum
#system is to register the central servers/miners, and the drones are to be authenticated in the central servers
#revise the modifiers in python to increase security

class Node:
    def __init__(self, x, creator):
        self.val = x
        #add more, like nonce
        #tx for each drone join miner network
        self.publisher=creator
        self.next = None

#to implement linked list

class BlockType(Enum):
    GENESISBLOCK=-1
    NONE: 0
    DRONEREGISTERED = 1

class System:
    def __init__(self, system_signature):
        self.num_miners=0
        #do i need to keep track of it
        self.miners = {}
        self.blockchain = Node(BlockType.GENESISBLOCK, None)
        #genesis block, having 0x00 address
        self.starting = self.blockchain
        #genesis block, helps us in tracking previous blocks
        self.miners_proof = system_signature
        #no reputation score implementation?
        #self.miners maps the address to number of drones around it 

    def register_miner(self, miner, signature):
        assert signature == self.miners_proof, "Not appropriate miner"
        if(miner.address not in self.miners):
            #check for govt`s cryptographic signature
            #the signature is a simple encryption proof of miner authentication
            self.miners[miner.address]=0
            self.num_miners+=1
            miner.chain = self
            print(f'A Miner,{miner} was registered')
            # block = Node()
            # self.add_block(), only the miner can write na
        else:
            assert 0==1, "miner is already registered in this network"

    def add_block(self, block, address_miner):
        #need to ensure that miner only calls in its own context
        assert address_miner==block.publisher, "Not fitting context"
        self.blockchain.next = block
        self.blockchain = block

class Miner:
    def __init__(self, address):
        self.address = address
        #address can be pincode...
        self.drones = {}
        self.num=0
        self.round = 0
        self.drone_round = 0
        self.minimum = 0.15
        self.chain = None
        self.rep_score = {}
        self.curr_data = []
        #score out of 1
    
    def register_drone(self, drone):
        if drone.name not in self.drones:
            self.authenticate(drone)
            info = BlockType(1)
            self.publishTx(info)
            self.curr_data.append(0)
        else:
            assert 0==1,"Drone already registered with miner"

    def authenticate(self, drone):
        #can be called by anyone
        if(self.chain):
            if(drone.name not in self.rep_score or self.rep_score[drone.name]<self.minimum) :
                status = self.rtmp_auth(drone)
                if(status):
                    self.drones[drone.name]=[drone, self.num,self.round]
                    self.num+=1
                    drone.connected(self)
                else:
                    assert 0==1, "Authentication failed"
            else:
                self.drones[drone.name]=[drone, self.num,self.round]
                drone.connected(self)
        else:
            assert 0==1, "Miner needs to be connected to a chain, for drone to register with miner"
            #not part of a chain, no pt of drone auth
    
    def rtmp_auth(self, drone):
        #3 step implementation, for now simply allow
        return drone != None

    def publishTx(self, info):
        #info is of type BlockType
        block = Node(info, self.address)
        self.chain.add_block(block, self.address)
        print(block, "was published")

    def accept_data(self, drone):
        if(self.drones[drone.name][2]==self.round):
            self.drones[drone.name][2]+=1
            self.drone_round+=1 
            self.curr_data[self.drones[drone.name][1]] = drone.val
            if(self.drone_round==len(self.drones)):
                self.global_model = sum(self.curr_data)/len(self.drones)
                self.drone_round=0
                self.num+=1
                for i in self.drones:
                    i[0].accept_global_model(self.global_model)
                
#hashmaps have high space n low t, can use specific nomenclature 

class Drone:
    def __init__(self, name, address):
        self.name = name
        self.chain = None
        self.address = address
        self.miner_parent = None
        #name is an alphanumeric string
    def connected(self, miner):
        self.miner_parent = miner 
        self.chain=miner.chain

    def train(self, data):
        #will constantly be run on the server 
        self.result = data#this will be some funciton of dat 
        self.miner_parent.accept_data(self)
    def accept_global_model(self, data):
        self.curr_global = data 


'''
    Questions
    1. will the miners/GCS have a reputation score 
    2. do we assume that the GCS is trustworthy at everypoint
    3. isnt this architecture very similar to others, should i change something or so...
        a. could be of leave and join
        b. could be of calling immediate drone reinforcements
        c. could be giving temporary miner access to a catching drone
    4. should i add async functionality ?
    5. should the addition of a new miner also be included in the transaction 
'''