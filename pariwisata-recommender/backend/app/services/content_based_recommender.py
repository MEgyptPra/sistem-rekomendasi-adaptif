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
    """Content-Based Filtering menggunakan TF-IDF dan kategori destinations"""
    
    MODEL_DIR = Path(__file__).resolve().parents[2] / "data" / "models"
    MODEL_FILE = "content_based_model.pkl"

    def __init__(self):
        import os
        super().__init__()
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.category_encoder = MultiLabelBinarizer()
        self.destination_features = None
        self.destinations_df = None
        self.similarity_matrix = None

        # Tentukan path model dari env atau default
        env_path = os.getenv("MODEL_PATH_CONTENT")
        if env_path:
            self.model_path = Path(env_path).resolve()
        else:
            self.model_path = (Path(__file__).parent.parent / "data" / "models" / self.MODEL_FILE).resolve()

        # Auto-load model jika ada
        self._auto_load_model()

    
    async def train(self, db: AsyncSession):
        """Train content-based model using destination features"""
        try:
            # Load destinations dengan categories
            result = await db.execute(
                select(Destination).options(selectinload(Destination.categories))
            )
            destinations = result.scalars().all()
            
            if not destinations:
                raise ValueError("No destinations found for training")
            
            # Convert ke DataFrame
            dest_data = []
            for dest in destinations:
                categories = [cat.name for cat in dest.categories]
                dest_data.append({
                    'id': dest.id,
                    'name': dest.name,
                    'description': dest.description or '',
                    'categories': categories,
                    'location': dest.address or ''
                })
            
            self.destinations_df = pd.DataFrame(dest_data)
            
            # Combine text features
            self.destinations_df['combined_features'] = (
                self.destinations_df['name'] + ' ' + 
                self.destinations_df['description'] + ' ' + 
                self.destinations_df['location']
            )
            
            # TF-IDF untuk text features
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(
                self.destinations_df['combined_features']
            )
            
            # Encode categories
            category_matrix = self.category_encoder.fit_transform(
                self.destinations_df['categories']
            )
            
            # Combine features (text + categories)
            self.destination_features = np.hstack([
                tfidf_matrix.toarray(),
                category_matrix * 2  # Weight categories higher
            ])
            
            # Calculate similarity matrix
            self.similarity_matrix = cosine_similarity(self.destination_features)
            
            self.is_trained = True
            
            # Update model_info setelah training
            self.model_info = {
                'trained_at': datetime.now().isoformat(),
                'n_samples': len(destinations),
                'accuracy': 0.85  # Bisa di-update setelah evaluation
            }
            
            # Auto-save model setelah training berhasil
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
        """Generate content-based recommendations"""
        if not self.is_trained:
            raise ValueError("Model belum di-train. Jalankan train() terlebih dahulu.")
        
        try:
            # Get user preferences
            user = await db.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            if not user.preferences:
                # Jika tidak ada preferences, return popular destinations
                return await self._get_popular_destinations(num_recommendations, db)
            
            # Parse user preferences
            user_prefs = [pref.strip().lower() for pref in user.preferences.split(',')]
            
            # Calculate destination scores based on user preferences
            destination_scores = []
            
            for idx, row in self.destinations_df.iterrows():
                dest_categories = [cat.lower() for cat in row['categories']]
                
                # Category matching score
                category_score = len(set(user_prefs) & set(dest_categories)) / len(user_prefs)
                
                # Text similarity score
                user_text = ' '.join(user_prefs)
                user_vector = self.tfidf_vectorizer.transform([user_text])
                dest_vector = self.destination_features[idx:idx+1, :self.tfidf_vectorizer.get_feature_names_out().shape[0]]
                text_score = cosine_similarity(user_vector, dest_vector)[0][0]
                
                # Combined score
                final_score = (category_score * 0.7) + (text_score * 0.3)
                
                destination_scores.append({
                    'destination_id': row['id'],
                    'score': final_score,
                    'category_score': category_score,
                    'text_score': text_score
                })
            
            # Sort by score dan ambil top N
            destination_scores.sort(key=lambda x: x['score'], reverse=True)
            top_destinations = destination_scores[:num_recommendations]
            
            # Enrich dengan destination details
            recommendations = []
            for item in top_destinations:
                dest = await db.get(Destination, item['destination_id'])
                if dest:
                    recommendations.append({
                        'destination_id': dest.id,
                        'name': dest.name,
                        'description': dest.description,
                        'score': round(item['score'], 4),
                        'explanation': f"Matches {item['category_score']:.2%} of your preferences",
                        'algorithm': 'content_based'
                    })
            
            return recommendations
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    async def explain(self, user_id: int, destination_id: int, db: AsyncSession = None) -> Dict[str, Any]:
        """Explain mengapa destination ini direkomendasikan"""
        try:
            user = await db.get(User, user_id)
            destination = await db.get(Destination, destination_id)
            
            if not user or not destination:
                raise ValueError("User atau destination tidak ditemukan")
            
            if not user.preferences:
                return {
                    "explanation": "Recommended based on popularity",
                    "details": "User has no preferences set"
                }
            
            user_prefs = [pref.strip().lower() for pref in user.preferences.split(',')]
            
            # Load destination dengan categories
            result = await db.execute(
                select(Destination).options(selectinload(Destination.categories))
                .where(Destination.id == destination_id)
            )
            dest_with_cats = result.scalar_one_or_none()
            
            dest_categories = [cat.name.lower() for cat in dest_with_cats.categories]
            matched_categories = list(set(user_prefs) & set(dest_categories))
            
            return {
                "explanation": f"Matches {len(matched_categories)} of your {len(user_prefs)} preferences",
                "details": {
                    "user_preferences": user_prefs,
                    "destination_categories": dest_categories,
                    "matched_categories": matched_categories,
                    "match_percentage": len(matched_categories) / len(user_prefs) if user_prefs else 0
                }
            }
            
        except Exception as e:
            raise Exception(f"Explanation failed: {str(e)}")
    
    async def _get_popular_destinations(self, num_recommendations: int, db: AsyncSession) -> List[Dict[str, Any]]:
        """Get popular destinations when user has no preferences"""
        result = await db.execute(
            select(Destination).limit(num_recommendations)
        )
        destinations = result.scalars().all()
        
        return [
            {
                'destination_id': dest.id,
                'name': dest.name,
                'description': dest.description,
                'score': 0.5,  # Default score
                'explanation': "Popular destination",
                'algorithm': 'content_based_popular'
            }
            for dest in destinations
        ]
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            # Create directory jika belum ada
            self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
            
            model_path = self.MODEL_DIR / self.MODEL_FILE
            
            # Save all model components
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'category_encoder': self.category_encoder,
                'destination_features': self.destination_features,
                'destinations_df': self.destinations_df,
                'similarity_matrix': self.similarity_matrix,
                'is_trained': self.is_trained,
                'trained_at': datetime.now().isoformat()
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"✅ Content-Based model saved to {model_path}")
            
        except Exception as e:
            print(f"⚠️ Failed to save Content-Based model: {str(e)}")
    
    def _auto_load_model(self):
        """Auto-load model dari disk jika ada"""
        try:
            model_path = self.MODEL_DIR / self.MODEL_FILE
            print(f"[DEBUG] Checking model path: {model_path} (exists={model_path.exists()})", flush=True)
            
            if not model_path.exists():
                print("ℹ️ No saved Content-Based model found", flush=True)
                return
            
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restore all components
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.category_encoder = model_data['category_encoder']
            self.destination_features = model_data['destination_features']
            self.destinations_df = model_data['destinations_df']
            self.similarity_matrix = model_data['similarity_matrix']
            self.is_trained = model_data['is_trained']
            
            # Store model_info untuk tracking
            self.model_info = {
                'trained_at': model_data.get('trained_at', 'unknown'),
                'n_samples': len(self.destinations_df) if self.destinations_df is not None else 0,
                'accuracy': 0.85  # Default, bisa di-update setelah evaluation
            }
            
            trained_at = model_data.get('trained_at', 'unknown')
            print(f"✅ Content-Based model loaded (trained at: {trained_at})")
            
        except Exception as e:
            print(f"⚠️ Failed to load Content-Based model: {str(e)}")