@ECHO OFF
set CD="%~dp0"
netconvert --osm-files map.osm -o map.net.xml
polyconvert -n map.net.xml --osm-files map.osm --type-file typemap.xml -o map.poly.xml
python randomTrips.py -n map.net.xml -e 100 -l -o map.trips.xml
duarouter -n map.net.xml -t map.trips.xml -o map.rou.xml --ignore-errors
sumo-gui map.sumo.cfg
