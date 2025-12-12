"""
YiDiDa API Client for creating shipping labels (UPS/FedEx)
"""
import requests
import json
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class YiDiDaClient:
    """Client for interacting with YiDiDa shipping label API"""
    
    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize the YiDiDa API client
        
        Args:
            base_url: Base URL for the API (e.g., http://twc.itdida.com/itdida-api)
            username: Your YiDiDa username
            password: Your YiDiDa password
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
        
    def login(self) -> bool:
        """
        Login to YiDiDa API and obtain authentication token
        
        Returns:
            bool: True if login successful, False otherwise
        """
        login_url = f"{self.base_url}/login"
        
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            # YiDiDa API requires form data, not JSON
            response = self.session.post(
                login_url,
                data=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if login was successful
                if result.get("success") and result.get("statusCode") == 200:
                    # Token is in the "data" field as a string
                    self.token = result.get("data")
                    
                    if self.token:
                        # Set token in session headers (without "Bearer" prefix based on API behavior)
                        self.session.headers.update({"Authorization": self.token})
                        logger.info("✓ Login successful! Token obtained.")
                        logger.debug(f"Token: {self.token[:20]}...")
                        return True
                    else:
                        logger.error(f"✗ Login response missing token: {result}")
                        return False
                else:
                    logger.error(f"✗ Login failed: {result.get('data', 'Unknown error')}")
                    return False
            else:
                logger.error(f"✗ Login failed with status code {response.status_code}")
                logger.debug(f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Login request failed: {e}")
            return False
    
    def create_labels(self, label_requests: List[Dict]) -> Optional[Dict]:
        """
        Create shipping labels using YiDiDa API
        
        Args:
            label_requests: List of label request dictionaries
            
        Returns:
            API response dictionary if successful, None otherwise
        """
        if not self.token:
            logger.error("✗ Not logged in. Please call login() first.")
            return None
        
        create_url = f"{self.base_url}/yundans/"
        logger.debug(f"Creating labels at: {create_url}")
        
        try:
            response = self.session.post(
                create_url,
                json=label_requests,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("success") or result.get("code") == 200:
                logger.info(f"✓ Labels created successfully!")
                return result
            else:
                logger.error(f"✗ Label creation failed: {result.get('message', 'Unknown error')}")
                logger.debug(f"Response: {json.dumps(result, indent=2)}")
                return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Label creation request failed: {e}")
            if hasattr(e.response, 'text'):
                logger.debug(f"Response body: {e.response.text}")
            return None
    
    @staticmethod
    def load_config(config_path: str = "config.json") -> Dict:
        """
        Load configuration from JSON file
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def load_label_template(template_path: str = "label_template.json", config: Optional[Dict] = None) -> List[Dict]:
        """
        Load label request template from JSON file and optionally substitute config values
        
        Args:
            template_path: Path to template file
            config: Optional config dictionary to substitute variables (use {{defaults.key}} in template)
            
        Returns:
            List of label request dictionaries
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        # If config is provided, substitute variables like {{defaults.key}}
        if config:
            template_str = YiDiDaClient._substitute_variables(template_str, config)
        
        return json.loads(template_str)
    
    @staticmethod
    def _substitute_variables(template_str: str, config: Dict) -> str:
        """
        Replace variables in template string with config values
        Variables format: {{key.subkey}}
        
        Args:
            template_str: Template string with variables
            config: Configuration dictionary
            
        Returns:
            Template string with variables replaced
        """
        import re
        
        # Find all {{...}} patterns - matches "{{variable}}"
        pattern = r'"{{([^}]+)}}"'
        
        def replace_var(match):
            var_path = match.group(1).strip()
            
            # Navigate through nested config
            keys = var_path.split('.')
            value = config
            try:
                for key in keys:
                    value = value[key]
                # Return JSON-formatted value
                return json.dumps(value, ensure_ascii=False)
            except (KeyError, TypeError):
                # If key not found, return original
                return match.group(0)
        
        return re.sub(pattern, replace_var, template_str)
    
    @staticmethod
    def save_label_template(label_requests: List[Dict], template_path: str = "label_template.json"):
        """
        Save label requests to JSON file
        
        Args:
            label_requests: List of label request dictionaries
            template_path: Path to save template file
        """
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(label_requests, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Template saved to {template_path}")
    
    def query_price(self, price_params: Dict) -> Optional[Dict]:
        """
        Query shipping rates/prices using YiDiDa API
        
        Args:
            price_params: Price query parameters dictionary containing:
                - priceZoneType (int, required): Zone type (1=postal, 2=port, 3=city, 4=region, 5=amazon, 6=state)
                - searchType (int, required): Query type (2=customer pricing, 3=public pricing)
                - wayTypeList (list[int], required): Logistics types (0=express, 1=small parcel, 2=dedicated, etc.)
                - weight (float, required): Weight in kg
                - toCustomer (dict, optional): Recipient info with countryCode, postcode, city, stateCode
                - Other optional parameters as per API documentation
            
        Returns:
            API response dictionary if successful, None otherwise
        """
        if not self.token:
            logger.error("✗ Not logged in. Please call login() first.")
            return None
        
        price_url = f"{self.base_url}/price"
        logger.debug(f"Querying prices at: {price_url}")
        logger.debug(f"Query parameters: {json.dumps(price_params, indent=2, ensure_ascii=False)}")
        
        try:
            response = self.session.post(
                price_url,
                json=price_params,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("success") or result.get("statusCode") == 200:
                logger.info(f"✓ Price query successful!")
                return result
            else:
                logger.error(f"✗ Price query failed: {result.get('message', 'Unknown error')}")
                logger.debug(f"Response: {json.dumps(result, indent=2)}")
                return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Price query request failed: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                logger.debug(f"Response body: {e.response.text}")
            return None
    
    def query_shipment(self, order_numbers: str) -> Optional[Dict]:
        """
        Query shipment details/tracking using YiDiDa API
        
        Args:
            order_numbers: Customer order numbers, comma-separated (max 10)
                          Example: "ORDER001,ORDER002,ORDER003"
            
        Returns:
            API response dictionary if successful, None otherwise
        """
        if not self.token:
            logger.error("✗ Not logged in. Please call login() first.")
            return None
        
        # Validate order numbers
        order_list = [num.strip() for num in order_numbers.split(',') if num.strip()]
        if not order_list:
            logger.error("✗ No order numbers provided.")
            return None
        
        if len(order_list) > 10:
            logger.warning(f"⚠ Maximum 10 order numbers allowed. Only querying first 10.")
            order_list = order_list[:10]
            order_numbers = ','.join(order_list)
        
        query_url = f"{self.base_url}/queryYunDanDetail"
        logger.debug(f"Querying shipment at: {query_url}")
        logger.info(f"Querying {len(order_list)} order(s): {order_numbers}")
        
        try:
            response = self.session.get(
                query_url,
                params={"danHaos": order_numbers},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if result.get("success") or result.get("statusCode") == 200:
                logger.info(f"✓ Shipment query successful!")
                return result
            else:
                logger.error(f"✗ Shipment query failed: {result.get('message', 'Unknown error')}")
                logger.debug(f"Response: {json.dumps(result, indent=2)}")
                return result
                
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Shipment query request failed: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                logger.debug(f"Response body: {e.response.text}")
            return None
    
    @staticmethod
    def load_price_template(template_path: str = "price_template.json", config: Optional[Dict] = None) -> Dict:
        """
        Load price query template from JSON file and optionally substitute config values
        
        Args:
            template_path: Path to template file
            config: Optional config dictionary to substitute variables (use {{defaults.key}} in template)
            
        Returns:
            Price query parameters dictionary
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        
        # If config is provided, substitute variables like {{defaults.key}}
        if config:
            template_str = YiDiDaClient._substitute_variables(template_str, config)
        
        return json.loads(template_str)
