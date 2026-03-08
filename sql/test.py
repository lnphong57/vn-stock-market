import sqlite3
import pandas as pd 
conn = sqlite3.connect("../vn-stock-market/sql/stock_data.db")
cursor = conn.cursor()
query = """
SELECT net_profit_parent FROM quarterly_fundamentals
WHERE symbol == 'VCB'
"""
print(pd.read_sql_query(query, conn))