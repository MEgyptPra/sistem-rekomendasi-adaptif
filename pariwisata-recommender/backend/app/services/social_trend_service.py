"""
Social Trend & Viral Detection Service
Mengambil data trending destinations dari user interactions
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import Counter

class SocialTrendService:
    """
    Deteksi trending destinations berdasarkan:
    1. View count (dari incremental learner)
    2. Click patterns (recent surge)
    3. Rating velocity (banyak rating dalam waktu singkat)
    4. Favorite velocity (banyak favorite baru)
    5. Social media mentions (future: API integration)
    """
    
    CACHE_DIR = Path("data/cache")
    TREND_CACHE_FILE = CACHE_DIR / "social_trends.json"
    CACHE_DURATION = 300  # 5 minutes
    
    # Thresholds untuk viral detection
    VIRAL_VIEW_THRESHOLD = 100  # views in 24h
    TRENDING_VIEW_THRESHOLD = 50  # views in 24h
    NORMAL_VIEW_THRESHOLD = 20
    
    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.incremental_scores = self._load_incremental_scores()
    
    def _load_incremental_scores(self) -> Dict[int, Dict]:
        """Load destination scores from incremental learner"""
        try:
            scores_file = Path("data/cache/destination_scores.json")
            if scores_file.exists():
                with open(scores_file, 'r') as f:
                    data = json.load(f)
                return data.get("destination_scores", {})
        except Exception as e:
            print(f"⚠️ Failed to load incremental scores: {e}")
        return {}
    
    def get_trending_status(self, destination_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get trending status for specific destination or overall trends
        
        Returns:
            {
                "overall_trend": "viral" | "trending" | "normal",
                "trending_destinations": [dest_ids],
                "viral_destinations": [dest_ids],
                "trend_score": 0-100
            }
        """
        # Try cache first
        cached = self._load_trend_cache()
        if cached:
            if destination_id:
                return self._get_destination_trend(destination_id, cached)
            return cached
        
        # Calculate new trends
        trends = self._calculate_trends()
        self._save_trend_cache(trends)
        
        if destination_id:
            return self._get_destination_trend(destination_id, trends)
        
        return trends
    
    def _calculate_trends(self) -> Dict[str, Any]:
        """Calculate trending destinations based on recent activity"""
        if not self.incremental_scores:
            return {
                "overall_trend": "normal",
                "trending_destinations": [],
                "viral_destinations": [],
                "top_trending": [],
                "trend_scores": {},
                "calculated_at": datetime.now().isoformat()
            }
        
        # Convert to list for sorting
        dest_scores = []
        for dest_id_str, score_data in self.incremental_scores.items():
            try:
                dest_id = int(dest_id_str)
                
                # Calculate trend score based on multiple factors
                view_score = score_data.get("view_count", 0)
                click_score = score_data.get("click_count", 0) * 2
                rating_score = score_data.get("rating_count", 0) * 5
                favorite_score = score_data.get("favorite_count", 0) * 3
                
                trend_score = view_score + click_score + rating_score + favorite_score
                
                # Check recency (destinations with recent activity score higher)
                last_interaction = score_data.get("last_interaction")
                if last_interaction:
                    try:
                        last_time = datetime.fromisoformat(last_interaction)
                        hours_ago = (datetime.now() - last_time).total_seconds() / 3600
                        
                        # Boost score for recent activity (within 24h)
                        if hours_ago < 24:
                            recency_boost = (24 - hours_ago) / 24 * 50
                            trend_score += recency_boost
                    except:
                        pass
                
                dest_scores.append({
                    "destination_id": dest_id,
                    "trend_score": round(trend_score, 2),
                    "views": view_score,
                    "clicks": click_score // 2,
                    "ratings": rating_score // 5,
                    "favorites": favorite_score // 3
                })
            except:
                continue
        
        # Sort by trend score
        dest_scores.sort(key=lambda x: x["trend_score"], reverse=True)
        
        # Classify destinations
        viral_destinations = []
        trending_destinations = []
        
        for dest in dest_scores:
            if dest["views"] >= self.VIRAL_VIEW_THRESHOLD:
                viral_destinations.append(dest["destination_id"])
            elif dest["views"] >= self.TRENDING_VIEW_THRESHOLD:
                trending_destinations.append(dest["destination_id"])
        
        # Overall trend status
        if len(viral_destinations) > 5:
            overall_trend = "viral"
        elif len(trending_destinations) > 10:
            overall_trend = "trending"
        else:
            overall_trend = "normal"
        
        # Top 10 trending
        top_trending = dest_scores[:10]
        
        # Create trend_scores dict
        trend_scores = {
            str(dest["destination_id"]): dest["trend_score"] 
            for dest in dest_scores
        }
        
        return {
            "overall_trend": overall_trend,
            "trending_destinations": trending_destinations[:20],  # Top 20
            "viral_destinations": viral_destinations[:10],  # Top 10 viral
            "top_trending": top_trending,
            "trend_scores": trend_scores,
            "total_destinations": len(dest_scores),
            "calculated_at": datetime.now().isoformat()
        }
    
    def _get_destination_trend(self, destination_id: int, trends: Dict) -> Dict[str, Any]:
        """Get trend status for specific destination"""
        dest_id_str = str(destination_id)
        
        is_viral = destination_id in trends["viral_destinations"]
        is_trending = destination_id in trends["trending_destinations"]
        
        trend_score = trends["trend_scores"].get(dest_id_str, 0)
        
        # Find rank in top_trending
        rank = None
        for idx, dest in enumerate(trends["top_trending"], 1):
            if dest["destination_id"] == destination_id:
                rank = idx
                break
        
        if is_viral:
            status = "viral"
            badge = "🔥"
        elif is_trending:
            status = "trending"
            badge = "📈"
        else:
            status = "normal"
            badge = None
        
        return {
            "destination_id": destination_id,
            "status": status,
            "badge": badge,
            "trend_score": trend_score,
            "rank": rank,
            "overall_trend": trends["overall_trend"],
            "calculated_at": trends["calculated_at"]
        }
    
    def _load_trend_cache(self) -> Optional[Dict[str, Any]]:
        """Load cached trend data if valid"""
        try:
            if self.TREND_CACHE_FILE.exists():
                with open(self.TREND_CACHE_FILE, 'r') as f:
                    cached = json.load(f)
                
                cached_at = datetime.fromisoformat(cached["calculated_at"])
                age_seconds = (datetime.now() - cached_at).total_seconds()
                
                if age_seconds < self.CACHE_DURATION:
                    return cached
                else:
                    print(f"⏰ Trend cache expired ({age_seconds:.0f}s > {self.CACHE_DURATION}s)")
        except Exception as e:
            print(f"⚠️ Failed to load trend cache: {e}")
        
        return None
    
    def _save_trend_cache(self, trends: Dict[str, Any]):
        """Save trend data to cache"""
        try:
            with open(self.TREND_CACHE_FILE, 'w') as f:
                json.dump(trends, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save trend cache: {e}")
    
    def get_trending_boost(self, destination_id: int) -> float:
        """
        Get trending boost multiplier for destination
        
        Returns:
            float: 1.0 (normal), 1.5 (trending), 2.0 (viral)
        """
        trends = self.get_trending_status()
        
        if destination_id in trends["viral_destinations"]:
            return 2.0
        elif destination_id in trends["trending_destinations"]:
            return 1.5
        else:
            return 1.0
    
    def get_top_trending(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top trending destinations"""
        trends = self.get_trending_status()
        return trends["top_trending"][:limit]
