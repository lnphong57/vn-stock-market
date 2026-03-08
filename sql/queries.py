import pandas as pd
import sqlite3
class Query: 
    #class truy van du lieu tu database
    def __init__(self):
        self.conn = sqlite3.connect("../vn-stock-market/sql/stock_data.db")
        self.cursor = self.conn.cursor()
    #Phản ứng thị trường trước các nỗ lực nâng hạng từ Chính phủ trong giai đoạn 01/06/2025 - 07/10/2025
    def q1(self):
        query = """
                SELECT
                    symbol,
                    SUM(price_change_pct)
                FROM price_history
                WHERE date BETWEEN '2025-06-01' AND '2025-10-07'
                GROUP BY symbol
                """
        return pd.read_sql_query(query, self.conn)
    def q2(self):
        query = """
                WITH DailyReturns AS (
                    SELECT 
                        symbol,
                        volume,
                        date,
                        close,
                        price_change_pct,
                        CASE WHEN date <= '2025-10-07' THEN 'Before_News' ELSE 'After_News' END AS Period
                    FROM price_history
                )
                SELECT 
                    symbol,
                    Period,
                    AVG(volume) AS Avg_Volume,
                    AVG(price_change_pct) AS Avg_Daily_Return
                FROM DailyReturns
                WHERE date BETWEEN '2025-06-01' AND '2025-12-31'
                GROUP BY symbol, Period
                """
        return pd.read_sql_query(query, self.conn)
    
    def q3(self):
        query = """
                WITH DailyReturns AS (
                    SELECT 
                        date,
                        symbol,
                        price_change_pct AS DailyReturn
                    FROM price_history
                    WHERE date BETWEEN '2025-06-01' AND '2025-12-31'
                )

                SELECT
                    date,
                    Bank_Momentum, 
                    VNIndex_Momentum, 
                    Bank_Momentum - VNIndex_Momentum AS "Excess Return"
                FROM (
                    SELECT 
                        date,
                        AVG(CASE WHEN symbol != 'VNINDEX' THEN DailyReturn END) AS Bank_Momentum,
                        AVG(CASE WHEN symbol = 'VNINDEX' THEN DailyReturn END) AS VNIndex_Momentum
                    FROM DailyReturns
                    GROUP BY date
                )
                ORDER BY date;
                """
        return pd.read_sql_query(query, self.conn)

    def q4(self):
        query = """
                WITH daily_returns AS (
                    SELECT
                        date,
                        symbol,
                        price_change_pct / 100.0 AS daily_ret
                    FROM price_history
                ),
                equity_curve AS (
                    SELECT
                        date,
                        symbol,
                        daily_ret,
                        EXP(
                            SUM(LN(1 + daily_ret)) OVER (
                                PARTITION BY symbol
                                ORDER BY date
                            )
                        ) AS equity_curve
                    FROM daily_returns
                ),
                peak_calc AS (
                    SELECT
                        date,
                        symbol,
                        daily_ret,
                        equity_curve,
                        MAX(equity_curve) OVER (
                            PARTITION BY symbol
                            ORDER BY date
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                        ) AS peak
                    FROM equity_curve
                ),
                drawdown_calc AS (
                    SELECT
                        date,
                        symbol,
                        daily_ret,
                        (equity_curve - peak) / peak AS drawdown
                    FROM peak_calc
                )
                SELECT
                    symbol,
                    SQRT(AVG(daily_ret * daily_ret) - AVG(daily_ret) * AVG(daily_ret)) * SQRT(250) * 100 AS volatility,
                    MIN(drawdown) * 100 AS max_drawdown
                FROM drawdown_calc
                GROUP BY symbol;
                """
        return pd.read_sql_query(query, self.conn)
    
    def q5(self):
        query = """
                WITH returns AS (
                    SELECT
                        symbol,
                        date,
                        price_change_pct / 100.0 AS ret
                    FROM price_history
                ),

                gain_loss AS (
                    SELECT
                        symbol,
                        date,
                        CASE WHEN ret > 0 THEN ret ELSE 0 END AS gain,
                        CASE WHEN ret < 0 THEN -ret ELSE 0 END AS loss
                    FROM returns
                ),

                rsi_calc AS (
                    SELECT
                        symbol,
                        date,
                        AVG(gain) OVER(
                            PARTITION BY symbol
                            ORDER BY date
                            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
                        ) AS avg_gain,
                        AVG(loss) OVER(
                            PARTITION BY symbol
                            ORDER BY date
                            ROWS BETWEEN 13 PRECEDING AND CURRENT ROW
                        ) AS avg_loss
                    FROM gain_loss
                )

                SELECT
                    symbol,
                    date,
                    100 - (100 / (1 + avg_gain/avg_loss)) AS RSI
                FROM rsi_calc
                WHERE (100 - (100 / (1 + avg_gain/avg_loss))) > 70;
                """
        return pd.read_sql_query(query, self.conn)

def main():
    query = Query()
    while True:
        n = int(input())
        if n in range(1, 6):
            break
    if n == 1:
        print(query.q1())
    elif n == 2:
        print(query.q2())
    elif n == 3:
        print(query.q3())
    elif n == 4:
        print(query.q4())
    else:
        print(query.q5())
if __name__ == "__main__":
    main()

