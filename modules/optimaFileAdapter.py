class optimaFileAdapter:

    def __init__(self, srcFile=""):
 
        self.env_srcFile = srcFile
           
            

    ###############################
    # Get products from file
    ###############################
          
    def getProductsFromFile(self):
        
        products = {}

        with open(self.env_srcFile, 'r') as file:
            for line in file:
                data = line.strip().split('|')

                prod_symbol = data[0]
                prod_price =  data[3].replace(',', '')                                    # bierzemy cenę brutto z pliku
                prod_amount = max(int(data[4]) - int(data[5]), 0)                         # liczymy ilość na stanie - ilość zarezerwowana. Jeżeli wyjdzie < 0 to zapisujemy 0

                if float(prod_price) > 0:                                                 # pobieramy produkt tylko jeżeli cena w Optima > 0
                    products[prod_symbol] = {}
                    products[prod_symbol]["prod_price"] = prod_price
                    products[prod_symbol]["prod_amount"] = prod_amount
            
            #print(products)

        return products