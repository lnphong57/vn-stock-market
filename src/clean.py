
class Cleaner:
    def clean_bctc(self, data):
        tempData = []
        for temp in data:
            raw = temp["Data"]
            indicators = {
                item["Code"]: item["Value"]
                for item in raw
            }
            indicators["symbol"] = temp["symbol"]
            cleanData = {
                "ticker": indicators["symbol"],
                "basicEPS": float(indicators["EPScoBan"]) * 1000,
                "dilutedEPS": float(indicators["EPSphaLoang"]) * 1000,
                "bookValue": float(indicators["GiaTriSoSach"].replace("_","")) * 1000,
                "marketCap": float(indicators["VonHoaThiTruong"].replace("_","")) * 1_000_000_000,
                "outstandingShares": float(indicators["KlcpLuuHanh"].replace("_",""))
                }
            tempData.append(cleanData)
        return tempData


    def clean_price_history(self, data):
        tempData = []
        for item in data:
            raw = item["Data"]
            rawItem = raw["Data"]        
            for day in rawItem:
                indicators = {
                    "ticker": item["symbol"],
                    "date": day["Ngay"],
                    "open": day["GiaMoCua"],
                    "close": day["GiaDongCua"],
                    "change": day["ThayDoi"],
                    "volume": int(f"{day['KhoiLuongKhopLenh']:_}"),
                    "transaction_value": int(f"{day['GiaTriKhopLenh']:_}"),
                    "high": day["GiaCaoNhat"],
                    "low": day["GiaThapNhat"],                
                }            
                tempData.append(indicators)
        return tempData

