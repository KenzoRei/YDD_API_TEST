"""
Example script demonstrating how to use the YiDiDa API client
"""
from yidida_client import YiDiDaClient
import json


def main():
    """Main function to demonstrate API usage"""
    
    print("=" * 60)
    print("YiDiDa Shipping Label Creator")
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
    print("\nAttempting to login...")
    if not client.login():
        print("\n✗ Failed to login. Please check your credentials in config.json")
        return
    
    print()
    
    # Load label template
    print("Loading label template...")
    label_requests = YiDiDaClient.load_label_template("label_template.json", config)
    print(f"✓ Loaded {len(label_requests)} label request(s)")
    
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
        print("\n✗ Label creation cancelled.")
        return
    
    # Create labels
    print("\nCreating labels...")
    result = client.create_labels(label_requests)
    
    if result:
        print("\n" + "=" * 60)
        print("API Response:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Save response to file
        with open("label_response.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\n✓ Response saved to label_response.json")
    else:
        print("\n✗ Failed to create labels.")


def create_custom_label():
    """Example: Create a label with custom data"""
    
    # Load and modify template
    label_requests = YiDiDaClient.load_label_template("label_template.json")
    
    # Customize the first label
    label = label_requests[0]
    label["keHuDanHao"] = "CUSTOM12345"  # Custom order number
    label["shouJianRenXingMing"] = "John Doe"  # Recipient name
    label["shouJianRenDiZhi1"] = "123 Main Street"  # Address
    label["shouJianRenChengShi"] = "Los Angeles"  # City
    label["zhouMing"] = "CA"  # State
    label["shouJianRenYouBian"] = "90001"  # Zip code
    
    # You can save this as a new template
    YiDiDaClient.save_label_template(label_requests, "custom_label.json")
    
    # Then use it to create labels
    config = YiDiDaClient.load_config("config.json")
    client = YiDiDaClient(
        base_url=config["api_base_url"],
        username=config["credentials"]["username"],
        password=config["credentials"]["password"]
    )
    
    if client.login():
        result = client.create_labels(label_requests)
        return result
    
    return None


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run custom label example
    # create_custom_label()
