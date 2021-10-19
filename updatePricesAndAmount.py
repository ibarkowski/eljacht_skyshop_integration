#!/bin/python3

from modules.skyshopApiAdapter import skyshopApiAdapter
from modules.optimaFileAdapter import optimaFileAdapter
from datetime import datetime

import argparse
import logging

ap = argparse.ArgumentParser()

ap.add_argument("-o", "--optimaFile", required=True, help="Source file from Optima system")
ap.add_argument("-a", "--webApi", required=True, help="Sky-Shop Web Api")

args = vars(ap.parse_args())

#Initializa logging
logging.basicConfig(filename=datetime.now().strftime("log\%Y%m%d_%H%M.log") , level=logging.DEBUG)

optimaFile = args["optimaFile"]
webApi = args["webApi"]


# MAIN SCRIPT

logging.info("Get products from source file: " + optimaFile)
optimaFile = optimaFileAdapter(optimaFile)
optimaProducts = optimaFile.getProductsFromFile()

logging.debug(str(len(optimaProducts)) + " products imported from Optima file" )

adapter = skyshopApiAdapter(webApi)

logging.info("Get products from Sky-Shop")
shopProducts = adapter.getAllProducts()
logging.debug(str(len(shopProducts)) + " products imported from Sky-Shop")


logging.info("Iterating through shop products - START")

for key in shopProducts:
    try:
        out_id = shopProducts[key]["prod_id"]
        out_shopPrice = shopProducts[key]["prod_price"]
        out_shopAmount = shopProducts[key]["prod_amount"]
        out_optimaPrice = optimaProducts[key]["prod_price"]
        out_optimaAmount = optimaProducts[key]["prod_amount"]




    except KeyError as e:
        logging.exception("Article with symbol " + key + " not found in Optima data", exc_info=False) 

#print (shopProducts["Ik213"]["prod_price"])
#print (len(products)) 

#print(products["0"]["prod_id"])

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
