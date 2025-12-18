"""Module 1: Create shipping labels from template"""
from yidida_client import YiDiDaClient
import json
import logging
from datetime import datetime


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
    label_requests = YiDiDaClient.load_label_template("templates/label_template.json", config)
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
        
        # Save response to file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/label_response_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Response saved to {filename}")
        return True
    else:
        logger.error("Failed to create labels")
        return False
