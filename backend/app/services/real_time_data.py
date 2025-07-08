import httpx

async def get_weather(lat, lon):
    # Dummy: return fixed weather, nanti diisi API cuaca asli
    return {"main": "Clear", "desc": "cerah"}