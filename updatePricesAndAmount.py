#!/bin/python3

from modules.skyshopApiAdapter import skyshopApiAdapter
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-o", "--optimaFile", required=True, help="Source file from Optima system")
ap.add_argument("-a", "--webApi", required=True, help="Sky-Shop Web Api")

args = vars(ap.parse_args())


optimaFile = args["optimaFile"]
webApi = args["webApi"]


# MAIN SCRIPT

adapter = skyshopApiAdapter(webApi)


#print("Getting list of hosts by tag " + tag)
#entities = adapter.getHostsByTag(tag)
#entities = adapter.getOneAgentsByTag(tag)

#hosts = {}

#for ent in entities:
#     hosts[ent["hostInfo"]["displayName"]] = ent["hostInfo"]["entityId"]


#if len(hosts)>0:

#     print ("Found " + str(len(hosts)) + " hosts by tag")

#     for k, v in sorted(hosts.items()):

#        print ("Setting " + k + ", hostId=" + v)


      
#else:
#     print ("ERROR: Hosts not found")
