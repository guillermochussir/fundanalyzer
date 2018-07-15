import requests
import pandas as pd
import json

class Crawler():
    #Extract market data from the API
    def __init__(self):
        self.FundsProducts = "https://fondosonline.com/Operations/Funds/GetFundsProducts"
        self.FundsProductsParams = "?sortColumn=YearPercent&isAscending=false&PageSize=1000&searchFundName=&searchCurrency=-1&searchFocus=-1&searchStrategy=&searchHorizon=-1&searchProfile=-1&isActive=false&searchMinInvestment=&page=1"
        self.PriceData = "https://fondosonline.com/Information/FundData/GetPriceData?ticker={}"
        self.IndustryGroupPieData = "https://fondosonline.com/Information/FundData/GetIndustryGroupPieData?ticker={}"
        self.IndustrySectorPieData = "https://fondosonline.com/Information/FundData/GetIndustrySectorPieData?ticker={}"
        self.CompositionPieData = "https://fondosonline.com/Information/FundData/GetCompositionPieData?ticker={}"
        
    def request(self, url):
        for tries in range(1, 4):
            try:
                print (url)
                r = requests.get(url)
                return r.text
            
            except Exception as e:
                print (e.reason)
                if tries < 3:
                    print ('hubo un error. reintentando en 5 segundos')
                    time.sleep(5)
                else:
                    print ('tercer error.')
    
    def extract(self, url):
        records = json.loads(self.request(url))
        return records
               
    def getFunds(self):
        funds = self.extract(self.FundsProducts + self.FundsProductsParams)
        funds = funds["records"]
        df = pd.DataFrame.from_records(funds)
        print(str(len(df)) + ' fondos scrappeados')
        return df
    
    def getTicker(self,ticker):
        ticker = self.extract(self.PriceData.format(ticker))
        df = pd.DataFrame.from_records(ticker['fundValues'])
        if df is None:
            print ('error. df vacío')
            return 0
        else:
            try:
                df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
                print(str(len(df)) + ' precios scrappeados')
                return df
            except Exception as e:
                return 0
    
    def getPrices(self):
        funds = self.getFunds()
        tickersList = funds['fundBloombergId']
        tickersList = tickersList[tickersList != '0']
        pricesList = [(t,self.getTicker(t)) for t in tickersList]
        return pricesList