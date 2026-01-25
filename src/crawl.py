import requests
class Crawler:  
    def __init__(self, banks, marketIndex):
        self.banks = banks
        self.marketIndex = marketIndex
        self.allSymbols = banks + marketIndex
    def crawl_info(self):
        url = "https://cafef.vn/du-lieu/Ajax/PageNew/ChiSoTaiChinh.ashx?Symbol=" 
        tempData = []
        for id in self.banks:
            fullUrl = url + id
            response = requests.get(fullUrl)
            data = response.json()
            data["ticker"] = id.upper()
            tempData.append(data)
        return tempData
    
    def crawl_price_history(self):
        symbolUrl = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol="
        pageIndex = "&StartDate=&EndDate=&PageIndex="  
        tempData = []       
        for id in self.allSymbols:
            tempUrl = symbolUrl + id +pageIndex
            for index in range(1, 21):
                fullUrl = tempUrl + str(index) 
                response = requests.get(fullUrl)
                data = response.json()
                data["ticker"] = id.upper()
                tempData.append(data)
        return tempData
            

        




