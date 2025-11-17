"""
Test script untuk cek apakah admin endpoint bisa akses database
"""
import requests
import json

# 1. Login dulu untuk dapat token
print("🔐 Testing Admin Login...")
login_response = requests.post(
    "http://localhost:8000/admin/login",
    json={
        "email": "admin@example.com",
        "password": "admin123"
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print(f"✅ Login successful! Token: {token[:50]}...")
    
    # 2. Test get destinations dengan token
    print("\n📍 Testing Get Destinations...")
    headers = {"Authorization": f"Bearer {token}"}
    dest_response = requests.get(
        "http://localhost:8000/admin/destinations",
        headers=headers
    )
    
    if dest_response.status_code == 200:
        destinations = dest_response.json()
        print(f"✅ Got {len(destinations)} destinations")
        print("\n📊 Destinations:")
        for dest in destinations[:5]:  # Show first 5
            print(f"  - ID: {dest['id']}, Name: {dest['name']}, Location: {dest['location']}")
        
        # Check if it's demo data or real data
        if any("Demo Destination" in d['name'] for d in destinations):
            print("\n⚠️  WARNING: This is DEMO DATA, not from database!")
            print("   Possible issues:")
            print("   1. Database connection failed")
            print("   2. Database is empty")
            print("   3. Destination table doesn't exist")
        else:
            print("\n✅ This is REAL DATA from database!")
    else:
        print(f"❌ Failed to get destinations: {dest_response.status_code}")
        print(dest_response.text)
    
    # 3. Test get stats
    print("\n📊 Testing Get Stats...")
    stats_response = requests.get(
        "http://localhost:8000/admin/stats",
        headers=headers
    )
    
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"✅ Stats: {json.dumps(stats, indent=2)}")
        if stats.get("dataSource") == "demo":
            print("⚠️  WARNING: Stats using DEMO data!")
        else:
            print("✅ Stats from REAL database!")
    else:
        print(f"❌ Failed to get stats: {stats_response.status_code}")
        
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
