# 🛡️ Project URIEL V6

**Universal Recon & Intelligence Extraction Layer**
*Clean reboot — streamlined, modular, and focused on supplier scraping.*

---

## 🚀 Overview

**Uriel V6** is a ground-up rebuild of the URIEL platform, designed to perform real-time price reconnaissance across industrial supplier websites.

This version removes GPT integration entirely to focus on core functionality:

* Direct web scraping
* Structured output (CSV/XLSX)
* Modular plugin architecture
* Supplier-by-supplier control
* Tactical logging and error tracking

---

## 🧩 Current Modules (Planned or In Progress)

* RS Components
* DigiKey
* Tropac
* Quador
* (More to come)

---

## 🛠️ Architecture (Planned Layout)

```
Uriel_V6/
├── scrapers/              # Supplier-specific scraping logic
├── gui/                   # GUI logic (optional)
├── utils/                 # Helpers: logging, filtering, etc.
├── main.py                # Entry point script
├── requirements.txt       # Dependency list
└── README.md              # This file
```

---

## 🧪 Usage

1. Place a list of SKUs into an input file (CSV or Excel)
2. Run `main.py` or use the GUI launcher
3. Select active suppliers
4. Scraped prices are output to a structured report (CSV/XLSX)
5. Logs provide per-SKU results, source, and any failures

---

## ⚙️ Requirements

* Python 3.9+
* Requests / Selenium (depending on scraper)
* Pandas / openpyxl for Excel output

---

## 🚧 Status

✅ Codebase reset
🚧 Scrapers being rebuilt
🧼 No GPT logic present
🔐 Secure & ready for packaging

---

## 🧙‍♂️ Maintainer

**Matthew Baker**
APS Industrial – Rowville HQ
[matthew.baker@apsindustrial.com.au](mailto:matthew.baker@apsindustrial.com.au)
[https://apsindustrial.com.au](https://apsindustrial.com.au)
