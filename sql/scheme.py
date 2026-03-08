import sqlite3
import json
import pandas as pd
conn = sqlite3.connect("../vn-stock-market/sql/stock_data.db")
cursor = conn.cursor()
create_table_price = """
CREATE TABLE IF NOT EXISTS price_history (
    symbol TEXT NOT NULL,
    date DATE NOT NULL,
    open REAL,
    close REAL,
    price_change_pct REAL,
    volume INTEGER,
    transaction_value INTEGER,
    high REAL,
    low REAL,
    UNIQUE (symbol, date)
);
"""
cursor.execute(create_table_price)
conn.commit()
print("Tạo bảng thành công!")
create_table_bctc = """
CREATE TABLE IF NOT EXISTS quarterly_fundamentals (
    symbol TEXT NOT NULL,      -- "BID"
    quarter TEXT,          -- Lưu lại chuỗi gốc "Quý 3/2025" cho chắc chắn
    -- Kết quả hoạt động kinh doanh (Income Statement)
    net_interest_income REAL,
    operating_expenses REAL,
    profit_before_tax REAL,
    net_profit REAL,
    net_profit_parent REAL,
    -- Cân đối kế toán (Balance Sheet)
    total_assets REAL,
    interbank_assets REAL,
    customer_loans REAL,
    total_liabilities REAL,
    interbank_liabilities REAL,
    customer_deposits REAL,
    equity REAL,
    charter_capital REAL,
    retained_earnings REAL,
    
    -- Các chỉ số định giá & Sinh lời (Ratios)
    eps_ttm REAL,
    bvps REAL,
    pe_ratio REAL,
    roae REAL,
    roaa REAL,
    
    -- Ràng buộc: Một mã cổ phiếu chỉ có 1 báo cáo duy nhất cho 1 quý của 1 năm
    UNIQUE (symbol, quarter)
);
"""
cursor.execute(create_table_bctc)
conn.commit()
print("Tạo bảng thành công!")

#
with open("../vn-stock-market/data/processed/price_history_processed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

    df_price = pd.DataFrame(data)

    # Chuẩn hóa date
    df_price["date"] = pd.to_datetime(df_price["date"], dayfirst=True)
    df_price["date"] = df_price["date"].dt.strftime("%Y-%m-%d")
    df_price = df_price[(df_price['date'] >= '2024-01-01') & (df_price['date'] <= '2025-12-31')]
    df_price = df_price.sort_values(['symbol', 'date'])
    df_price.to_sql('price_history', conn, if_exists='append', index=False)

    print("Thêm dữ liệu thành công!")


with open("../vn-stock-market/data/processed/bctc_2024_processed.json", encoding="utf-8-sig") as f:
    data = json.load(f)
    bctc_2024 = pd.DataFrame(data)
    bctc_2024.to_sql("quarterly_fundamentals", conn, if_exists='append', index=False)
    print("Thêm dữ liệu thành công!")

with open("../vn-stock-market/data/processed/bctc_2025_processed.json", encoding="utf-8-sig") as f:
    data = json.load(f)
    bctc_2025 = pd.DataFrame(data)
    bctc_2025.to_sql("quarterly_fundamentals", conn, if_exists='append', index=False)
    print("Thêm dữ liệu thành công!")

print("Thêm dữ liệu thành công!")
conn.close()