import numpy as np
import math
import random 
import sys
import os
#import traci
import pandas as pd
from Parameter import On_Board_Unit
from Parameter import Charging_Station_Information
import subprocess
import time
 


#------------------------------- data loaded by ns-3
#fo = open("trajectory.txt", "w")
#global trajectoryList   
#global max_num_veh 
#max_num_veh = 0
#trajectoryList = list(range(0,1000))
#------------------------------- data loaded by ns-3

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


data = [['Time','CarID','Speed','Battery']]
df   = pd.DataFrame(data)


CurVehNum = 0
CS01 = 200000
CS02 = 200000
CS03 = 200000
CS04 = 200000

CsParm = Charging_Station_Information()

# =============================================================================
# def Print_Vehicle_information(Vehicle):       
#     global df
#     for VehId in Vehicle:
#  
# 
#         Speed = traci.vehicle.getSpeed(VehId)
#         Vehicle[VehId].Caculate_Current_Battery_Capacity()
#         msTimer = traci.simulation.getCurrentTime()
#         s = [[msTimer/1000,VehId,Speed,Vehicle[VehId].CurrentBatteryCapacity]]
#         df = df.append (s)
#         
#         if msTimer%100000 == 0:    #每100SEC寫檔
#             df.to_csv("route.csv")
# =============================================================================
        
    

        

def Charging_Station_Parameter (ChargingStation) :
    global CsParm
    for CharingStationID in range(0,6) :
        ChargingStation[CharingStationID] = Charging_Station_Information()
        ChargingStation[CharingStationID].CharingStationID = 'CS' + str(CharingStationID+1)
        ChargingStation[CharingStationID].CharingStationLane = ChargingStation[CharingStationID].CharingStationLane[CharingStationID]
        
        if ChargingStation[CharingStationID].count == 1 :
            ChargingStation[CharingStationID].ChargingWaitingTime      = [0]*100
            ChargingStation[CharingStationID].ChargingWaitingTime2     = [0]*100
            ChargingStation[CharingStationID].CharingStationIdentityID = [0]*100
            ChargingStation[CharingStationID].count = 0 
    


def Create_Vehicle (Vehicle , VehilceDensity) :
    global CurVehNum
    np.random.seed()
    
    EnterVehNum = int(np.random.poisson(VehilceDensity, 1))   # λ=1 k=VehilceDensity
#    CurVehNum = len(Vehicle)  # current vehicle number
    if EnterVehNum > 0:       
        for i in range(CurVehNum, CurVehNum + EnterVehNum):
#            Vehicle.append(On_Board_Unit())
            traci.vehicle.addFull(str(i),'routedist1',typeID='typedist1')
    CurVehNum = CurVehNum + EnterVehNum # current vehicle number  
    return Vehicle



def Vehicle_Enter_Network(DepartVeh,Vehicle):
    for VehId in DepartVeh:
        Vehicle[VehId] = On_Board_Unit()
        Vehicle[VehId].VehId = VehId
        
        
# =============================================================================
# def Vehicle_Leave_Network(Leave,Vehicle):
#     Leave = traci.simulation.getArrivedIDList()
#     for Leave in Vehicle:
#         del Vehicle[Leave].MaxBatteryCapacity,  Vehicle[Leave].GivePower
#         del Vehicle[Leave].VehId,  Vehicle[Leave].Speed,  Vehicle[Leave].CurrentBatteryCapacity
#         del Vehicle[Leave].MaxReceivePower,  Vehicle[Leave].CurrentReceivePower
#         del Vehicle[Leave].BatteryConsume,  Vehicle[Leave].Position
#         del Vehicle[Leave].Route ,Vehicle[Leave].RoadID ,Vehicle[Leave].EndTarget
#         del Vehicle[Leave].Distance, Vehicle[Leave].RealDistance, Vehicle[Leave].BatteryPercent
#         del Vehicle[Leave].count ,Vehicle[Leave].count2 ,Vehicle[Leave].num
# =============================================================================
        
        
def Vehicle_Information3(Vehicle):
    global trajectoryList   
    global max_num_veh 
    
    for VehId in Vehicle:
     #   traci.vehicle.setParameter(VehId, "device.battery.vehicleMass", '1521')            #將車重改為1521KG (Nissan Leaf)
        Vehicle[VehId].Get_Vehicle_Information()
        Vehicle[VehId].Caculate_Current_Battery_Capacity()

        

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

    if s == 50 :  #output time
        for id1 in trajectoryList :
            id1 = str(id1)
            id1 = id1 + " \n"
            #os.write(fo, id1)
            fo.write(id1)
            #print(id1)
            cnt +=1
            if cnt == (max_num_veh+1):
                fo.close()
                print("############## %s ################", str(max_num_veh+1))
                subprocess.call("./RunNs3.sh", shell=True)
                break
        #print(len(Vehicle))
        #time.sleep(5)
            
    return Vehicle

def Vehicle_Information(Vehicle):
    for VehId in Vehicle:
     #   traci.vehicle.setParameter(VehId, "device.battery.vehicleMass", '1521')            #將車重改為1521KG (Nissan Leaf)
        Vehicle[VehId].Get_Vehicle_Information()
        Vehicle[VehId].Caculate_Current_Battery_Capacity()
        print("CarID is = %s " % VehId)
        #print("MaxBatteryCapacity is = %s " % Vehicle[VehId].MaxBatteryCapacity)        
        #print("CurrentBatteryCapacity = %s" % Vehicle[VehId].CurrentBatteryCapacity)
        #print("BatteryConsumption = %s"% Vehicle[VehId].BatteryConsume)
        #print("BatteryPercent = " , Vehicle[VehId].BatteryPercent,"%")
        #print("Position = %s" % Vehicle[VehId].Position)
        print("Position = %s, %s" % traci.vehicle.getPosition(VehId))
        msTimer = traci.simulation.getCurrentTime()
        s =  msTimer/1000 
        print("Current time = %s" % s)

def Threshold_Of_Vehicle_Charging(Vehicle,ChargingStation) :
    global CS01
    global CS02
    global CS03
    global CS04
    EverySec_ChargingPower = 50     #16/3     #19.2K/HR  320/min  5.33333/sec
    #每小時充電量 3.7K/HR   61.6666666 /MIN     1.027777777778 /SEC (慢充)
    
    
    
    for VehId in Vehicle:
        MaxEffective = -100000   #每台車maxEffective 重設
        MinDistance = 10000000
        MaxDistance = 0
        Charing_or_not = traci.vehicle.isStoppedParking(VehId)
        if Charing_or_not == False :
             if Vehicle[VehId].BatteryPercent < 40 :
                        for CharingStationID in range(0,6) :
                            LanePosition = traci.vehicle.getLanePosition(VehId)
                            CS_Postion   = ChargingStation[CharingStationID].CharingStationLane
                            ChargingStation[CharingStationID].CharingStationDistance = traci.simulation.getDistanceRoad(Vehicle[VehId].RoadID,LanePosition,CS_Postion,35,1)
        
                            
                        for i in range(0,6) : 
                            if ChargingStation[i].CharingStationDistance < MinDistance:
                                     MinDistance = ChargingStation[i].CharingStationDistance
                            if ChargingStation[i].CharingStationDistance > MaxDistance:
                                     MaxDistance = ChargingStation[i].CharingStationDistance
                                     
                        if MaxDistance < 10000 :
                            for j in range(0,6) :
                            
                                DistanceWeight  = ChargingStation[j].CharingStationDistance * -0.4
                                CSWaitingWeight = ChargingStation[j].MinChargingWaitingTime * -0.3
                                CSMoneyWeight   = ChargingStation[j].CurrentChargingMoney   * -0.2
                                ChargingStation[j].ChargingEffective = DistanceWeight + CSWaitingWeight + CSMoneyWeight
                                if ChargingStation[j].ChargingEffective > MaxEffective :
                                    MaxEffective = ChargingStation[j].ChargingEffective   
 #                                   print("MaxEffective = ",MaxEffective)    
                                    
                            for n in range(0,6):
                                if MaxEffective == ChargingStation[n].ChargingEffective :
                                    Vehicle[VehId].VehCS1 = ChargingStation[n].CharingStationID
                                    print("Now Vehcile want to go %s" %ChargingStation[n].CharingStationID)
                                    if ChargingStation[n].CharingStationVehNum == 5:
                                         Vehicle[VehId].VehWaitingTime = ChargingStation[n].MinChargingWaitingTime
                                         print("CarID%s go to  %s need to wait %s"%(VehId,ChargingStation[n].CharingStationID,Vehicle[VehId].VehWaitingTime))
                                    else:
                                         Vehicle[VehId].VehWaitingTime = 0
                                         print("CarID%s go to  %s need to wait %s"%(VehId,ChargingStation[n].CharingStationID,Vehicle[VehId].VehWaitingTime))
                            print("    ")                    
                            if Vehicle[VehId].VehCS1 != Vehicle[VehId].VehCS2 :   # 充電的時候 VehCS2 記得歸0             
                                for k in range(0,6) :
                                    if MaxEffective == ChargingStation[k].ChargingEffective :
                                        print("The CarID is = %s " % VehId)
                                        Vehicle[VehId].VehCS2 = ChargingStation[k].CharingStationID
                                        
                                        traci.vehicle.changeTarget(VehId, ChargingStation[k].CharingStationLane )
                                        Vehicle[VehId].IdentityID = random.randrange(0,200000)  #給予充電編碼ID
                                        
                                        Vehicle[VehId].Give_Power     = random.randrange(15000,19200)
                                        Vehicle[VehId].ChargingTime   = Vehicle[VehId].Give_Power / EverySec_ChargingPower
        #                                Vehicle[VehId].VehWaitingTime = Vehicle[VehId].ChargingTime
                                        CS_ID = ChargingStation[k].CharingStationID
                                        traci.vehicle.setParkingAreaStop(VehId,CS_ID,duration=float(Vehicle[VehId].ChargingTime),flags=1)
            #                        ChargingStation[k].CharingStationPower -= Vehicle[VehId].Give_Power
                                        for c in range(0,100) :
                                            if  ChargingStation[k].ChargingWaitingTime[c] == 0 :
                                                ChargingStation[k].ChargingWaitingTime[c] = float(Vehicle[VehId].ChargingTime)
                                                ChargingStation[k].ChargingWaitingTime2[c] = ChargingStation[k].ChargingWaitingTime[c]
                                                if  ChargingStation[k].ChargingWaitingTime[c] != 0 :
                                                    break
                                        for a in range(0,100) :
                                            if  ChargingStation[k].CharingStationIdentityID[a] == 0:
                                                ChargingStation[k].CharingStationIdentityID[a] = float(Vehicle[VehId].IdentityID)
                                                if ChargingStation[k].CharingStationIdentityID[a] != 0:
                                                    break
                                        print("      ")
                                        print("Let's go to ",ChargingStation[k].CharingStationID)
                                        print("CharingStationPower = ",ChargingStation[k].CharingStationPower)
                                        print("Give_Power = ",Vehicle[VehId].Give_Power)
                                        print("ChargingTime = ",Vehicle[VehId].ChargingTime)
                        else:
                            print("CarID%s is too close to CS" %VehId)
                        


                        
    return Vehicle


#每小時充電量 3.7K/HR   61.6666666 /MIN     1.027777777778 /SEC (慢充)
    
def Vehicle_Charging(Vehicle,ChargingStation):
    EverySec_ChargingPower = 50  # 16/3   #19.2K/HR  320/min  5.33333/sec
    for CSID in ChargingStation :
        Min_ChargingTime       = 1000000
        ChargingStation[CSID].CharingStationVehNum = 0
        for VehId in Vehicle:
            Charing_or_not = traci.vehicle.isStoppedParking(VehId)
            if Charing_or_not == True:
                for i in range(0,100):
                    if ChargingStation[CSID].CharingStationIdentityID[i] == Vehicle[VehId].IdentityID:
                        ChargingStation[CSID].CharingStationVehNum +=1             #停車場有幾台車?
                        ChargingStation[CSID].ChargingWaitingTime2[i] =  ChargingStation[CSID].ChargingWaitingTime2[i] - 1
                        print("CarID %s is in %s" %(VehId,ChargingStation[CSID].CharingStationID))
                        print("Waiting Time left = ",ChargingStation[CSID].ChargingWaitingTime2[i])
                        
                            
                        
                        if ChargingStation[CSID].ChargingWaitingTime2[i] > 0 :
                            Vehicle[VehId].BatteryConsume = float(traci.vehicle.getParameter(VehId,"device.battery.energyConsumed"))
                            Vehicle[VehId].CurrentBatteryCapacity +=  EverySec_ChargingPower + Vehicle[VehId].BatteryConsume #停車站充電 電池消耗
                            Vehicle[VehId].CumlativePower += EverySec_ChargingPower
                            print ("Give_Power =",Vehicle[VehId].Give_Power)
                            print("CumlativePower = ",Vehicle[VehId].CumlativePower)
                            
                            if ChargingStation[CSID].ChargingWaitingTime2[i] != 0:
                                 if ChargingStation[CSID].ChargingWaitingTime2[i] < Min_ChargingTime:
                                     Min_ChargingTime = ChargingStation[CSID].ChargingWaitingTime2[i]
                                     ChargingStation[CSID].MinChargingWaitingTime = Min_ChargingTime

                        else :
                            Vehicle[VehId].CumlativePower = 0
                            traci.vehicle.changeTarget(VehId,Vehicle[VehId].EndTarget)
                            print("CarID %s is GOing to ENDTARGET " %VehId)
                            Vehicle[VehId].count  = Vehicle[VehId].count  + 1
                            for j in range(0,100):
                                if ChargingStation[CSID].ChargingWaitingTime2[j] < 0:
                                    ChargingStation[CSID].ChargingWaitingTime2[j] = 0   #清空充完電車輛儲存格
                                    ChargingStation[CSID].ChargingWaitingTime[j]  = 0
                                    ChargingStation[CSID].CharingStationIdentityID[j] = 0
  #                                  Vehicle[VehId].IdentityID = 0
                                    Vehicle[VehId].VehCS2     = 0
                            
                            
        print("%s : How many Cars = %s "%(ChargingStation[CSID].CharingStationID,ChargingStation[CSID].CharingStationVehNum))
        
        if ChargingStation[CSID].CharingStationVehNum < 5 :
            ChargingStation[CSID].MinChargingWaitingTime = 0
            print ("%s : Min_Charging_Waiting_Time = 0"%ChargingStation[CSID].CharingStationID)
        else :
            print ("%s : Min_Charging_Waiting_Time = %s"%(ChargingStation[CSID].CharingStationID,Min_ChargingTime))
        print ("                ")
                                
                    
                
    
# =============================================================================
#                             if ChargingStation[CSID].ChargingWaitingTime2[i] != 0:
#                                 if ChargingStation[CSID].ChargingWaitingTime2[i] < Min_ChargingTime:
#                                     Min_ChargingTime = ChargingStation[CSID].ChargingWaitingTime2[i]
#                                     print("CS %s : Min_ChargingWaitingTime = %s" %(ChargingStation[CSID].CharingStationID,Min_ChargingTime))
# =============================================================================
            
    return Vehicle




    
    
    
    
