# -*- coding: utf-8 -*-
import numpy as np
import random 
import sys
import os
#import traci

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

           
class On_Board_Unit():
    def __init__(self): 
        self.VehId   = ' '
        self.Speed   = self.Speed()
        self.Mass    = 0
# =============================================================================
#         self.frontSurfaceArea        = 2.65   #迎風面積(車寬*車高)
#         self.airDragCoefficient      = 0.32   #空氣阻力係數
# #        self.internalMomentOflnertia = 5      #恩災
#         self.rollDragCoefficient     = 0.015    #滾動阻力係數
# #        self.radialDragCoefficient   = 0.5    #恩災
#         self.recuperationEfficiency  = 0.9    #傳動效率 
# =============================================================================
        
        self.MaxBatteryCapacity     = int(np.random.choice(['24000']))
        self.CurrentBatteryCapacity = int(np.random.randint(15000, self.MaxBatteryCapacity))
        self.MaxReceivePower        = float(np.random.uniform(2, 5, 1))               
        self.CurrentReceivePower    = 0                                         
        self.BatteryConsume         = 0
        self.Position               = 0
        self.Route                  = {}
        self.RoadID                 = {}
        self.EndTarget              = {}
        self.Distance               = 0    #車子離開網路，Distance錯誤 -1001
        self.RealDistance           = 0    #選擇 >0的行車距離
        self.BatteryPercent         = 0
        self.Give_Power             = 0    #充電站給車子的電量
        self.ChargingTime           = 0
        self.VehWaitingTime         = 0
        self.CumlativePower         = 0
        self.count                  = 1
        self.count2                 = 0
        self.num                    = 1
        self.cnt                    = 1
        
        self.IdentityID             = 0    #車子進充電站所給的識別碼
        self.ChargingEffective      = 0
        self.VehCS1                 = 0    #持續偵測下 所決定的充電站 (可能與CS2不同)
        self.VehCS2                 = 0    #第一時間點 所決定的充電站
        

        
    def Speed(self):                                    # 50 ~ 100
        np.random.seed()                                     
        return random.uniform(13.89, 22.78)
    
    def Get_Vehicle_Information(self) :
        self.Position  =  traci.vehicle.getLanePosition(self.VehId)
        self.Route     =  traci.vehicle.getRoute(self.VehId)
        if self.num == 1 :
            self.EndTarget = self.Route[-1]    #紀錄最終目的地
            self.num = self.num - 1
        self.RoadID    =  traci.vehicle.getRoadID(self.VehId)
        self.Distance  =  traci.vehicle.getDistance(self.VehId)
        if self.Distance > 0:
            self.RealDistance = self.Distance          
    
    
    def Caculate_Current_Battery_Capacity(self):
        np.random.seed()
        
        self.Mass = traci.vehicle.setParameter(self.VehId, "device.battery.vehicleMass", '1521')                         #將車重改為1521KG (Nissan Leaf)
 #       self.frontSurfaceArea = traci.vehicle.setParameter (self.VehId,"device.battery.frontSurfaceArea",'2.65')           #迎風面積改為2.65
 #       self.airDragCoefficient = traci.vehicle.setParameter (self.VehId,"device.battery.airDragCoefficient",'0.32')       #空氣阻力係數0.32
 #       self.rollDragCoefficient = traci.vehicle.setParameter(self.VehId,"device.battery.rollDragCoefficient", '0.015')    #滾動阻力係數0.015
 #       self.recuperationEfficiency = traci.vehicle.setParameter(self.VehId,"device.battery.recuperationEfficiency",'0.9') #傳動效率 0.9
        self.BatteryConsume = float(traci.vehicle.getParameter(self.VehId,"device.battery.energyConsumed"))
        self.CurrentBatteryCapacity = self.CurrentBatteryCapacity - self.BatteryConsume
        self.BatteryPercent = (self.CurrentBatteryCapacity / self.MaxBatteryCapacity) * 100


class Charging_Station_Information():
    def __init__(self):
        self.CharingStationVehNum   =  0
        self.ChargingWaitingTime    =  []
        self.ChargingWaitingTime2   =  []    #會隨時間減少的Charging time
        self.CharingStationPower    = 200000
        self.CharingStationLane     = ['313194389#2','111343192#0','111343192#2','536831320#4','279049706#6','496257368#3']
        self.CharingStationID       = ' '
        self.CharingStationDistance = 0
        self.count                  = 1
                
        self.CurrentChargingMoney   = 10
        self.CharingStationIdentityID = []
        self.MinChargingWaitingTime = 0
        self.ChargingEffective      = 0

    


        
            
            
            

         
