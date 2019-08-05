@ECHO OFF
rem set CD="%~dp0"
cd D:\SUMO\RoutingRealMap\data\RouteFile
del *.rou.xml *.rou.alt.xml
duarouter.exe -n Net.net.xml --route-files Trip.trips.xml -o Route.rou.xml --ignore-errors
copy /y *.rou.xml ..\Simulation
pause
