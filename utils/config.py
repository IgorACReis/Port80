# utils/config.py

# ==========================================
# CRAWLER CONFIGURATIONS
# ==========================================
URL_BASE = "https://www.diretorio-exemplo.com/searches"
URL_CRAWL = "https://www.diretorio-exemplo.com/"

# ==========================================
# FILE PATHS
# ==========================================
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG_FILE = os.path.join(BASE_DIR, "data", "inputs", "regions.txt")
IND_FILE = os.path.join(BASE_DIR, "data", "inputs", "industries.txt")

# ==========================================
# REQUEST HEADERS
# ==========================================

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3','Accept-Language':'en-US'}
