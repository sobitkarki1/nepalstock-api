#!/usr/bin/env python3
"""
NEPSE API - Comprehensive Data Download Script

Downloads all available NEPSE market data according to priority levels:
- PRIORITY 1: Static Reference Data (30 minutes)
- PRIORITY 2: Historical Data (4-6 hours)
- PRIORITY 3: Daily Snapshots (ongoing)

Usage:
    python download_all_data.py --priority 1,2,3
    python download_all_data.py --priority 1              # Static data only
    python download_all_data.py --all                      # Everything
"""

import requests
import json
import os
from datetime import datetime, timedelta
import time
from pathlib import Path
import argparse
import sys

BASE_URL = "http://127.0.0.1:5000"
DATA_DIR = Path("nepse_data")
LOG_FILE = DATA_DIR / "download_log.txt"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_message(message, level="INFO", color=RESET):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    print(f"{color}{formatted_msg}{RESET}")
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(formatted_msg + "\n")

def ensure_directories():
    """Create necessary directory structure"""
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "static").mkdir(exist_ok=True)
    (DATA_DIR / "daily").mkdir(exist_ok=True)
    (DATA_DIR / "historical").mkdir(exist_ok=True)
    (DATA_DIR / "historical" / "indices").mkdir(exist_ok=True)
    (DATA_DIR / "historical" / "securities").mkdir(exist_ok=True)

def check_api_status():
    """Check if API is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/index", timeout=5)
        if response.status_code == 200:
            log_message("✓ API is accessible", color=GREEN)
            return True
        else:
            log_message(f"✗ API returned status {response.status_code}", "ERROR", color=RED)
            return False
    except Exception as e:
        log_message(f"✗ Cannot reach API: {e}", "ERROR", color=RED)
        return False

def download_endpoint(endpoint, filename, method="GET", params=None):
    """Download data from an endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=30)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=params or {}, timeout=30)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, indent=2, ensure_ascii=False)
            log_message(f"✓ {endpoint}", color=GREEN)
            return True
        else:
            log_message(f"✗ {endpoint} - Status {response.status_code}", "WARN", color=YELLOW)
            return False
    except requests.exceptions.Timeout:
        log_message(f"✗ {endpoint} - Timeout", "ERROR", color=RED)
        return False
    except Exception as e:
        log_message(f"✗ {endpoint} - {str(e)}", "ERROR", color=RED)
        return False

def priority_1_static_data():
    """
    PRIORITY 1: Static Reference Data (Never Changes)
    Download Once - Takes ~30 minutes
    Size: ~200 KB
    """
    log_message(f"\n{BOLD}{'='*60}", color=BLUE)
    log_message(f"PRIORITY 1: STATIC REFERENCE DATA", color=BLUE)
    log_message(f"{'='*60}{RESET}\n", color=BLUE)
    
    static_dir = DATA_DIR / "static"
    total = 0
    success = 0
    
    # Company & Security Info
    endpoints = {
        "companies.json": ("/company/list", "GET"),
        "classifications.json": ("/security/classification", "GET"),
        "promoters.json": ("/security/promoters", "GET"),
        "non_delisted.json": ("/security?nonDelisted=true", "GET"),
        "indices.json": ("/index", "GET"),
        "sectorwise.json": ("/sectorwise", "GET"),
        "holidays.json": ("/holiday/year", "GET"),
    }
    
    log_message("Company & Security Information:", color=BOLD)
    for filename, (endpoint, method) in endpoints.items():
        total += 1
        if download_endpoint(endpoint, static_dir / filename, method):
            success += 1
        time.sleep(0.5)  # Rate limiting
    
    # Holiday lists for multiple years
    log_message("\nHoliday Lists:", color=BOLD)
    for year in [2022, 2023, 2024, 2025]:
        total += 1
        if download_endpoint(
            f"/holiday/list?year={year}",
            static_dir / f"holidays_{year}.json"
        ):
            success += 1
        time.sleep(0.5)
    
    # Broker Information
    log_message("\nBroker Information:", color=BOLD)
    total += 2
    if download_endpoint(
        "/member?size=500",
        static_dir / "members.json",
        method="POST"
    ):
        success += 1
    time.sleep(0.5)
    
    if download_endpoint(
        "/member/dealer?size=500",
        static_dir / "dealers.json",
        method="POST"
    ):
        success += 1
    time.sleep(0.5)
    
    log_message(f"\n{BOLD}PRIORITY 1 COMPLETE: {success}/{total} endpoints downloaded{RESET}\n", color=GREEN)
    return success, total

def priority_2_historical_data():
    """
    PRIORITY 2: Complete Historical Data
    Downloads index histories and sample security data
    Takes 4-6 hours for complete download
    """
    log_message(f"\n{BOLD}{'='*60}", color=BLUE)
    log_message(f"PRIORITY 2: HISTORICAL DATA", color=BLUE)
    log_message(f"{'='*60}{RESET}\n", color=BLUE)
    
    total = 0
    success = 0
    
    # Get list of companies first
    log_message("Fetching company list...", color=BOLD)
    try:
        response = requests.get(f"{BASE_URL}/company/list")
        companies = response.json()
        company_ids = [str(c.get('id')) for c in companies if 'id' in c]
        log_message(f"Found {len(company_ids)} companies", color=GREEN)
    except Exception as e:
        log_message(f"Error fetching company list: {e}", "ERROR", color=RED)
        company_ids = []
    
    # Download Index Histories (17 indices)
    log_message(f"\nDownloading Index Histories (2020-2024):", color=BOLD)
    index_ids = list(range(51, 68))  # 51-67
    
    for index_id in index_ids:
        total += 1
        endpoint = f"/index/history/{index_id}?startDate=2020-01-01&endDate=2024-12-31"
        filename = DATA_DIR / "historical" / "indices" / f"index_{index_id}_history.json"
        
        if download_endpoint(endpoint, filename):
            success += 1
        time.sleep(1)  # Rate limiting - 1 second between requests
    
    # Download sample security histories (top 20 by index order)
    log_message(f"\nDownloading Sample Security Histories (first 20 companies):", color=BOLD)
    
    for i, security_id in enumerate(company_ids[:20]):
        total += 1
        endpoint = f"/market/history/security/{security_id}?startDate=2020-01-01&endDate=2024-12-31&size=10000"
        filename = DATA_DIR / "historical" / "securities" / f"security_{security_id}_history.json"
        
        if download_endpoint(endpoint, filename):
            success += 1
        time.sleep(1)
        
        if (i + 1) % 5 == 0:
            log_message(f"  Progress: {i + 1}/20 securities", color=YELLOW)
    
    # Market summary history
    log_message(f"\nDownloading Market Summary History:", color=BOLD)
    total += 1
    if download_endpoint(
        "/market-summary-history?startDate=2020-01-01&endDate=2024-12-31",
        DATA_DIR / "historical" / "market_summary_history.json"
    ):
        success += 1
    
    log_message(f"\n{BOLD}PRIORITY 2 COMPLETE: {success}/{total} endpoints downloaded{RESET}\n", color=GREEN)
    return success, total, len(company_ids)

def priority_3_daily_snapshot():
    """
    PRIORITY 3: Daily Market Snapshot
    Downloads current day's market data
    Takes ~10 minutes
    """
    log_message(f"\n{BOLD}{'='*60}", color=BLUE)
    log_message(f"PRIORITY 3: DAILY MARKET SNAPSHOT", color=BLUE)
    log_message(f"{'='*60}{RESET}\n", color=BLUE)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    daily_dir = DATA_DIR / "daily" / date_str
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    total = 0
    success = 0
    
    # Market State
    log_message("Market State:", color=BOLD)
    endpoints = {
        "market_state.json": "/nepse-data/market-open",
        "nepse_index.json": "/nepse-index",
        "market_summary.json": "/market-summary",
    }
    
    for filename, endpoint in endpoints.items():
        total += 1
        if download_endpoint(endpoint, daily_dir / filename):
            success += 1
        time.sleep(0.5)
    
    # All Securities Daily Data (by sector index IDs)
    log_message("\nDaily Trading Stats (by sector):", color=BOLD)
    sector_ids = [58, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67]
    
    for sector_id in sector_ids:
        total += 1
        if download_endpoint(
            f"/securityDailyTradeStat/{sector_id}",
            daily_dir / f"daily_stats_{sector_id}.json"
        ):
            success += 1
        time.sleep(0.5)
    
    # Top Performers
    log_message("\nTop Performers:", color=BOLD)
    top_endpoints = {
        "top_gainers.json": "/top-ten/top-gainer?all=true",
        "top_losers.json": "/top-ten/top-loser?all=true",
        "top_turnover.json": "/top-ten/turnover?all=true",
        "top_volume.json": "/top-ten/trade?all=true",
        "top_transactions.json": "/top-ten/transaction?all=true",
    }
    
    for filename, endpoint in top_endpoints.items():
        total += 1
        if download_endpoint(endpoint, daily_dir / filename):
            success += 1
        time.sleep(0.5)
    
    # Aggregates
    log_message("\nAggregates:", color=BOLD)
    aggregate_endpoints = {
        "sectorwise.json": "/sectorwise",
        "supply_demand.json": "/nepse-data/supplydemand",
        "trading_average.json": "/nepse-data/trading-average?nDays=120",
    }
    
    for filename, endpoint in aggregate_endpoints.items():
        total += 1
        if download_endpoint(endpoint, daily_dir / filename):
            success += 1
        time.sleep(0.5)
    
    # Floor Sheet (Negotiated Trades)
    log_message("\nFloor Sheet:", color=BOLD)
    total += 1
    if download_endpoint(
        "/nepse-data/floorsheet?page=0&size=500&sort=contractId,desc",
        daily_dir / "floorsheet.json",
        method="POST"
    ):
        success += 1
    time.sleep(0.5)
    
    # Today's Prices
    total += 1
    if download_endpoint(
        "/nepse-data/today-price",
        daily_dir / "today_price.json",
        method="POST"
    ):
        success += 1
    
    log_message(f"\n{BOLD}PRIORITY 3 COMPLETE: {success}/{total} endpoints downloaded{RESET}\n", color=GREEN)
    return success, total

def generate_summary():
    """Generate download summary report"""
    log_message(f"\n{BOLD}{'='*60}", color=BLUE)
    log_message(f"DOWNLOAD SUMMARY", color=BLUE)
    log_message(f"{'='*60}{RESET}\n", color=BLUE)
    
    # Calculate disk usage
    total_size = 0
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    size_mb = total_size / (1024 * 1024)
    
    log_message(f"Data Directory: {DATA_DIR}", color=BOLD)
    log_message(f"Total Size: {size_mb:.2f} MB")
    log_message(f"Directories Created:", color=BOLD)
    
    for subdir in ["static", "daily", "historical/indices", "historical/securities"]:
        dir_path = DATA_DIR / subdir
        if dir_path.exists():
            file_count = len(list(dir_path.glob("*.json")))
            log_message(f"  • {subdir}: {file_count} files")
    
    log_message(f"\nLog file: {LOG_FILE}", color=YELLOW)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Download NEPSE API data by priority level"
    )
    parser.add_argument(
        "--priority",
        type=str,
        default="1,2,3",
        help="Comma-separated list of priorities (1,2,3 or 1 or 1,2 etc)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all priorities (same as --priority 1,2,3)"
    )
    parser.add_argument(
        "--static-only",
        action="store_true",
        help="Download only static data (Priority 1)"
    )
    parser.add_argument(
        "--daily-only",
        action="store_true",
        help="Download only daily snapshot (Priority 3)"
    )
    
    args = parser.parse_args()
    
    # Determine priorities to download
    if args.all or args.priority == "all":
        priorities = [1, 2, 3]
    elif args.static_only:
        priorities = [1]
    elif args.daily_only:
        priorities = [3]
    else:
        try:
            priorities = [int(p.strip()) for p in args.priority.split(",")]
        except ValueError:
            print("Invalid priority format. Use comma-separated numbers (e.g., 1,2,3)")
            sys.exit(1)
    
    # Setup and start
    ensure_directories()
    log_message(f"\n{BOLD}NEPSE API - Comprehensive Data Download{RESET}", color=BLUE)
    log_message(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", color=BLUE)
    log_message(f"Downloading Priorities: {priorities}\n", color=BOLD)
    
    # Check API status
    if not check_api_status():
        log_message("Cannot proceed without API. Ensure the server is running.", "ERROR", color=RED)
        sys.exit(1)
    
    total_success = 0
    total_endpoints = 0
    company_count = 0
    
    try:
        # Priority 1: Static Data
        if 1 in priorities:
            s, t = priority_1_static_data()
            total_success += s
            total_endpoints += t
            time.sleep(2)
        
        # Priority 2: Historical Data
        if 2 in priorities:
            s, t, c = priority_2_historical_data()
            total_success += s
            total_endpoints += t
            company_count = c
            time.sleep(2)
        
        # Priority 3: Daily Snapshot
        if 3 in priorities:
            s, t = priority_3_daily_snapshot()
            total_success += s
            total_endpoints += t
    
    except KeyboardInterrupt:
        log_message("\n\nDownload interrupted by user", "WARN", color=YELLOW)
    except Exception as e:
        log_message(f"\nUnexpected error: {e}", "ERROR", color=RED)
    
    # Final summary
    generate_summary()
    
    log_message(f"\n{BOLD}FINAL RESULTS:{RESET}", color=GREEN)
    log_message(f"Total Endpoints: {total_endpoints}", color=GREEN)
    log_message(f"Successful: {total_success}", color=GREEN)
    log_message(f"Failed: {total_endpoints - total_success}", color=RED if (total_endpoints - total_success) > 0 else GREEN)
    log_message(f"Success Rate: {(total_success/total_endpoints*100):.1f}%", color=GREEN)
    log_message(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", color=BLUE)

if __name__ == "__main__":
    main()
