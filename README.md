# NEPSE Proxy - Unofficial API Gateway

A proxy server that bypasses authorization on Nepal Stock Exchange (NEPSE) API endpoints. Uses WASM-based token decoding to generate valid authorization headers.

**Note:** This is an unofficial tool created for educational purposes. Use responsibly.

## How It Works

1. **Token Generation**: Uses WebAssembly (WASM) to decode authentication tokens from NEPSE
2. **Request Proxying**: Intercepts your requests and adds valid authorization headers
3. **Response Forwarding**: Returns the API response directly to you

```
Your Request → Proxy Server → NEPSE API → Proxy Server → Your Response
                ↓
            Adds Authorization (via WASM token)
```

## Setup

### Prerequisites
- Python 3.7+
- Required: `css.wasm` file (included)

### Installation

```bash
# Clone repository
git clone https://github.com/Prabesh01/nepalstock-api.git
cd nepse-proxy-source

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server starts on `http://127.0.0.1:5000`

## Quick Start

### Visit Dashboard
Open in browser: `http://127.0.0.1:5000/info`

### Basic API Calls

```bash
# Market Status
curl http://127.0.0.1:5000/nepse-data/market-open

# All Securities
curl http://127.0.0.1:5000/security?nonDelisted=true

# NEPSE Index (Main Index)
curl -X POST http://127.0.0.1:5000/graph/index/58

# Sensitive Index
curl -X POST http://127.0.0.1:5000/graph/index/57

# Floor Sheet Data
curl -X POST http://127.0.0.1:5000/nepse-data/floorsheet

# Today's Price (POST required)
curl -X POST http://127.0.0.1:5000/nepse-data/today-price
```

## API Endpoints

### GET Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | NEPSE Subindices |
| `/security?nonDelisted=true` | Securities Listing |
| `/nepse-data/market-open` | Market Status |
| `/securityDailyTradeStat/{id}` | Daily Trade Statistics |
| `/news/companies/disclosure` | Corporate Disclosures |

### POST Endpoints (Graph Data)

#### Main Indices (POST required)
| Endpoint | Index |
|----------|-------|
| `/graph/index/58` | NEPSE Index |
| `/graph/index/57` | Sensitive Index |
| `/graph/index/62` | Float Index |
| `/graph/index/63` | Sensitive Float Index |

#### Sub-Indices (POST required)
| Endpoint | Sector |
|----------|--------|
| `/graph/index/51` | Banking |
| `/graph/index/55` | Development Bank |
| `/graph/index/60` | Finance |
| `/graph/index/52` | Hotel & Tourism |
| `/graph/index/54` | Hydropower |
| `/graph/index/67` | Investment |
| `/graph/index/65` | Life Insurance |
| `/graph/index/56` | Manufacturing |
| `/graph/index/64` | Microfinance |
| `/graph/index/66` | Mutual Fund |
| `/graph/index/59` | Non-Life Insurance |
| `/graph/index/61` | Trading |

#### Data Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nepse-data/floorsheet` | POST | Floor sheet trades |
| `/nepse-data/today-price` | POST | Today's prices |

## Example Usage

### Python
```python
import requests

# Market Status
response = requests.get('http://127.0.0.1:5000/nepse-data/market-open')
print(response.json())

# Graph Data (POST)
response = requests.post('http://127.0.0.1:5000/graph/index/58')
print(response.json())
```

### cURL with JSON Response Pretty Print
```bash
# Market Status
curl http://127.0.0.1:5000/nepse-data/market-open | jq

# Get All Securities
curl http://127.0.0.1:5000/security?nonDelisted=true | jq '.[] | {symbol, companyName}' | head -20
```

### Node.js/JavaScript
```javascript
// Market Status
fetch('http://127.0.0.1:5000/nepse-data/market-open')
  .then(res => res.json())
  .then(data => console.log(data));

// Graph Data
fetch('http://127.0.0.1:5000/graph/index/58', { method: 'POST' })
  .then(res => res.json())
  .then(data => console.log(data));
```

## Response Format

All responses are JSON format:

```json
{
  "id": 123,
  "subIndex": "NEPSE",
  "totalTransactions": 45000,
  "totalTradedShares": 1500000,
  "totalTradedValue": 5000000
}
```

## Environment Variables

- `PORT` - Server port (default: 5000)

```bash
# Run on custom port
PORT=8080 python main.py
```

## Important Notes

### Token Generation
- Tokens are generated automatically on first request
- Uses WASM runtime (`css.wasm`) for token parsing
- Tokens are cached and reused for performance
- Tokens refresh automatically when needed

### Request Limits
- No built-in rate limiting
- NEPSE API may have rate limits
- Use responsibly

### Authentication
- All requests are authenticated using decoded WASM tokens
- Authorization: `Salter {token}` header format
- Different payload IDs for different endpoint types

## Troubleshooting

### `css.wasm not found`
- Ensure `css.wasm` is in the same directory as `main.py`

### 500 Error
- Check server console for error messages
- Verify network connection to nepalstock.com.np

### Authorization Failures
- Try restarting the server
- Check if token parsing is working correctly

## Deploy

### Render.com
Click the button below to deploy:

<a href="https://render.com/deploy?repo=https://github.com/Prabesh01/nepalstock-api">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

### Other Platforms
- Railway, Heroku, or any Python-compatible host
- Set `PORT` environment variable
- Ensure `css.wasm` is included in deployment

## References
Instead of using nepalstock.onrender.com, you can deploy it yourself on [render](https://render.com/):

<a href="https://render.com/deploy?repo=https://github.com/Prabesh01/nepalstock-api">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

