# NEPSE API Endpoint Visual Map

Complete visual guide to all available NEPSE API endpoints organized by data type and update frequency.

## 🗺️ Complete Endpoint Map

```
NEPSE API (80+ Endpoints)
│
├── 📋 STATIC REFERENCE DATA (Download Once - Never Changes)
│   │
│   ├── Company Information
│   │   ├── GET /company/list                      → All companies
│   │   ├── GET /security/{id}                     → Specific security details
│   │   ├── GET /security/classification           → Security categories
│   │   └── GET /security/promoters                → Promoter holdings
│   │
│   ├── Market Structure
│   │   ├── GET /index                             → All indices defined
│   │   ├── GET /sectorwise                        → All sectors
│   │   ├── GET /security?nonDelisted=true         → Active securities list
│   │   └── GET /holiday/year                      → Trading calendar
│   │
│   └── Market Participants
│       ├── POST /member?&size=500                 → All brokers
│       └── POST /member/dealer?&size=500          → Dealer brokers
│
├── 📊 DAILY MARKET DATA (Download Once Per Day at 3 PM)
│   │
│   ├── Market Totals
│   │   ├── GET /market-summary                    → Today's totals
│   │   ├── GET /nepse-index                       → Current index value
│   │   ├── GET /nepse-data/market-open            → Market status
│   │   └── GET /market-summary-history            → Historical summaries
│   │
│   ├── Security-Level Data
│   │   ├── GET /securityDailyTradeStat/58         → All securities daily stats
│   │   ├── GET /securityDailyTradeStat/51         → Banking sector data
│   │   ├── GET /securityDailyTradeStat/{id}       → Any sector data
│   │   ├── POST /nepse-data/today-price           → Opening prices for today
│   │   └── GET /market/security/price/{id}        → Individual security prices
│   │
│   ├── Rankings (Updated at Close)
│   │   ├── GET /top-ten/top-gainer?all=true       → Best performers
│   │   ├── GET /top-ten/top-loser?all=true        → Worst performers
│   │   ├── GET /top-ten/turnover?all=true         → By trading value
│   │   ├── GET /top-ten/trade?all=true            → By volume
│   │   └── GET /top-ten/transaction?all=true      → By # transactions
│   │
│   ├── Aggregated Data
│   │   ├── GET /sectorwise                        → Sector performance
│   │   ├── GET /sectorwise?businessDate=DATE      → Sector data by date
│   │   ├── GET /nepse-data/supplydemand           → Supply/demand levels
│   │   ├── GET /nepse-data/trading-average?nDays=120  → Moving averages
│   │   └── GET /nepse-data/marcapbydate/{date}    → Market cap by date
│   │
│   └── Floor Sheet (Negotiated Trades)
│       ├── POST /nepse-data/floorsheet            → All floor sheet today
│       ├── POST /security/floorsheet/{id}         → Floor sheet per security
│       └── GET /nepse-data/floorsheet?businessDate=DATE → Historical floor sheet
│
├── ⚡ REAL-TIME DATA (Every Minute During 9:15 AM - 3 PM)
│   │
│   └── Index Charts (17 Indices Available)
│       ├── POST /graph/index/58  → NEPSE Main Index
│       ├── POST /graph/index/57  → Sensitive (Top 30)
│       ├── POST /graph/index/62  → Float Index
│       ├── POST /graph/index/63  → Sensitive Float
│       ├── POST /graph/index/51  → Banking
│       ├── POST /graph/index/55  → Development Bank
│       ├── POST /graph/index/60  → Finance
│       ├── POST /graph/index/52  → Hotel & Tourism
│       ├── POST /graph/index/54  → Hydropower
│       ├── POST /graph/index/56  → Manufacturing
│       ├── POST /graph/index/59  → Non-Life Insurance
│       ├── POST /graph/index/61  → Trading
│       ├── POST /graph/index/53  → Others
│       ├── POST /graph/index/64  → Microfinance
│       ├── POST /graph/index/65  → Life Insurance
│       ├── POST /graph/index/66  → Mutual Fund
│       └── POST /graph/index/67  → Investment
│
├── 📈 HISTORICAL DATA (Queryable by Date Range)
│   │
│   ├── Time Series
│   │   ├── GET /market/history/security/{id}     → Security OHLC history
│   │   ├── GET /index/history/{id}               → Index history
│   │   └── GET /market-summary-history           → Market totals history
│   │
│   └── Chart Data
│       ├── POST /market/graphdata/{id}           → Security chart data
│       └── GET /market/security/price/{id}       → Historical prices
│
└── 🔧 CONFIGURATION (Rarely Changes)
    │
    └── Holiday Management
        ├── GET /holiday/year                     → Holidays for current year
        ├── GET /holiday/list?year=YYYY           → Holidays for specific year
        └── GET /holiday/list?year=2022, etc      → Any year available
```

---

## 🔄 Data Flow & Relationships

```
                    ┌─────────────────────────┐
                    │   START: Company List   │
                    │  GET /company/list      │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Index List   │  │ Sector List  │  │ Holiday List │
        │ GET /index   │  │GET /sectorway│  │ GET /holiday │
        └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
               │                 │                  │
               └─────────────────┼──────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   STATIC DATA COMPLETE  │
                    │   (Download once)       │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
    ┌──────────────────┐  ┌──────────────┐  ┌────────────────┐
    │ Historical Data  │  │ Broker List  │  │  Classification│
    │ For All Years    │  │ GET /member  │  │  GET /security │
    │ GET /*/history   │  └──────────────┘  └────────────────┘
    └────────────┬─────┘
                 │
    ┌────────────▼────────────┐
    │  DAILY WORKFLOW         │
    │  (Repeat every day)     │
    └────────────┬────────────┘
                 │
    ┌────────────▼─────────────────────┐
    │  Download at Market Close (3 PM)  │
    └────────────┬─────────────────────┘
                 │
    ┌────────────┼────────────────────────────────────────┐
    │            │                                        │
    ▼            ▼                                        ▼
 ┌────────┐  ┌──────────┐                       ┌──────────────┐
 │ Market │  │ Security │                       │    Floor     │
 │Summary │  │   Data   │                       │    Sheet     │
 │GET /*  │  │GET /sec* │                       │POST /nepse*  │
 └────────┘  └──────────┘                       └──────────────┘
    │           │                                       │
    └───────────┼───────────────────────────────────────┘
                │
                ▼
    ┌──────────────────────┐
    │   Top 10 Performers  │
    │ GET /top-ten/*       │
    │ (Updated at close)   │
    └──────────────────────┘
```

---

## 📥 Download Priority Matrix

### Priority 1: MUST HAVE
```
Status: Must Download
Frequency: ONE TIME
Size: ~200 KB
Time: 30 minutes

Endpoints:
  1. GET /company/list
  2. GET /security/classification
  3. GET /index
  4. GET /sectorwise

Purpose: Foundation for everything else
Use: Reference data for analysis
```

### Priority 2: ESSENTIAL DAILY
```
Status: Must Download DAILY
Frequency: Every trading day at 3 PM
Size: ~10-20 MB per day
Time: 10 minutes

Endpoints:
  1. GET /market-summary
  2. GET /nepse-index
  3. GET /securityDailyTradeStat/58
  4. GET /top-ten/* (all 5)
  5. POST /nepse-data/floorsheet

Purpose: Daily market snapshot
Use: Track daily performance, trends
```

### Priority 3: ANALYSIS READY
```
Status: Should Download (Initial Setup)
Frequency: ONE TIME + updates
Size: ~1-2 GB
Time: 4-6 hours

Endpoints:
  1. GET /market/history/security/{all}
  2. GET /index/history/{all}
  3. GET /market-summary-history

Purpose: Historical analysis
Use: Backtesting, trends, correlations
```

### Priority 4: OPTIONAL EXTRAS
```
Status: Nice to Have
Frequency: Every minute (during trading)
Size: 100-500 MB per day
Time: Automated, runs in background

Endpoints:
  1. POST /graph/index/* (all 17)
  2. POST /market/graphdata/*

Purpose: Intraday charts
Use: Real-time monitoring, scalping
Caution: Huge data volume
```

---

## 🎯 Endpoint Groups by Use Case

### For General Market Overview
```
GET /market-summary             → Overall market health
GET /nepse-index                → Market direction
GET /top-ten/top-gainer         → Sector momentum
GET /top-ten/top-loser          → Sector weakness
GET /sectorwise                 → Sector breakdown
```

### For Security Analysis
```
GET /securityDailyTradeStat/58  → All securities daily data
GET /market/history/security/X  → Historical prices
POST /market/graphdata/X        → Chart data
GET /security/X                 → Security details
POST /security/floorsheet/X     → Large trades
```

### For Sector Rotation
```
POST /graph/index/51            → Banking sector performance
POST /graph/index/54            → Hydropower sector performance
POST /graph/index/60            → Finance sector performance
GET /sectorwise                 → Sector comparison
```

### For Trading Analysis
```
POST /nepse-data/floorsheet     → Institutional trading activity
GET /top-ten/turnover           → Liquidity tracking
GET /top-ten/transaction        → Trading activity
GET /nepse-data/supplydemand    → Order flow
```

### For Fundamental Analysis
```
GET /company/list               → Company information
GET /security/promoters         → Ownership structure
GET /security/classification    → Security categorization
GET /nepse-data/marcapbydate    → Market cap trends
```

---

## ⏱️ Timing Guide

### During Trading Hours (9:15 AM - 3:00 PM IST)
```
AVAILABLE BUT UPDATING:
├─ POST /graph/index/* (Every minute)
├─ POST /nepse-data/today-price (Every minute)
├─ GET /nepse-data/supplydemand (Frequently)
├─ POST /nepse-data/floorsheet (Throughout)
└─ GET /market-summary (Frequently)

AVAILABLE BUT STALE:
└─ GET /securityDailyTradeStat/* (Shows yesterday + today partial)

NOT USEFUL YET:
├─ GET /top-ten/* (Updated only at close)
└─ GET /market-summary-history (Updated after close)
```

### After Market Close (3:00 PM IST)
```
FRESH & READY:
├─ GET /market-summary ✓
├─ GET /securityDailyTradeStat/* ✓
├─ GET /top-ten/* ✓
├─ GET /market-summary-history ✓
├─ POST /nepse-data/floorsheet ✓
└─ GET /sectorwise ✓

BEST TIME TO DOWNLOAD:
3:00 - 3:30 PM IST (give API 30 min to update)
```

### Before Trading Hours (Before 9:15 AM)
```
AVAILABLE:
├─ GET /company/list
├─ GET /index
├─ GET /security/*
├─ GET /market/history/* (Historical data only)
└─ GET /holiday/list

NOT AVAILABLE:
├─ POST /graph/index/* (Returns empty or stale)
├─ GET /top-ten/* (Yesterday's data)
└─ GET /market-summary (Yesterday's close)
```

---

## 📊 Data Dependency Graph

```
Applications Depending on NEPSE API Data:

Analysis Tools
├─ Portfolio Trackers
│  ├─ Needs: /company/list, /security/*, /securityDailyTradeStat/*
│  ├─ Frequency: Daily at close
│  └─ Update: Real-time during trading
│
├─ Alert Systems
│  ├─ Needs: /graph/index/*, /top-ten/*, /nepse-data/today-price
│  ├─ Frequency: Every minute during trading
│  └─ Update: Real-time
│
├─ Reporting
│  ├─ Needs: /market-summary-history, /market/history/security/*
│  ├─ Frequency: Weekly/Monthly
│  └─ Update: Historical queries
│
└─ Trading Systems
   ├─ Needs: /nepse-data/floorsheet, /nepse-data/supplydemand, /graph/index/*
   ├─ Frequency: Every minute during trading
   └─ Update: Real-time
```

---

## 🔍 Endpoint Classification Matrix

```
                    │ GET  │ POST │ Real-time │ Historical │ Queryable
────────────────────┼──────┼──────┼───────────┼─────────────┼──────────
Market Summary      │ ✓    │      │    ✓      │      ✓      │    ✓
Index Data          │ ✓    │      │    ✓      │      ✓      │    ✓
Security Data       │ ✓    │      │    ✓      │      ✓      │    ✓
Graph Data          │      │ ✓    │    ✓      │             │    
Company Info        │ ✓    │      │           │             │    
Sector Data         │ ✓    │      │    ✓      │      ✓      │    ✓
Floor Sheet         │      │ ✓    │    ✓      │      ✓      │    ✓
Broker List         │      │ ✓    │           │             │    ✓
Top Performers      │ ✓    │      │           │             │    
Historical Data     │ ✓    │      │           │      ✓      │    ✓
Configuration       │ ✓    │      │           │             │    
```

---

## 💡 Smart Download Combinations

### Combo 1: Daily Market Pulse (5 min, 5 MB)
```
GET /nepse-index
GET /market-summary
GET /top-ten/top-gainer?all=true
GET /top-ten/top-loser?all=true
GET /sectorwise
```
→ Use for: Daily dashboard

### Combo 2: Complete Daily Record (15 min, 20 MB)
```
GET /market-summary
GET /securityDailyTradeStat/58
GET /top-ten/*  (all 5)
POST /nepse-data/floorsheet
GET /sectorwise
```
→ Use for: Archiving

### Combo 3: Sector Analysis (10 min, 2 MB)
```
POST /graph/index/51  (Banking)
POST /graph/index/54  (Hydropower)
POST /graph/index/60  (Finance)
GET /sectorwise
```
→ Use for: Sector rotation

### Combo 4: Security Deep Dive (per security, 1 MB)
```
GET /security/{id}
GET /market/history/security/{id}?startDate=...&endDate=...
POST /market/graphdata/{id}
POST /security/floorsheet/{id}
```
→ Use for: Individual stock analysis

---

**Generated:** December 4, 2025
**Endpoint Count:** 80+
**Use Cases:** 5+
**Data Types:** 6 major categories
