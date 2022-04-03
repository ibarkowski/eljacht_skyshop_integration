#!/bin/python3

from modules.skyshopApiAdapter import skyshopApiAdapter
from modules.optimaFileAdapter import optimaFileAdapter
from datetime import datetime

import argparse
import logging

ap = argparse.ArgumentParser()

ap.add_argument("-f", "--optimaFile", required=True, help="Source file from Optima system")
ap.add_argument("-d", "--domain", required=True, help="Sky-Shop domain")
ap.add_argument("-k", "--webApiKey", required=True, help="Web Api Key")

args = vars(ap.parse_args())

# Initialize logging
logging.basicConfig(filename=datetime.now().strftime("log\%Y%m%d_%H%M.log"), level=logging.DEBUG)

optimaFile = args["optimaFile"]
webApi = args["webApiKey"]
domain = args["domain"]

# MAIN SCRIPT

######################################################
# STEP 1 - Import products from Optima file

logging.info("STEP 1 - Get products from source file: " + optimaFile)

optimaFile = optimaFileAdapter(optimaFile)
optimaProducts = optimaFile.getProducts()

logging.debug("STEP 1 - " + str(len(optimaProducts)) + " products imported from Optima file")

######################################################
# STEP 2 - Get all products to verify from Sky-Shop

logging.info("STEP 2 - Get products from Sky-Shop")
shopAdapter = skyshopApiAdapter(domain, webApi)

shopProducts = shopAdapter.getAllProducts(0)


logging.debug("STEP 2 - " + str(len(shopProducts)) + " products imported from Sky-Shop")

#####################################################################################################
# STEP 3 - Iterate through shop products, compare to Optima, and generate product list to change

logging.info("STEP 3 - Iterating through shop products - START")

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
        logging.exception("STEP 3 - Article with symbol " + key + " not found in Optima input file", exc_info=False)

logging.info("STEP 3 - Iterating through shop products - END")

#####################################################################################################
# STEP 4 - Change product prices and amount 

logging.info("STEP 4 - Change product prices and amount")

logging.info("STEP 4 - Prepare payloads for prices, and amount bulk change")

bulkPricesPayload = {}
bulkAmountPayload = {}

p_count = 0
a_count = 0

for k, v in products_to_change.items():

    if v["P"] == "Y":
        bulkPricesPayload["productID[" + str(p_count) + "]"] = str(k)
        bulkPricesPayload["price[" + str(p_count) + "]"] = str(v["new_price"])
        p_count = p_count + 1

    if v["A"] == "Y":
        bulkAmountPayload["productID[" + str(a_count) + "]"] = str(k)
        bulkAmountPayload["amount[" + str(a_count) + "]"] = str(v["new_amount"])
        a_count = a_count + 1

# proceed with prices change

if len(bulkPricesPayload) > 0:

    logging.info("STEP 4 - Execute bulk prices change request")
    pricesChangeResponse = shopAdapter.bulkProductPricesChange(bulkPricesPayload)
    logging.debug(pricesChangeResponse.content)

    if pricesChangeResponse.status_code == 200:

        changed = pricesChangeResponse.json()["changed"]
        skipped = pricesChangeResponse.json()["skipped"]

        if len(changed) > 0:

            logging.info("STEP 4 - Prices changed for " + str(len(changed)) + " products:")

            for k in changed:
                logging.info("  ProductID: " + str(k) + "; Product Symbol: " + products_to_change[str(k)][
                    "symbol"] + "; Price " + products_to_change[str(k)]["old_price"] + " >> " +
                             products_to_change[str(k)]["new_price"])

        if len(skipped) > 0:

            logging.info("STEP 4 - Prices change skipped for " + str(len(skipped)) + " products:")

            for k in skipped:
                logging.info("  ProductID: " + str(k) + "; Product Symbol: " + products_to_change[str(k)][
                    "symbol"] + "; Price " + products_to_change[str(k)]["old_price"] + " >> " +
                             products_to_change[str(k)]["new_price"])
        else:
            logging.info("STEP 4 - All prices changed")

else:
    logging.info("STEP 4 - There is no prices to change - skipping")

# proceed with amount change

if len(bulkAmountPayload) > 0:

    logging.info("STEP 4 - Execute bulk amount change request")

    amountChangeResponse = shopAdapter.bulkProductAmountChange(bulkAmountPayload)
    logging.debug(amountChangeResponse.content)

    if amountChangeResponse.status_code == 200:

        changed = amountChangeResponse.json()["changed"]
        skipped = amountChangeResponse.json()["skipped"]

        if len(changed) > 0:

            logging.info("STEP 4 - Amount changed for " + str(len(changed)) + " products:")

            for k in changed:
                logging.info("  ProductID: " + str(k) + "; Product Symbol: " + products_to_change[str(k)][
                    "symbol"] + "; Amount " + products_to_change[str(k)]["old_amount"] + " >> " +
                             products_to_change[str(k)]["new_amount"])

        if len(skipped) > 0:

            logging.info("STEP 4 - Amount change skipped for " + str(len(skipped)) + " products:")

            for k in skipped:
                logging.info("  ProductID: " + str(k) + "; Product Symbol: " + products_to_change[str(k)][
                    "symbol"] + "; Amount " + products_to_change[str(k)]["old_amount"] + " >> " +
                             products_to_change[str(k)]["new_amount"])
        else:
            logging.info("STEP 4 - All amounts changed")

else:

    logging.info("STEP 4 - There is no amount to change - skipping")

logging.info("Update completed")
