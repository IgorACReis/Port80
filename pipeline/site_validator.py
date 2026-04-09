import requests
from utils.config import headers

def getstatus(url:str, phone:str, name:str, email:str,industry:list):
    """Check website availability and basic metrics.

    Performs an HTTP request and builds a base data dictionary, then passes it
    to `test_request` for further validation.

    Args:
        url (str): Website URL.
        phone (str): Company phone number.
        name (str): Company name.
        email (str): Company email.
        industry (list[str]): Industry-category pair.

    Returns:
        dict | None: Website status and metadata or None if website is healthy.
    """
    try:
        r = requests.get(url, headers=headers, timeout=5, verify=False)
        dic = {
            "Name":name,
            "Email":email,
            "Url":r.url,
            "Phone":phone,
            "Status":r.status_code,
            "Latency":round(r.elapsed.total_seconds(), 2),
            "Industry":industry,
            "Category":industry[1].replace("-"," ")
        }
        return test_request(dic)
    except requests.exceptions.Timeout:
        return {"Name": name,"Email":email,"Url": url, "Phone": phone, "Security": "False", "Status": "TIMEOUT", "Latency": ">5s","Industry":str(industry[0].replace("-"," ")),"Category":str(industry[1]).replace("-"," ")}
        
    except requests.exceptions.SSLError:
        return {"Name": name,"Email":email,"Url": url, "Phone": phone, "Security": "False", "Status": "SSL_ERROR", "Latency": "999","Industry":str(industry[0].replace("-"," ")),"Category":str(industry[1]).replace("-"," ")}
        
    except requests.exceptions.ConnectionError:
        return {"Name": name,"Email":email,"Url": url, "Phone": phone, "Security": "False", "Status": "CONNECTION_REFUSED", "Latency": "999","Industry":str(industry[0].replace("-"," ")),"Category":str(industry[1]).replace("-"," ")}
        
    except Exception as e:
        if "facebook" in url or "instagram" in url:
            return{"Name": name,"Email":email,"Url": url, "Phone": phone, "Security": "Social Page", "Status": "Social Page", "Latency": "Social Page","Industry":str(industry[0].replace("-"," ")),"Category":str(industry[1]).replace("-"," ")}
        return {"Name": name,"Email":email,"Url": url, "Phone": phone, "Security": "False", "Status": f"ERROR_{str(e)[:20]}", "Latency": "999","Industry":str(industry[0].replace("-"," ")),"Category":str(industry[1]).replace("-"," ")}

def test_request(request:dict):
    """Evaluate website health based on security, status, and latency. 
    Healthy sites return None.
    """
    if not request:
        return None
        
    url = request["Url"]
    status_code = request["Status"]
    latency = request["Latency"]
    
    sec = True if url.startswith("https") else False
    con = True if status_code == 200 else False
        
    if (sec and con and latency < 3) and not ("facebook" in url or "instagram" in url):
        return None
        
    request["Security"] = str(sec)
    request["Status"] = str(status_code)
    request["Latency"] = str(latency)
    
    return request