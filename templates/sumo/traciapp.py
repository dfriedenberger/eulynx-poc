import traci
import traci.constants as tc
import logging
import sys
import os
import queue
import uuid


if 'SUMO_HOME' in os.environ:
    SUMO_HOME = os.environ['SUMO_HOME']
    sys.path.append(os.path.join(SUMO_HOME, 'tools'))
    os.environ['PATH'] += os.pathsep + os.path.join(SUMO_HOME, 'bin')


class Simulation:

    def __init__(self,name):
        self.name = name
        self.qcommands = queue.Queue()

    def commands(self,cmd,data):
        self.qcommands.put({"cmd" : cmd , "data" : data })

    def run(self):
        logging.info("Thread %s: starting", self.name)

        #Config
        sumo_cmd="sumo-gui"
        #sumo_cmd="sumo"
        config_path="example/sumo.sumocfg"

        traci.start([sumo_cmd, '--no-warnings', '-c', config_path])

        while True:
            
            #Next step
            traci.simulationStep()
            for vehID in traci.vehicle.getIDList():
                road_id = traci.vehicle.getRoadID(vehID)
                logging.debug('Vehicle %s %s', vehID,road_id)

            if self.qcommands.qsize() > 0:
                c = self.qcommands.get()
                if c["cmd"] == "train":
                    traci.vehicle.add(str(uuid.uuid4()), "route1", typeID="train2")
                else:
                    print("Unknown Command",c)
            
            #if len(traci.vehicle.getIDList()) == 0:
                #traci.route.add("route1", ["gneE20", "gneE16"])
                


            #traci.vehicle.setRouteID(train.name, next_operation.route.id)



        logging.info("Thread %s: finishing", self.name)
