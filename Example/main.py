# -*- coding: utf-8 -*-

import os
import sys
import optparse
import subprocess
#import traci
import numpy as np

#from ControlNs3 import Vehicle_Enter_Network2

from function import Vehicle_Enter_Network
from function import Create_Vehicle
from function import Vehicle_Information
from function import Threshold_Of_Vehicle_Charging
from function import Vehicle_Charging
from function import Charging_Station_Parameter
# =============================================================================
# from function import Print_Vehicle_information
# =============================================================================





try:
    
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
    import traci
    from ControlNs3 import Ns3LteSimulation

except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


def get_options():
    
    
    
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options



# =============================================================================
# <parkingArea id="CS04" lane="536831320#1_0" startPos="5" endPos="23" roadsideCapacity="3" width="5" length="6" angle="0"/>
# =============================================================================

ChargingStation = {}
Vehicle = {}
VehilceDensity = 1

def run():
    global Vehicle
    global CS

    #-------------------------for storing trajectory

    #----------------------------------------------


    Charging_Station_Parameter(ChargingStation)
    msTimer = traci.simulation.getCurrentTime()

    

    
    while True:
        traci.simulationStep()
#多台測試
        print("#############################################################")
        getCurrentTime = traci.simulation.getCurrentTime()
        print("getCurrentTime = ",getCurrentTime)
        if (msTimer % 1000) == 0: # create device to network  (每1秒增加車輛 Poisson λ=1 k=1)
            Create_Vehicle(Vehicle, VehilceDensity)



        msTimer =  traci.simulation.getCurrentTime()
        DepartVeh = traci.simulation.getDepartedIDList()
        if len(DepartVeh) > 0:
           Vehicle_Enter_Network(DepartVeh, Vehicle)
           #Vehicle_Enter_Network2()
   
           
        ArrivedVeh = traci.simulation.getArrivedIDList()
        if ArrivedVeh: 
            for VehName in ArrivedVeh:
               del Vehicle[VehName]

                
            
        if len(Vehicle) > 0: 
            getIDList = traci.vehicle.getIDList()
            print("getIDList = ",getIDList)
            Vehicle_Information(Vehicle)
            #Vehicle_Information2()
          
                          #得到車輛資訊
# =============================================================================
#             Print_Vehicle_information(Vehicle)                     #輸出車輛資料至route.csv
# =============================================================================
            Threshold_Of_Vehicle_Charging(Vehicle,ChargingStation) #偵測車輛是否需要充電 並尋找最佳充電站
            Vehicle_Charging(Vehicle,ChargingStation)              #正在充電車輛判斷 哪個CS 還要多久?
            print("#############################################################")


            

#=================================================================================
        Ns3LteSimulation(simTime=50, ulpacketSize= 512)             # function for control ns-3
#=================================================================================

        ArrivedVeh = traci.simulation.getArrivedIDList()
        if ArrivedVeh:
            print("The Car is leaving = " , ArrivedVeh)




    
    sys.stdout.flush()
    traci.close()

    




# this is the main entry point of this script
if __name__ == "__main__":

    
  
    
    
    options = get_options()   
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    


        
        
    traci.start([sumoBinary, '-c', os.path.join('data/Simulation', 'map.sumocfg')])

    #BatteryTimer = threading.Timer(1, Battery_Timer)
    #BatteryTimer.start()
    run()
    
    
    #BatteryTimer.cancel()
    
    
    
    
    
    
    
    
    
