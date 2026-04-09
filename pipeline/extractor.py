from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import time
import requests

import urllib3
from urllib3.exceptions import InsecureRequestWarning

from utils.config import URL_CRAWL, headers
from pipeline.site_validator import getstatus

urllib3.disable_warnings(InsecureRequestWarning)

def urlcrawer_engine(region:str,industry:list):
    """Main crawler loop over industries and regions.

    Builds search URLs, paginates through results, extracts leads, and stores them in the database.
    Data is saved after each region to prevent loss on interruption.

    Args:
        region (str): List of region slugs.
        industry (list[str]): Industry-category pairs.
    """
    dic = []
    seen_urls = set()
    url_round = []
    
    u = URL_CRAWL + industry[0] + "/"+ region.lower().replace(" ","-")
    try:
        r = requests.get(u, headers=headers)
        r.raise_for_status()
        page_count = 1
        while True:
            try:
                old_round = url_round
                url_round = []
                print(f"Processing Page {page_count}...")
                soup = BeautifulSoup(r.text, features="lxml")
                if soup is None:
                    break

                #Lamento não encontrámos
                if(soup.find("h2",class_="not-found-title")):
                    print("\n*****NO RESULTS ON SEARCH*****\n")
                    break

                new_leads = gethref(soup,industry)
                for lead in new_leads:
                    url_round.append(lead['Url'])
                    if lead['Url'] not in seen_urls:
                        dic.append(lead)          
                        seen_urls.add(lead['Url'])
                nextpage = soup.find("li", class_= "next")
                if nextpage is None:
                    print("No 'Next' button found. Crawl finished.")
                    break
                
                nextpage_link = nextpage.find("a")
                if nextpage_link is None:
                    break

                url = urljoin(URL_CRAWL,str(nextpage_link["href"]))

                time.sleep(2)
                try:
                    r = requests.get(url,headers=headers)
                    if old_round == url_round:
                        break
                except Exception as e:
                    print(f"Request after {e}...")
                    time.sleep(5)
                    try:
                        r = requests.get(url,headers=headers)
                    except: 
                        break
                page_count += 1
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                break
        return dic
    except Exception as e:
        print(f"Could not load first page in region {region}: {e}")
        return []
def gethref(soup:BeautifulSoup,industry:list):
    """Extract business detail page links and process them.

    Args:
        soup (BeautifulSoup): Parsed HTML of listing page.
        industry (list[str]): Industry-category pair.

    Returns:
        list[dict]: Extracted business data dictionaries.
    """
    dic = []
    store = soup.find_all("a", class_="card-link")
    if store:
            for i in store:
                a = i["href"]
                # Add delay between store detail requests
                time.sleep(2)
                url = store_url(str(a),industry)  
                if url is not None:         
                    dic.append(url)
                
    return dic


def store_url(href:str,industry:list):
    """Scrape a business detail page for contact and website information.

    Args:
        href (str): Relative URL to the business page.
        industry (list[str]): Industry-category pair.

    Returns:
        dict | None:
            - dict: Extracted business data if successful
            - None: If request fails or data is invalid
    """
    url = urljoin(URL_CRAWL,href)
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
    except Exception as e:
                print(f"Request after {e}...")
                time.sleep(5)
                try:
                    r = requests.get(url,headers=headers)
                except:
                    return None

    soup = BeautifulSoup(r.text, features="lxml")
    try:
        btn_phone = soup.find("button", attrs={"data-trackable-event": "call-phone"})
        name_tag = soup.find("h2", class_ = "desktop-title")
        name = name_tag.get_text(strip=True) if name_tag else "Unknown"
        email = "Not Listed"
    
        try:
            lists = soup.find_all("li", class_="listing-item")
            
            for l in lists:
                a_tag = l.find("a")
                if a_tag and a_tag.has_attr("href"):
                    href_str = str(a_tag["href"])
                    if href_str.startswith("mailto:"):
                        email_raw = href_str.split(":")[1]
                        email = email_raw.split("?")[0].strip()
                        break
            
                        
        except Exception as e:
            print(f"Erro a processar e-mail: {e}")

        if btn_phone:
            phone = btn_phone.get("value")
        else:
            phone = "Not Listed"
    except:
        phone = None
    try:
        website = soup.find_all("li", class_ = "listing-item")
        for i in website:
            try:
                a = i.find("a")
                if( a and str(a["href"]).startswith("http")):
                    url_store = a["href"]
                    return getstatus(str(url_store),str(phone),name, email,industry)
            except:
                continue
        if phone:
            return {
                "Name": name,
                "Email":email,
                "Url": "NO WEBSITE", 
                "Phone": str(phone), 
                "Security": "NULL", 
                "Status": "NO WEBSITE", 
                "Latency": "NULL",
                "Industry":industry[0],
                "Category":industry[1].replace("-"," ")
            }
    except Exception as e:
        print(f"Error getting store website! {e}")