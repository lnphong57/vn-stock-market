import requests
import const
import re
from playwright.sync_api import sync_playwright
class Crawler:  
    def __init__(self, banks, marketIndex, url):
        self.banks = banks
        self.marketIndex = marketIndex
        self.url = url
        self.allSymbols = banks + marketIndex
    def crawl_bctc(self, target_year):
        all_data = {}
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled", "--start-maximized"])
        # Tạo context với User Agent thật (giả làm Chrome trên Windows 10)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080} # Set màn hình to để tránh giao diện mobile
            )
            for link, symbol in zip(const.url, const.bankId):
                temp = []
                page = context.new_page()
                page.goto(link, timeout=120000)
                page.wait_for_selector("span.fa.fa-chevron-left.pull-left", timeout=60000)
                while True:
                    current_year = page.locator("th.text-center.col-100.al-middle b").first.inner_text()
                    match = re.search(r"\d{4}", current_year)
                    current_year = match.group() if match else None
                    if int(current_year) == target_year:
                        break
                    button = page.locator("span.fa.fa-chevron-left.pull-left")
                    page.wait_for_timeout(15000)
                    button.first.click()
                    page.wait_for_timeout(15000)
                finance = page.locator("div.pos-relative")
                tables = finance.locator("div.table-responsive")
                firstTable = tables.nth(0)
                head = firstTable.locator("thead tr th.text-center.col-100.al-middle b")
                temp.append(head.all_inner_texts())
                for i in range(3):
                    table = tables.nth(i)              
                    rows = table.locator("tbody tr")
                    for x in range(rows.count()):
                        row = rows.nth(x)
                        cells = row.locator("td")
                        row_data = cells.all_inner_texts()
                        temp.append(row_data)   
                all_data[symbol] = temp
            browser.close()
        return all_data
    
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
