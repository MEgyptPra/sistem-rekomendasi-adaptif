import numpy as np
import json
import os
from typing import List, Dict, Any, Optional

class MABOptimizer:
    """
    Contextual Multi-Armed Bandit (UCB1)
    Diadaptasi langsung dari 'ContextualMAB' di Notebook Evaluasi.
    """
    
    def __init__(self, n_arms: int = 5, exploration_param: float = 2.0, persistence_file: str = "data/mab_state.json"):
        self.c = exploration_param
        self.persistence_file = persistence_file
        
        # Fixed arms sama dengan notebook evaluasi (5 arms)
        # Sesuai penelitian: [0.0, 0.3, 0.5, 0.7, 1.0]
        self.arms = [0.0, 0.3, 0.5, 0.7, 1.0]
        self.n_arms = len(self.arms)
        
        # Sama seperti self.context_brains di notebook
        self.context_data = {}
        
        self.load_state()

    def _get_context_key(self, context: Dict[str, Any]) -> str:
        """Generate string key dari context dict (Sama dengan get_context_key_string di notebook)"""
        if not context:
            return "default"
        
        # Urutan harus konsisten agar key stabil
        keys = sorted(context.keys())
        parts = []
        for k in keys:
            val = context[k]
            parts.append(str(val).lower())
        return "_".join(parts)

    def _get_or_create_brain(self, context_key: str):
        """
        [ADAPTASI DARI NOTEBOOK]
        Helper untuk mengambil atau membuat 'otak' (state) baru untuk konteks baru.
        Mencegah KeyError saat menemui konteks yang belum pernah dilihat.
        """
        if context_key not in self.context_data:
            print(f"🌟 MAB: New context found '{context_key}', initializing learning...")
            self.context_data[context_key] = {
                'counts': np.zeros(self.n_arms).tolist(),
                'values': np.zeros(self.n_arms).tolist(), # values = avg_rewards di notebook
                'total_selections': 0
            }
            # Auto-save saat menemukan konteks baru
            self.save_state()
            
        return self.context_data[context_key]

    def select_arm(self, context_state: Dict[str, Any]) -> int:
        """
        Select arm using UCB1.
        Sama persis dengan logika 'select_arm' di notebook.
        """
        context_key = self._get_context_key(context_state)
        
        # Gunakan helper 'aman' seperti di notebook
        brain = self._get_or_create_brain(context_key)
        
        counts = np.array(brain['counts'])
        values = np.array(brain['values'])
        
        # Hitung total selections (bisa dari variabel atau sum counts)
        total_selections = np.sum(counts)
        
        # Logic UCB1 dari Notebook
        if total_selections == 0:
            # Cold start: pilih tengah
            return self.n_arms // 2
            
        ucb_values = np.zeros(self.n_arms)
        for arm in range(self.n_arms):
            if counts[arm] == 0:
                # Prioritaskan arm yang belum pernah dicoba (Infinite UCB)
                return arm
            else:
                # Rumus UCB1
                bonus = self.c * np.sqrt((2 * np.log(total_selections)) / counts[arm])
                ucb_values[arm] = values[arm] + bonus
                
        return int(np.argmax(ucb_values))

    def update_reward(self, arm_index: int, reward: float, context: Dict[str, Any] = None):
        """
        Update statistics.
        Sama persis dengan logika 'update' di notebook.
        """
        context_key = self._get_context_key(context)
        brain = self._get_or_create_brain(context_key)
        
        counts = brain['counts']
        values = brain['values']
        
        # Update counts
        counts[arm_index] += 1
        n = counts[arm_index]
        
        # Update Average Reward (Incremental Formula)
        # NewAvg = OldAvg + (Reward - OldAvg) / n
        old_value = values[arm_index]
        new_value = old_value + (reward - old_value) / n
        values[arm_index] = new_value
        
        # Simpan kembali ke dictionary & file
        brain['counts'] = counts
        brain['values'] = values
        brain['total_selections'] += 1
        
        self.save_state()

    def get_lambda_value(self, arm_index: int) -> float:
        if 0 <= arm_index < self.n_arms:
            return self.arms[arm_index]
        return 0.5

    def save_state(self):
        try:
            os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
            with open(self.persistence_file, 'w') as f:
                json.dump(self.context_data, f)
        except Exception as e:
            print(f"⚠️ Failed to save MAB state: {e}")

    def load_state(self):
        try:
            if os.path.exists(self.persistence_file):
                with open(self.persistence_file, 'r') as f:
                    self.context_data = json.load(f)
                print(f"📁 Contextual MAB state loaded ({len(self.context_data)} contexts)")
            else:
                print("ℹ️ No MAB state found, starting fresh")
        except Exception as e:
            print(f"⚠️ Failed to load MAB state: {e}")
            self.context_data = {}

    def get_statistics(self) -> Dict[str, Any]:
        return {
            "total_contexts": len(self.context_data),
            "contexts": self.context_data
        }

    def reset(self):
        self.context_data = {}
        self.save_state()