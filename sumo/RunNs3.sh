
#!/bin/bash


# ----------------------------------------------------defined by user
export NS3_HOME='/home/hank/ns-allinone-3.26/ns-3.26' #ns-3 working directory (the folder contained with "scratch", "waf-tools" etc.)
# ----------------------------------------------------



export simconfig=''
export ns3path='scratch/UrbanMobilitySimulationwithLte '




if [ $1 == 'simTime' ] || [ $1 == 'enbTxPowerDbm' ] || [ $1 == 'packetSize' ] || [ $1 == 'packetsInterval' ] || [ $1 == 'fadingModel' ] 
then
    export simconfig='--'$1'='$2' '$simconfig
fi
if [ $3 == 'simTime' ] || [ $3 == 'enbTxPowerDbm' ] || [ $3 == 'packetSize' ] || [ $3 == 'packetsInterval' ] || [ $3 == 'fadingModel' ]
then
    export simconfig='--'$3'='$4' '$simconfig
fi
if [ $5 == 'simTime' ] || [ $5 == 'enbTxPowerDbm' ] || [ $5 == 'packetSize' ] || [ $5 == 'packetsInterval' ] || [ $5 == 'fadingModel' ]
then
    export simconfig='--'$5'='$6' '$simconfig
fi
if [ $7 == 'simTime' ] || [ $7 == 'enbTxPowerDbm' ] || [ $7 == 'packetSize' ] || [ $7 == 'packetsInterval' ] || [ $7 == 'fadingModel' ]
then
    export simconfig='--'$7'='$8' '$simconfig
fi
if [ $9 == 'simTime' ] || [ $9 == 'enbTxPowerDbm' ] || [ $9 == 'packetSize' ] || [ $9 == 'packetsInterval' ] || [ $9 == 'fadingModel' ]
then
    export simconfig='--'$9'='${10}' '$simconfig

fi
echo $simconfig
cp trajectory.txt $NS3_HOME/scratch
cd $NS3_HOME

./waf --run "$ns3path$simconfig"

