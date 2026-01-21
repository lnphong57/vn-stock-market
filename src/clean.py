import json
def clean_bank_info():
    tempData = []
    with open("D:/Projects/DS/data/raw/bank_info.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        for temp in data:
            raw = temp["Data"]
            indicators = {
                item["Code"]: item["Value"]
                for item in raw
            }
            indicators["symbol"] = temp["symbol"]
            cleanData = {
                "ID": indicators["symbol"],
                "EPS cơ bản (nghìn đồng)": float(indicators["EPScoBan"]),
                "EPS pha loãng (nghìn đồng)": float(indicators["EPSphaLoang"]),
                "Giá trị sổ sách (nghìn đồng)": float(indicators["GiaTriSoSach"].replace(",","")),
                "Vốn hóa thị trường (tỷ đồng)": float(indicators["VonHoaThiTruong"].replace(",","")),
                "Khối lượng cổ phiếu lưu hành": float(indicators["KlcpLuuHanh"].replace(",",""))
                }
            tempData.append(cleanData)
    with open("D:/Projects/DS/data/processed/bank_info_processed.json", "w", encoding="utf-8") as file:
        json.dump(clean_bank_info(), file, ensure_ascii=False, indent=4)


def clean_price_history():
    tempData = []
    with open("D:/Projects/DS/data/raw/price_history.json", "r", encoding="utf-8") as file:
        data = json.load(file)    
        for item in data:
            raw = item["Data"]
            rawItem = raw["Data"]        
            for day in rawItem:
                indicators = {
                    "symbol": item["symbol"],
                    "Ngày": day["Ngay"],
                    "Mở cửa": day["GiaMoCua"],
                    "Đóng cửa": day["GiaDongCua"],
                    "Thay đổi": day["ThayDoi"],
                    "Khối lượng": day["KhoiLuongKhopLenh"],
                    "Giá trị giao dịch": day["GiaTriKhopLenh"],
                    "Cao nhất": day["GiaCaoNhat"],
                    "Thấp nhất": day["GiaThapNhat"],                
                }            
                tempData.append(indicators)
    with open("D:/Projects/DS/data/processed/price_history_processed.json", "w", encoding="utf-8") as file:
        json.dump(tempData, file, ensure_ascii=False, indent=4)



clean_price_history()
    
