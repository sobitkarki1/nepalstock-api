#!/usr/bin/env python3
"""
Download historical data for all NEPSE companies - Parallel Version
"""
import requests
import json
import pandas as pd
from pathlib import Path
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

BASE_URL = "http://127.0.0.1:5000"

# Thread-safe counters
lock = Lock()
progress = {'success': 0, 'no_data': 0, 'error': 0, 'total': 0}

def download_company_data(company):
    """Download data for a single company"""
    security_id = company['id']
    symbol = company['symbol']
    company_name = company['companyName']
    sector = company.get('sectorName', 'Unknown')
    
    url = f"{BASE_URL}/market/history/security/{security_id}?startDate=2000-01-01&endDate=2030-12-31&size=100000"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', [])
            
            if content:
                # Convert to DataFrame
                df = pd.DataFrame(content)
                df = df.sort_values('businessDate')
                
                # Add company info
                df['Symbol'] = symbol
                df['CompanyName'] = company_name
                df['Sector'] = sector
                df['SecurityID'] = security_id
                
                # Reorder columns
                df = df[['Symbol', 'CompanyName', 'Sector', 'businessDate', 'highPrice', 
                        'lowPrice', 'closePrice', 'totalTradedQuantity', 
                        'totalTradedValue', 'totalTrades']]
                
                df.columns = ['Symbol', 'CompanyName', 'Sector', 'Date', 'High', 
                             'Low', 'Close', 'Volume', 'Value_NPR', 'Trades']
                
                with lock:
                    progress['success'] += 1
                    progress['total'] += 1
                
                return {'status': 'success', 'symbol': symbol, 'data': df}
            else:
                with lock:
                    progress['no_data'] += 1
                    progress['total'] += 1
                return {'status': 'no_data', 'symbol': symbol}
        else:
            with lock:
                progress['error'] += 1
                progress['total'] += 1
            return {'status': 'error', 'symbol': symbol}
    except Exception as e:
        with lock:
            progress['error'] += 1
            progress['total'] += 1
        return {'status': 'error', 'symbol': symbol, 'error': str(e)}

def main():
    # Load companies
    with open('nepse_data/static/companies.json', 'r') as f:
        companies = json.load(f)
    
    print(f"Found {len(companies)} companies")
    print("Starting comprehensive download for ALL companies...")
    print("="*70)
    
    # Create directory structure
    output_dir = Path('nepse_data/all_companies')
    output_dir.mkdir(exist_ok=True)
    (output_dir / 'individual_csvs').mkdir(exist_ok=True)
    (output_dir / 'by_sector').mkdir(exist_ok=True)
    
    # Check for already downloaded files
    downloaded_symbols = set()
    individual_csv_dir = output_dir / 'individual_csvs'
    if individual_csv_dir.exists():
        for csv_file in individual_csv_dir.glob('*.csv'):
            # Get original symbol (may have been cleaned)
            symbol = csv_file.stem.replace('_', '/')  # Restore potential slashes
            # Check against actual company symbols
            for company in companies:
                safe_symbol = company['symbol'].replace('/', '_').replace('\\', '_').replace(':', '_')
                if csv_file.stem == safe_symbol:
                    downloaded_symbols.add(company['symbol'])
                    break
    
    # Filter out already downloaded companies
    companies_to_download = [c for c in companies if c['symbol'] not in downloaded_symbols]
    
    print(f"Already downloaded: {len(downloaded_symbols)} companies")
    print(f"Remaining to download: {len(companies_to_download)} companies")
    
    if len(companies_to_download) == 0:
        print("\nAll companies already downloaded! Loading existing data...")
        # Load existing data for combining
        all_data = []
        for csv_file in individual_csv_dir.glob('*.csv'):
            try:
                df = pd.read_csv(csv_file)
                # Find company info
                symbol = csv_file.stem
                company = next((c for c in companies if c['symbol'] == symbol), None)
                if company:
                    df['Symbol'] = symbol
                    df['CompanyName'] = company['companyName']
                    df['Sector'] = company.get('sectorName', 'Unknown')
                    all_data.append(df)
            except:
                pass
    else:
        # Track progress
        all_data = []
        
        start_time = datetime.now()
        max_workers = 8  # Number of parallel downloads (reduced from 20)
        print(f"\nDownloading data for {len(companies_to_download)} companies in parallel...")
        print(f"Using {max_workers} concurrent workers")
        print(f"Estimated time: {len(companies_to_download) * 0.4 / max_workers / 60:.1f} minutes (vs {len(companies_to_download) * 0.4 / 60:.1f} minutes sequential)")
        print("-"*70)
        
        # Download in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all download tasks
            future_to_company = {executor.submit(download_company_data, company): company 
                                for company in companies_to_download}
        
            # Process completed downloads
            for future in as_completed(future_to_company):
                result = future.result()
                
                # Progress update every 50 companies
                if progress['total'] % 50 == 0 or progress['total'] == len(companies_to_download):
                    elapsed = (datetime.now() - start_time).total_seconds() / 60
                    remaining = len(companies_to_download) - progress['total']
                    eta = (elapsed / progress['total'] * remaining) if progress['total'] > 0 else 0
                    print(f"Progress: {progress['total']}/{len(companies_to_download)} ({progress['total']/len(companies_to_download)*100:.1f}%) - "
                          f"Time: {elapsed:.1f}m - ETA: {eta:.1f}m - "
                          f"Success: {progress['success']}, No Data: {progress['no_data']}, Errors: {progress['error']}")
                
                # Save successful downloads
                if result['status'] == 'success':
                    df = result['data']
                    symbol = result['symbol']
                    
                    # Clean symbol for filename (remove invalid characters)
                    safe_symbol = symbol.replace('/', '_').replace('\\', '_').replace(':', '_')
                    
                    # Save individual CSV
                    csv_file = output_dir / 'individual_csvs' / f'{safe_symbol}.csv'
                    df[['Date', 'High', 'Low', 'Close', 'Volume', 'Value_NPR', 'Trades']].to_csv(csv_file, index=False)
                    
                    # Add to combined data
                    all_data.append(df)
        
        print(f"\n{'='*70}")
        print(f"Download Complete!")
        print(f"{'='*70}")
        print(f"Successful: {progress['success']}")
        print(f"No Data: {progress['no_data']}")
        print(f"Errors: {progress['error']}")
        print(f"Total Time: {(datetime.now() - start_time).total_seconds() / 60:.1f} minutes")
        print(f"Speed-up: {max_workers}x faster than sequential!")
        
        # Load previously downloaded data to combine with new downloads
        print(f"\nLoading previously downloaded data...")
        for symbol in downloaded_symbols:
            safe_symbol = symbol.replace('/', '_').replace('\\', '_').replace(':', '_')
            csv_file = output_dir / 'individual_csvs' / f'{safe_symbol}.csv'
            try:
                df = pd.read_csv(csv_file)
                company = next((c for c in companies if c['symbol'] == symbol), None)
                if company:
                    df['Symbol'] = symbol
                    df['CompanyName'] = company['companyName']
                    df['Sector'] = company.get('sectorName', 'Unknown')
                    all_data.append(df)
            except:
                pass
    
    if all_data:
        print(f"\nCreating combined datasets...")
        
        # 1. Create master CSV with all companies
        df_master = pd.concat(all_data, ignore_index=True)
        master_file = output_dir / 'ALL_COMPANIES_COMPLETE.csv'
        df_master.to_csv(master_file, index=False)
        print(f"  ✓ Created: {master_file.name} ({len(df_master):,} records)")
        
        # 2. Create sector-wise CSVs
        sectors = df_master['Sector'].unique()
        for sector in sectors:
            sector_df = df_master[df_master['Sector'] == sector]
            safe_sector_name = sector.replace('/', '_').replace(' ', '_')
            sector_file = output_dir / 'by_sector' / f'{safe_sector_name}.csv'
            sector_df.to_csv(sector_file, index=False)
        print(f"  ✓ Created: {len(sectors)} sector-wise CSV files")
        
        # 3. Create summary statistics
        summary = df_master.groupby('Symbol').agg({
            'CompanyName': 'first',
            'Sector': 'first',
            'Date': ['min', 'max', 'count'],
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Value_NPR': 'sum'
        }).reset_index()
        
        summary.columns = ['Symbol', 'CompanyName', 'Sector', 'FirstDate', 'LastDate', 
                          'TradingDays', 'MaxHigh', 'MinLow', 'LatestClose', 
                          'TotalVolume', 'TotalValue']
        
        summary_file = output_dir / 'SUMMARY_STATISTICS.csv'
        summary.to_csv(summary_file, index=False)
        print(f"  ✓ Created: {summary_file.name}")
        
        print(f"\n{'='*70}")
        print("DATASET ORGANIZATION")
        print(f"{'='*70}")
        print(f"\nDirectory: {output_dir}/")
        print(f"  ├── ALL_COMPANIES_COMPLETE.csv ({len(df_master):,} records)")
        print(f"  ├── SUMMARY_STATISTICS.csv ({len(summary)} companies)")
        total_csvs = len(list((output_dir / 'individual_csvs').glob('*.csv')))
        print(f"  ├── individual_csvs/ ({total_csvs} files)")
        print(f"  │   └── [Symbol].csv for each company")
        print(f"  └── by_sector/ ({len(sectors)} files)")
        for i, sector in enumerate(sorted(sectors)[:5]):
            print(f"      {'├──' if i < 4 else '└──'} {sector.replace('/', '_').replace(' ', '_')}.csv")
        if len(sectors) > 5:
            print(f"      └── ... ({len(sectors) - 5} more)")
        
        print(f"\n{'='*70}")
        print("TOP 10 COMPANIES BY TOTAL TRADING VALUE")
        print(f"{'='*70}")
        top10 = summary.nlargest(10, 'TotalValue')[['Symbol', 'CompanyName', 'TotalValue', 'TradingDays']]
        top10['TotalValue_B'] = (top10['TotalValue'] / 1e9).round(2)
        print(top10[['Symbol', 'CompanyName', 'TotalValue_B', 'TradingDays']].to_string(index=False))
    
    print(f"\n✓ All data downloaded and organized successfully!")
    print(f"\nFiles saved in: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
