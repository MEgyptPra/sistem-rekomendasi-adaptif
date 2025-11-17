"""
Script untuk switch antara Simulation dan Production Real-Time Data Service
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_api_configuration():
    """Check which APIs are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openweather = os.getenv("OPENWEATHER_API_KEY", "")
    google_maps = os.getenv("GOOGLE_MAPS_API_KEY", "")
    tomtom = os.getenv("TOMTOM_API_KEY", "")
    
    print("\n" + "="*60)
    print("🔍 API Configuration Status")
    print("="*60)
    
    print(f"\n1. OpenWeatherMap API:")
    if openweather and openweather != "your_openweathermap_api_key_here":
        print(f"   ✅ Configured: {openweather[:10]}...{openweather[-4:]}")
    else:
        print(f"   ❌ Not configured (using simulation)")
    
    print(f"\n2. Google Maps API:")
    if google_maps and google_maps != "your_google_maps_api_key_here":
        print(f"   ✅ Configured: {google_maps[:10]}...{google_maps[-4:]}")
    else:
        print(f"   ❌ Not configured (will skip traffic)")
    
    print(f"\n3. TomTom API:")
    if tomtom and tomtom != "your_tomtom_api_key_here":
        print(f"   ✅ Configured: {tomtom[:10]}...{tomtom[-4:]}")
    else:
        print(f"   ❌ Not configured (will skip traffic)")
    
    print("\n" + "="*60)
    
    # Determine mode
    has_weather = openweather and openweather != "your_openweathermap_api_key_here"
    has_traffic = (google_maps and google_maps != "your_google_maps_api_key_here") or \
                  (tomtom and tomtom != "your_tomtom_api_key_here")
    
    if has_weather or has_traffic:
        print("🎯 Mode: PRODUCTION (using real APIs)")
        print("   Weather:", "✅ Real API" if has_weather else "❌ Simulation")
        print("   Traffic:", "✅ Real API" if has_traffic else "❌ Simulation")
    else:
        print("🎲 Mode: SIMULATION (no API keys configured)")
    
    print("="*60 + "\n")
    
    return {
        "has_weather_api": has_weather,
        "has_traffic_api": has_traffic,
        "mode": "production" if (has_weather or has_traffic) else "simulation"
    }

async def test_real_api():
    """Test real API connection"""
    from app.services.real_time_data_production import RealTimeContextService
    
    print("\n" + "="*60)
    print("🧪 Testing Real-Time Data APIs")
    print("="*60 + "\n")
    
    service = RealTimeContextService()
    
    # Test with default Sumedang location
    print(f"📍 Testing with location: Sumedang ({service.DEFAULT_LAT}, {service.DEFAULT_LON})\n")
    
    try:
        context = await service.get_current_context()
        
        print("✅ Context Retrieved Successfully!")
        print("\n📊 Results:")
        print(f"   Weather: {context['weather']} ({context.get('temperature', 'N/A')}°C)")
        print(f"   Traffic: {context['traffic']} ({context.get('traffic_speed', 'N/A')} km/h)")
        print(f"   Season: {context['season']}")
        print(f"   Time: {context['hour_of_day']}:00 ({context.get('time_period', 'N/A')})")
        print(f"   Weekend: {context['is_weekend']}")
        print(f"   Social Trend: {context.get('social_trend', 'N/A')}")
        if context.get('viral_destinations'):
            print(f"   🔥 Viral Destinations: {len(context['viral_destinations'])}")
        if context.get('trending_destinations'):
            print(f"   📈 Trending Destinations: {len(context['trending_destinations'])}")
        
        print(f"\n🔍 Data Sources:")
        print(f"   Weather: {context['data_source']['weather']}")
        print(f"   Traffic: {context['data_source']['traffic']}")
        print(f"   Social Trends: {context['data_source'].get('social_trend', 'user_interactions')}")
        
        if context['data_source']['weather'] == 'simulation' and \
           context['data_source']['traffic'] == 'simulation':
            print("\n⚠️  All data is simulated. Configure API keys in .env for real data.")
        elif context['data_source']['weather'] == 'simulation':
            print("\n⚠️  Weather is simulated. Add OPENWEATHER_API_KEY to .env for real data.")
        elif context['data_source']['traffic'] == 'simulation':
            print("\n⚠️  Traffic is simulated. Add GOOGLE_MAPS_API_KEY or TOMTOM_API_KEY to .env.")
        else:
            print("\n🎉 All data is from real APIs!")
        
        print("\n" + "="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        print("="*60 + "\n")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n" + "="*60)
    print("📚 Setup Instructions")
    print("="*60)
    
    print("""
1. Get OpenWeatherMap API Key (FREE):
   - Go to: https://home.openweathermap.org/api_keys
   - Sign up for free account
   - Generate API key
   - Free tier: 1,000 calls/day (enough for us!)

2. Get Google Maps API Key (OPTIONAL):
   - Go to: https://console.cloud.google.com/
   - Create project
   - Enable "Distance Matrix API"
   - Generate API key
   - Free tier: $200 credit/month

3. Add to .env file:
   OPENWEATHER_API_KEY=your_actual_key_here
   GOOGLE_MAPS_API_KEY=your_actual_key_here

4. Restart server to load new keys

5. Test with: python check_realtime_api.py
    """)
    
    print("="*60 + "\n")

def main():
    import asyncio
    
    print("\n🤖 Real-Time Data Service Configuration Tool\n")
    
    # Check configuration
    config = check_api_configuration()
    
    # Test APIs
    print("Testing APIs...\n")
    success = asyncio.run(test_real_api())
    
    # Show instructions if needed
    if config["mode"] == "simulation":
        print("\n💡 Want to use real data instead of simulation?")
        show_setup_instructions()
    else:
        print("\n✅ Setup complete! Your system is using real APIs.\n")

if __name__ == "__main__":
    main()
