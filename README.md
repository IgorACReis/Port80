# Port80: Automated ETL & Web Health Audit Pipeline

An end-to-end Python ETL (Extract, Transform, Load) pipeline designed to extract business data from online directories, autonomously audit the technical health of their websites, and securely load the processed data into a relational database.

## 🚀 What it does (The ETL Process)

* **Extract:** Navigates through regional pages of online business directories, scraping Business Names, Phone Numbers, and Emails (dynamically extracted via hidden `mailto:` tags).
* **Transform:** Visits each extracted website URL and performs a rigorous technical health check. It filters out blacklisted domains and applies custom logic to categorize social media pages.
* **Load:** Securely injects the audited data into a **PostgreSQL** database. It utilizes `UPSERT` (`ON CONFLICT`) logic to ensure data integrity, update existing records with the latest latency/status, and prevent duplicates during recurring runs.

## ⚡ Connection & Health Tests

* **HTTP Status Codes:** Detection of active pages, redirects, or client/server errors (e.g., 200, 404, 403).
* **Server Diagnostics:** Expired domains or server-down detection (`CONNECTION_REFUSED`).
* **Performance:** Real-time response latency monitoring and timeout handling (> 5 seconds).
* **Security:** SSL Certificate verification (HTTP vs HTTPS detection).

## 🏗️ Architecture & Storage

Transitioning from static CSV exports, this project now leverages a modern data architecture:
* **PostgreSQL Database:** Data is stored in a structured, queryable `business` table.
* **Dockerized Environment:** The database runs in an isolated Docker container, ensuring a scalable and consistent environment between development and production.
* **Secure Credentials:** Infrastructure connections are strictly managed via `.env` files, keeping sensitive credentials out of the source code.

## 🛠️ Technologies Stack

* **Core:** Python 3
* **Infrastructure:** PostgreSQL, Docker
* **Data Engineering / Libraries:**
    * `psycopg2` (PostgreSQL adapter for Python)
    * `python-dotenv` (Environment variable management)
    * `requests` (HTTP calls and robust network exception handling)
    * `beautifulsoup4` / `lxml` (HTML Parsing & DOM navigation)