import sys
import os
import subprocess
import time


try:
    
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
    import traci
    
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


fo = open("trajectory.txt", "w")
global trajectoryList   
global max_num_veh 
global VehinMap
VehinMap = {}
max_num_veh = 0
trajectoryList = list(range(0,1000))


class On_Board_Unit2():
    def __init__(self): 
        self.VehId   = ' '
    
    


def Vehicle_Enter_Network2():
    DepartVeh = traci.simulation.getDepartedIDList()
    global VehinMap
 
    for VehId in DepartVeh:
        VehinMap[VehId] = On_Board_Unit2()
        VehinMap[VehId].VehId = VehId



def Ns3LteSimulation( simTime = 50, enbTxPowerDbm = 46, ulpacketSize = 1024, ulpacketsInterval = 500, dlpacketSize = 1024, dlpacketsInterval = 500, fadingModel = 0):
#============================================================================================
# simTime", "Total duration of the simulation (in seconds)
# enbTxPowerDbm", "TX power [dBm] used by HeNBs (default = 46.0)
# ulpacketSize","Size (bytes) of UL packets generated send to Remote Server. (default = 1024 bytes). The minimum packet size is 12 bytes which is the size of the header carrying the sequence number and the time stamp.
# ulpacketsInterval","The time (ms) wait between UL packets send to Remote Server. (default = 500 ms)
# dlpacketSize","Size (bytes) of DL packets generated send to Remote Server. (default = 1024 bytes). The minimum packet size is 12 bytes which is the size of the header carrying the sequence number and the time stamp.
# dlpacketsInterval","The time (ms) wait between DL packets send to Remote Server. (default = 500 ms)
# fadingModel","setting fading model (1, 2 and 3 represent pedestrian, urban and vehicular scenario respectively)
#============================================================================================


    #RunNs3 = "./RunNs3.sh"+" "+"simTime"+" "+str(simTime)+" "+ "enbTxPowerDbm"+" "+str(enbTxPowerDbm)+" "+"packetSize"+" "+str(packetSize)+" "+"packetsInterval"+" "+str(packetsInterval)+" "+"fadingModel"+" "+str(fadingModel)

    global trajectoryList   
    global max_num_veh 
    global VehinMap
    
    DepartVeh = traci.simulation.getDepartedIDList()

    if len(DepartVeh) > 0:
        Vehicle_Enter_Network2()

    if len(VehinMap) > 0: 
        for VehId in VehinMap:
        #   traci.vehicle.setParameter(VehId, "device.battery.vehicleMass", '1521')            #將車重改為1521KG (Nissan Leaf)
            #Vehicle[VehId].Get_Vehicle_Information()
            #Vehicle[VehId].Caculate_Current_Battery_Capacity()

            

            max_num_veh = int(VehId) if max_num_veh < int(VehId) else max_num_veh
            
                
            print("CarID is = %s " % VehId)
            #print("MaxBatteryCapacity is = %s " % Vehicle[VehId].MaxBatteryCapacity)        
            #print("CurrentBatteryCapacity = %s" % Vehicle[VehId].CurrentBatteryCapacity)
            #print("BatteryConsumption = %s"% Vehicle[VehId].BatteryConsume)
            #print("BatteryPercent = " , Vehicle[VehId].BatteryPercent,"%")
            #print("Position = %s" % Vehicle[VehId].Position)
            print("Position = %s, %s" % traci.vehicle.getPosition(VehId))
            [xp, xy] =  traci.vehicle.getPosition(VehId)
            xp = str(xp)
            xy = str(xy)
            msTimer = traci.simulation.getCurrentTime()
            s =  msTimer/1000 
            print("Current time = %s" % s)

            s = str(s)
            id = int (VehId)
            tmp = str(trajectoryList[id])
            trajectoryList[id] = tmp+ " "+s+":"+xp+":"+xy
            print(trajectoryList[id])
            print("      ")
            
    
    #        print("RouteID = %s " % Vehicle[VehId].RoadID )
    #       print("Route = %s" % Vehicle[VehId].Route)
    #        print("EndTarget = %s" % Vehicle[VehId].EndTarget)
    #        print("Distance = %s" %Vehicle[VehId].RealDistance)
        msTimer = traci.simulation.getCurrentTime()
        s =  msTimer/1000 
        cnt = 0;       

        if s == simTime :  #output time
            for id1 in trajectoryList :
                id1 = str(id1)
                id1 = id1 + " \n"
                #os.write(fo, id1)
                fo.write(id1)
                #print(id1)
                cnt +=1
                if cnt == (max_num_veh+1):
                    fo.close()
                    print("###################", str(max_num_veh+1))
                    #print(RunNs3)
                    sumohome = os.environ['SUMO_HOME']
                    subprocess.call(["bash",sumohome+"/tools/RunNs3.sh","simTime" , str(simTime), "enbTxPowerDbm", str(enbTxPowerDbm), "dlpacketSize", str(dlpacketSize), "dlpacketsInterval", str(dlpacketsInterval), "ulpacketSize", str(ulpacketSize), "ulpacketsInterval", str(ulpacketsInterval), "fadingModel", str(fadingModel)])
                    sys.stdout.flush()
                    traci.close()
                    break
            #print(len(Vehicle))
            #time.sleep(5)
            
    
