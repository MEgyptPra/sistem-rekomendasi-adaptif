"""
Script untuk check status model persistence
Digunakan untuk memverifikasi bahwa models tersimpan dan dapat di-load
"""

import pickle
from pathlib import Path
from datetime import datetime

MODEL_DIR = Path("data/models")

def check_model_file(filename: str, model_type: str):
    """Check single model file"""
    model_path = MODEL_DIR / filename
    
    print(f"\n{'='*60}")
    print(f"📦 Checking {model_type} Model")
    print(f"{'='*60}")
    
    if not model_path.exists():
        print(f"❌ File not found: {model_path}")
        return False
    
    try:
        # Load model data
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        # Display basic info
        print(f"✅ File exists: {model_path}")
        print(f"📁 File size: {model_path.stat().st_size / 1024:.2f} KB")
        
        # Display training info
        trained_at = model_data.get('trained_at', 'unknown')
        is_trained = model_data.get('is_trained', False)
        
        print(f"🤖 Training Status: {'✅ TRAINED' if is_trained else '❌ NOT TRAINED'}")
        print(f"📅 Trained At: {trained_at}")
        
        # Display model-specific info
        print(f"\n📊 Model Components:")
        for key in model_data.keys():
            if key not in ['trained_at', 'is_trained']:
                value = model_data[key]
                if hasattr(value, 'shape'):
                    print(f"   - {key}: {type(value).__name__} {value.shape}")
                elif isinstance(value, dict):
                    print(f"   - {key}: dict with {len(value)} items")
                else:
                    print(f"   - {key}: {type(value).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def main():
    """Main check function"""
    print("\n" + "="*60)
    print("🔍 MODEL PERSISTENCE STATUS CHECK")
    print("="*60)
    
    # Check if model directory exists
    if not MODEL_DIR.exists():
        print(f"\n❌ Model directory not found: {MODEL_DIR}")
        print("   Models have not been trained yet.")
        return
    
    print(f"\n✅ Model directory exists: {MODEL_DIR}")
    
    # Check each model
    models = [
        ("content_based_model.pkl", "Content-Based"),
        ("collaborative_model.pkl", "Collaborative"),
        ("hybrid_model.pkl", "Hybrid")
    ]
    
    results = {}
    for filename, model_type in models:
        results[model_type] = check_model_file(filename, model_type)
    
    # Summary
    print("\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    
    for model_type, status in results.items():
        status_icon = "✅" if status else "❌"
        status_text = "READY" if status else "NOT FOUND"
        print(f"   {status_icon} {model_type}: {status_text}")
    
    all_ready = all(results.values())
    print("\n" + "="*60)
    if all_ready:
        print("✅ All models are persisted and ready!")
        print("   Server dapat di-restart tanpa perlu re-training.")
    else:
        print("⚠️ Some models are missing!")
        print("   Jalankan training endpoint untuk create models.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
