"""
YiDiDa API Testing Tool - Multi-function client for label creation, rate inquiry, and shipment tracking
"""
from yidida_client import YiDiDaClient
import json
import argparse
import logging
import sys


def setup_logging(config):
    """Configure logging based on config.json settings"""
    log_config = config.get("logging", {})
    log_level = log_config.get("log_level", "INFO")
    log_to_file = log_config.get("log_to_file", False)
    log_file_path = log_config.get("log_file_path", "yidida_api.log")
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='[%(levelname)s] %(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file_path, encoding='utf-8') if log_to_file else logging.NullHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    if log_to_file:
        logger.info(f"Logging to file: {log_file_path}")
    return logger


def create_labels_module():
    """Module 1: Create shipping labels from template"""
    logger = logging.getLogger(__name__)
    
    print("\n" + "=" * 60)
    print("MODULE 1: Shipping Label Creator")
    print("=" * 60)
    print()
    
    # Load configuration
    print("Loading configuration...")
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
    
    # Load label template
    logger.info("Loading label template...")
    label_requests = YiDiDaClient.load_label_template("label_template.json", config)
    logger.info(f"Loaded {len(label_requests)} label request(s)")
    
    # Display summary
    print("\nLabel Request Summary:")
    for i, label in enumerate(label_requests, 1):
        print(f"  Label {i}:")
        print(f"    - Customer: {config['credentials']['username']}")
        print(f"    - Customer Order #: {label.get('keHuDanHao', 'N/A')}")
        print(f"    - Recipient: {label.get('shouJianRenXingMing', 'N/A')}")
        print(f"    - Address: {label.get('shouJianRenDiZhi1', 'N/A')}")
        print(f"    - City: {label.get('shouJianRenChengShi', 'N/A')}")
        print(f"    - State: {label.get('zhouMing', 'N/A')}")
        print(f"    - Zip: {label.get('shouJianRenYouBian', 'N/A')}")
        print(f"    - Service: {label.get('shouHuoQuDao', 'N/A')}")
    
    print()
    confirm = input("Do you want to create these labels? (yes/no): ").strip().lower()
    
    if confirm not in ['yes', 'y']:
        logger.info("Label creation cancelled by user")
        return False
    
    # Create labels
    logger.info("Creating labels...")
    result = client.create_labels(label_requests)
    
    if result:
        print("\n" + "=" * 60)
        print("API Response:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save response to file
        with open("label_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info("Response saved to label_response.json")
        return True
    else:
        logger.error("Failed to create labels")
        return False


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
    price_params = YiDiDaClient.load_price_template("price_template.json", config)
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
        
        # Save response to file
        with open("price_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info("Response saved to price_response.json")
        return True
    else:
        logger.error("Failed to query rates")
        return False


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
        
        # Save response to file
        with open("shipment_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info("Response saved to shipment_response.json")
        return True
    else:
        logger.error("Failed to query shipment information")
        return False


def main_menu():
    """Display interactive menu and route to appropriate module"""
    # Load config and setup logging first
    config = YiDiDaClient.load_config("config.json")
    logger = setup_logging(config)
    
    while True:
        print("\n" + "=" * 60)
        print("YiDiDa API Testing Tool")
        print("=" * 60)
        print("\nAvailable Modules:")
        print("  [1] Create Shipping Labels")
        print("  [2] Query Shipping Rates")
        print("  [3] Query Shipment Status")
        print("  [4] Exit")
        print()
        
        choice = input("Select a module (1-4): ").strip()
        
        if choice == '1':
            create_labels_module()
        elif choice == '2':
            query_price_module()
        elif choice == '3':
            query_shipment_module()
        elif choice == '4':
            logger.info("Exiting YiDiDa API Testing Tool")
            print("\nGoodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please select 1-4.")


def main():
    """Main entry point with CLI argument support"""
    parser = argparse.ArgumentParser(
        description='YiDiDa API Testing Tool - Multi-function client',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                      # Interactive menu mode
  python main.py --create-labels      # Create shipping labels
  python main.py --query-price        # Query shipping rates
  python main.py --query-shipment     # Query shipment status
        '''
    )
    
    parser.add_argument('--create-labels', action='store_true',
                       help='Run label creation module')
    parser.add_argument('--query-price', action='store_true',
                       help='Run rate inquiry module')
    parser.add_argument('--query-shipment', action='store_true',
                       help='Run shipment tracking module')
    parser.add_argument('--menu', action='store_true',
                       help='Show interactive menu (default)')
    
    args = parser.parse_args()
    
    # Setup logging
    config = YiDiDaClient.load_config("config.json")
    setup_logging(config)
    
    # Route to appropriate module based on CLI args
    if args.create_labels:
        create_labels_module()
    elif args.query_price:
        query_price_module()
    elif args.query_shipment:
        query_shipment_module()
    else:
        # Default to interactive menu if no args or --menu specified
        main_menu()


if __name__ == "__main__":
    main()
