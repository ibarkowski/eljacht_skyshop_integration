import requests

class skyshopApiAdapter:

    def __init__(self, webApi=""):
 
        self.env_uri = "https://yd859.mysky-shop.pl/api/?function="
           
            

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
    # GET All Hosts
    #########################

    def getHosts(self):
          
          resp = self.__apiRequest("GET", "/api/v2/entities?entitySelector=type(\"HOST\")&pageSize=999&from=now-1y")
          if resp.status_code == 200:
               hosts = resp.json()
               return hosts["entities"]
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
