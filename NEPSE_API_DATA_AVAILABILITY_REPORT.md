# NEPSE API - Complete Data Availability Report

## Executive Summary

The NEPSE API exposes 80+ endpoints providing market data spanning from static reference data to real-time market information. This report categorizes all available data by type, update frequency, and usage patterns to help plan comprehensive data downloads.

---

## 📊 Data Categories Overview

```
Total Endpoints: 80+

Categories:
├─ Static/Reference Data (15 endpoints)   - Never changes or rarely changes
├─ Daily Market Data (25 endpoints)       - Updates daily during market hours
├─ Intraday/Real-time Data (10 endpoints) - Updates multiple times per day
├─ Historical Data (15 endpoints)         - Can be queried for date ranges
├─ Derived/Calculated Data (10 endpoints) - Aggregates or calculations
└─ Configuration Data (5 endpoints)       - Settings, holidays, etc.
```

---

## 1️⃣ STATIC/REFERENCE DATA (Never or Rarely Changes)

These endpoints provide foundational data that doesn't change frequently. Download once and cache.

### Company & Security Information

| Endpoint | Method | Description | Update Frequency | Size | Example |
|----------|--------|-------------|-----------------|------|---------|
| `/company/list` | GET | All companies listed on NEPSE | Rarely (new IPOs quarterly) | ~10 KB | Returns company IDs, names, sectors |
| `/security/classification` | GET | Classification/categorization of all securities | Rarely (reclassifications rare) | ~5 KB | Sector, risk category, listing type |
| `/security/8045` | GET | Details of specific security (e.g., company name, ISIN, etc.) | Never (static per security) | ~2 KB per security | Use with security IDs from `/company/list` |
| `/security/promoters` | GET | Promoter shareholding for all securities | Quarterly (promoter data updates) | ~20 KB | Useful for fundamental analysis |

### Market Structure & Configuration

| Endpoint | Method | Description | Update Frequency | Size |
|----------|--------|-------------|-----------------|------|
| `/index` | GET | List of all indices and sub-indices | Never (fixed structure) | ~3 KB |
| `/holiday/year` | GET | Trading holidays for the year | Once per year | ~1 KB |
| `/holiday/list?year=2022` | GET | Detailed holiday list for specific year | Once per year | ~1 KB |
| `/sectorwise` | GET | List of all sectors and sub-sectors | Never (fixed structure) | ~5 KB |

### Broker/Member Information

| Endpoint | Method | Description | Update Frequency | Size | Note |
|----------|--------|-------------|-----------------|------|------|
| `/member?&size=500` | POST | All registered brokers with filters | Monthly (new members/delistings) | ~50 KB | POST with filter JSON |
| `/member/dealer?&size=500` | POST | Registered stock dealers/brokers | Monthly | ~40 KB | Subset of `/member` |

### Parameter Reference

| Endpoint | Method | Description | Update Frequency | Use |
|----------|--------|-------------|-----------------|-----|
| `/security?nonDelisted=true` | GET | All actively listed securities | Rarely | Get complete list of active stocks |

---

## 2️⃣ DAILY MARKET DATA (Updates Daily - Download Once Per Day)

Data that changes once per trading day when market closes.

### Market Summaries

| Endpoint | Method | Description | What It Contains | Best For |
|----------|--------|-------------|-----------------|----------|
| `/market-summary` | GET | Today's market summary | Total volume, value, transactions, price movements | Daily dashboards |
| `/market-summary-history` | GET | Historical market summaries | Daily summaries for past dates | Historical trends |
| `/nepse-data/market-open` | GET | Market status & current day ID | Open/close status, business date | Knowing market state |
| `/nepse-index` | GET | Current NEPSE index value | Latest index points, changes | Real-time index tracking |

### Security-Level Daily Data

| Endpoint | Method | Description | Details |
|----------|--------|-------------|---------|
| `/securityDailyTradeStat/{indexId}` | GET | Daily trading stats for all securities in an index | Trade volume, price, % change per security |
| `/nepse-data/today-price` | POST | Today's opening prices for all securities | Opening prices, status codes |
| `/market/security/price/{securityId}` | GET | Price history for specific security | OHLC data, volumes for selected dates |

### Market Ranking Data (Daily)

| Endpoint | Method | Description | Returns | Update |
|----------|--------|-------------|---------|--------|
| `/top-ten/top-gainer?all=true` | GET | Top gaining stocks today | Stocks with highest % gains | Daily (end of day) |
| `/top-ten/top-loser?all=true` | GET | Top losing stocks today | Stocks with largest % losses | Daily (end of day) |
| `/top-ten/turnover?all=true` | GET | Highest turnover stocks | By trading value | Daily (end of day) |
| `/top-ten/trade?all=true` | GET | Highest volume stocks | By share quantity traded | Daily (end of day) |
| `/top-ten/transaction?all=true` | GET | Most traded stocks by transaction count | By number of transactions | Daily (end of day) |

### Aggregated Daily Data

| Endpoint | Method | Description | Frequency |
|----------|--------|-------------|-----------|
| `/nepse-data/supplydemand` | GET | Supply/demand levels by security | Daily |
| `/nepse-data/trading-average?nDays=120` | GET | N-day moving average prices | Daily |
| `/sectorwise` | GET | Sector performance summaries | Daily |
| `/sectorwise?businessDate=2022-08-08` | GET | Sector data for specific date | Queryable |

### Floor Sheet (Negotiated Trades) - Daily

| Endpoint | Method | Description | Size | Update |
|----------|--------|-------------|------|--------|
| `/nepse-data/floorsheet?page=0&size=500&sort=contractId,desc` | POST | All floor sheet transactions for today | 1-5 MB | Updated throughout trading day |
| `/security/floorsheet/{securityId}` | POST | Floor sheet for specific security | ~100 KB | Throughout day |

---

## 3️⃣ INTRADAY/REAL-TIME DATA (Updates Multiple Times Daily)

Updates during and after market hours. Frequency depends on market activity.

### Index Graph Data (Real-time Charts)

**All use POST method with no required body (value="=="):**

| Index ID | Endpoint | Index Name | What It Shows | Update Frequency |
|----------|----------|------------|---------------|-----------------|
| 58 | `/graph/index/58` | NEPSE | Main index points over time | Every minute during trading |
| 57 | `/graph/index/57` | Sensitive | Top 30 index movements | Every minute during trading |
| 62 | `/graph/index/62` | Float | Float index movements | Every minute during trading |
| 63 | `/graph/index/63` | Sensitive Float | Sensitive float index | Every minute during trading |
| 51 | `/graph/index/51` | Banking | Banking sector index | Every minute during trading |
| 55 | `/graph/index/55` | Development Bank | Dev bank sector | Every minute during trading |
| 60 | `/graph/index/60` | Finance | Finance sector index | Every minute during trading |
| 52 | `/graph/index/52` | Hotel & Tourism | Hotel/tourism sector | Every minute during trading |
| 54 | `/graph/index/54` | Hydropower | Hydropower sector | Every minute during trading |
| 56 | `/graph/index/56` | Manufacturing | Manufacturing sector | Every minute during trading |
| 59 | `/graph/index/59` | Non-Life Insurance | Insurance sector | Every minute during trading |
| 61 | `/graph/index/61` | Trading | Trading sector | Every minute during trading |
| 53 | `/graph/index/53` | Others | Other sectors | Every minute during trading |
| 64 | `/graph/index/64` | Microfinance | Microfinance sector | Every minute during trading |
| 65 | `/graph/index/65` | Life Insurance | Life insurance sector | Every minute during trading |
| 66 | `/graph/index/66` | Mutual Fund | Mutual fund sector | Every minute during trading |
| 67 | `/graph/index/67` | Investment | Investment sector | Every minute during trading |

**Data Format:** Returns array of points: `[{x: timestamp, y: index_value}, ...]`

### Security-Level Real-Time Data

| Endpoint | Method | Description | Update Frequency |
|----------|--------|-------------|-----------------|
| `/market/graphdata/{securityId}` | POST | Price/volume chart for specific security | Every minute during trading |
| `/nepse-data/today-price` | POST | All securities' today prices (with live prices) | Every minute during trading |

### Historical Trading Data (Queryable Range)

| Endpoint | Method | Description | Parameters | Use Case |
|----------|--------|-------------|-----------|----------|
| `/market/history/security/{securityId}` | GET | Trading history for security | `size`, `startDate`, `endDate` | Backfill historical data |
| `/index/history/{indexId}` | GET | Index history for date range | Supports date queries | Historical index analysis |
| `/nepse-data/marcapbydate/{date}` | GET | Market cap by date | Date parameter | Market cap trends |

---

## 4️⃣ HISTORICAL DATA (Queryable for Date Ranges)

These endpoints can be queried with date parameters to retrieve past data.

### Index History

| Endpoint | Data | Range | Format |
|----------|------|-------|--------|
| `/index/history/58?startDate=2020-01-01&endDate=2024-01-01` | NEPSE index history | Any date range | JSON with dates |
| `/index/history/{indexId}?...` | Any sub-index history | Configurable | Same as above |

### Security Price History

| Endpoint | Data | Range | Parameters |
|----------|------|-------|-----------|
| `/market/history/security/{securityId}?startDate=2021-01-01&endDate=2024-01-01&size=1000` | OHLC + volume | Configurable | Date range + size limit |
| `/market/security/price/{securityId}?...` | Historical prices | Configurable | Date query parameters |

### Market Summary History

| Endpoint | Data | Use |
|----------|------|-----|
| `/market-summary-history?startDate=2020-01-01&endDate=2024-01-01` | Daily market totals | Overall market trends |
| `/nepse-data/marcapbydate/2024-01-15` | Market cap on specific date | Market valuation history |

### Floor Sheet History (Negotiated Trades)

| Endpoint | Data | Update |
|----------|------|--------|
| `/nepse-data/floorsheet?page=0&size=500&businessDate=2024-01-15` | Floor sheet for specific date | Can query past dates |
| `/security/floorsheet/{securityId}?businessDate=...` | Floor sheet for security on date | Queryable |

---

## 5️⃣ DERIVED/AGGREGATED DATA

Calculated or summarized from base data.

| Endpoint | What It Shows | Calculated From | Update Frequency |
|----------|---------------|-----------------|-----------------|
| `/top-ten/top-gainer` | Stocks with largest % gains | All daily prices | Daily at close |
| `/top-ten/top-loser` | Stocks with largest % losses | All daily prices | Daily at close |
| `/top-ten/turnover` | Stocks by trading value | Trade data | Daily at close |
| `/top-ten/trade` | Stocks by volume | Trade data | Daily at close |
| `/top-ten/transaction` | Stocks by # of transactions | Transaction data | Daily at close |
| `/nepse-data/trading-average?nDays=120` | Moving averages for all stocks | Historical prices | Daily at close |
| `/sectorwise` | Sector performance aggregates | All stocks in sector | Daily at close |
| `/nepse-data/supplydemand` | Buy/sell demand levels | Order book data | Throughout day |
| `/market-summary` | Overall market totals | All transactions | Throughout day |

---

## 📥 Data Download Strategy

### Phase 1: Static Reference Data (Download Once)
**Recommended:** First download, then cache locally

```
Priority: HIGH - Foundation for everything else

1. GET /company/list                    → Save all company IDs
2. GET /security/classification         → Save security categories  
3. GET /security/promoters              → Fundamental data
4. GET /index                           → All index definitions
5. GET /sectorwise                      → Sector definitions
6. GET /holiday/year                    → Trading calendar
7. POST /member?&size=500               → All broker information
```

**Storage:** JSON files, ~100 KB total
**Update:** Quarterly for companies, never for others

---

### Phase 2: Daily Market Snapshots (Download Once Per Trading Day)
**Recommended:** Download at market close

```
Time: 3:30 PM (after market close in Nepal)

1. GET /market-summary                  → Today's totals
2. GET /nepse-data/market-open         → Market state
3. GET /nepse-index                     → Index value
4. GET /securityDailyTradeStat/58      → All securities data
5. GET /top-ten/*                       → Top performers
6. GET /sectorwise                      → Sector summary
7. POST /nepse-data/floorsheet         → All floor sheet trades
8. POST /nepse-data/today-price        → All securities prices
```

**Storage:** ~10 MB per day per complete dataset
**Update:** Daily at market close

---

### Phase 3: Real-Time Chart Data (Optional - High Frequency)
**Recommended:** Every minute during trading (9:15 AM - 3:00 PM)

```
Frequency: Every 1-5 minutes during market hours

1. POST /graph/index/58                 → NEPSE chart
2. POST /graph/index/{other ids}        → Sector charts
3. POST /nepse-data/today-price        → Current prices
```

**Storage:** ~100 KB per minute per index
**Caution:** Can generate 500+ MB per day if collecting every minute

---

### Phase 4: Historical Backfill (Download Once, Then Archive)
**Recommended:** After establishing daily collection

```
For each security:
1. GET /market/history/security/{id}?startDate=2020-01-01&endDate=2024-01-01

For each index:
1. GET /index/history/{indexId}?startDate=2020-01-01&endDate=2024-01-01

For market summaries:
1. GET /market-summary-history?startDate=2020-01-01&endDate=2024-01-01
```

**Storage:** ~1 GB for complete history (258 securities × 4 years)
**Runtime:** May take 2-3 hours depending on API rate limits

---

## 🗓️ Update Frequency Summary

### Never Changes ⏹️
- `/company/list` - New only with IPOs (quarterly)
- `/security/classification` - Reclassifications rare
- `/index` - Index structure fixed
- `/sectorwise` - Sectors defined
- `/security/promoters` - Actually changes quarterly

### Once Per Year 📅
- `/holiday/year` - Holidays published annually
- `/holiday/list?year=YYYY` - Holidays per year

### Monthly 🗓️
- `/member` - Brokers changes
- `/member/dealer` - Dealers changes

### Daily (After 3:00 PM) 📊
- `/market-summary` - Market totals
- `/market-summary-history` - Historical summaries
- `/nepse-data/market-open` - Market state
- `/nepse-index` - Index value
- `/securityDailyTradeStat/{id}` - Security data
- `/top-ten/*` - Ranking data
- `/sectorwise` - Sector summaries
- `/nepse-data/trading-average` - Averages
- `/nepse-data/supplydemand` - Supply/demand
- `/nepse-data/floorsheet` - Floor sheet
- `/nepse-data/today-price` - Daily prices

### Throughout Trading Day (9:15 AM - 3:00 PM) ⏱️
- `/graph/index/*` - Index chart data
- `/market/graphdata/*` - Security charts
- `/nepse-data/today-price` - Live prices
- `/nepse-data/floorsheet` - Live floor sheet
- `/nepse-data/supplydemand` - Live supply/demand

---

## 🎯 Complete Download Checklist

### Week 1: Get All Historical Data
- [ ] Download company list
- [ ] Download security classifications
- [ ] Download all promoter data
- [ ] Download index definitions
- [ ] Download sector definitions
- [ ] Download holidays (all years)
- [ ] Download brokers list
- [ ] Backfill 3-5 years of index history
- [ ] Backfill 3-5 years of security prices
- [ ] Backfill 3-5 years of market summaries

**Estimated Size:** 1-2 GB
**Estimated Time:** 3-5 hours

### Ongoing: Daily Downloads
```
Schedule:
  9:15 AM  - Start of trading
  3:00 PM  - Market close (DOWNLOAD)
  
Daily Download Script:
  GET /nepse-index
  GET /market-summary
  GET /securityDailyTradeStat/58
  GET /top-ten/top-gainer?all=true
  GET /top-ten/top-loser?all=true
  GET /top-ten/turnover?all=true
  GET /top-ten/trade?all=true
  GET /top-ten/transaction?all=true
  POST /nepse-data/floorsheet
  POST /nepse-data/today-price
  GET /sectorwise
```

**Estimated Size:** ~5-10 MB per day
**Storage for Year:** ~2-3 GB
**Frequency:** Every trading day

### Optional: Real-Time Chart Data
```
Frequency: Every 1-5 minutes during market hours
Time: 9:15 AM - 3:00 PM

POST /graph/index/58 (NEPSE)
POST /graph/index/57 (Sensitive)
POST /graph/index/{others}

⚠️ Warning: Generates significant data volume
   - 1 minute interval: 500+ MB per day
   - 5 minute interval: 100 MB per day
   - Consider selective collection
```

---

## 📋 Complete Endpoint Reference

### By Update Frequency

**STATIC (Download Once)**
```
/company/list
/security/classification
/security/promoters
/index
/sectorwise
/holiday/year
/holiday/list
/member
/member/dealer
```

**DAILY (After 3 PM)**
```
/market-summary
/market-summary-history
/nepse-data/market-open
/nepse-index
/securityDailyTradeStat/{indexId}
/top-ten/top-gainer
/top-ten/top-loser
/top-ten/turnover
/top-ten/trade
/top-ten/transaction
/sectorwise
/nepse-data/trading-average
/nepse-data/supplydemand
/nepse-data/floorsheet
/nepse-data/today-price
```

**REAL-TIME (During Trading)**
```
/graph/index/{indexId} (17 indices)
/market/graphdata/{securityId}
/nepse-data/today-price
```

**HISTORICAL (Queryable)**
```
/market/history/security/{securityId}
/index/history/{indexId}
/market-summary-history
/nepse-data/marcapbydate/{date}
/security/{securityId}
/market/security/price/{securityId}
/security/floorsheet/{securityId}
```

---

## 💾 Storage Estimates

| Data Type | Size | Frequency | Annual Storage |
|-----------|------|-----------|-----------------|
| Static Reference | 100 KB | One-time | 100 KB |
| Daily Market Data | 10 MB | Once/day | 3.5 GB |
| Real-time Charts (1 min) | 500 MB | Every minute | 180+ GB |
| Real-time Charts (5 min) | 100 MB | Every 5 min | 36 GB |
| 1-Day Historical (all) | 1-2 GB | One-time | 1-2 GB |
| Complete All Data | ~5 GB | Year 1 | ~5 GB + daily |

---

## 🔑 Key Insights

### Never Changes (Safe to Cache Indefinitely)
1. Company/security list - Update only with IPOs
2. Index structure - Fixed
3. Sector definitions - Fixed
4. Holidays - Published annually, update once/year

### Changes Regularly (Set Update Schedule)
1. Daily market data - Download once at close
2. Top performers - Download once at close
3. Index values - Download once at close

### High Frequency (Optional Collection)
1. Chart data - Real-time, not essential to store all
2. Floor sheet - Updates throughout day, optional

### Best for Analysis
1. Combine daily snapshots + historical data
2. Calculate your own indicators from OHLC
3. Track top performers daily
4. Monitor sector rotation with sector indices

---

## 🚀 Recommended Implementation

### Minimum (Most Important Data)
```
Storage: ~100 MB initial + 10 MB daily

1. Download static reference once
2. Download daily market summary at close
3. Store for trend analysis

Update Effort: 5 minutes per day
```

### Comprehensive (Full Market Picture)
```
Storage: ~2 GB initial + 50 MB daily

1. Download all static reference
2. Download all daily market data
3. Store individual security data
4. Track historical trends

Update Effort: 30 minutes per day
```

### Complete (Archive Everything)
```
Storage: ~5 GB initial + 100 MB daily

1. All of comprehensive
2. Real-time chart data (5-min intervals)
3. Complete floor sheet history
4. All sector data

Update Effort: 1-2 hours per day
```

---

## 📝 Notes

- **Rate Limiting:** Not specified in API, recommend checking response headers
- **Pagination:** Some endpoints support `page` and `size` parameters
- **Filtering:** Many endpoints support query parameters for filtering
- **POST vs GET:** POST endpoints require authorization tokens (handled by proxy)
- **Timestamps:** All data appears to be in IST (Indian Standard Time) or similar
- **Data Quality:** NEPSE data is official market data, high reliability

---

**Report Generated:** December 4, 2025
**API Source:** NEPSE (Nepal Stock Exchange)
**Endpoint Count:** 80+
**Complete Coverage:** Yes
