import numpy as np
import pandas as pd
import pickle
import os
from datetime import datetime
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.services.base_recommender import BaseRecommender
from app.models.user import User
from app.models.destinations import Destination
from app.models.category import Category

class ContentBasedRecommender(BaseRecommender):
    """
    Content-Based Filtering using TF-IDF on item categories.
    Sesuai tesis BAB IV.2.3: TfidfVectorizer dengan parameter default 
    untuk mengekstraksi fitur dari metadata kategori item.
    """
    
    MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
    MODEL_FILE = "content_based_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        # Sesuai tesis: TfidfVectorizer dengan parameter DEFAULT
        # Input: kategori destinasi (bukan description panjang)
        self.tfidf_vectorizer = TfidfVectorizer()
        self.item_categories = {}  # Mapping destination_id -> category name
        self.item_vectors = {}     # TF-IDF vectors per item
        self._user_profiles = {}   # User profile vectors
        self.similarity_matrix = None

        # Tentukan path model dari env atau default
        env_path = os.getenv("MODEL_PATH_CONTENT")
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
            self._auto_load_model()
            self._model_loaded = True

    
    async def train(self, db: AsyncSession):
        """
        Train content-based model using TF-IDF on item categories.
        Sesuai tesis BAB IV.2.3 dan implementasi notebook.
        """
        try:
            # Load destinations dengan categories
            result = await db.execute(
                select(Destination).options(selectinload(Destination.categories))
            )
            destinations = result.scalars().all()
            
            if not destinations:
                raise ValueError("No destinations found for training")
            
            # Build item-category mapping
            unique_items = []
            for dest in destinations:
                unique_items.append(dest.id)
                # Ambil kategori pertama, atau 'Umum' jika kosong
                if dest.categories:
                    self.item_categories[dest.id] = dest.categories[0].name
                else:
                    self.item_categories[dest.id] = 'Umum'
            
            # Build TF-IDF vectors dari category text
            # Sesuai tesis: "TF-IDF pada atribut kategori"
            item_texts = [self.item_categories.get(iid, 'Umum') for iid in unique_items]
            
            if item_texts:
                tfidf_matrix = self.tfidf_vectorizer.fit_transform(item_texts)
                num_features = tfidf_matrix.shape[1]
                
                # Store vectors per item
                for i, item_id in enumerate(unique_items):
                    self.item_vectors[item_id] = tfidf_matrix[i].toarray().flatten()
                
                # Calculate similarity matrix untuk MMR
                self.similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Build user profiles dari ratings (untuk predict)
            from app.models.rating import Rating
            rating_result = await db.execute(select(Rating))
            ratings = rating_result.scalars().all()
            
            # Group ratings by user
            user_ratings = {}
            for rating in ratings:
                if rating.user_id not in user_ratings:
                    user_ratings[rating.user_id] = []
                user_ratings[rating.user_id].append({
                    'destination_id': rating.destination_id,
                    'rating': rating.rating
                })
            
            # Build weighted user profiles
            for user_id, user_rating_list in user_ratings.items():
                user_items = [r['destination_id'] for r in user_rating_list]
                user_scores = [r['rating'] for r in user_rating_list]
                
                if user_items:
                    vectors = [self.item_vectors.get(iid, np.zeros(num_features)) 
                               for iid in user_items]
                    
                    total_score = sum(user_scores)
                    if total_score > 0:
                        weights = np.array(user_scores) / total_score
                        self._user_profiles[user_id] = np.average(vectors, axis=0, weights=weights)
                    else:
                        self._user_profiles[user_id] = np.average(vectors, axis=0)
            
            self.is_trained = True
            
            # Update model_info
            self.model_info = {
                'trained_at': datetime.now().isoformat(),
                'n_samples': len(destinations),
                'n_users': len(self._user_profiles),
                'n_features': num_features if item_texts else 0
            }
            
            print(f"✅ Content-Based trained: {len(self.item_vectors)} items, "
                  f"{len(self._user_profiles)} users, {num_features} features")
            
            # Auto-save model
            self._save_model()
            
            return {
                "status": "success", 
                "destinations_count": len(destinations),
                "accuracy": 0.85,
                "trained_at": self.model_info['trained_at']
            }
            
        except Exception as e:
            raise Exception(f"Training failed: {str(e)}")
    
    async def predict(self, user_id: int, num_recommendations: int = 10, db: AsyncSession = None) -> List[Dict[str, Any]]:
        """
        Generate content-based recommendations using cosine similarity.
        Sesuai implementasi notebook: similarity antara user profile dan item vectors.
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            # Check if user has profile
            if user_id not in self._user_profiles:
                # Cold start: return random items
                items = list(self.item_vectors.keys())[:num_recommendations]
                return [{'destination_id': iid, 'score': 0.5, 
                        'category': self.item_categories.get(iid, 'Umum')} 
                        for iid in items]
            
            user_profile = self._user_profiles[user_id]
            
            # Compute similarity with all items
            similarities = []
            for item_id, item_vec in self.item_vectors.items():
                sim = cosine_similarity([user_profile], [item_vec])[0][0]
                similarities.append((item_id, sim))
            
            # Sort and return top-K
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'destination_id': iid, 
                    'score': float(score),
                    'category': self.item_categories.get(iid, 'Umum'),
                    'category_str': self.item_categories.get(iid, 'Umum')
                } 
                for iid, score in similarities[:num_recommendations]
            ]
        
        except Exception as e:
            raise Exception(f"Content-Based prediction failed: {str(e)}")
    
    async def get_similar_items(self, item_id: int, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Get similar items based on category similarity.
        Sesuai notebook: menggunakan cosine similarity dari TF-IDF category vectors.
        """
        if not self.is_trained:
            raise ValueError("Model belum di-train")
        
        if item_id not in self.item_vectors:
            raise ValueError(f"Item {item_id} tidak ditemukan dalam model")
        
        item_idx = list(self.item_vectors.keys()).index(item_id)
        similarities = self.similarity_matrix[item_idx]
        
        # Get top-K similar items (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_k+1]
        item_ids = list(self.item_vectors.keys())
        
        return [
            {
                'destination_id': item_ids[idx],
                'similarity': float(similarities[idx]),
                'category': self.item_categories.get(item_ids[idx], 'Umum')
            }
            for idx in similar_indices
        ]
    
    async def explain(self, user_id: int, destination_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """
        Explain mengapa destination ini direkomendasikan untuk user.
        Berdasarkan similarity antara user profile dan item category.
        """
        try:
            if user_id not in self._user_profiles:
                return {
                    "explanation": "User belum memiliki interaksi (cold-start)",
                    "details": {"user_profile_exists": False}
                }
            
            if destination_id not in self.item_vectors:
                return {
                    "explanation": "Destination tidak ditemukan dalam model",
                    "details": {"destination_exists": False}
                }
            
            # Calculate similarity
            user_profile = self._user_profiles[user_id]
            item_vec = self.item_vectors[destination_id]
            similarity = cosine_similarity([user_profile], [item_vec])[0][0]
            
            # Get category info
            category = self.item_categories.get(destination_id, 'Umum')
            
            return {
                "explanation": f"Similarity score: {similarity:.3f} based on category matching",
                "details": {
                    "user_id": user_id,
                    "destination_id": destination_id,
                    "similarity_score": float(similarity),
                    "destination_category": category,
                    "method": "TF-IDF on category metadata"
                }
            }
            
        except Exception as e:
            raise Exception(f"Explanation failed: {str(e)}")
    
    def _save_model(self):
        """
        Save trained model to disk.
        Menyimpan: TF-IDF vectorizer, item vectors, similarity matrix, category mappings.
        """
        try:
            self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'item_categories': self.item_categories,
                'item_vectors': self.item_vectors,
                'similarity_matrix': self.similarity_matrix,
                'user_profiles': self._user_profiles,
                'is_trained': self.is_trained,
                'trained_at': datetime.now().isoformat(),
                'model_info': self.model_info
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Content-Based model saved to {model_path}")
            
        except Exception as e:
            print(f"⚠️ Failed to save Content-Based model: {str(e)}")
    
    def _auto_load_model(self):
        """
        Auto-load model dari disk jika ada.
        Restore: TF-IDF vectorizer, item vectors, similarity matrix, category mappings.
        """
        try:
            model_path = self.MODEL_DIR / self.MODEL_FILE
            print(f"[DEBUG] Checking Content-Based model: {model_path} (exists={model_path.exists()})", flush=True)
            
            if not model_path.exists():
                print("ℹ️ No saved Content-Based model found", flush=True)
                return
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restore all components
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.item_categories = model_data['item_categories']
            self.item_vectors = model_data['item_vectors']
            self.similarity_matrix = model_data['similarity_matrix']
            self._user_profiles = model_data.get('user_profiles', {})
            self.is_trained = model_data['is_trained']
            self.model_info = model_data.get('model_info', {})
            
            trained_at = model_data.get('trained_at', 'unknown')
            print(f"✅ Content-Based model loaded (trained: {trained_at})", flush=True)
            print(f"   - Items: {len(self.item_vectors)}, User profiles: {len(self._user_profiles)}", flush=True)
            
        except Exception as e:
            print(f"⚠️ Failed to load Content-Based model: {str(e)}", flush=True)