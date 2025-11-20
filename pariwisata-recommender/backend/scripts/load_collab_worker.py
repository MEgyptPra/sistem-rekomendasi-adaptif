import os
import sys
import time
import json
import traceback

def check_memory_threshold(threshold_bytes: int = None) -> bool:
    """Check if available memory is above `threshold_bytes`.

    If psutil is available, use it. If not, conservatively return True
    so the caller can decide. Caller should still run in a separate
    process/container for safety.
    """
    try:
        import psutil
    except Exception:
        return True

    vm = psutil.virtual_memory()
    avail = vm.available
    if threshold_bytes is None:
        # default: require at least 4GB available
        threshold_bytes = 4 * 1024 ** 3
    return avail >= threshold_bytes


def load_collaborative_model(model_path: str):
    """Load the collaborative model using joblib with mmap if possible.

    This script is intended to be run in its own process with extra memory.
    """
    try:
        print(f"[worker] Starting collaborative model load from: {model_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(model_path)

        # Try to use joblib with mmap_mode to reduce peak memory when possible
        try:
            from joblib import load as joblib_load
            print("[worker] Using joblib to load model with mmap_mode='r'")
            model = joblib_load(model_path, mmap_mode='r')
        except Exception:
            # Fallback to pickle
            import pickle
            print("[worker] joblib load failed, falling back to pickle.load")
            with open(model_path, 'rb') as f:
                model = pickle.load(f)

        # Optionally verify model shape/metadata if present
        meta = getattr(model, 'trained_at', None)
        print(f"[worker] Model loaded successfully. trained_at={meta}")
        # Keep process alive briefly to allow inspection/logging
        time.sleep(1)
        return {'status': 'loaded', 'trained_at': str(meta)}
    except Exception as e:
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}


def main():
    # Expect model path as first arg, else use default mounted path
    model_path = sys.argv[1] if len(sys.argv) > 1 else '/app/data/models/collaborative_model.pkl'

    # Check memory
    ok = check_memory_threshold()
    if not ok:
        print('[worker] Available memory is below threshold, refusing to load model.')
        sys.exit(2)

    result = load_collaborative_model(model_path)
    print(json.dumps(result))


if __name__ == '__main__':
    main()
