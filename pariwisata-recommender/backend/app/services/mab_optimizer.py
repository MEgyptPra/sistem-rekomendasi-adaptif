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
    def __init__(self, n_arms: int = 11, exploration_param: float = 2.0, persistence_file: str = None):
        """
        IMPROVED: Selaras dengan tesis research design
        """
        # Arms as lambda values - consistent dengan tesis methodology
        self.arms = np.linspace(0, 1, n_arms)  # [0.0, 0.1, 0.2, ..., 1.0]
        self.n_arms = n_arms
        self.c = exploration_param
        self.persistence_file = persistence_file
        
        # Context data format: {context_key: {'counts': array, 'rewards': array, 'total_pulls': int}}
        self.context_data = {}
        
        # Load previous state if available
        self.load_state()

    def initialize_context(self, context: Dict[str, Any]) -> str:
        context_key = self.get_context_key(context)
        if context_key not in self.context_data:
            self.context_data[context_key] = {
                'counts': np.zeros(self.n_arms, dtype=int),
                'rewards': np.zeros(self.n_arms, dtype=float),
                'total_pulls': 0
            }
        return context_key

    
    def get_context_key(self, context: Dict[str, Any]) -> str:
        """
        Mengubah dictionary konteks menjadi string hash yang unik.
        🛡️ SAFE VERSION: Handles dict/string/None gracefully
        """
        # 🛡️ Type check and conversion
        if context is None:
            return "default"
        
        if isinstance(context, str):
            # Already a context key string
            return context
        
        if not isinstance(context, dict):
            # Unexpected type, use string representation
            return f"unknown_{str(context)}"
        
        # Normal dict processing
        try:
            hour_category = self.categorize_hour(context.get('hour_of_day', 12))
            key_components = [
                f"weather={context.get('weather', 'unknown')}",
                f"weekend={context.get('is_weekend', False)}",
                f"hour_cat={hour_category}",
                f"season={context.get('season', 'unknown')}"
            ]
            key_str = "_".join(key_components)
            return key_str
        except Exception as e:
            # Fallback if any error
            print(f"⚠️ get_context_key error: {e}, using default")
            return "default"
        

    def categorize_hour(self, hour: int) -> str:  # ← ADD THIS METHOD HERE
        """Categorize hour into time periods"""
        if 5 <= hour < 10:
            return "pagi"
        elif 10 <= hour < 15:
            return "siang"
        elif 15 <= hour < 19:
            return "sore"
        else:
            return "malam"
    
    def select_arm(self, context: Dict[str, Any] = None) -> int:
        """
        IMPROVED: Contextual UCB1 selection selaras dengan tesis
        """
        if context is None:
            return self.select_arm_non_contextual()
        
        context_key = self.get_context_key(context)
        self.initialize_context(context_key)
        
        data = self.context_data[context_key]
        
        # Early exploration: try each arm at least once for this context
        for arm_index in range(self.n_arms):
            if data['counts'][arm_index] == 0:
                print(f"Exploring arm {arm_index} (λ={self.arms[arm_index]:.1f}) for context {context_key}")
                return arm_index
        
        # UCB1 selection after initial exploration
        avg_rewards = data['rewards'] / np.maximum(data['counts'], 1)
        safe_total_pulls = max(data['total_pulls'], 1)
        
        exploration_bonus = self.c * np.sqrt(
            math.log(safe_total_pulls) / np.maximum(data['counts'], 1)
        )
        
        ucb_scores = avg_rewards + exploration_bonus
        selected_arm = np.argmax(ucb_scores)
        
        print(f"UCB selected arm {selected_arm} (λ={self.arms[selected_arm]:.1f}) for context {context_key}")
        return selected_arm
    
    def update_reward(self, arm_index: int, reward: float, context: Dict[str, Any] = None):
        """
        IMPROVED: Update reward dengan consistent context handling
        """
        if not (0 <= arm_index < self.n_arms):
            print(f"Invalid arm_index: {arm_index}")
            return
        
        if context is None:
            print("No context provided for reward update")
            return
        
        context_key = self.get_context_key(context)
        
        if context_key not in self.context_data:
            self.initialize_context(context_key)
        
        data = self.context_data[context_key]
        data['counts'][arm_index] += 1
        data['rewards'][arm_index] += reward
        data['total_pulls'] += 1
        
        lambda_value = self.get_lambda_value(arm_index)
        avg_reward = data['rewards'][arm_index] / data['counts'][arm_index]
        
        print(f"Reward updated: arm {arm_index} (λ={lambda_value:.1f}) "
             f"got reward {reward:.3f}, avg now {avg_reward:.3f} "
             f"for context {context_key}")
        
        # Save state after update
        self.save_state()

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
        self.save_state()
        print("🔄 MAB state has been reset")

    def save_state(self):
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

    def load_state(self):
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
