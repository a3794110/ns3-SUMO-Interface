# Network Simulation for Urban Mobility: ns-3 and SUMO

## Project Overview
To make network simulation of urban mobility more user-friendly, we design a SUMO module which can do the network simulation in ns-3 with SUMO configuration.

The SUMO module outputs its vehicle trajectory file into ns-3; ns-3 deploy UE mobility with trajectory file. Moreover, the UE in ns-3 are intalled with ***LTE module*** and attach eNodeB when they enter the map. 

To simulate the V2X application scenario, all UE are installed with UDP client application which send packets to remote server in cetain period. The packet interval and packet size can control with SUMO module we build.

## License

BSD 3-Clause License

Copyright (c) 2019, Ping-Han
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.
## Prerequisite
We test our project on following version of ns-3 and SUMO.

    ns-3.26
    SUMO 1.2.0
    python 3.7

Please install SUMO with following commands.
```
sudo apt-get install cmake python g++ libxerces-c-dev libfox-1.6-dev libgdal-dev libproj-dev libgl2ps-dev swig
git clone --recursive https://github.com/eclipse/sumo
export SUMO_HOME="$PWD/sumo"
mkdir sumo/build/cmake-build && cd sumo/build/cmake-build
cmake ../..
make -j$(nproc)
```
    

## Build and Installation

### ns-3
Put files in folder **scratch** we offered into folder **scracth** in ns-3 working directory.
### SUMO 
Put files in folder **SUMO** we offered into the folder **tools** in SUMO working directory.

### Envirment Variables
Modify enviroment variable setting in file **RunNs3.sh** for customization.

    # ----------------------------------------------------defined by user
    export NS3_HOME='/home/hank/ns-allinone-3.26/ns-3.26'                 
    #-----------------------------------------------------defined by user
Make NS3_HOME as your working directory of ns-3.

Moreover, please do the following setting before run this project **everytime**.

    export SUMO_HOME='home/hank/sumo'                  
Make SUMO_HOME as **your** working directory of SUMO (contained with folder bin, build, tools etc.)

## Tutorial

### How to start?

For importing modules, add the following content into the main python script of the project you want to simulate.

```
try:
    
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
    from ControlNs3 import Ns3Simulation
    import traci
    
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")
```


After that, add the following function into the script to call ns-3 for network simulaiton.

    Ns3LteSimulation(simTime = 50, enbTxPowerDbm = 46, packetSize = 1024, packetsInterval = 500, fadingModel = 0) 


### How to modify network simulation configuration?

The description of the function arguments is offered in the following content.
```
def Ns3LteSimulation( simTime = 50, enbTxPowerDbm = 46, packetSize = 1024, packetsInterval = 500, fadingModel = 0):
#============================================================================================
# simTime", "Total duration of the simulation (in seconds)
# enbTxPowerDbm", "TX power [dBm] used by HeNBs (default = 46.0)
# packetSize","Size (bytes) of packets generated (default = 1024 bytes). The minimum packet size is 12 bytes which is the size of the header carrying the sequence number and the time stamp.
# packetsInterval","The time (ms) wait between packets (default = 500 ms)
# fadingModel","setting fading model (1, 2 and 3 represent pedestrian, urban and vehicular scenario respectively)
#============================================================================================
```
As you can see, we can control 5 types of ns-3 simulation parameter from SUMO. (user-friendly!!)

### How to import eNodeB Location files?

We defined the format of eNodeB location file for importing eNodeB locations to simulation scenario. The following content shows the example file. 
```
0 250:500 
1 500:500 
2 750:500 
3 250:750 
4 500:750 
5 750:750 
6 250:1000 
7 500:1000 
8 750:1000
```
The meaning of above mentioned file is offered in the following content.
```
eNodeB_id0 x_position_id0:y_position_id0
eNodeB_id1 x_position_id1:y_position_id1
```

Please modify line 143 and 152 in file UrbanMobilitySimulationwithLte.cc for changing the imported eNodeB location file.
```
ifstream EnbinFile("scratch/EnbLocations2.txt"); 
ifstream Enbcin("scratch/EnbLocations2.txt"); 
```

## Example

We offered an example project in folder **Example**. In this project, vehicles enter the map according to Poisson λ=1 k=1. You can see the example usage in file **main.py**.

The following video shows the result of using different simulation configuration with this project.
https://youtu.be/9UtVOFBHFtk
