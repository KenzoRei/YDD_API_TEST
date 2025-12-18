"""
YiDiDa API Testing Tool - Multi-function client for label creation, rate inquiry, and shipment tracking
"""
from yidida_client import YiDiDaClient
from modules import create_labels_module, query_price_module, query_shipment_module
import argparse
import logging
import sys


def setup_logging(config):
    """Configure logging based on config.json settings"""
    log_config = config.get("logging", {})
    log_level = log_config.get("log_level", "INFO")
    log_to_file = log_config.get("log_to_file", False)
    log_file_path = log_config.get("log_file_path", "logs/yidida_api.log")
    
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
