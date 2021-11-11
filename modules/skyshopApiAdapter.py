import requests
import json

class skyshopApiAdapter:

    def __init__(self, domain="", webApi=""):
 
        self.env_uri = "https://" + domain + "/api/?APIkey=" + webApi + "&function="
           
            

    ###############################
    # Generic request to SKY-SHOP
    ###############################
          
    def __apiRequest(self, method="GET", uri="", body=""):

          header = {}

          files=[]

          url = self.env_uri + uri

          if method == 'GET':
               response = requests.get(url, headers=header, params=body, files=files)
          elif method == 'POST':
               response = requests.post(url, headers=header, data=body, files=files)
          elif method == 'PUT':
               response = requests.put(url, headers=header, data=body, files=files)
               

          return response


    #########################
    # GET All Active Products
    #########################

    def getAllProducts(self, offset="0"):

          search = {'search': 'prod_hidden=0'}
          
          resp = self.__apiRequest("GET", "getProducts&start=" + offset + "&limit=1000", search)

          products = {}

          if resp.status_code == 200:
            prd = resp.json()

            for r in range(len(prd)-1):

                prod_id = (prd[str(r)]["prod_id"])
                prod_symbol = (prd[str(r)]["prod_symbol"])
                prod_price = (prd[str(r)]["prod_price"])
                prod_price = "{:.2f}".format(float(prod_price))   # normalize to 2 decimal places
                prod_amount = (prd[str(r)]["prod_amount"])
                prod_amount = "{:.0f}".format(float(prod_amount))

                if prod_symbol.strip():                           # get only products with symbol defined

                    products[prod_symbol] = {}
                    products[prod_symbol]["prod_id"] = prod_id
                    products[prod_symbol]["prod_price"] = prod_price
                    products[prod_symbol]["prod_amount"] = prod_amount

            return products

          else:
               return -1

    ###############################
    # Bulk product prices change
    ###############################

    def bulkProductPricesChange(self, body={}):

         

         resp = self.__apiRequest("POST", "setProductPrice", body)


         if resp.status_code == 200:
               return resp

         else:
               return resp

    ###############################
    # Bulk product amount change
    ###############################

    def bulkProductAmountChange(self, body={}):

         

         resp = self.__apiRequest("POST", "setProductAmount", body)


         if resp.status_code == 200:
               return resp

         else:
               return resp