import crawl
import clean
import const
import json
def save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def pipeline():
    crawl_data = crawl.Crawler(const.bankId, const.marketIndex, const.url)
    
    # Crawl and save bctc data
    year = int(input("Choose a year: "))
    data = crawl_data.crawl_bctc(year)
    save_json(data, f"data/raw/bctc_{year}.json")
    processed_data = clean.Cleaner().clean_bctc(data)
    save_json(processed_data, f"data/processed/bctc_{year}_processed.json")

    #Crawl and save price history data of banks
    data = crawl_data.crawl_price_history()
    save_json(data, "data/raw/price_history.json")
    processed_data = clean.Cleaner().clean_price_history(data)
    save_json(processed_data, "data/processed/price_history_processed.json")

    
if __name__ == "__main__":
    pipeline()
    print("Pipeline executed successfully.")