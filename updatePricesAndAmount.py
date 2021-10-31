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

######################################################
# STEP 1 - Import products from Optima file

logging.info("Get products from source file: " + optimaFile)

optimaFile = optimaFileAdapter(optimaFile)
optimaProducts = optimaFile.getProductsFromFile()

logging.debug(str(len(optimaProducts)) + " products imported from Optima file" )


######################################################
# STEP 2 - Get all products to verify from Sky-Shop

logging.info("Get products from Sky-Shop")
shopAdapter = skyshopApiAdapter(webApi)
shopProducts = shopAdapter.getAllProducts()
logging.debug(str(len(shopProducts)) + " products imported from Sky-Shop")


#####################################################################################################
# STEP 3 - Iterate through shop products, compare to Optima, and generate product list to change

logging.info("Iterating through shop products - START")

products_to_change = {}

for key in shopProducts:
    try:
        out_id = shopProducts[key]["prod_id"]
        out_symbol = key
        out_shopPrice = shopProducts[key]["prod_price"]
        out_shopAmount = shopProducts[key]["prod_amount"]
        out_optimaPrice = optimaProducts[key]["prod_price"]
        out_optimaAmount = optimaProducts[key]["prod_amount"]

        products_to_change[out_id] = {}
        products_to_change[out_id]["symbol"] = out_symbol
        products_to_change[out_id]["old_price"] = out_shopPrice
        products_to_change[out_id]["new_price"] = out_optimaPrice
        products_to_change[out_id]["old_amount"] = out_shopAmount
        products_to_change[out_id]["new_amount"] = out_optimaAmount

        if out_shopPrice != out_optimaPrice:
            products_to_change[out_id]["P"] = "Y"
        else:
            products_to_change[out_id]["P"] = "N"

        if out_shopAmount != out_optimaAmount:
            products_to_change[out_id]["A"] = "Y"
        else:
            products_to_change[out_id]["A"] = "N"

    except KeyError as e:
        logging.exception("Article with symbol " + key + " not found in Optima input file", exc_info=True) 


logging.info("Iterating through shop products - END")


#####################################################################################################
# STEP 4 - Change product prices and amount 

logging.info("Iterating through shop products - START")

print (len(products_to_change))


for k, v in products_to_change.items():
    print(k, v)
