# YiDiDa Shipping Label Creator

A Python application to create UPS/FedEx shipping labels using the YiDiDa (易递达) API integration platform.

## Features

- ✓ Login authentication with YiDiDa API
- ✓ Create shipping labels (UPS/FedEx)
- ✓ Customizable configuration for credentials
- ✓ Template-based label requests (easily modifiable)
- ✓ Support for multiple labels in a single request
- ✓ Response logging for tracking

## Project Structure

```
YDD_API_TEST/
├── main.py                  # Main script to run the application
├── yidida_client.py        # YiDiDa API client library
├── config.json             # Configuration file (credentials)
├── label_template.json     # Label request template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure Credentials

Edit `config.json` and add your YiDiDa credentials:

```json
{
  "credentials": {
    "username": "your_username_here",
    "password": "your_password_here"
  },
  "api_base_url": "http://twc.itdida.com/itdida-api"
}
```

### 3. Customize Label Template (Optional)

Edit `label_template.json` to modify the default label request. You can change:
- Recipient information (name, address, phone)
- Shipper information
- Package details (weight, dimensions)
- Declared items
- Service type
- And more...

## Usage

### Basic Usage

Run the main script:

```powershell
python main.py
```

This will:
1. Load your credentials from `config.json`
2. Login to YiDiDa API
3. Load label requests from `label_template.json`
4. Display a summary and ask for confirmation
5. Create the labels
6. Save the API response to `label_response.json`

### Custom Label Creation

You can modify `label_template.json` directly or programmatically create labels:

```python
from yidida_client import YiDiDaClient

# Load config
config = YiDiDaClient.load_config("config.json")
client = YiDiDaClient(
    base_url=config["api_base_url"],
    username=config["credentials"]["username"],
    password=config["credentials"]["password"]
)

# Login
client.login()

# Load and customize template
label_requests = YiDiDaClient.load_label_template("label_template.json")

# Modify the label
label_requests[0]["keHuDanHao"] = "ORDER123456"
label_requests[0]["shouJianRenXingMing"] = "John Doe"
label_requests[0]["shouJianRenDiZhi1"] = "123 Main St"
label_requests[0]["shouJianRenChengShi"] = "Los Angeles"
label_requests[0]["zhouMing"] = "CA"
label_requests[0]["shouJianRenYouBian"] = "90001"

# Create labels
result = client.create_labels(label_requests)
```

## Key Label Fields

Here are some important fields you might want to customize in `label_template.json`:

| Field | Description | Example |
|-------|-------------|---------|
| `keHuDanHao` | Customer order number | "ORDER123456" |
| `shouJianRenXingMing` | Recipient name | "John Doe" |
| `shouJianRenDiZhi1` | Recipient address line 1 | "123 Main Street" |
| `shouJianRenChengShi` | Recipient city | "Los Angeles" |
| `zhouMing` | Recipient state | "CA" |
| `shouJianRenYouBian` | Recipient zip code | "90001" |
| `shouJianRenShouJi` | Recipient phone | "1234567890" |
| `shouHuoQuDao` | Shipping service | "UPS Ground CA CITY IND" |
| `shiZhong` | Package weight (lbs) | 10.0 |
| `shenBaoXinXiList` | Declared items list | See template |

## API Documentation

- **Login API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/loginUsingPOST_7
- **Create Label API**: http://twc.itdida.com/itdida-api/swagger-ui.html#/%E8%BF%90%E5%8D%95API/%E5%8A%9F%E8%83%BD%E6%A8%A1%E5%9D%97/importYundanUsingPOST

## Troubleshooting

### Login Failed
- Verify your credentials in `config.json`
- Check if the API base URL is correct
- Ensure you have internet connectivity

### Label Creation Failed
- Check the API response in `label_response.json`
- Verify all required fields are present in your label request
- Ensure address information is valid
- Check that the shipping service is available for the destination

### Import Error
Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## Notes

- The API response will be saved to `label_response.json` for your reference
- You can create multiple labels in one request by adding more objects to the array in `label_template.json`
- All JSON files support UTF-8 encoding for international characters
- The default template includes a complete example with all fields

## Support

For API-specific questions, refer to the official YiDiDa API documentation linked above.
