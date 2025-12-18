"""Module 2: Query shipping rates/prices"""
from yidida_client import YiDiDaClient
import json
import logging
from datetime import datetime


def query_price_module():
    """Module 2: Query shipping rates/prices"""
    logger = logging.getLogger(__name__)
    
    print("\n" + "=" * 60)
    print("MODULE 2: Rate Inquiry / Price Query")
    print("=" * 60)
    print()
    
    # Load configuration
    logger.info("Loading configuration...")
    config = YiDiDaClient.load_config("config.json")
    
    # Initialize client
    client = YiDiDaClient(
        base_url=config["api_base_url"],
        username=config["credentials"]["username"],
        password=config["credentials"]["password"]
    )
    
    # Login
    logger.info("Attempting to login...")
    if not client.login():
        logger.error("Failed to login. Please check your credentials in config.json")
        return False
    
    logger.info("Login successful")
    
    # Load price template
    logger.info("Loading price query template...")
    price_params = YiDiDaClient.load_price_template("templates/price_template.json", config)
    logger.info("Price query template loaded")
    
    # Display summary
    print("\nPrice Query Parameters:")
    print(f"  - Price Zone Type: {price_params.get('priceZoneType', 'N/A')} (1=Postal, 2=Port, 3=City, 4=Area, 5=Amazon, 6=State)")
    print(f"  - Search Type: {price_params.get('searchType', 'N/A')} (2=Customer pricing, 3=Public pricing)")
    print(f"  - Logistics Types: {price_params.get('wayTypeList', 'N/A')} (0=Express, 1=Small parcel, 2=Dedicated, etc.)")
    print(f"  - Weight: {price_params.get('weight', 'N/A')} kg")
    
    to_customer = price_params.get('toCustomer', {})
    if to_customer:
        print(f"\n  Destination:")
        print(f"    - Country: {to_customer.get('countryCode', 'N/A')}")
        print(f"    - State: {to_customer.get('stateCode', 'N/A')}")
        print(f"    - City: {to_customer.get('city', 'N/A')}")
        print(f"    - Postcode: {to_customer.get('postcode', 'N/A')}")
    
    print()
    confirm = input("Do you want to query rates with these parameters? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        logger.info("Rate query cancelled by user")
        return False
    
    # Query price
    logger.info("Querying rates...")
    result = client.query_price(price_params)
    
    if result:
        print("\n" + "=" * 60)
        print("API Response:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save response to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/price_response_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Response saved to {filename}")
        return True
    else:
        logger.error("Failed to query rates")
        return False
