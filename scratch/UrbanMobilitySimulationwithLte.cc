#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/lte-module.h"
#include "ns3/applications-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/config-store-module.h"
#include <ns3/netanim-module.h>
//================================-------------------------------------
#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
//=================================--------------------------------------
using namespace ns3;
using namespace std;

NS_LOG_COMPONENT_DEFINE ("LenaX2HandoverMeasures");
Ptr<LteHelper> lteHelper = CreateObject<LteHelper> ();

void attachinfuture(NetDeviceContainer& ues, int ueid){
  lteHelper->Attach (ues.Get(ueid));
  //lteHelper->Attach (ues, enbs.Get (1));
  std::cout<<"attach"<<std::endl;
}


void
NotifyConnectionEstablishedUe (std::string context,
                              uint64_t imsi,
                              uint16_t cellid,
                              uint16_t rnti)
{
  std::cout << "at "<<Simulator::Now ().GetSeconds () << "s "<< context
            << " UE IMSI " << imsi
            << ": connected to CellId " << cellid
            << " with RNTI " << rnti
            << std::endl;
}

void
NotifyHandoverStartUe (std::string context,
                      uint64_t imsi,
                      uint16_t cellid,
                      uint16_t rnti,
                      uint16_t targetCellId)
{
  std::cout << context
            << " UE IMSI " << imsi
            << ": previously connected to CellId " << cellid
            << " with RNTI " << rnti
            << ", doing handover to CellId " << targetCellId
            << std::endl;
}

void
NotifyHandoverEndOkUe (std::string context,
                      uint64_t imsi,
                      uint16_t cellid,
                      uint16_t rnti)
{
  std::cout << context
            << " UE IMSI " << imsi
            << ": successful handover to CellId " << cellid
            << " with RNTI " << rnti
            << std::endl;
}

void
NotifyConnectionEstablishedEnb (std::string context,
                                uint64_t imsi,
                                uint16_t cellid,
                                uint16_t rnti)
{
  std::cout << context
            << " eNB CellId " << cellid
            << ": successful connection of UE with IMSI " << imsi
            << " RNTI " << rnti
            << std::endl;
}

void
NotifyHandoverStartEnb (std::string context,
                        uint64_t imsi,
                        uint16_t cellid,
                        uint16_t rnti,
                        uint16_t targetCellId)
{
  std::cout << context
            << " eNB CellId " << cellid
            << ": start handover of UE with IMSI " << imsi
            << " RNTI " << rnti
            << " to CellId " << targetCellId
            << std::endl;
}

void
NotifyHandoverEndOkEnb (std::string context,
                        uint64_t imsi,
                        uint16_t cellid,
                        uint16_t rnti)
{
  std::cout << context
            << " eNB CellId " << cellid
            << ": completed handover of UE with IMSI " << imsi
            << " RNTI " << rnti
            << std::endl;
}


int
main (int argc, char *argv[])
{
  // LogLevel logLevel = (LogLevel)(LOG_PREFIX_ALL | LOG_LEVEL_ALL);

  // LogComponentEnable ("LteHelper", logLevel);
  // LogComponentEnable ("EpcHelper", logLevel);
  // LogComponentEnable ("EpcEnbApplication", logLevel);
  // LogComponentEnable ("EpcX2", logLevel);
  // LogComponentEnable ("EpcSgwPgwApplication", logLevel);
  // LogComponentEnable ("LteEnbRrc", logLevel);
  // LogComponentEnable ("LteEnbNetDevice", logLevel);
  // LogComponentEnable ("LteUeRrc", logLevel);
  // LogComponentEnable ("LteUeNetDevice", logLevel);
  // LogComponentEnable ("A2A4RsrqHandoverAlgorithm", logLevel);
  // LogComponentEnable ("A3RsrpHandoverAlgorithm", logLevel);
  // LogComponentEnable ("UdpTraceClient", LOG_LEVEL_INFO);


  //============================================================================================================ for retrieve number of ues
    ifstream inFile("scratch/trajectory.txt"); 
    int lines;                  //counting number of lines in this file
    string words ;               //store the word we are processing on

    lines = count( istreambuf_iterator<char>(inFile),    //count line
        istreambuf_iterator<char>(), '\n');
    cout<<lines<<endl; //----------------------------------------set node number here
    inFile.close();
  //=============================================================================================================

  //============================================================================================================ for retrieve number of enbs
    ifstream EnbinFile("scratch/EnbLocations2.txt"); 
    int enblines;                  //counting number of lines in this file
    //string words ;               //store the word we are processing on

    enblines = count( istreambuf_iterator<char>(EnbinFile),    //count line
        istreambuf_iterator<char>(), '\n');
    cout<<enblines<<endl; //----------------------------------------set node number here
    EnbinFile.close();  
    
    ifstream Enbcin("scratch/EnbLocations2.txt"); 
  //=============================================================================================================

  uint16_t numberOfUes = lines;
  uint16_t numberOfEnbs = enblines;
  uint16_t numBearersPerUe = 1;
  //double distance = 500.0; // m
  //double yForUe = 500.0;   // m
  //double speed = 40;       // m/s
  //double simTime = (double)(numberOfEnbs + 1) * distance / speed; // 1500 m / 20 m/s = 75 secs
  double simTime = (double)30;
  double enbTxPowerDbm = 46.0;




  // Command line arguments
  unsigned int dlinterval = 300, dlpacketsize = 1024, ulinterval = 300, ulpacketsize = 1024, fadingmodel = 0;
  CommandLine cmd;
  cmd.AddValue ("simTime", "Total duration of the simulation (in seconds)", simTime);
  //cmd.AddValue ("speed", "Speed of the UE (default = 20 m/s)", speed);
  cmd.AddValue ("enbTxPowerDbm", "TX power [dBm] used by HeNBs (default = 46.0)", enbTxPowerDbm);
  cmd.AddValue ("dlpacketSize","Size (bytes) of packets generated (default = 1024 bytes). The minimum packet size is 12 bytes which is the size of the header carrying the sequence number and the time stamp.", dlpacketsize);
  cmd.AddValue ("dlpacketsInterval","The time (ms) wait between packets (default = 500 ms)", dlinterval);
  cmd.AddValue ("ulpacketSize","Size (bytes) of packets generated (default = 1024 bytes). The minimum packet size is 12 bytes which is the size of the header carrying the sequence number and the time stamp.", ulpacketsize);
  cmd.AddValue ("ulpacketsInterval","The time (ms) wait between packets (default = 500 ms)", ulinterval);
  cmd.AddValue ("fadingModel","setting fading model (1, 2 and 3 represent pedestrian, urban and vehicular scenario respectively)", fadingmodel);
  cmd.Parse (argc, argv);

  // change some default attributes so that they are reasonable for
  // this scenario, but do this before processing command line
  // arguments, so that the user is allowed to override these settings
  Config::SetDefault ("ns3::UdpClient::Interval", TimeValue (MilliSeconds (500)));
  Config::SetDefault ("ns3::UdpClient::MaxPackets", UintegerValue (4294967295));
  //Config::SetDefault ("ns3::UdpClient::PacketSize", UintegerValue (packetsize));
  //Config::SetDefault ("ns3::UdpClient::Interval", TimeValue(MilliSeconds (interval)));
  Config::SetDefault ("ns3::LteHelper::UseIdealRrc", BooleanValue (true));
  Config::SetDefault ("ns3::LteEnbPhy::TxPower", DoubleValue (enbTxPowerDbm));

  //=========================================================================================================setting fading model
  if (fadingmodel != 0){
    lteHelper->SetFadingModel("ns3::TraceFadingLossModel");

    switch (fadingmodel)
    {
    case 1/* constant-expression */:
      lteHelper->SetFadingModelAttribute ("TraceFilename", StringValue ("src/lte/model/fading-traces/fading_trace_EPA_3kmph.fad"));
      break;

    case 2:
      lteHelper->SetFadingModelAttribute ("TraceFilename", StringValue ("src/lte/model/fading-traces/fading_trace_ETU_3kmph.fad"));
      break;

    case 3:
      lteHelper->SetFadingModelAttribute ("TraceFilename", StringValue ("src/lte/model/fading-traces/fading_trace_EVA_3kmph.fad"));
      break;

    default:
      break;
    }  
    lteHelper->SetFadingModelAttribute ("TraceLength", TimeValue (Seconds (10.0)));
    lteHelper->SetFadingModelAttribute ("SamplesNum", UintegerValue (10000));
    lteHelper->SetFadingModelAttribute ("WindowSize", TimeValue (Seconds (0.5)));
    lteHelper->SetFadingModelAttribute ("RbNum", UintegerValue (100));
  }
  //=========================================================================================================setting fading model

  //Ptr<LteHelper> lteHelper = CreateObject<LteHelper> ();
  Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper> ();

  lteHelper->SetEpcHelper (epcHelper);
  lteHelper->SetSchedulerType ("ns3::RrFfMacScheduler");

  lteHelper->SetHandoverAlgorithmType ("ns3::A2A4RsrqHandoverAlgorithm");
  lteHelper->SetHandoverAlgorithmAttribute ("ServingCellThreshold",
                                            UintegerValue (30));
  lteHelper->SetHandoverAlgorithmAttribute ("NeighbourCellOffset",
                                            UintegerValue (1));

  //  lteHelper->SetHandoverAlgorithmType ("ns3::A3RsrpHandoverAlgorithm");
  //  lteHelper->SetHandoverAlgorithmAttribute ("Hysteresis",
  //                                            DoubleValue (3.0));
  //  lteHelper->SetHandoverAlgorithmAttribute ("TimeToTrigger",
  //                                            TimeValue (MilliSeconds (256)));

  Ptr<Node> pgw = epcHelper->GetPgwNode ();

  // Create a single RemoteHost
  NodeContainer remoteHostContainer;
  remoteHostContainer.Create (1);
  Ptr<Node> remoteHost = remoteHostContainer.Get (0);
  InternetStackHelper internet;
  internet.Install (remoteHostContainer);

  // Create the Internet
  PointToPointHelper p2ph;

  p2ph.SetDeviceAttribute ("DataRate", DataRateValue (DataRate ("100Gb/s")));
  p2ph.SetDeviceAttribute ("Mtu", UintegerValue (1500));
  p2ph.SetChannelAttribute ("Delay", TimeValue (Seconds (0.010)));
  NetDeviceContainer internetDevices = p2ph.Install (pgw, remoteHost);
  Ipv4AddressHelper ipv4h;
  ipv4h.SetBase ("1.0.0.0", "255.0.0.0");
  Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign (internetDevices);
  Ipv4Address remoteHostAddr = internetIpIfaces.GetAddress (1);


  // Routing of the Internet Host (towards the LTE network)
  Ipv4StaticRoutingHelper ipv4RoutingHelper;
  Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting (remoteHost->GetObject<Ipv4> ());
  // interface 0 is localhost, 1 is the p2p device
  remoteHostStaticRouting->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.0.0.0"), 1);

  /*
  * Network topology:
  *
  *      |     + --------------------------------------------------------->
  *      |     UE
  *      |
  *      |               d                   d                   d
  *    y |     |-------------------x-------------------x-------------------
  *      |     |                 eNodeB              eNodeB
  *      |   d |
  *      |     |
  *      |     |                                             d = distance
  *            o (0, 0, 0)                                   y = yForUe
  */

  NodeContainer ueNodes;
  NodeContainer enbNodes;
  enbNodes.Create (numberOfEnbs);
  ueNodes.Create (numberOfUes);

  // Install Mobility Model in eNB---------------------------------------------------------------------------------

  /* for (uint16_t i = 0; i < numberOfEnbs; i++)
    {
      Vector enbPosition (distance/2 * (i + 1), distance, 0);
      enbPositionAlloc->Add (enbPosition);
    }*/
  Ptr<ListPositionAllocator> enbPositionAlloc = CreateObject<ListPositionAllocator> ();
  for(int i = 0 ; i < enblines ; i ++ ){
      string enbtmp_ch, locationx, locationy;                  //for comparing
      getline(Enbcin, words);
      int xory=0;
      for (unsigned int j = 0; j < words.length(); j++){
        enbtmp_ch = words[j];

        if( enbtmp_ch == ":"  ){
            xory+=1;
            continue;
        }
        if( enbtmp_ch == " "){
            if(xory != 0){
                Vector enbPosition (stof(locationx), stof(locationy), 0);
                enbPositionAlloc->Add (enbPosition);
                //ueWaypointMobility->AddWaypoint(Waypoint(Seconds(stof(time)),Vector(stof(locationx),stof(locationy),0)));
                cout<<locationx<<" "<<locationy<<endl;  //----------------------deploy node in here
            }
            xory+=1;
            continue;
        }
        else if( xory == 1){
            locationx.append(enbtmp_ch);
            //cout<<"location:"<<location<<endl;
        }
        else if( xory == 2){
            locationy.append(enbtmp_ch);
        }
      }
      xory = 0;
      locationx.erase();
      locationy.erase();
  }
  //----------------------------------------------------------------------------------------------------------------

  MobilityHelper enbMobility;
  enbMobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  enbMobility.SetPositionAllocator (enbPositionAlloc);
  enbMobility.Install (enbNodes);

  // Install Mobility Model in UE
  MobilityHelper ueMobility;
  ueMobility.SetMobilityModel ("ns3::WaypointMobilityModel");
  //ueMobility.SetMobilityModel("ns3::WaypointMobilityModel");  //mobility.SetMobilityModel ("ns3::");
  ueMobility.Install (ueNodes);

/*for(int i = 0; i < 1500; i++){
  Ptr<WaypointMobilityModel> ueWaypointMobility = DynamicCast<WaypointMobilityModel>( ueNodes.Get(i)->GetObject<MobilityModel>());
  ueWaypointMobility->AddWaypoint(Waypoint(Seconds(2+1/15),Vector(i,500,0)));
}*/







//=======================================================================================================================================================
ifstream cin("scratch/trajectory.txt"); 
int first_enter[lines];    //store enter time for each vehicle
for(int i = 0 ; i < lines ; i ++ ){
  Ptr<WaypointMobilityModel> ueWaypointMobility = DynamicCast<WaypointMobilityModel>( ueNodes.Get(i)->GetObject<MobilityModel>());   
  string tmp_ch;                  //for comparing

  int TimeOrLocation = 0, num_locations=0;        //using this variable for checking the loaded data is time or location ( odd is time)
  
  string node_id, time, locationx, locationy;    // time/location string for storing configuration

  getline(cin, words);
  
  //cout<<words<<endl;

  for (unsigned int j = 0; j < words.length(); j++){
    tmp_ch = words[j];

    if( tmp_ch == ":"  ){
        TimeOrLocation+=1;
        continue;
    }
    if( tmp_ch == " "){
        if(TimeOrLocation != 0){
            
            ueWaypointMobility->AddWaypoint(Waypoint(Seconds(stof(time)),Vector(stof(locationx),stof(locationy),0)));
            cout<<time<<" "<<locationx<<" "<<locationy<<endl;  //----------------------deploy node in here
            num_locations += 1;
            if (num_locations == 1)
              first_enter[i] = stof(time);  
        }
        TimeOrLocation+=1;
        time.erase()  ;       //erase for the next round
        locationx.erase();
        locationy.erase();
        continue;
    }
    if(TimeOrLocation == 0){
        node_id.append(tmp_ch);   //-----------------------------------------------------set node mobility
        cout<<"node id:"<<tmp_ch<<endl;
        continue;
    }

    if ( (TimeOrLocation%3) == 1){
        time.append(tmp_ch);
        //tmp2 = stoi(time);
        //cout<<"time:"<<time<<" "<<endl;
    }
    else if( (TimeOrLocation%3) == 2){
        locationx.append(tmp_ch);
        //cout<<"location:"<<location<<endl;
    }
    else{
        locationy.append(tmp_ch);
    }
  }
    //cout<<time<<" "<<locationx<<" "<<locationy<<endl;
    
    TimeOrLocation = 0;
    num_locations = 0;
}
  //ueNodes.Get (0)->GetObject<MobilityModel> ()->SetPosition (Vector (0, yForUe, 0));
  //ueNodes.Get (0)->GetObject<ConstantVelocityMobilityModel> ()->SetVelocity (Vector (speed, 0, 0));


//======================================================================================================================================================








  // Install LTE Devices in eNB and UEs
  NetDeviceContainer enbLteDevs = lteHelper->InstallEnbDevice (enbNodes);
  NetDeviceContainer ueLteDevs = lteHelper->InstallUeDevice (ueNodes);

  // Install the IP stack on the UEs
  internet.Install (ueNodes);
  Ipv4InterfaceContainer ueIpIfaces;
  ueIpIfaces = epcHelper->AssignUeIpv4Address (NetDeviceContainer (ueLteDevs));

  // Attach all UEs to the first eNodeB
  /*for (uint16_t i = 0; i < numberOfUes; i++)
    {
      lteHelper->Attach (ueLteDevs.Get (i), enbLteDevs.Get (0));
    }*/


  NS_LOG_LOGIC ("setting up applications");

  // Install and start applications on UEs and remote host
  uint16_t dlPort = 10000;
  uint16_t ulPort = 20000;

  // randomize a bit start times to avoid simulation artifacts
  // (e.g., buffer overflows due to packet transmissions happening
  // exactly at the same time)
  Ptr<UniformRandomVariable> startTimeSeconds = CreateObject<UniformRandomVariable> ();
  startTimeSeconds->SetAttribute ("Min", DoubleValue (0));
  startTimeSeconds->SetAttribute ("Max", DoubleValue (0.010));

  lteHelper->AddX2Interface (enbNodes);

  for (uint32_t u = 0; u < numberOfUes; ++u)
    {
      Ptr<Node> ue = ueNodes.Get (u);
      // Set the default gateway for the UE
      Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting (ue->GetObject<Ipv4> ());
      ueStaticRouting->SetDefaultRoute (epcHelper->GetUeDefaultGatewayAddress (), 1);

      for (uint32_t b = 0; b < numBearersPerUe; ++b)
        {
          ++dlPort;
          ++ulPort;

          ApplicationContainer clientApps;
          ApplicationContainer serverApps;

          NS_LOG_LOGIC ("installing UDP DL app for UE " << u);
          UdpClientHelper dlClientHelper (ueIpIfaces.GetAddress (u), dlPort);

          dlClientHelper.SetAttribute ("Interval", TimeValue(MilliSeconds (dlinterval)));
          //dlClientHelper.SetAttribute ("MaxPackets", UintegerValue(100000));
          dlClientHelper.SetAttribute ("PacketSize", UintegerValue (dlpacketsize));


          clientApps.Add (dlClientHelper.Install (remoteHost));
          PacketSinkHelper dlPacketSinkHelper ("ns3::UdpSocketFactory",
                                              InetSocketAddress (Ipv4Address::GetAny (), dlPort));
          serverApps.Add (dlPacketSinkHelper.Install (ue));

          NS_LOG_LOGIC ("installing UDP UL app for UE " << u);
          UdpClientHelper ulClientHelper (remoteHostAddr, ulPort);

          ulClientHelper.SetAttribute ("Interval", TimeValue(MilliSeconds (ulinterval)));
          //dlClientHelper.SetAttribute ("MaxPackets", UintegerValue(100000));
          ulClientHelper.SetAttribute ("PacketSize", UintegerValue (ulpacketsize));

          clientApps.Add (ulClientHelper.Install (ue));
          PacketSinkHelper ulPacketSinkHelper ("ns3::UdpSocketFactory",
                                              InetSocketAddress (Ipv4Address::GetAny (), ulPort));
          serverApps.Add (ulPacketSinkHelper.Install (remoteHost));

          Ptr<EpcTft> tft = Create<EpcTft> ();
          EpcTft::PacketFilter dlpf;
          dlpf.localPortStart = dlPort;
          dlpf.localPortEnd = dlPort;
          tft->Add (dlpf);
          EpcTft::PacketFilter ulpf;
          ulpf.remotePortStart = ulPort;
          ulpf.remotePortEnd = ulPort;
          tft->Add (ulpf);
          EpsBearer bearer (EpsBearer::NGBR_VIDEO_TCP_DEFAULT);
          lteHelper->ActivateDedicatedEpsBearer (ueLteDevs.Get (u), bearer, tft);

          Time startTime = Seconds (startTimeSeconds->GetValue ());
          serverApps.Start (startTime);
          clientApps.Start (startTime);

        } // end for b
    }


  // Add X2 interface
 

  // X2-based Handover
  //lteHelper->HandoverRequest (Seconds (0.100), ueLteDevs.Get (0), enbLteDevs.Get (0), enbLteDevs.Get (1));

  // Uncomment to enable PCAP tracing
  // p2ph.EnablePcapAll("lena-x2-handover-measures");

  lteHelper->EnablePhyTraces ();
  lteHelper->EnableMacTraces ();
  lteHelper->EnableRlcTraces ();
  lteHelper->EnablePdcpTraces ();
  Ptr<RadioBearerStatsCalculator> rlcStats = lteHelper->GetRlcStats ();
  rlcStats->SetAttribute ("EpochDuration", TimeValue (Seconds (1.0)));
  Ptr<RadioBearerStatsCalculator> pdcpStats = lteHelper->GetPdcpStats ();
  pdcpStats->SetAttribute ("EpochDuration", TimeValue (Seconds (1.0)));

  // connect custom trace sinks for RRC connection establishment and handover notification
  Config::Connect ("/NodeList/*/DeviceList/*/LteEnbRrc/ConnectionEstablished",
                  MakeCallback (&NotifyConnectionEstablishedEnb));
  Config::Connect ("/NodeList/*/DeviceList/*/LteUeRrc/ConnectionEstablished",
                  MakeCallback (&NotifyConnectionEstablishedUe));
  Config::Connect ("/NodeList/*/DeviceList/*/LteEnbRrc/HandoverStart",
                  MakeCallback (&NotifyHandoverStartEnb));
  Config::Connect ("/NodeList/*/DeviceList/*/LteUeRrc/HandoverStart",
                  MakeCallback (&NotifyHandoverStartUe));
  Config::Connect ("/NodeList/*/DeviceList/*/LteEnbRrc/HandoverEndOk",
                  MakeCallback (&NotifyHandoverEndOkEnb));
  Config::Connect ("/NodeList/*/DeviceList/*/LteUeRrc/HandoverEndOk",
                  MakeCallback (&NotifyHandoverEndOkUe));

for ( int i = 0; i < lines ; i ++){
  Simulator::Schedule(Seconds(first_enter[i]),
                        &attachinfuture,
                        ueLteDevs,
                        i
                        );
}

  Simulator::Stop (Seconds (simTime));
  AnimationInterface anim("handover.xml");
  anim.SetStartTime (Seconds(0));
  anim.SetStopTime(Seconds(simTime));

  p2ph.EnablePcapAll ("Ns3andSumo722");


  Simulator::Run ();

  // GtkConfigStore config;
  // config.ConfigureAttributes ();

  Simulator::Destroy ();
  return 0;
 
 }
