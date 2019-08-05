@ECHO OFF
rem set CD="%~dp0"
rem cd D:\\SumoPractice\\RealMap_0626\\data\\OsmConvertNet
netconvert --osm-files NCKU.osm --remove-edges.by-vclass hov,taxi,bus,delivery,transport,lightrail,cityrail,rail_slow,rail_fast,motorcycle,bicycle,pedestrian -o Net.net.xml
copy /y *.net.xml ..\Simulation 
copy /y *.net.xml ..\NetFile
copy /y *.net.xml ..\RouteFile
pause