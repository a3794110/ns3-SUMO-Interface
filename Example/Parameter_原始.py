# -*- coding: utf-8 -*-
import numpy as np


class DataBase():
    def __init__(self):
        self.VehId              = []
        self.CurBatCap          = []    # current battery energy
        self.MaxBatCap          = []    # battery capacity
        self.LowBatTh           = []    # low battery threshold
        self.LowBatFlag         = []    # low battery flag
        self.DestEdge           = []    # destination edge
        self.WaitingTime        = []    #
        self.CurRcvPow          = []    # current receive power
        self.MaxRcvPow          = []    # max receive power
        self.SvcCsId            = []    # service charging station
        self.ChargingFlag       = []    # Charging flag
        self.ChargingTime       = []    # not (ChargEndTime - ChargeStartTime)
        self.ChargeStartTime    = []    # vehicle enter cs to charge, record simulation time 
        self.ChargeEndTime      = []    # vehicle leave cs to charge, record simulation time 
   

class Electric_Vehicle_Parameter():
    def __init__(self):
        self.Accel                   = 3.0
        self.Decel                   = 2.0
        self.Length                  = 5.0
        self.MinGap                  = 2.5
        self.MaxSpeed                = 50
        self.Sigma                   = 0.5
        self.MaximumBatteryCapacity  = 24000
        self.MaximumPower            = 1000
        self.VehicleMass             = 1500
        self.FrontSurfaceArea        = 5
        self.AirDragCoefficient      = 0.6
        self.InternalMomentOfInertia = 0.01
        self.RadialDragCoefficient   = 0.5
        self.RollDragCoefficient     = 0.01
        self.ConstantPowerIntake     = 100
        self.PropulsionEfficiency    = 0.9
        self.RecuperationEfficiency  = 0.9
        self.StoppingTreshold        = 0.1

        
class Charging_Station_Parameter(): 
    def __init__(self):
        self.StartPos           = ['10', '10']
        self.EndPos             = ['50', '50']
        self.RoadsideCapacity   = ['6', '6']
        self.Width              = ['5', '5']
        self.Length             = ['10', '10']
        self.Angle              = ['90', '90']
        #self.CsLane             = ['298600770#4_0', '496257368#24_0', '496257369#1_0']
        self.CsLane             = ['298600770#4_0', '496257369#1_0']                           

    
    def Cs_Edge(self):
        CsEdge = []
        for i in self.CsLane:                    #cs need lane id,but calculate the driving distance that need edge id
            Redundant = i.index('_')
            CsEdge.append(i[0:Redundant])
        return CsEdge
    
    def Cs_Id(self):
        CsId = []
        for i in range(0, len(self.CsLane)):
            CsId.append('CS' + str(i))
        return CsId
    
    def Cs_Num(self):
        return len(self.CsLane)

     
class Current_Charging_Vehicle(): 
    def __init__(self, Name):
        self.CsName = Name
        self.CurChgVeh      = []
        self.CurChgVehNum   = 0
        self.CurCsPowSup    = 0
        self.MaxCsPowSup    = float(np.random.uniform(5, 6, 1))
        
        
class Extra_Handle_Vehicle():
    def __init__(self):
        self.ExtraHandleVehId = []
        self.Curedge = []
        self.ChangeFlag = []
        
    
    
    