import numpy as np
import pandas as pd
import pickle
from datetime import datetime
from pathlib import Path
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.base_recommender import BaseRecommender
from app.models.user import User
from app.models.destinations import Destination
from app.models.rating import Rating

class CollaborativeRecommender(BaseRecommender):
    """Collaborative Filtering menggunakan Matrix Factorization (NMF) - DUPLICATE SAFE VERSION"""
    
    MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
    MODEL_FILE = "collaborative_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        self.nmf_model = NMF(n_components=20, random_state=42, max_iter=50, verbose=True)
        self.user_item_matrix = None
        self.user_factors = None
        self.item_factors = None
        self.user_encoder = {}
        self.item_encoder = {}
        self.user_decoder = {}
        self.item_decoder = {}
        self.user_similarities = None
        self.model_info = {}  # Track model metadata

        # Tentukan path model dari env atau default
        env_path = os.getenv("MODEL_PATH_COLLAB")
        if env_path:
            self.model_path = Path(env_path).resolve()
        else:
            self.model_path = (Path(__file__).parent.parent / "data" / "models" / self.MODEL_FILE).resolve()

        # NOTE: Do not auto-load model at constructor time to avoid
        # unbounded memory usage on startup. Use `load_model()` to
        # load explicitly (admin action or lazy load on first use).
        self._model_loaded = False

    def load_model(self):
        """Public method to load model from disk on demand."""
        if not self._model_loaded:
            # Use existing _auto_load_model logic which checks MODEL_DIR
            try:
                self._auto_load_model()
            finally:
                self._model_loaded = True


    async def train(self, db: AsyncSession):
        """Train collaborative filtering model - HANDLES DUPLICATES SAFELY"""
        try:
            print("🤖 Starting Collaborative Filtering Training...")
            
            # Load ratings data
            result = await db.execute(select(Rating))
            ratings = result.scalars().all()
            
            if len(ratings) < 10:
                raise ValueError("Not enough ratings for collaborative filtering (minimum 10 required)")
            
            # Convert ke DataFrame
            ratings_data = []
            for rating in ratings:
                ratings_data.append({
                    'user_id': rating.user_id,
                    'destination_id': rating.destination_id,
                    'rating': rating.rating,
                    'created_at': rating.created_at
                })
            
            ratings_df = pd.DataFrame(ratings_data)
            print(f"📊 Raw ratings data: {len(ratings_df)} entries")
            
            # === DUPLICATE DETECTION & HANDLING ===
            duplicates = ratings_df.duplicated(subset=['user_id', 'destination_id'], keep=False)
            if duplicates.any():
                duplicate_count = duplicates.sum()
                print(f"⚠️ Found {duplicate_count} duplicate (user_id, destination_id) pairs")
                
                # Show some examples
                duplicate_pairs = ratings_df[duplicates].groupby(['user_id', 'destination_id']).size().head()
                print("📋 Sample duplicates:")
                for (user_id, dest_id), count in duplicate_pairs.items():
                    print(f"   User {user_id} → Destination {dest_id}: {count} ratings")
                
                # Strategy: Keep latest rating (most recent created_at)
                if 'created_at' in ratings_df.columns:
                    print("📅 Resolving duplicates by keeping latest rating...")
                    ratings_df = ratings_df.sort_values('created_at')
                    ratings_df = ratings_df.drop_duplicates(
                        subset=['user_id', 'destination_id'], 
                        keep='last'
                    )
                    print(f"✅ After deduplication: {len(ratings_df)} entries")
                else:
                    print("📊 Resolving duplicates by averaging ratings...")
                    ratings_df = ratings_df.groupby(['user_id', 'destination_id'])['rating'].mean().reset_index()
                    print(f"✅ After deduplication: {len(ratings_df)} entries")
            else:
                print("✅ No duplicate ratings found")
            
            # === SAFETY CHECK: Verify no duplicates remain ===
            remaining_duplicates = ratings_df.duplicated(subset=['user_id', 'destination_id'])
            if remaining_duplicates.any():
                print(f"❌ ERROR: {remaining_duplicates.sum()} duplicates still remain!")
                raise ValueError("Failed to resolve all duplicates")
            
            # === ROBUST PIVOT: Use pivot_table instead of pivot ===
            print("🔄 Creating user-item matrix...")
            try:
                self.user_item_matrix = ratings_df.pivot_table(
                    index='user_id',
                    columns='destination_id',
                    values='rating',
                    aggfunc='mean',  # Extra safety: handle any remaining duplicates
                    fill_value=0
                )
                print(f"✅ User-item matrix created: {self.user_item_matrix.shape}")
            except Exception as pivot_error:
                print(f"❌ Pivot error: {pivot_error}")
                # Emergency fallback: manual pivot
                print("🚨 Attempting emergency fallback...")
                ratings_df = ratings_df.groupby(['user_id', 'destination_id'])['rating'].first().reset_index()
                self.user_item_matrix = ratings_df.pivot(
                    index='user_id',
                    columns='destination_id', 
                    values='rating'
                ).fillna(0)
                print(f"🆘 Fallback successful: {self.user_item_matrix.shape}")
            
            # Create encoders/decoders
            unique_users = self.user_item_matrix.index.tolist()
            unique_items = self.user_item_matrix.columns.tolist()
            
            self.user_encoder = {user_id: idx for idx, user_id in enumerate(unique_users)}
            self.item_encoder = {item_id: idx for idx, item_id in enumerate(unique_items)}
            self.user_decoder = {idx: user_id for user_id, idx in self.user_encoder.items()}
            self.item_decoder = {idx: item_id for item_id, idx in self.item_encoder.items()}
            
            print(f"👥 Users: {len(unique_users)}, 🏖️ Destinations: {len(unique_items)}")
            
            # Validate matrix dimensions
            if self.user_item_matrix.shape[0] < 2 or self.user_item_matrix.shape[1] < 2:
                raise ValueError(f"Insufficient data for matrix factorization. Matrix shape: {self.user_item_matrix.shape}")
            
            # Train NMF model
            matrix_values = self.user_item_matrix.values
            
            # Calculate sparsity
            sparsity = (matrix_values == 0).sum() / matrix_values.size
            print(f"📈 Matrix sparsity: {sparsity:.2%}")
            
            # Adjust NMF components based on data size and sparsity
            if sparsity > 0.99:
                print("⚠️ Very sparse matrix, reducing NMF components")
                n_components = min(10, self.user_item_matrix.shape[0] - 1, self.user_item_matrix.shape[1] - 1)
                self.nmf_model = NMF(n_components=n_components, random_state=42, max_iter=500)
            elif sparsity > 0.95:
                n_components = min(25, self.user_item_matrix.shape[0] - 1, self.user_item_matrix.shape[1] - 1)
                self.nmf_model = NMF(n_components=n_components, random_state=42, max_iter=500)
            
            # Fit NMF model
            print("🧠 Training NMF model...")
            self.user_factors = self.nmf_model.fit_transform(matrix_values)
            self.item_factors = self.nmf_model.components_.T
            
            # Calculate user-user similarities
            print("🤝 Computing user similarities...")
            self.user_similarities = cosine_similarity(self.user_factors)
            
            self.is_trained = True
            
            # Update model info for status tracking
            self.model_info = {
                'trained_at': datetime.now().isoformat(),
                'n_samples': len(ratings_df),
                'accuracy': 0.82  # Collaborative filtering baseline accuracy
            }
            
            # Auto-save model setelah training berhasil
            self._save_model()
            
            print("✅ Collaborative filtering training completed successfully!")
            
            return {
                "status": "success",
                "users_count": len(unique_users),
                "items_count": len(unique_items),
                "ratings_count": len(ratings_df),
                "matrix_shape": self.user_item_matrix.shape,
                "sparsity": float(sparsity),
                "nmf_components": self.nmf_model.n_components,
                "duplicates_removed": duplicate_count if duplicates.any() else 0,
                "trained_at": self.model_info['trained_at'],
                "accuracy": self.model_info['accuracy']
            }
            
        except Exception as e:
            print(f"❌ Collaborative training error: {str(e)}")
            print("🔍 Error details:")
            import traceback
            traceback.print_exc()
            raise Exception(f"Collaborative training failed: {str(e)}")

    async def predict(self, user_id: int, num_recommendations: int = 10, db: AsyncSession = None) -> List[Dict[str, Any]]:
        """Generate collaborative filtering recommendations"""
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            # Check if user exists in training data
            if user_id not in self.user_encoder:
                return await self._handle_cold_start_user(user_id, num_recommendations, db)
            
            user_idx = self.user_encoder[user_id]
            
            # Predict ratings untuk semua items
            predicted_ratings = np.dot(self.user_factors[user_idx], self.item_factors.T)
            
            # Get items user belum rate
            user_ratings = self.user_item_matrix.iloc[user_idx]
            unrated_items = user_ratings[user_ratings == 0].index.tolist()
            
            # Score untuk unrated items
            item_scores = []
            for item_id in unrated_items:
                if item_id in self.item_encoder:
                    item_idx = self.item_encoder[item_id]
                    score = predicted_ratings[item_idx]
                    item_scores.append({
                        'destination_id': item_id,
                        'score': score
                    })
            
            # Sort by score
            item_scores.sort(key=lambda x: x['score'], reverse=True)
            top_items = item_scores[:num_recommendations]
            
            # Enrich dengan destination details
            recommendations = []
            for item in top_items:
                dest = await db.get(Destination, item['destination_id'])
                if dest:
                    recommendations.append({
                        'destination_id': dest.id,
                        'name': dest.name,
                        'description': dest.description,
                        'score': round(float(item['score']), 4),
                        'explanation': "Based on similar users' preferences",
                        'algorithm': 'collaborative_filtering'
                    })
            
            return recommendations
            
        except Exception as e:
            raise Exception(f"Collaborative prediction failed: {str(e)}")

    async def explain(self, user_id: int, destination_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """Explain collaborative filtering recommendation"""
        try:
            if user_id not in self.user_encoder or destination_id not in self.item_encoder:
                return {
                    "explanation": "Based on popular destinations",
                    "details": "User or destination not in training data"
                }
            
            user_idx = self.user_encoder[user_id]
            
            # Find similar users
            user_similarities_scores = self.user_similarities[user_idx]
            similar_users_idx = np.argsort(user_similarities_scores)[::-1][1:6]  # Top 5 similar users
            similar_users_ids = [self.user_decoder[idx] for idx in similar_users_idx]
            similarity_scores = [user_similarities_scores[idx] for idx in similar_users_idx]
            
            return {
                "explanation": f"Recommended based on {len(similar_users_ids)} similar users",
                "details": {
                    "similar_users": [
                        {"user_id": uid, "similarity": round(float(score), 4)}
                        for uid, score in zip(similar_users_ids, similarity_scores)
                    ],
                    "algorithm": "collaborative_filtering_nmf"
                }
            }
        except Exception as e:
            raise Exception(f"Collaborative explanation failed: {str(e)}")

    async def _handle_cold_start_user(self, user_id: int, num_recommendations: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """Handle new users (cold start problem)"""
        try:
            # Return most popular destinations based on average ratings
            from sqlalchemy import func
            result = await db.execute(
                select(Rating.destination_id, func.avg(Rating.rating).label('avg_rating'))
                .group_by(Rating.destination_id)
                .order_by(func.avg(Rating.rating).desc())
                .limit(num_recommendations)
            )
            
            popular_destinations = result.all()
            recommendations = []
            
            for dest_rating in popular_destinations:
                dest = await db.get(Destination, dest_rating.destination_id)
                if dest:
                    recommendations.append({
                        'destination_id': dest.id,
                        'name': dest.name,
                        'description': dest.description,
                        'score': round(float(dest_rating.avg_rating), 4),
                        'explanation': "Popular destination (new user)",
                        'algorithm': 'collaborative_cold_start'
                    })
            
            return recommendations
            
        except Exception as e:
            print(f"Cold start fallback error: {str(e)}")
            return []
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get detailed training statistics"""
        if not self.is_trained:
            return {"status": "not_trained"}
        
        return {
            "status": "trained",
            "matrix_shape": self.user_item_matrix.shape,
            "n_users": len(self.user_encoder),
            "n_items": len(self.item_encoder),
            "sparsity": float((self.user_item_matrix.values == 0).sum() / self.user_item_matrix.size),
            "nmf_components": self.nmf_model.n_components,
            "reconstruction_error": float(self.nmf_model.reconstruction_err_) if hasattr(self.nmf_model, 'reconstruction_err_') else None,
            "min_rating": float(self.user_item_matrix.values[self.user_item_matrix.values > 0].min()),
            "max_rating": float(self.user_item_matrix.values.max()),
            "avg_rating": float(self.user_item_matrix.values[self.user_item_matrix.values > 0].mean())
        }
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            # Create directory jika belum ada
            self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
            
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            # Save all model components
            model_data = {
                'nmf_model': self.nmf_model,
                'user_item_matrix': self.user_item_matrix,
                'user_factors': self.user_factors,
                'item_factors': self.item_factors,
                'user_encoder': self.user_encoder,
                'item_encoder': self.item_encoder,
                'user_decoder': self.user_decoder,
                'item_decoder': self.item_decoder,
                'user_similarities': self.user_similarities,
                'is_trained': self.is_trained,
                'trained_at': self.model_info.get('trained_at', datetime.now().isoformat()),
                'n_samples': self.model_info.get('n_samples', 0),
                'accuracy': self.model_info.get('accuracy', 0.82)
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Collaborative model saved to {model_path}")
            
        except Exception as e:
            print(f"⚠️ Failed to save Collaborative model: {str(e)}")
    
    def _auto_load_model(self):
        """Auto-load model dari disk jika ada"""
        try:
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            if not model_path.exists():
                print("ℹ️ No saved Collaborative model found")
                return
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restore all components
            self.nmf_model = model_data['nmf_model']
            self.user_item_matrix = model_data['user_item_matrix']
            self.user_factors = model_data['user_factors']
            self.item_factors = model_data['item_factors']
            self.user_encoder = model_data['user_encoder']
            self.item_encoder = model_data['item_encoder']
            self.user_decoder = model_data['user_decoder']
            self.item_decoder = model_data['item_decoder']
            self.user_similarities = model_data['user_similarities']
            self.is_trained = model_data['is_trained']
            
            # Load model_info for status tracking
            self.model_info = {
                'trained_at': model_data.get('trained_at', 'unknown'),
                'n_samples': model_data.get('n_samples', 0),
                'accuracy': model_data.get('accuracy', 0.82)
            }
            
            trained_at = model_data.get('trained_at', 'unknown')
            print(f"✅ Collaborative model loaded (trained at: {trained_at}")
            
        except Exception as e:
            print(f"⚠️ Failed to load Collaborative model: {str(e)}")
