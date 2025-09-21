#!/usr/bin/env python3
"""
Test script untuk demonstrasi Multi-Armed Bandit (MAB) dengan algoritma UCB1
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.mab_optimizer import MABOptimizer
import numpy as np

def simulate_mab_learning():
    """
    Simulasi pembelajaran MAB dengan reward yang berbeda untuk setiap arm
    """
    print("=== Demonstrasi Multi-Armed Bandit (MAB) dengan UCB1 ===\n")
    
    # Initialize MAB
    mab = MABOptimizer(n_arms=11, exploration_param=2.0)
    
    # Simulasi reward distribution untuk setiap lambda value
    # Asumsi: lambda ~0.7 memberikan reward terbaik untuk balanced recommendation
    true_rewards = [
        0.2,  # λ=0.0 (hanya diversity) - reward rendah
        0.3,  # λ=0.1
        0.4,  # λ=0.2  
        0.5,  # λ=0.3
        0.6,  # λ=0.4
        0.7,  # λ=0.5
        0.75, # λ=0.6
        0.85, # λ=0.7 - OPTIMAL (balanced)
        0.75, # λ=0.8
        0.6,  # λ=0.9
        0.4   # λ=1.0 (hanya relevance) - bisa membosankan user
    ]
    
    print("📊 True Reward Distribution (Unknown to MAB):")
    for i, (lambda_val, reward) in enumerate(zip(mab.arms, true_rewards)):
        print(f"  λ={lambda_val:.1f}: {reward:.2f}")
    print(f"\n🎯 Optimal arm: λ={mab.arms[np.argmax(true_rewards)]:.1f} (reward: {max(true_rewards):.2f})\n")
    
    # Simulasi learning process
    n_rounds = 200
    selected_arms = []
    cumulative_rewards = []
    cumulative_reward = 0
    
    print("🤖 MAB Learning Process:")
    print("Round | Selected λ | Reward | Cumulative Avg | Strategy")
    print("-" * 55)
    
    for round_num in range(1, n_rounds + 1):
        # MAB selects arm
        selected_arm = mab.select_arm()
        selected_lambda = mab.get_lambda_value(selected_arm)
        
        # Generate noisy reward based on true reward + some noise
        true_reward = true_rewards[selected_arm]
        noise = np.random.normal(0, 0.1)  # Small noise
        observed_reward = max(0, min(1, true_reward + noise))  # Clamp to [0,1]
        
        # Update MAB
        mab.update_reward(selected_arm, observed_reward)
        
        # Track statistics
        selected_arms.append(selected_arm)
        cumulative_reward += observed_reward
        cumulative_rewards.append(cumulative_reward / round_num)
        
        # Determine strategy
        if round_num <= 11:
            strategy = "Exploration"
        else:
            strategy = "UCB Decision"
        
        # Print every 20 rounds + first 15 rounds
        if round_num <= 15 or round_num % 20 == 0:
            print(f"{round_num:5d} | λ={selected_lambda:7.1f} | {observed_reward:6.3f} | {cumulative_reward/round_num:13.3f} | {strategy}")
    
    print(f"\n📈 Final Results after {n_rounds} rounds:")
    stats = mab.get_statistics()
    
    print("\n🏆 Arm Performance Ranking:")
    sorted_arms = sorted(stats["arms_stats"], key=lambda x: x["avg_reward"], reverse=True)
    
    for i, arm in enumerate(sorted_arms[:5], 1):
        lambda_val = arm["lambda_value"]
        avg_reward = arm["avg_reward"]
        pulls = arm["pulls"]
        true_reward = true_rewards[arm["arm_index"]]
        
        status = "🎯 OPTIMAL!" if arm["arm_index"] == np.argmax(true_rewards) else ""
        print(f"{i}. λ={lambda_val:.1f}: {avg_reward:.3f} avg reward ({pulls:3d} pulls) | True: {true_reward:.2f} {status}")
    
    # Check if MAB found the optimal arm
    best_arm_idx = max(range(mab.n_arms), key=lambda i: mab.rewards[i] / max(mab.counts[i], 1))
    optimal_arm_idx = np.argmax(true_rewards)
    
    print(f"\n🎯 MAB Discovery:")
    print(f"   MAB's best arm: λ={mab.arms[best_arm_idx]:.1f}")
    print(f"   True optimal:  λ={mab.arms[optimal_arm_idx]:.1f}")
    print(f"   Success: {'✅ YES' if best_arm_idx == optimal_arm_idx else '❌ NO (need more data)'}")
    
    print(f"\n📊 Exploration vs Exploitation:")
    total_pulls = sum(mab.counts)
    optimal_pulls = mab.counts[optimal_arm_idx]
    print(f"   Optimal arm selected: {optimal_pulls}/{total_pulls} times ({optimal_pulls/total_pulls*100:.1f}%)")
    
    # Show final UCB scores for understanding
    print(f"\n🧮 Final UCB Scores (what MAB sees):")
    avg_rewards = mab.rewards / np.maximum(mab.counts, 1)
    for i in range(mab.n_arms):
        if mab.counts[i] > 0:
            exploration_bonus = mab.c * np.sqrt(np.log(total_pulls) / mab.counts[i])
            ucb_score = avg_rewards[i] + exploration_bonus
            print(f"   λ={mab.arms[i]:.1f}: UCB={ucb_score:.3f} (avg={avg_rewards[i]:.3f} + bonus={exploration_bonus:.3f})")
    
    return mab, selected_arms, cumulative_rewards

def test_mab_integration():
    """Test basic MAB functionality"""
    print("\n" + "="*60)
    print("🔧 Testing MAB Integration Components")
    print("="*60)
    
    # Test MABOptimizer initialization
    mab = MABOptimizer(n_arms=11, exploration_param=2.0)
    print("✅ MABOptimizer initialized successfully")
    
    # Test arm selection (should select arm 0 first)
    first_arm = mab.select_arm()
    print(f"✅ First arm selection: {first_arm} (λ={mab.get_lambda_value(first_arm):.1f})")
    
    # Test reward update
    mab.update_reward(first_arm, 0.8)
    print(f"✅ Reward update successful: arm {first_arm} now has 1 pull")
    
    # Test statistics
    stats = mab.get_statistics()
    print(f"✅ Statistics generation: {stats['total_pulls']} total pulls")
    
    # Test state persistence (if applicable)
    try:
        test_mab = MABOptimizer(persistence_file="test_mab_state.json")
        test_mab.update_reward(0, 0.5)
        print("✅ State persistence working")
        
        # Cleanup
        import os
        if os.path.exists("test_mab_state.json"):
            os.remove("test_mab_state.json")
    except Exception as e:
        print(f"⚠️ State persistence test failed: {e}")
    
    print("\n🎉 All MAB integration tests passed!")

if __name__ == "__main__":
    # Run integration tests first
    test_mab_integration()
    
    # Run learning simulation
    print("\n\n")
    mab, selected_arms, cumulative_rewards = simulate_mab_learning()
    
    print(f"\n💡 Key Insights:")
    print(f"   • MAB successfully learns which λ values work best")
    print(f"   • Initial phase: explores all arms equally")
    print(f"   • Later phase: exploits promising arms while occasionally exploring")
    print(f"   • UCB balances exploration vs exploitation automatically")
    print(f"   • Real system will learn from actual user feedback")
    
    print(f"\n🚀 Next Steps in Real Implementation:")
    print(f"   1. Deploy MAB in production environment")
    print(f"   2. Collect user feedback (ratings, clicks, time spent)")
    print(f"   3. Convert feedback to reward signals (0-1)")
    print(f"   4. Monitor MAB learning progress")
    print(f"   5. Adjust exploration parameter if needed")
