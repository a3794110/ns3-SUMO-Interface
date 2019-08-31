
#!/bin/bash


# ----------------------------------------------------defined by user
export NS3_HOME='/home/hank/ns-allinone-3.26/ns-3.26' #ns-3 working directory (the folder contained with "scratch", "waf-tools" etc.)
# ----------------------------------------------------



export simconfig=''
export ns3path='scratch/UrbanMobilitySimulationwithLte '




if [ $1 == 'simTime' ] || [ $1 == 'enbTxPowerDbm' ] || [ $1 == 'dlpacketSize' ] || [ $1 == 'dlpacketsInterval' ] || [ $1 == 'ulpacketSize' ] || [ $1 == 'ulpacketsInterval' ] || [ $1 == 'fadingModel' ] 
then
    export simconfig='--'$1'='$2' '$simconfig
fi
if [ $3 == 'simTime' ] || [ $3 == 'enbTxPowerDbm' ] || [ $3 == 'dlpacketSize' ] || [ $3 == 'dlpacketsInterval' ] || [ $3 == 'ulpacketSize' ] || [ $3 == 'ulpacketsInterval' ] || [ $3 == 'fadingModel' ]
then
    export simconfig='--'$3'='$4' '$simconfig
fi
if [ $5 == 'simTime' ] || [ $5 == 'enbTxPowerDbm' ] || [ $5 == 'dlpacketSize' ] || [ $5 == 'dlpacketsInterval' ] || [ $5 == 'ulpacketSize' ] || [ $5 == 'ulpacketsInterval' ] || [ $5 == 'fadingModel' ]
then
    export simconfig='--'$5'='$6' '$simconfig
fi
if [ $7 == 'simTime' ] || [ $7 == 'enbTxPowerDbm' ] || [ $7 == 'dlpacketSize' ] || [ $7 == 'dlpacketsInterval' ] || [ $7 == 'ulpacketSize' ] || [ $7 == 'ulpacketsInterval' ] || [ $7 == 'fadingModel' ]
then
    export simconfig='--'$7'='$8' '$simconfig
fi
if [ $9 == 'simTime' ] || [ $9 == 'enbTxPowerDbm' ] || [ $9 == 'dlpacketSize' ] || [ $9 == 'dlpacketsInterval' ] || [ $9 == 'ulpacketSize' ] || [ $9 == 'ulpacketsInterval' ]|| [ $9 == 'fadingModel' ]
then
    export simconfig='--'$9'='${10}' '$simconfig
fi
if [ ${11} == 'simTime' ] || [ ${11} == 'enbTxPowerDbm' ] || [ ${11} == 'dlpacketSize' ] || [ ${11} == 'dlpacketsInterval' ] || [ ${11} == 'ulpacketSize' ] || [ ${11} == 'ulpacketsInterval' ]|| [ ${11} == 'fadingModel' ]
then
    export simconfig='--'${11}'='${12}' '$simconfig
fi
if [ ${13} == 'simTime' ] || [ ${13} == 'enbTxPowerDbm' ] || [ ${13} == 'dlpacketSize' ] || [ ${13} == 'dlpacketsInterval' ] || [ ${13} == 'ulpacketSize' ] || [ ${13} == 'ulpacketsInterval' ]|| [ ${13} == 'fadingModel' ]
then
    export simconfig='--'${13}'='${14}' '$simconfig
fi


echo $simconfig
cp trajectory.txt $NS3_HOME/scratch
cd $NS3_HOME

./waf --run "$ns3path$simconfig"

