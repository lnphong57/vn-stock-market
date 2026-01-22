import json
class Cleaner:
    def clean_bank_info(self, data):
        tempData = []
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
        return tempData


    def clean_price_history(self, data):
        tempData = []
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
        return tempData

