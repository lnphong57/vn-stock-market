import crawl
import clean
import const
import json
def save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def pipeline_bctc(years):
    crawler = crawl.Crawler(const.bankId, const.marketIndex, const.url)
    cleaner = clean.Cleaner()

    for year in years:
        raw = crawler.crawl_bctc(year)
        save_json(raw, f"data/raw/bctc_{year}.json")

        processed = cleaner.clean_bctc(raw)
        save_json(processed, f"data/processed/bctc_{year}_processed.json")
    #Crawl and save price history data of banks
def pipeline_price_history():
    crawler = crawl.Crawler(const.bankId, const.marketIndex, const.url)
    cleaner = clean.Cleaner()

    raw = crawler.crawl_price_history()
    save_json(raw, "data/raw/price_history.json")

    processed = cleaner.clean_price_history(raw)
    save_json(processed, "data/processed/price_history_processed.json")
    
if __name__ == "__main__":
    years = list(map(int, input("Enter years (e.g. 2024 2025): ").split()))
    pipeline_bctc(years)
    print("BCTC done")
    pipeline_price_history()
    print("Price history done")