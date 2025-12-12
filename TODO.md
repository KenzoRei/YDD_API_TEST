# YDD API Client Extension - TODO

## Project Goal
Extend single-function label creator into a modular multi-function testing tool with:
1. Label creation (existing)
2. Rate inquiry (new)
3. Shipment tracking (new)

## Progress Status

### ✅ COMPLETED

1. **yidida_client.py - Core API Client**
   - ✅ Added logging framework (replacing print statements)
   - ✅ Added `query_price()` method for rate inquiry (POST /itdida-api/price)
   - ✅ Added `query_shipment()` method for shipment tracking (GET /itdida-api/queryYunDanDetail)
   - ✅ Added `load_price_template()` static method for price template loading
   - ✅ Added `validate_order_numbers()` static method with basic validation (max 10 orders, comma-separated)

2. **price_template.json - Rate Query Template**
   - ✅ Created template with required fields (priceZoneType, searchType, wayTypeList, weight)
   - ✅ Added toCustomer contact fields (countryCode, postcode, city, stateCode)
   - ✅ Included variable substitution placeholders ({{defaults.*}})
   - ✅ Added _comment fields explaining parameter meanings

3. **Git Repository Setup**
   - ✅ Repository initialized and pushed to GitHub
   - ✅ URL: https://github.com/KenzoRei/YDD_API_TEST

### 🚧 TODO - NEXT STEPS

1. **Update config.json**
   - [ ] Add logging configuration section (log_level, log_to_file, log_file_path)
   - [ ] Add default values for price queries in defaults section
   - [ ] Add default values for shipment queries (if needed)

2. **Update .gitignore**
   - [ ] Add pattern to exclude `*_response.json` files
   - [ ] Add pattern to exclude `*.log` files

3. **Refactor main.py - Module Functions**
   - [ ] Add logging configuration at startup
   - [ ] Refactor existing code into `create_labels_module()` function
   - [ ] Create `query_price_module()` function (load template, display, confirm, call API)
   - [ ] Create `query_shipment_module()` function (prompt for order numbers, validate, call API)
   - [ ] Create `main_menu()` function with interactive menu loop
   - [ ] Add CLI argument support (--create-labels, --query-price, --query-shipment, --menu)
   - [ ] Update `if __name__ == "__main__"` to handle CLI args or show menu

4. **Response File Handling**
   - [ ] Ensure price_response.json is saved after rate queries
   - [ ] Ensure shipment_response.json is saved after shipment queries
   - [ ] Add timestamps to response files (optional enhancement)

5. **Testing & Validation**
   - [ ] Test rate query module with price_template.json
   - [ ] Test shipment query module with sample order numbers
   - [ ] Test interactive menu navigation
   - [ ] Test CLI argument execution
   - [ ] Verify logging output (console and file)

6. **Documentation**
   - [ ] Update README.md with new features and usage examples
   - [ ] Document CLI argument options
   - [ ] Add examples for each module (label, rate, shipment)

## Technical Notes

### API Endpoints
- **Label Creation**: POST /itdida-api/guaHaoDan/chuangJianGuaHaoDan
- **Rate Query**: POST /itdida-api/price
- **Shipment Tracking**: GET /itdida-api/queryYunDanDetail

### Key Design Decisions
1. **Logging**: Using Python's built-in logging module with configurable levels
2. **Templates**: JSON-based templates with {{variable}} substitution pattern
3. **Validation**: Lightweight validation module (expandable later)
4. **CLI Support**: argparse for command-line execution of individual modules
5. **Session Management**: Shared authentication session across all API calls

### Dependencies
- requests (existing)
- logging (Python stdlib)
- argparse (Python stdlib, for CLI)

## Current Commit
Files ready to commit:
- yidida_client.py (modified - added logging and new API methods)
- price_template.json (new - rate query template)
