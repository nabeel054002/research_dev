#consider domains, a,b and c
#with miners as ma, mb, mc
#each will have drones as a.1, a.2, a.3...
#b.1,b.2,b.3...

import structs

#instantiated 3 miners
ma = structs.Miner("a")
mb = structs.Miner("b")
mc = structs.Miner("c")

#instantiate the chain
chain=structs.System("0100")

#register miners
chain.register_miner(ma, "0100")
chain.register_miner(mb, "0100")
#chain.register_miner(mc, "0000")
chain.register_miner(mc, "0100")

#initialize 3 drones for each city/domain, a, b and c
a1 = structs.Drone("a1", "a")
a2 = structs.Drone("a2", "a")
a3 = structs.Drone("a3", "a")

b1 = structs.Drone("b1", "b")
b2 = structs.Drone("b2", "b")
b3 = structs.Drone("b3", "b")

c1 = structs.Drone("c1", "c")
c2 = structs.Drone("c2", "c")
c3 = structs.Drone("c3", "c")

#register the different drones to different miners
ma.register_drone(a1)
ma.register_drone(a2)
ma.register_drone(a3)

mb.register_drone(b1)
mb.register_drone(b2)
mb.register_drone(b3)

mc.register_drone(c1)
mc.register_drone(c2)
mc.register_drone(c3)

# data_a
# while(True):


# print(a1)
# print(a2)
# print(b1)
# print(ma)
# print(mb)

# ptr = chain.starting
# while(ptr!=None):
#     print(ptr.val)
#     ptr = ptr.next