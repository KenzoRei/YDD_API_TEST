"""Module 3: Query shipment tracking information"""
from yidida_client import YiDiDaClient
import json
import logging
from datetime import datetime


def query_shipment_module():
    """Module 3: Query shipment tracking information"""
    logger = logging.getLogger(__name__)
    
    print("\n" + "=" * 60)
    print("MODULE 3: Shipment Tracking / Status Inquiry")
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
    
    # Get order numbers from user
    print("\nEnter customer order numbers to track:")
    print("  - Separate multiple orders with commas (e.g., ORDER001,ORDER002,ORDER003)")
    print("  - Maximum 10 order numbers per query")
    print()
    order_numbers = input("Order numbers: ").strip()
    
    if not order_numbers:
        logger.warning("No order numbers provided")
        return False
    
    # Validate order numbers
    is_valid, message = YiDiDaClient.validate_order_numbers(order_numbers)
    if not is_valid:
        logger.error(f"Invalid input: {message}")
        print(f"\n✗ {message}")
        return False
    
    # Query shipment
    logger.info(f"Querying shipment information for: {order_numbers}")
    result = client.query_shipment(order_numbers)
    
    if result:
        print("\n" + "=" * 60)
        print("API Response:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save response to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/shipment_response_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Response saved to {filename}")
        return True
    else:
        logger.error("Failed to query shipment information")
        return False
