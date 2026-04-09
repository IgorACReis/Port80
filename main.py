import time
import unicodedata
from datetime import timedelta

from utils.config import REG_FILE,IND_FILE,URL_CRAWL, headers
from database.db_manager import save_to_db
from pipeline.extractor import urlcrawer_engine
from database.excel_save import save_to_excel

START_TIME = time.time()


def load_regions():
    """Reads regions from file into a list.

    Returns:
        list[str] | None: List of regions in normalized format, or None if file reading fails.
    """
    region_list = []
    try:
        with open(REG_FILE,"r") as file:
            for l in file:
                if l:
                    txt = unicodedata.normalize('NFKD', l).encode('ASCII', 'ignore').decode('utf-8')
                    region_list.append(txt.lower().replace(" ", "-").strip())
        return region_list
    except Exception as e:
        print(f"Error with region file: {e}")

def load_industries():
    """Load industries and categories from file.

    Returns:
        list[list[str]] | None: Each entry contains [industry, category] in normalized format, or None if file reading fails.
    """
    industries_list = []
    try:
        with open(IND_FILE,"r") as file:
            for l in file:
                if l:
                    txt = unicodedata.normalize('NFKD', l).encode('ASCII', 'ignore').decode('utf-8')
                    industries_list.append(txt.lower().replace(" ", "-").strip().split(","))
        return industries_list
    except Exception as e:
        print(f"Error with industries file: {e}")

def start():
    print("STARTING PORT80...")
    reg_list = load_regions()
    ind_list = load_industries()
    t = time.localtime()

    if not reg_list or not ind_list:
        print("Error: Regions or Industries list is empty.")
        return
    
    for industry in ind_list:
        for region in reg_list:
            print(f"""
                {'='*60}
                ------------------------------------------------------------
                REGION:    {region.upper():<25}
                INDUSTRY:  {industry[0].upper():<25}
                START TIME: {str(time.strftime("%d/%m/%Y %H:%M:%S",t))} UPTIME: {str(timedelta(seconds=int(time.time() - START_TIME))):<25}
                ============================================================
                """)
            dic = urlcrawer_engine(region, industry)
            worth = [lead for lead in dic if lead is not None]
            if worth:
                save_to_excel(worth)
                print(f"Sucess: {len(worth)} leads saved.")
            else:
                print("No lead found in this region.")

    print(f"Shutting Port80 total time: {str(timedelta(seconds=int(time.time() - START_TIME))):<25}")
def main():
    """Entry point. Loads config and starts the crawler."""
    start()

if __name__ == "__main__":
        main()
