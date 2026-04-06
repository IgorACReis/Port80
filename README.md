# Port80: Automated ETL & Web Health Audit Pipeline
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end Python **ETL (Extract, Transform, Load)** pipeline designed to extract business data from online directories, autonomously audit the technical health of their websites, and securely load the processed data into a relational database.

## 🚀 What it does (The ETL Process)

* **Extract:** Navigates through 300+ regional pages of business directories, scraping Business Names, Phone Numbers, and Emails (dynamically extracted via hidden `mailto:` tags).
* **Transform:** Visits each extracted website URL and performs a rigorous technical health check. It filters out blacklisted domains and applies custom logic to categorize social media pages.
* **Load:** Securely injects the audited data into a **PostgreSQL** database. It utilizes `UPSERT` (`ON CONFLICT`) logic and **Region-by-Region Checkpointing** to ensure data integrity and prevent loss during long-running executions.

## ⚡ Connection & Health Tests

* **HTTP Status Codes:** Detection of active pages, redirects, or client/server errors (e.g., 200, 404, 403).
* **Server Diagnostics:** Expired domains or server-down detection (`CONNECTION_REFUSED`).
* **Performance:** Real-time response latency monitoring and timeout handling (> 5 seconds).
* **Security:** SSL Certificate verification (HTTP vs HTTPS detection).

## 🏗️ Architecture & Storage

Transitioning from static CSV exports, this project leverages a modern data architecture:
* **PostgreSQL Database:** Data is stored in a structured, queryable `business` table.
* **Dockerized Environment:** The database runs in an isolated **Docker** container, ensuring a scalable and consistent environment between development and production (Ubuntu Server).
* **Secure Credentials:** Infrastructure connections are strictly managed via `.env` files, keeping sensitive credentials out of the source code.

## 🛠️ Technologies Stack

* **Core:** Python 3.10+
* **Infrastructure:** PostgreSQL, Docker
* **Data Engineering / Libraries:**
    * `psycopg2` (PostgreSQL adapter for Python)
    * `python-dotenv` (Environment variable management)
    * `requests` (HTTP calls and robust network exception handling)
    * `beautifulsoup4` / `lxml` (HTML Parsing & DOM navigation)
    * `unicodedata` / `datetime` (Data normalization and execution logging)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### 1. Clone the repository
```bash
git clone https://github.com/IgorACReis/Port80.git
cd port80
```

### 2. Configure environment variables
Create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_db
```

### 3. Start the database
```bash
docker-compose up -d
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the crawler
```bash
python main.py
```

> ⚠️ Crawl duration depends on the number of regions and industries configured in `regions.txt` and `industries.txt`.

