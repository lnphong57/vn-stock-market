import json
vi_to_en_map = {
    "Thu nhập lãi thuần": "net_interest_income",
    "Chi phí hoạt động": "operating_expenses",
    "Tổng TNTT": "profit_before_tax",
    "Tổng LNST": "net_profit",
    "LNST của CĐ Ngân hàng mẹ": "net_profit_(parent)",
    "Tổng tài sản": "total_assets",
    "- Tiền, vàng gửi và cho vay các TCTD": "interbank_assets",
    "- Cho vay khách hàng": "customer_loans",
    "Nợ phải trả": "total_liabilities",
    "- Tiền gửi và vay các TCTD": "interbank_liabilities",
    "- Tiền gửi của khách hàng": "customer_deposits",
    "Vốn và các quỹ": "equity",
    "- Vốn của TCTD": "charter_capital",
    "- Lợi nhuận chưa phân phối": "retained_earnings",
    "EPS 4 quý": "eps_ttm",
    "BVPS cơ bản": "bvps",
    "P/E cơ bản": "pe_ratio",
    "ROEA": "roae",
    "ROAA": "roaa"
}
class Cleaner:
    def to_number(self, x):
        if x is None:
            return None

        if isinstance(x, str):
            x = x.strip()
            if x == "":
                return None
            return float(x.replace(",", ""))

        return x
    def clean_bctc(self, data):
        
        rows = []
        for symbol, table in data.items():
            quarters = table[0]       # ['Quý 1/2025', ...]
            metrics = table[1:]       # các chỉ tiêu
            for i, q in enumerate(quarters):
                row = {
                    "symbol": symbol,
                    "quarter": q
                }
                for m in metrics:
                    key = m[0]
                    eng = vi_to_en_map.get(key)
                    row[eng] = self.to_number(m[i + 1])
                rows.append(row)
        return rows

    def clean_price_history(self, data):
        tempData = []
        for item in data:
            raw = item["Data"]
            rawItem = raw["Data"]        
            for day in rawItem:
                indicators = {
                    "symbol": item["symbol"],
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


