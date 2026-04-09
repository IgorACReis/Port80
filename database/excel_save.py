import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE_WEBSITE = os.path.join(BASE_DIR, "data", "outputs", "Stores_Website.csv")
SOCIAL_WEBSITE = os.path.join(BASE_DIR, "data", "outputs", "Stores_Social.csv")
def save_to_excel(dic:list):
    """Save scraped data to CSV files for debugging and inspection.

    Separates business websites from social media links.

    Args:
        dic (list[dict]): List of business data entries.
    """
    audit_list = []
    social_list = []
    blacklist = ['tripadvisor', 'thefork', 'zomato', 'yelp', 'pai.pt', 'eatbu', 'wix', 'google']

    for row in dic:
        url = row['Url'].lower()
        if any(bad_word in url for bad_word in blacklist):
            continue
        if 'facebook' in url or 'instagram' in url:
            social_list.append(row)
        else:
            audit_list.append(row)
            
    with open(STORE_WEBSITE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, ["Name","Email","Url","Phone","Security","Status","Latency","Industry","Category"])
        writer.writeheader()
        writer.writerows(audit_list)
        
    with open(SOCIAL_WEBSITE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, ["Name","Email","Url","Phone","Security","Status","Latency","Industry","Category"])
        writer.writeheader()
        writer.writerows(social_list)
        
    print(f"Saved {len(audit_list)} Website Leads.")
    print(f"Saved {len(social_list)} Social Media Leads.")