# YiDiDa API Testing Tool

A comprehensive Python application for testing YiDiDa (易递达) API endpoints. This multi-function tool supports label creation, rate inquiry, and shipment tracking through an interactive menu or command-line interface.

## Features

- ✓ **Login authentication** with YiDiDa API
- ✓ **Module 1: Create shipping labels** (UPS/FedEx)
- ✓ **Module 2: Query shipping rates** (price inquiry for different services)
- ✓ **Module 3: Track shipments** (query shipment status and details)
- ✓ Interactive menu interface
- ✓ Command-line argument support for automation
- ✓ Structured logging (console + file output)
- ✓ Template-based requests with variable substitution
- ✓ Automatic response persistence (JSON files)

## Project Structure

```
YDD_API_TEST/
├── main.py                    # Main script with menu and CLI support
├── yidida_client.py           # YiDiDa API client library
├── config.json                # Configuration (credentials, logging, defaults)
├── label_template.json        # Template for label creation
├── price_template.json        # Template for rate inquiry
├── requirements.txt           # Python dependencies
├── TODO.md                    # Development progress tracker
└── README.md                  # This file

# Generated files (not tracked in git):
├── label_response.json        # Label creation API responses
├── price_response.json        # Rate query API responses
├── shipment_response.json     # Shipment tracking API responses
└── yidida_api.log            # Application log file
```

## Setup

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure Settings

Edit `config.json` with your credentials and preferences:

```json
{
  "credentials": {
    "username": "your_username_here",
    "password": "your_password_here"
  },
  "api_base_url": "http://twc.itdida.com/itdida-api",
  "logging": {
    "log_level": "INFO",
    "log_to_file": true,
    "log_file_path": "yidida_api.log"
  },
  "defaults": {
    "keHuDanHao": "ORDER_PREFIX",
    "shouHuoQuDao": "FedEx Ground",
    "weight": 1.0,
    "countryCode": "US",
    "stateCode": "CA",
    "city": "Los Angeles",
    "postcode": "90001"
  }
}
```

### 3. Customize Templates (Optional)

- **label_template.json**: Customize recipient, shipper, package details
- **price_template.json**: Customize rate query parameters (destination, weight, service types)

Templates support variable substitution using `{{defaults.fieldName}}` syntax.

## Usage

### Interactive Menu Mode (Default)

Run without arguments to access the interactive menu:

```powershell
python main.py
```

You'll see:
```
============================================================
YiDiDa API Testing Tool
============================================================

Available Modules:
  [1] Create Shipping Labels
  [2] Query Shipping Rates
  [3] Query Shipment Status
  [4] Exit

Select a module (1-4):
```

### Command-Line Mode

Run specific modules directly using CLI arguments:

```powershell
# Create shipping labels
python main.py --create-labels

# Query shipping rates
python main.py --query-price

# Track shipment status
python main.py --query-shipment

# Show interactive menu explicitly
python main.py --menu
```

## Module Details

### Module 1: Create Shipping Labels

Creates UPS/FedEx shipping labels using template parameters.

**Workflow:**
1. Loads label template from `label_template.json`
2. Applies variable substitution from config defaults
3. Displays summary and requests confirmation
4. Calls API endpoint: `POST /itdida-api/guaHaoDan/chuangJianGuaHaoDan`
5. Saves response to `label_response.json`

**Key Fields:**
- `keHuDanHao`: Customer order number
- `shouJianRenXingMing`: Recipient name
- `shouJianRenDiZhi1`: Address line 1
- `shouJianRenChengShi`: City
- `zhouMing`: State code
- `shouJianRenYouBian`: Zip code
- `shouHuoQuDao`: Shipping service

### Module 2: Query Shipping Rates

Queries pricing for different shipping services and destinations.

**Workflow:**
1. Loads price template from `price_template.json`
2. Applies variable substitution from config defaults
3. Displays query parameters and requests confirmation
4. Calls API endpoint: `POST /itdida-api/price`
5. Saves response to `price_response.json`

**Key Parameters:**
- `priceZoneType`: Zone type (1=Postal, 2=Port, 3=City, 4=Area, 5=Amazon, 6=State)
- `searchType`: Pricing type (2=Customer, 3=Public)
- `wayTypeList`: Service types (0=Express, 1=Small parcel, 2=Dedicated line, etc.)
- `weight`: Package weight
- `toCustomer`: Destination details (country, state, city, postcode)

### Module 3: Query Shipment Status

Tracks shipment status and retrieves detailed information.

**Workflow:**
1. Prompts for customer order numbers (comma-separated, max 10)
2. Validates input format and count
3. Calls API endpoint: `GET /itdida-api/queryYunDanDetail`
4. Saves response to `shipment_response.json`

**Input Format:**
```
ORDER001,ORDER002,ORDER003
```

**Response includes:**
- Order status, tracking numbers, dates
- Recipient information
- Package details (weight, dimensions)
- Fee breakdown
- Issue reports (if any)

## Logging

The application uses Python's logging framework with configurable levels:

- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Console Output**: Always enabled with formatted messages
- **File Output**: Configurable via `config.json` (`log_to_file`, `log_file_path`)
- **Format**: `[LEVEL] YYYY-MM-DD HH:MM:SS - Message`

Example log output:
```
[INFO] 2025-12-18 10:30:15 - Loading configuration...
[INFO] 2025-12-18 10:30:15 - Attempting to login...
[INFO] 2025-12-18 10:30:16 - Login successful
[INFO] 2025-12-18 10:30:16 - Creating labels...
[INFO] 2025-12-18 10:30:17 - Response saved to label_response.json
```

## Programmatic Usage

You can also use the client library directly in your own scripts:

```python
from yidida_client import YiDiDaClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load config
config = YiDiDaClient.load_config("config.json")

# Initialize client
client = YiDiDaClient(
    base_url=config["api_base_url"],
    username=config["credentials"]["username"],
    password=config["credentials"]["password"]
)

# Login
if client.login():
    # Example 1: Create labels
    labels = YiDiDaClient.load_label_template("label_template.json", config)
    result = client.create_labels(labels)
    
    # Example 2: Query rates
    price_params = YiDiDaClient.load_price_template("price_template.json", config)
    result = client.query_price(price_params)
    
    # Example 3: Track shipments
    result = client.query_shipment("ORDER001,ORDER002")
```

## API Documentation

Official YiDiDa API documentation:

- **Login API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/loginUsingPOST_7
- **Create Label API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/importYundanUsingPOST
- **Rate Query API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/queryPricesUsingPOST
- **Shipment Tracking API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/queryYunDanDetailUsingGET

## Troubleshooting

### Login Failed
- Verify your credentials in `config.json`
- Check if the API base URL is correct
- Ensure you have internet connectivity

### API Call Failed
- Check the saved response file (`*_response.json`) for error details
- Review the log file (`yidida_api.log`) for detailed information
- Verify all required fields are present in template files
- Ensure data formats are correct (especially for weight, dimensions, dates)

### Invalid Input (Shipment Query)
- Order numbers must be comma-separated
- Maximum 10 order numbers per query
- No spaces around commas (e.g., `ORDER001,ORDER002` not `ORDER001, ORDER002`)

### Import Error
Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## Development

### Repository
GitHub: https://github.com/KenzoRei/YDD_API_TEST

### Contributing
This is a testing tool for API validation. Contributions welcome:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Notes

- All API responses are automatically saved to JSON files for reference and debugging
- Templates support UTF-8 encoding for international characters
- Variable substitution works with nested config paths (e.g., `{{defaults.countryCode}}`)
- Multiple labels can be created in one request (array in `label_template.json`)
- Log files rotate automatically if size exceeds limits (Python logging default behavior)
- Response files (`*_response.json`) are excluded from git to protect sensitive data

## License

This is a testing/development tool. Use at your own discretion.

## Support

For API-specific questions, refer to the official YiDiDa API documentation linked above.
