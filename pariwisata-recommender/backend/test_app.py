import sys
sys.path.insert(0, '/app')
try:
    from app.main import app
    print('SUCCESS: App imported successfully')
    print('App type:', type(app))
except Exception as e:
    print('ERROR importing app:', str(e))
    import traceback
    traceback.print_exc()
