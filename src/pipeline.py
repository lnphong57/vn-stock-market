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
    data = crawl_data.crawl_bctc()
    save_json(data, "data/raw/bctc_2025.json")
    processed_data = clean.Cleaner().clean_bank_info(data)
    save_json(processed_data, "data/processed/bank_info_processed.json")

    # Crawl and save price history data of banks
    data = crawl_data.crawl_price_history()
    save_json(data, "data/raw/price_history.json")
    processed_data = clean.Cleaner().clean_price_history(data)
    save_json(processed_data, "data/processed/price_history_processed.json")

    
if __name__ == "__main__":
    pipeline()
    print("Pipeline executed successfully.")