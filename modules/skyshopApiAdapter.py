import requests

class skyshopApiAdapter:

    def __init__(self, webApi=""):
 
        self.env_uri = "https://yd859.mysky-shop.pl/api/?APIkey=" + webApi + "&function="
           
            

    ###############################
    # Generic request to SKY-SHOP
    ###############################
          
    def __apiRequest(self, method="GET", uri="", body=""):

          header = {
               'content-type': 'application/json'
               }

          url = self.env_uri + uri

          if method == 'GET':
               response = requests.get(url, headers=header, data=body)
          elif method == 'POST':
               response = requests.post(url, headers=header, data=body)
          elif method == 'PUT':
               response = requests.put(url, headers=header, data=body)
               
          return response


    #########################
    # GET All Products
    #########################

    def getAllProducts(self, offset="0"):
          
          resp = self.__apiRequest("GET", "getProducts&start=" + offset + "&limit=1000")

          products = {}

          if resp.status_code == 200:
            prd = resp.json()

            for r in range(len(prd)-1):

                prod_id = (prd[str(r)]["prod_id"])
                prod_symbol = (prd[str(r)]["prod_symbol"])
                prod_price = (prd[str(r)]["prod_price"])
                prod_amount = (prd[str(r)]["prod_amount"])

                products[prod_symbol] = {}
                products[prod_symbol]["prod_id"] = prod_id
                products[prod_symbol]["prod_price"] = prod_price
                products[prod_symbol]["prod_amount"] = prod_amount

            
            return products

          else:
               return -1


    #########################
    # GET All Hosts by TAG
    #########################

    def getHostsByTag(self, tag):
          
          resp = self.__apiRequest("GET", "/api/v2/entities?entitySelector=type(\"HOST\"),tag(\"" + tag + "\")&pageSize=999&from=now-1y")
          if resp.status_code == 200:
               hosts = resp.json()
               return hosts["entities"]
          else:
               return -1
