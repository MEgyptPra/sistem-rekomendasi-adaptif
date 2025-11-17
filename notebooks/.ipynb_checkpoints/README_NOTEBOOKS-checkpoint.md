# 📓 Notebooks Directory - Documentation

## ✅ PRODUCTION NOTEBOOK (USE THIS!)

### `evaluasi_kuantitatif_PRODUCTION.ipynb`
**Status:** ✅ Production-Ready (Cleaned & Optimized)

**Description:** Comprehensive evaluation notebook for adaptive recommendation system with MAB optimization.

**Key Features:**
- **48 cells** (optimized from 56 cells)
- **~6,200 lines** (cleaned from 7,104 lines)
- No redundant debug prints
- No duplicate analysis cells
- Clear structure and documentation

**Structure:**
1. **Data Preparation (Cells 1-4)**
   - Import modules with reproducibility fixes
   - Database connection setup
   - Load and temporal split data

2. **Model Components (Cells 5-10)**
   - Vectorized MMR implementation
   - Evaluation metrics (ranx-based)
   - Popularity baseline
   - Collaborative Filtering (NMF)
   - Content-Based filtering
   - Context-Aware component
   - MMR Reranker
   - MAB (UCB1) optimizer
   - Hybrid orchestrator

3. **Evaluation (Cells 11-18)**
   - Batch evaluation pipeline
   - Performance metrics computation
   - Statistical significance testing
   - Result interpretation

4. **Analysis & Visualization (Cells 19-33)**
   - Pareto frontier analysis
   - Long-tail coverage
   - MAB convergence visualization
   - Lambda sensitivity analysis
   - Statistical interpretation

5. **Export (Cells 34-48)**
   - LaTeX table generation
   - Matplotlib visualizations
   - JSON/CSV export
   - Final results summary

**How to Use:**
```python
# 1. Run cells 1-4 to load data
# 2. Run cells 5-10 to initialize models
# 3. Run cell 11 to train all models
# 4. Run cells 12-18 for evaluation
# 5. Run cells 19-48 for analysis and export
```

**Reproducibility:**
- ✅ Random seed: 42 (fixed)
- ✅ Temporal split: 80/20
- ✅ OpenBLAS threads: 1 (no race conditions)

---

## 🗑️ ARCHIVED/DEBUG NOTEBOOKS (DO NOT USE)

### Files to Ignore:
- ❌ `evaluasi_kuantitatif_FINAL copy.ipynb` - Original (before cleanup)
- ❌ `evaluasi_kuantitatif_FINAL copy 2.ipynb` - Experimental version
- ❌ `evaluasi_kuantitatif_ARCHIVE.ipynb` - Old archive
- ❌ `evaluasi_kuantitatif_.ipynb` - Early version
- ❌ `evaluasi_kuantitatif_deepseek.ipynb` - Debug/test version
- ❌ `evaluasi_deepseek&perplexcity.ipynb` - Experimental
- ❌ `kode evaluasi.ipynb` - Code snippets
- ❌ `Evaluasi Kuantitatif.ipynb` - Very old version
- ❌ `notebooks_evaluasi_adaptif_Version3.ipynb` - Deprecated

### Reason for Archival:
- 🐛 Contains debug print statements
- 📋 Redundant/duplicate analysis cells
- 🗂️ Poor structure and organization
- ❌ Not reproducible (no fixed seeds)
- 📝 Excessive documentation/comments

---

## 📊 DATA & RESULTS

### `/data/` Directory
- Training/test split data (if cached)
- Item metadata (categories, popularity)

### `/evaluation_results/` Directory
**Generated Outputs:**
- `experiment_config_complete.json` - Full experiment configuration
- `table_iv2_enhanced_publication_ready.tex` - LaTeX table for paper
- `pareto_frontier_corrected.html` - Interactive Pareto plot
- `longtail_coverage_fixed.html` - Long-tail analysis plot
- `mab_convergence_analysis.html` - MAB learning curve
- `mmr_lambda_sensitivity.html` - Lambda sensitivity plot
- `table_*.csv` - CSV exports for all tables
- `mab_final_state_detailed.json` - MAB final statistics

---

## 🔧 MAINTENANCE

### Cleanup Completed (November 4, 2025):
✅ Removed Cell 1 (Install Libraries) - Run once manually
✅ Removed Cell 1B (Clear Cache) - Manual operation
✅ Removed debug/test cells (3 cells)
✅ Removed redundant documentation markdown cells (5 cells)
✅ Cleaned up verbose print statements in all model cells
✅ Optimized imports and dependencies
✅ Fixed reproducibility issues (random seeds)

**Before:** 56 cells, 7,104 lines  
**After:** 48 cells, ~6,200 lines  
**Reduction:** 14% fewer cells, 13% fewer lines

### Future Cleanup Recommendations:
1. Consider splitting into multiple focused notebooks:
   - `01_data_preparation.ipynb`
   - `02_model_training.ipynb`
   - `03_evaluation.ipynb`
   - `04_analysis_visualization.ipynb`

2. Move model classes to separate `.py` files in `/backend/app/services/`

3. Create utility module for metrics computation

4. Add automated tests for reproducibility

---

## 📚 DEPENDENCIES

**Required Libraries:**
```bash
# Modern evaluation
pip install ranx mabwiser scikit-surprise

# Visualization
pip install plotly kaleido matplotlib seaborn

# ML & Data
pip install scikit-learn pandas numpy scipy

# Database
pip install asyncpg sqlalchemy
```

**Backend Integration:**
- Requires `pariwisata-recommender/backend` in parent directory
- Database: PostgreSQL on localhost:5432
- Database name: `pariwisata_db`

---

## 🎯 KEY METRICS

**Evaluation Metrics:**
- **Accuracy:** Precision@10, Recall@10, NDCG@10 (ranx library)
- **Diversity:** Intra-List Diversity (ILD) - category-based
- **Novelty:** Inverse popularity score
- **Coverage:** Long-tail item coverage analysis

**Statistical Tests:**
- Paired t-test for significance
- Cohen's d for effect size
- Bonferroni correction for multiple comparisons

**Models Evaluated:**
1. Popularity (baseline)
2. Collaborative Filtering (NMF)
3. Content-Based (TF-IDF)
4. Hybrid (CF + CB)
5. Hybrid + MMR (static λ)
6. Hybrid + MAB + MMR (adaptive λ) ⭐

---

## 📞 CONTACT

For questions about this notebook:
- Check inline comments and markdown cells
- Review backend code in `pariwisata-recommender/backend`
- Consult research paper methodology section

**Last Updated:** November 4, 2025  
**Notebook Version:** Production v1.0 (Post-Cleanup)
