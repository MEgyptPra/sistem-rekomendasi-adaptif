"""
Contextual Multi-Armed Bandit Optimizer using Upper Confidence Bound (UCB1) algorithm.
Learns optimal lambda values for different contexts (weather, time, user situation).
"""

import numpy as np
import math
from typing import Tuple, List, Dict, Any
import json
import os
import hashlib

class MABOptimizer:
    """
    Mengimplementasikan Contextual Multi-Armed Bandit menggunakan algoritma UCB1.
    Memelihara set UCB terpisah untuk setiap konteks unik.
    Tugasnya adalah memilih nilai lambda terbaik untuk MMR secara dinamis berdasarkan konteks.
    """
    
    def __init__(self, n_arms: int = 11, exploration_param: float = 2.0, persistence_file: str = None):
        """
        Inisialisasi Contextual MAB Optimizer.

        Args:
            n_arms (int): Jumlah 'arm' atau pilihan, sesuai dengan jumlah nilai lambda.
            exploration_param (float): Parameter 'c' dalam formula UCB, mengontrol tingkat eksplorasi.
            persistence_file (str): Path file untuk menyimpan state MAB (optional).
        """
        # Mendefinisikan arms sebagai nilai lambda dari 0.0 hingga 1.0
        self.arms = np.linspace(0, 1, n_arms)
        self.n_arms = n_arms
        self.c = exploration_param
        self.persistence_file = persistence_file
        
        # Menggunakan dictionary untuk menyimpan data UCB per konteks
        # Format: {context_key: {'counts': array, 'rewards': array, 'total_pulls': int}}
        self.context_data = {}
        
        # Load state dari file jika tersedia
        self._load_state()

    def _get_context_key(self, context: Dict[str, Any]) -> str:
        """
        Mengubah dictionary konteks menjadi string hash yang unik.
        
        Args:
            context: Dictionary konteks dari RealTimeContextService
            
        Returns:
            str: Context key yang unik
        """
        # Pilih fitur konteks yang paling relevan untuk recommendation strategy
        # Kita fokus pada weather, is_weekend, dan hour category
        hour_category = self._categorize_hour(context.get('hour_of_day', 12))
        
        key_components = [
            f"weather:{context.get('weather', 'unknown')}",
            f"weekend:{context.get('is_weekend', False)}",
            f"hour_cat:{hour_category}",
            f"season:{context.get('season', 'unknown')}"
        ]
        
        key_str = "|".join(key_components)
        return key_str

    def _categorize_hour(self, hour: int) -> str:
        """Kategorikan jam menjadi periode yang lebih general"""
        if 6 <= hour <= 11:
            return "morning"
        elif 12 <= hour <= 17:
            return "afternoon"
        elif 18 <= hour <= 22:
            return "evening"
        else:
            return "night"

    def _initialize_context(self, context_key: str):
        """Membuat entri baru jika konteks ini belum pernah dilihat."""
        if context_key not in self.context_data:
            self.context_data[context_key] = {
                'counts': np.zeros(self.n_arms, dtype=int),
                'rewards': np.zeros(self.n_arms, dtype=float),
                'total_pulls': 0
            }
            print(f"🆕 New context initialized: {context_key}")

    def select_arm(self, context: Dict[str, Any] = None) -> int:
        """
        Memilih arm (nilai lambda) berdasarkan konteks yang diberikan.
        
        Args:
            context: Dictionary konteks dari RealTimeContextService
            
        Returns:
            int: Index dari arm yang terpilih.
        """
        # Fallback ke behavior non-contextual jika tidak ada context
        if context is None:
            return self._select_arm_non_contextual()
        
        context_key = self._get_context_key(context)
        self._initialize_context(context_key)
        
        data = self.context_data[context_key]

        # Tahap awal: coba setiap arm setidaknya sekali untuk konteks ini
        for arm_index in range(self.n_arms):
            if data['counts'][arm_index] == 0:
                print(f"🔍 Exploring arm {arm_index} (λ={self.arms[arm_index]:.1f}) for context: {context_key}")
                return arm_index

        # Setelah semua arm dicoba untuk konteks ini, gunakan formula UCB
        avg_rewards = data['rewards'] / np.maximum(data['counts'], 1)
        
        # Hindari division by zero dan log(0)
        safe_total_pulls = max(data['total_pulls'], 1)
        
        exploration_bonus = self.c * np.sqrt(
            math.log(safe_total_pulls) / np.maximum(data['counts'], 1)
        )
        
        ucb_scores = avg_rewards + exploration_bonus
        
        # Pilih arm dengan skor UCB tertinggi
        selected_arm = np.argmax(ucb_scores)
        print(f"🎯 UCB selected arm {selected_arm} (λ={self.arms[selected_arm]:.1f}) for context: {context_key}")
        return selected_arm

    def _select_arm_non_contextual(self) -> int:
        """Fallback method untuk non-contextual selection"""
        # Use global data (sum across all contexts)
        if not self.context_data:
            return 0  # Start with first arm
        
        global_counts = np.zeros(self.n_arms)
        global_rewards = np.zeros(self.n_arms)
        global_pulls = 0
        
        for data in self.context_data.values():
            global_counts += data['counts']
            global_rewards += data['rewards']
            global_pulls += data['total_pulls']
        
        # Check if any arm hasn't been tried
        for arm_index in range(self.n_arms):
            if global_counts[arm_index] == 0:
                return arm_index
        
        # Use UCB on global data
        avg_rewards = global_rewards / np.maximum(global_counts, 1)
        exploration_bonus = self.c * np.sqrt(
            math.log(max(global_pulls, 1)) / np.maximum(global_counts, 1)
        )
        ucb_scores = avg_rewards + exploration_bonus
        return np.argmax(ucb_scores)

    def update_reward(self, arm_index: int, reward: float, context: Dict[str, Any] = None):
        """
        Memperbarui data reward untuk arm yang dipilih dalam konteks spesifik.

        Args:
            arm_index (int): Index dari arm yang baru saja dipilih.
            reward (float): Reward yang diterima dari pemilihan arm tersebut.
            context (Dict): Konteks saat arm dipilih.
        """
        if not (0 <= arm_index < self.n_arms):
            print(f"❌ Invalid arm_index: {arm_index}")
            return
            
        if context is None:
            print("⚠️ No context provided for reward update")
            return
            
        context_key = self._get_context_key(context)
        
        # Pastikan konteks sudah ada (biasanya sudah karena select_arm dipanggil dulu)
        if context_key not in self.context_data:
            self._initialize_context(context_key)
        
        data = self.context_data[context_key]
        data['counts'][arm_index] += 1
        data['rewards'][arm_index] += reward
        data['total_pulls'] += 1
        
        lambda_value = self.get_lambda_value(arm_index)
        avg_reward = data['rewards'][arm_index] / data['counts'][arm_index]
        
        print(f"📈 Reward updated: arm {arm_index} (λ={lambda_value:.1f}) "
              f"got reward {reward:.3f}, avg now {avg_reward:.3f} "
              f"for context: {context_key}")
        
        # Simpan state setelah update
        self._save_state()

    def get_lambda_value(self, arm_index: int) -> float:
        """
        Mendapatkan nilai lambda dari arm index.
        
        Args:
            arm_index (int): Index dari arm.
            
        Returns:
            float: Nilai lambda (0.0 - 1.0).
        """
        if 0 <= arm_index < self.n_arms:
            return self.arms[arm_index]
        return 0.7  # Default fallback

    def get_statistics(self) -> Dict[str, Any]:
        """
        Mendapatkan statistik performance dari semua contexts dan arms.
        
        Returns:
            Dict: Statistik lengkap Contextual MAB.
        """
        total_contexts = len(self.context_data)
        global_pulls = sum(data['total_pulls'] for data in self.context_data.values())
        
        # Aggregate statistics across all contexts
        global_counts = np.zeros(self.n_arms)
        global_rewards = np.zeros(self.n_arms)
        
        for data in self.context_data.values():
            global_counts += data['counts']
            global_rewards += data['rewards']
        
        global_avg_rewards = np.divide(global_rewards, global_counts, 
                                     out=np.zeros_like(global_rewards), 
                                     where=global_counts != 0)
        
        stats = {
            "total_contexts": total_contexts,
            "total_pulls": int(global_pulls),
            "global_arms_stats": [],
            "context_breakdown": {}
        }
        
        # Global arm statistics
        for i in range(self.n_arms):
            arm_stats = {
                "arm_index": i,
                "lambda_value": float(self.arms[i]),
                "pulls": int(global_counts[i]),
                "total_reward": float(global_rewards[i]),
                "avg_reward": float(global_avg_rewards[i]),
                "pull_percentage": float(global_counts[i] / max(global_pulls, 1) * 100)
            }
            stats["global_arms_stats"].append(arm_stats)
        
        # Per-context breakdown
        for context_key, data in self.context_data.items():
            context_avg_rewards = np.divide(data['rewards'], data['counts'], 
                                          out=np.zeros_like(data['rewards']), 
                                          where=data['counts'] != 0)
            
            stats["context_breakdown"][context_key] = {
                "total_pulls": int(data['total_pulls']),
                "best_arm": int(np.argmax(context_avg_rewards)) if data['total_pulls'] > 0 else None,
                "best_lambda": float(self.arms[np.argmax(context_avg_rewards)]) if data['total_pulls'] > 0 else None,
                "best_avg_reward": float(np.max(context_avg_rewards)) if data['total_pulls'] > 0 else 0.0
            }
        
        return stats

    def reset(self):
        """Reset semua data MAB ke kondisi awal."""
        self.context_data = {}
        self._save_state()
        print("🔄 MAB state has been reset")

    def _save_state(self):
        """Simpan state MAB ke file (jika persistence_file diset)."""
        if self.persistence_file:
            try:
                # Convert numpy arrays to lists for JSON serialization
                serializable_data = {}
                for context_key, data in self.context_data.items():
                    serializable_data[context_key] = {
                        "counts": data['counts'].tolist(),
                        "rewards": data['rewards'].tolist(),
                        "total_pulls": data['total_pulls']
                    }
                
                state = {
                    "context_data": serializable_data,
                    "n_arms": self.n_arms,
                    "exploration_param": self.c
                }
                
                # Create directory if not exists
                if self.persistence_file:
                    os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
                    
                    with open(self.persistence_file, 'w') as f:
                        json.dump(state, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save MAB state: {e}")

    def _load_state(self):
        """Load state MAB dari file (jika ada)."""
        if self.persistence_file and os.path.exists(self.persistence_file):
            try:
                with open(self.persistence_file, 'r') as f:
                    state = json.load(f)
                
                # Restore context data
                for context_key, data in state.get("context_data", {}).items():
                    if len(data["counts"]) == self.n_arms and len(data["rewards"]) == self.n_arms:
                        self.context_data[context_key] = {
                            'counts': np.array(data["counts"], dtype=int),
                            'rewards': np.array(data["rewards"], dtype=float),
                            'total_pulls': data["total_pulls"]
                        }
                
                print(f"📁 Contextual MAB state loaded from {self.persistence_file}")
                print(f"   Loaded {len(self.context_data)} contexts")
                    
            except Exception as e:
                print(f"Warning: Could not load MAB state: {e}")
