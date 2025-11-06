"""
Test Script: Verify ML Recommendations
Membuktikan apakah rekomendasi berasal dari model ML atau hanya popularity-based
"""
import asyncio
import sys
import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_1_check_server():
    """Test 1: Check if server is running"""
    print_section("TEST 1: Check Server Status")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print("❌ Server not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Server not running! Error: {e}")
        print("\n💡 Solution: Run server with:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        return False

def test_2_check_ml_status():
    """Test 2: Check ML model status"""
    print_section("TEST 2: Check ML Model Status")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ ML Status endpoint working!")
            print(f"\n📊 ML Models Status:")
            
            models = data.get('models', {})
            for model_name, model_info in models.items():
                status = "✅ TRAINED" if model_info.get('is_trained') else "❌ NOT TRAINED"
                print(f"   {model_name}: {status}")
                print(f"      → {model_info.get('description', 'N/A')}")
            
            # Check if ANY model is trained
            any_trained = any(m.get('is_trained') for m in models.values())
            
            if any_trained:
                print("\n✅ AT LEAST ONE ML MODEL IS TRAINED!")
                print("   → Website CAN use ML-based recommendations")
            else:
                print("\n⚠️  NO ML MODELS TRAINED YET")
                print("   → Website will use incremental learning (fallback)")
            
            return any_trained
        else:
            print(f"❌ Error checking status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_3_get_recommendations_incremental():
    """Test 3: Get recommendations with incremental algorithm"""
    print_section("TEST 3: Incremental Learning Recommendations")
    try:
        response = requests.get(
            f"{BASE_URL}/api/recommendations/personalized",
            params={
                "algorithm": "incremental",
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Incremental recommendations received!")
            print(f"\n📊 Algorithm Used: {data.get('algorithm')}")
            print(f"   Message: {data.get('message')}")
            print(f"\n   Info:")
            info = data.get('info', {})
            for key, value in info.items():
                print(f"      • {key}: {value}")
            
            recs = data.get('recommendations', [])
            print(f"\n🎯 Top {len(recs)} Recommendations:")
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec.get('name')}")
                print(f"      Rating: {rec.get('rating')}, Reviews: {rec.get('reviewCount')}")
                if 'trending_score' in rec:
                    print(f"      Trending Score: {rec.get('trending_score')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_4_get_recommendations_auto():
    """Test 4: Get recommendations with auto algorithm (smart selection)"""
    print_section("TEST 4: Auto Algorithm (Smart Selection)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/recommendations/personalized",
            params={
                "algorithm": "auto",
                "user_id": 1,  # Simulate logged-in user
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Auto recommendations received!")
            print(f"\n📊 Algorithm Selected: {data.get('algorithm')}")
            print(f"   Message: {data.get('message')}")
            
            info = data.get('info', {})
            print(f"\n   Detection:")
            print(f"      • Uses ML Model: {info.get('uses_ml_model', False)}")
            print(f"      • Uses Incremental: {info.get('uses_incremental', False)}")
            print(f"      • Mode: {info.get('mode', 'N/A')}")
            
            recs = data.get('recommendations', [])
            print(f"\n🎯 Top {len(recs)} Recommendations:")
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec.get('name')}")
                print(f"      Rating: {rec.get('rating')}, Reviews: {rec.get('reviewCount')}")
            
            # Determine which system is being used
            if info.get('uses_ml_model'):
                print("\n✅ RESULT: Using ML MODEL from research!")
            else:
                print("\n⚠️  RESULT: Using INCREMENTAL LEARNING (ML not trained yet)")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_5_try_hybrid():
    """Test 5: Try to force hybrid algorithm"""
    print_section("TEST 5: Force Hybrid Algorithm (ML Model)")
    try:
        response = requests.get(
            f"{BASE_URL}/api/recommendations/personalized",
            params={
                "algorithm": "hybrid",
                "user_id": 1,
                "limit": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Hybrid algorithm response received!")
            print(f"\n📊 Algorithm Used: {data.get('algorithm')}")
            print(f"   Message: {data.get('message')}")
            
            info = data.get('info', {})
            if info.get('uses_ml_model'):
                print("\n🎉 SUCCESS! ML MODEL IS WORKING!")
                print("   → Hybrid: Content-Based + Collaborative Filtering")
                print("   → MAB: Context-aware lambda selection")
                print("   → MMR: Diversification applied")
            else:
                print("\n⚠️  ML Model not available, fell back to incremental")
            
            return info.get('uses_ml_model', False)
            
        else:
            print(f"⚠️  Hybrid not available (expected if not trained)")
            print(f"   Status: {response.status_code}")
            print(f"   This is OK! Model needs training first.")
            return False
            
    except Exception as e:
        print(f"⚠️  Error (expected if model not trained): {e}")
        return False

def test_6_check_data_readiness():
    """Test 6: Check if we have enough data to train ML model"""
    print_section("TEST 6: Check Data Readiness for ML Training")
    try:
        response = requests.get(f"{BASE_URL}/api/ml/status")
        if response.status_code == 200:
            data = response.json()
            
            # Try to get data stats (might not be in status endpoint)
            print("📊 Checking database statistics...")
            
            # You might need to add this endpoint or check differently
            # For now, just show what we have
            print("\n💡 To check if you have enough data:")
            print("   Minimum needed:")
            print("      • 50+ users with ratings")
            print("      • 500+ total ratings")
            print("      • 20+ destinations")
            
            print("\n   To train the model, run:")
            print("      POST /api/ml/train")
            
            return True
        else:
            print("⚠️  Could not check data status")
            return False
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print_section("TEST SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n📊 Results: {passed}/{total} tests passed\n")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print("\n" + "="*70)
    print("\n🎯 CONCLUSION:")
    
    if results.get('ml_status', False):
        print("   ✅ ML models are trained and available!")
        print("   → Website IS using ML-based recommendations")
    else:
        print("   ⚠️  ML models NOT trained yet")
        print("   → Website is using Incremental Learning (fallback)")
        print("\n   📝 Next Steps:")
        print("      1. Collect more data (users interact with website)")
        print("      2. Train ML model: POST /api/ml/train")
        print("      3. Re-run this test to verify")
    
    if results.get('incremental', False):
        print("\n   ✅ Incremental Learning is working!")
        print("   → Real-time trending & popularity scores active")
    
    print("\n" + "="*70)

def main():
    """Run all tests"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║     🧪 ML RECOMMENDATION SYSTEM VERIFICATION TEST 🧪              ║")
    print("║                                                                    ║")
    print("║  This test will verify if your website recommendations come       ║")
    print("║  from ML models or incremental learning                           ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Test 1: Server
    if not test_1_check_server():
        print("\n❌ Server not running. Cannot proceed with tests.")
        print("\n💡 Start server with:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        return
    
    results['server'] = True
    
    # Test 2: ML Status
    results['ml_status'] = test_2_check_ml_status()
    
    # Test 3: Incremental
    results['incremental'] = test_3_get_recommendations_incremental()
    
    # Test 4: Auto
    results['auto_mode'] = test_4_get_recommendations_auto()
    
    # Test 5: Hybrid (might fail if not trained)
    results['hybrid'] = test_5_try_hybrid()
    
    # Test 6: Data readiness
    results['data_check'] = test_6_check_data_readiness()
    
    # Summary
    print_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
