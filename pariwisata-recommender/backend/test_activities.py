import requests

# Login first
login_response = requests.post(
    "http://localhost:8000/admin/login",
    json={"email": "admin@example.com", "password": "admin123"}
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login successful!")
    
    # Test activities endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://localhost:8000/admin/activities", headers=headers)
    
    if response.status_code == 200:
        activities = response.json()
        print(f"\n✅ Got {len(activities)} activities")
        
        if len(activities) > 0:
            print(f"\n📊 First 3 activities:")
            for act in activities[:3]:
                print(f"   - ID: {act['id']}, Name: {act['name']}, Category: {act['category']}")
            print(f"\n✅ This is REAL DATA from database!")
        else:
            print("⚠️ No activities found")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
else:
    print(f"❌ Login failed: {login_response.status_code}")
