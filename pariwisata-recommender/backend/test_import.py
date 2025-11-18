import sys
sys.path.insert(0, '/app')
try:
    from app.main import app
    print('App loaded successfully')
except Exception as e:
    print('Error loading app:', e)
    import traceback
    traceback.print_exc()
