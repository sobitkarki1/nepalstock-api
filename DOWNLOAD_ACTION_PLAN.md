# NEPSE API Download Action Plan

Quick checklist for actually downloading all available NEPSE data.

## 🎯 Download Strategy by Priority

### PRIORITY 1: Static Reference (Do This First - 30 Minutes)
```
Must-Have Foundation Data - Download ONCE

□ Company & Security Info
  GET /company/list
  GET /security/classification
  GET /security/promoters
  GET /security?nonDelisted=true

□ Market Structure
  GET /index
  GET /sectorwise
  GET /holiday/year
  GET /holiday/list?year=2024
  GET /holiday/list?year=2023
  GET /holiday/list?year=2022

□ Broker Information
  POST /member?&size=500
  POST /member/dealer?&size=500

Result: ~200 KB total, cached forever
Time: ~30 min (includes manual review)
Storage: Local JSON files
```

---

### PRIORITY 2: Complete Historical Data (Do This Once - 4-6 Hours)
```
Full Market History - Download ONCE per project setup

□ Index History (For each index ID: 51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67)
  GET /index/history/{indexId}?startDate=2020-01-01&endDate=2024-12-31
  
  Script: Loop through index IDs
  Expected: 17 requests × 4 years = Large dataset

□ Security Price History (For each security ID from /company/list)
  GET /market/history/security/{securityId}?startDate=2020-01-01&endDate=2024-12-31&size=10000
  
  Script: Loop through all company IDs
  Expected: 250+ requests, 1-2 GB total

□ Market Summary History
  GET /market-summary-history?startDate=2020-01-01&endDate=2024-12-31

Result: 1-2 GB total history
Time: 4-6 hours (API requests)
Storage: Daily CSV files organized by year

Tip: Start with one index/sector first to test
```

---

### PRIORITY 3: Daily Snapshots (Start Immediately - 10 Minutes)
```
Daily Routine - Run EVERY TRADING DAY at 3:00 PM (after market close)

Optimal Time: 3:00-3:30 PM IST (after market closes)

□ Market State
  GET /nepse-data/market-open
  GET /nepse-index
  GET /market-summary

□ All Securities Daily Data
  GET /securityDailyTradeStat/58 (NEPSE main index, covers all)
  
  Alternative: Get by sector
  GET /securityDailyTradeStat/51  (Banking)
  GET /securityDailyTradeStat/54  (Hydropower)
  GET /securityDailyTradeStat/60  (Finance)
  ... (continue for other sectors)

□ Top Performers
  GET /top-ten/top-gainer?all=true
  GET /top-ten/top-loser?all=true
  GET /top-ten/turnover?all=true
  GET /top-ten/trade?all=true
  GET /top-ten/transaction?all=true

□ Aggregates
  GET /sectorwise
  GET /nepse-data/trading-average?nDays=120
  GET /nepse-data/supplydemand

□ Floor Sheet (Negotiated Trades)
  POST /nepse-data/floorsheet?page=0&size=500&sort=contractId,desc
  POST /nepse-data/today-price

Result: ~10 MB per day
Time: ~10 minutes
Storage: Daily folder: data/2024-01-15/
Frequency: Every trading day (250 days/year)
```

---

### PRIORITY 4: Real-Time Charts (Optional - Continuous)
```
⚠️ OPTIONAL - Large data volume. Consider if you have good storage.

During Trading Hours Only: 9:15 AM - 3:00 PM IST

Option A: Every 1 Minute (Detailed - 500+ MB/day)
  Loop every 60 seconds:
    POST /graph/index/58
    POST /graph/index/57
    POST /graph/index/51  (+ 14 more indices)

Option B: Every 5 Minutes (Moderate - 100 MB/day)
  Loop every 300 seconds:
    POST /graph/index/58
    POST /graph/index/57
    POST /graph/index/51  (+ 14 more indices)

Option C: Every 15 Minutes (Minimal - 30 MB/day)
  Loop every 900 seconds:
    POST /graph/index/58
    POST /graph/index/57

My Recommendation: SKIP unless you need tick data
Use daily snapshots instead (much less storage)
```

---

## 📥 Implementation Priority

### Week 1: Foundation Setup
```
Time Investment: ~5 hours total

Day 1 (30 min):
  - Download all static reference data
  - Organize company IDs
  - Set up directory structure

Days 2-3 (4-6 hours):
  - Start historical backfill
  - Download index histories
  - Download 2-3 complete security histories as test
  - Monitor for issues

Days 4-5 (1-2 hours):
  - Continue historical backfill (or set automated)
  - Test daily download script
  - Verify data quality
```

### Week 2 Onward: Daily Routine
```
Daily (3:00-3:15 PM):
  - Run daily snapshot download
  - Verify files created
  - Check for errors

Weekly:
  - Review data for anomalies
  - Backup to external storage
  - Archive old raw files

Monthly:
  - Reorganize data
  - Create monthly reports
  - Update documentation
```

---

## 🐍 Python Implementation Template

### Download Static Data
```python
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
DATA_DIR = "nepse_data"

def download_static_data():
    """Download all static reference data"""
    
    static_endpoints = {
        "companies": "/company/list",
        "classifications": "/security/classification",
        "indices": "/index",
        "sectors": "/sectorwise",
        "promoters": "/security/promoters",
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    for name, endpoint in static_endpoints.items():
        try:
            print(f"Downloading {name}...")
            response = requests.get(f"{BASE_URL}{endpoint}")
            
            filename = f"{DATA_DIR}/{name}.json"
            with open(filename, 'w') as f:
                json.dump(response.json(), f, indent=2)
            
            print(f"  ✓ Saved: {filename}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    download_static_data()
```

### Download Daily Data
```python
def download_daily_data(date_str=None):
    """Download all daily market data"""
    
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    daily_dir = f"{DATA_DIR}/daily/{date_str}"
    os.makedirs(daily_dir, exist_ok=True)
    
    endpoints = {
        "market_summary": "/market-summary",
        "market_open": "/nepse-data/market-open",
        "nepse_index": "/nepse-index",
        "daily_stats_58": "/securityDailyTradeStat/58",
        "top_gainers": "/top-ten/top-gainer?all=true",
        "top_losers": "/top-ten/top-loser?all=true",
        "top_turnover": "/top-ten/turnover?all=true",
        "top_volume": "/top-ten/trade?all=true",
        "top_transactions": "/top-ten/transaction?all=true",
        "sectorwise": "/sectorwise",
    }
    
    for name, endpoint in endpoints.items():
        try:
            print(f"  Downloading {name}...")
            response = requests.get(f"{BASE_URL}{endpoint}")
            
            filename = f"{daily_dir}/{name}.json"
            with open(filename, 'w') as f:
                json.dump(response.json(), f, indent=2)
                
        except Exception as e:
            print(f"  Error downloading {name}: {e}")
    
    # POST endpoints
    post_endpoints = {
        "floorsheet": "/nepse-data/floorsheet?page=0&size=500",
        "today_price": "/nepse-data/today-price",
    }
    
    for name, endpoint in post_endpoints.items():
        try:
            print(f"  Downloading {name}...")
            response = requests.post(f"{BASE_URL}{endpoint}")
            
            filename = f"{daily_dir}/{name}.json"
            with open(filename, 'w') as f:
                json.dump(response.json(), f, indent=2)
                
        except Exception as e:
            print(f"  Error downloading {name}: {e}")

if __name__ == "__main__":
    download_daily_data()
```

---

## 📊 Recommended Download Order

### For Quick Start (Just Data Points)
1. Static reference (companies, sectors)
2. Last 30 days of daily data
3. Last 6 months of market summaries
= ~200 MB, 1-2 hours

### For Analysis (Good Foundation)
1. All static reference
2. All daily data for 2024
3. Historical data for top 50 securities
4. Index histories
= ~1-2 GB, 3-4 hours

### For Complete Archive
1. All of above
2. Complete 5-year history
3. All security prices
4. All index data
= ~5-10 GB, 6-8 hours

---

## ⏱️ Recommended Schedule

### One-Time Setup
```
Week 1, Days 1-3: Download static data + historical
Time: ~5 hours
Storage: ~2 GB
```

### Ongoing Daily
```
Every Trading Day at 3:15 PM:
  - Run daily download script
  - Verify files created
  - Takes ~10 minutes

Time: 10 minutes
Storage: ~10 MB/day = ~2.5 GB/year
```

### Monthly Maintenance
```
Every Month:
  - Archive old raw files
  - Create monthly summary
  - Backup to external drive
  
Time: 30 minutes
```

---

## 🎯 Quick Command Reference

### Download All Static Data
```bash
curl http://127.0.0.1:5000/company/list > companies.json
curl http://127.0.0.1:5000/index > indices.json
curl http://127.0.0.1:5000/sectorwise > sectors.json
curl http://127.0.0.1:5000/security/promoters > promoters.json
curl http://127.0.0.1:5000/holiday/year > holidays.json
```

### Download Today's Market Data
```bash
curl http://127.0.0.1:5000/market-summary > market_summary.json
curl http://127.0.0.1:5000/nepse-index > nepse_index.json
curl http://127.0.0.1:5000/securityDailyTradeStat/58 > daily_stats.json
curl http://127.0.0.1:5000/top-ten/top-gainer?all=true > top_gainers.json
curl http://127.0.0.1:5000/top-ten/top-loser?all=true > top_losers.json
```

### Download Index History (5 Years)
```bash
# For NEPSE (58)
curl "http://127.0.0.1:5000/index/history/58?startDate=2020-01-01&endDate=2024-12-31" > index_58_history.json

# For all indices, loop 51-67
```

---

## 📋 Checklist: What to Download Now vs Later

### RIGHT NOW (Week 1)
- [ ] Static company list
- [ ] Index definitions
- [ ] Sector definitions
- [ ] Historical index data (last 2-3 years)
- [ ] Sample security data (10-20 companies)

### THIS MONTH
- [ ] Complete 5-year history
- [ ] All security data (258 companies)
- [ ] Complete market summaries

### ONGOING (Every Day)
- [ ] Daily market summary
- [ ] Top 10 lists
- [ ] Floor sheet data
- [ ] Individual security updates

### OPTIONAL (Only if Storage Available)
- [ ] 1-minute interval chart data
- [ ] Real-time floor sheet history
- [ ] Complete transaction data

---

## 🚨 Important Notes

1. **Market Hours:** 9:15 AM - 3:00 PM IST (Monday-Thursday, Friday)
2. **Download Time:** 3:00-3:30 PM IST (after close)
3. **Rate Limits:** Not publicly specified - be gentle
4. **API Status:** Check `/info` endpoint for available data
5. **Storage:** Plan for ~10-20 GB for 1-2 years complete data

---

**Last Updated:** December 4, 2025
