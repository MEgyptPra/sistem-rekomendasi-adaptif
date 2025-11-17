import numpy as np
import logging

logger = logging.getLogger(__name__)

class ContextAwareComponent:
    """
    Menerapkan boost kontekstual (logika aditif) ke rekomendasi 
    menggunakan aturan konteks pariwisata Indonesia.
    Sama persis dengan evaluasi_kuantitatif_FINAL.md
    """
    
    def __init__(self):
        self.context_rules = {
            # --- Tipe Hari ---
            'weekend': {
                'Wisata Alam': 1.5, 'Wisata Keluarga': 1.6, 'Wisata Buatan/Rekreasi': 1.6,
                'Wisata Kuliner': 1.4, 'Wisata Petualangan': 1.4, 'Wisata Budaya & Sejarah': 1.1
            },
            'weekday': {
                'Wisata Budaya & Sejarah': 1.4, 'Wisata Religi': 1.3, 'Wisata Kuliner': 1.2,
                'Wisata Kesehatan & Wellness': 1.4, 'Wisata Alam': 1.1, 'Wisata Keluarga': 0.8,
            },
            'libur_nasional': {
                'Wisata Buatan/Rekreasi': 1.8, 'Wisata Keluarga': 1.8, 'Wisata Kuliner': 1.6,
                'Wisata Alam': 1.7, 'Wisata Petualangan': 1.5
            },
             'libur_lebaran': {
                'Wisata Keluarga': 2.0, 'Wisata Buatan/Rekreasi': 1.9, 'Wisata Kuliner': 1.7,
                'Wisata Alam': 1.5
            },

            # --- Cuaca ---
            'cerah': {
                'Wisata Alam': 1.7, 'Wisata Petualangan': 1.6, 'Wisata Olahraga': 1.5,
                'Wisata Buatan/Rekreasi': 1.4, 'Wisata Keluarga': 1.4,
                'Wisata Kuliner': 1.0, 'Wisata Budaya & Sejarah': 0.9
            },
            'mendung': {
                'Wisata Budaya & Sejarah': 1.4, 'Wisata Kuliner': 1.3, 'Wisata Keluarga': 1.2,
                'Wisata Alam': 1.2, 'Wisata Buatan/Rekreasi': 1.2
            },
            'hujan': {
                'Wisata Kuliner': 1.8, 'Wisata Budaya & Sejarah': 1.7,
                'Wisata Kesehatan & Wellness': 1.6, 'Wisata Buatan/Rekreasi': 1.2,
                'Wisata Alam': 0.5, 'Wisata Petualangan': 0.4, 'Wisata Olahraga': 0.3
            },

            # --- Musim ---
            'musim_kemarau': { 'Wisata Alam': 1.4, 'Wisata Petualangan': 1.3 },
            'musim_hujan': { 'Wisata Budaya & Sejarah': 1.3, 'Wisata Kuliner': 1.2, 'Wisata Alam': 0.8 },

            # --- Waktu ---
            'pagi': {'Wisata Alam': 1.3, 'Wisata Olahraga': 1.4, 'Wisata Budaya & Sejarah': 1.1},
            'siang': {'Wisata Kuliner': 1.3, 'Wisata Buatan/Rekreasi': 1.2, 'Wisata Budaya & Sejarah': 1.2},
            'sore': {'Wisata Kuliner': 1.4, 'Wisata Alam': 1.1},
            'malam': {'Wisata Kuliner': 1.7, 'Wisata Buatan/Rekreasi': 1.3},

            # --- Tren & Event ---
            'viral_trend': {'all_categories': 2.0},
            'festival_kuliner': {'Wisata Kuliner': 2.2, 'Wisata Keluarga': 1.5},
            'festival_budaya': {'Wisata Budaya & Sejarah': 2.2, 'Wisata Keluarga': 1.4}
        }

    def get_contextual_boost(self, recommendations, user_context, item_categories):
        """
        Logika ADITIF (Penambahan Skor) - Kunci keberhasilan di evaluasi
        """
        boosted_recs = []
        
        # Default values jika context kosong
        day_type = user_context.get('day_type', 'weekday')
        weather = user_context.get('weather', 'cerah')
        season = user_context.get('season', 'musim_kemarau')
        time_of_day = user_context.get('time_of_day', 'siang')
        crowd_density = user_context.get('crowd_density', 'sedang')
        is_viral = user_context.get('viral_trend', False)
        special_event = user_context.get('special_event')

        for rec in recommendations:
            item_id = rec['destination_id']
            original_score = rec['score']
            category = item_categories.get(item_id, 'Other') 
            
            total_additive_boost = 0.0 
            
            # 1. Tipe Hari
            boost = self.context_rules.get(day_type, {}).get(category, 1.0)
            total_additive_boost += (boost - 1.0)

            # 2. Cuaca
            boost = self.context_rules.get(weather, {}).get(category, 1.0)
            total_additive_boost += (boost - 1.0)

            # 3. Musim
            boost = self.context_rules.get(season, {}).get(category, 1.0)
            total_additive_boost += (boost - 1.0)

            # 4. Waktu
            boost = self.context_rules.get(time_of_day, {}).get(category, 1.0)
            total_additive_boost += (boost - 1.0)

            # 5. Kepadatan (Logika khusus)
            crowd_boost = 1.0
            if crowd_density == 'puncak_kepadatan': crowd_boost = 0.5
            elif crowd_density == 'sangat_ramai': crowd_boost = 0.7
            elif crowd_density == 'ramai': crowd_boost = 0.9
            elif crowd_density == 'sepi': crowd_boost = 1.2
            elif crowd_density == 'sangat_sepi': crowd_boost = 1.3
            total_additive_boost += (crowd_boost - 1.0)

            # 6. Tren Viral
            if is_viral:
                total_additive_boost += 1.0 # (2.0 - 1.0)
                
            # 7. Event
            if special_event:
                boost = self.context_rules.get(special_event, {}).get(category, 1.0)
                total_additive_boost += (boost - 1.0)

            # PENAMBAHAN SKOR
            new_score = original_score + total_additive_boost
            
            # Update record
            new_rec = rec.copy()
            new_rec['score'] = new_score
            new_rec['original_score'] = original_score # Untuk debugging
            new_rec['boost_amount'] = total_additive_boost
            boosted_recs.append(new_rec)
            
        return boosted_recs

    def get_context_key_string(self, context_dict):
        """Membuat key unik untuk MAB"""
        weather = context_dict.get('weather', 'unknown')
        day = context_dict.get('day_type', 'unknown')
        season = context_dict.get('season', 'unknown')
        time = context_dict.get('time_of_day', 'unknown')
        crowd = context_dict.get('crowd_density', 'unknown')
        event = context_dict.get('special_event', 'noevent')
        viral = 'viral' if context_dict.get('viral_trend') else 'notviral'
        return f"{weather}_{day}_{season}_{time}_{crowd}_{event}_{viral}"