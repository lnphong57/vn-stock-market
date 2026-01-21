import requests
import json
class Crawler:  
    stockCode = [
        "acb", "bid", "ctg", "eib","evf", "hdb", "klb", "lpb", "mbb", "msb", "nab", 
        "ocb", "pvf", "shb", "ssb", "stb", "tcb", "tpb", "vab", "vcb", "vib", "vpb"
        ] 
    
    def crawl_info(self):
        url = "https://cafef.vn/du-lieu/Ajax/PageNew/ChiSoTaiChinh.ashx?Symbol=" 
        tempData = []
        for id in self.stockCode:
            fullUrl = url + id
            response = requests.get(fullUrl)
            data = response.json()
            data["symbol"] = id.upper()
            tempData.append(data)
            
        with open("D:/Projects/DS/data/raw/bank_info.json", "w", encoding="utf-8") as file:
            json.dump(tempData, file, ensure_ascii=False, indent=4)

    
    def crawl_price_history(self):
        symbolUrl = "https://cafef.vn/du-lieu/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol="
        pageIndex = "&StartDate=&EndDate=&PageIndex="  
        tempData = []       
        for id in self.stockCode:
            tempUrl = symbolUrl + id +pageIndex
            for index in range(1, 21):
                fullUrl = tempUrl + str(index) 
                response = requests.get(fullUrl)
                data = response.json()
                data["symbol"] = id.upper()
                tempData.append(data)
            
        with open("D:/Projects/DS/data/raw/price_history.json", "w", encoding="utf-8") as file:
            json.dump(tempData, file, ensure_ascii=False, indent=4)

            

test = Crawler()
test.crawl_price_history()
print("suc")

            

        




