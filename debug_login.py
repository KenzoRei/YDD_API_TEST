"""
Debug script to test YiDiDa login and see the actual response
"""
import requests
import json

# Configuration
base_url = "http://twc.itdida.com/itdida-api"
username = "F000210"
password = "abc12345"

# Test endpoints
login_endpoints = [
    "/login",
    "/api/yundan/login", 
    "/api/login"
]

payload = {
    "username": username,
    "password": password
}

print("=" * 60)
print("YiDiDa Login Debug Tool")
print("=" * 60)

for endpoint in login_endpoints:
    login_url = f"{base_url}{endpoint}"
    print(f"\n\nTesting: {login_url}")
    print("-" * 60)
    
    # Try JSON
    try:
        print("\n[JSON Method]")
        response = requests.post(
            login_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"JSON Parsed Successfully!")
                print(f"Response Type: {type(result)}")
                print(f"Response Content: {json.dumps(result, indent=2, ensure_ascii=False)[:1000]}")
            except:
                print(f"Failed to parse as JSON")
    except Exception as e:
        print(f"JSON Request Error: {e}")
    
    # Try Form Data
    try:
        print("\n[Form Data Method]")
        response = requests.post(
            login_url,
            data=payload,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"JSON Parsed Successfully!")
                print(f"Response Type: {type(result)}")
                print(f"Response Content: {json.dumps(result, indent=2, ensure_ascii=False)[:1000]}")
            except:
                print(f"Failed to parse as JSON")
    except Exception as e:
        print(f"Form Data Request Error: {e}")

print("\n\n" + "=" * 60)
print("Debug Complete")
print("=" * 60)
