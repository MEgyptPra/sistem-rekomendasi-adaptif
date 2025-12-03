from pathlib import Path

# Test path resolution for hybrid_recommender
hybrid_file = Path("/app/app/services/hybrid_recommender.py")
model_dir = hybrid_file.resolve().parents[2] / "data" / "models"

print(f"Hybrid file: {hybrid_file}")
print(f"Resolved: {hybrid_file.resolve()}")
print(f"MODEL_DIR: {model_dir}")
print(f"MODEL_DIR exists: {model_dir.exists()}")

if model_dir.exists():
    files = list(model_dir.glob("*.pkl"))
    print(f"Model files found: {files}")
else:
    print("MODEL_DIR does not exist!")
