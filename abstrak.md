# ABSTRAK

**PENGEMBANGAN SISTEM REKOMENDASI ADAPTIF *REAL-TIME* UNTUK DESTINASI WISATA: OPTIMALISASI KEBERAGAMAN DAN CAKUPAN GUNA MENDORONG PEMERATAAN DISTRIBUSI PARIWISATA**

Oleh

M Egypt Pratama

NIM: 23523311

(Program Studi Magister Informatika)

---

Transformasi digital dalam industri pariwisata telah menghadirkan tantangan mendasar terkait distribusi kunjungan yang tidak merata. Fenomena bias popularitas dalam sistem rekomendasi konvensional berkontribusi terhadap konsentrasi kunjungan wisatawan pada sekelompok kecil destinasi populer, sementara destinasi alternatif yang berpotensi mengalami marjinalisasi. Secara global, data menunjukkan bahwa sebagian besar kedatangan wisatawan terkonsentrasi pada destinasi yang telah populer, menciptakan ketimpangan distribusi yang tidak berkelanjutan. Di Kabupaten Sumedang, pola serupa teramati di mana mayoritas kunjungan terpusat pada sejumlah kecil destinasi, sementara destinasi lainnya menghadapi tantangan dalam menarik perhatian wisatawan. Sistem rekomendasi berbasis *Collaborative Filtering* tradisional cenderung memperkuat preferensi mayoritas melalui mekanisme *feedback loop*, sehingga memperparah ketimpangan distribusi eksposur destinasi.

Dalam konteks literatur sistem rekomendasi, berbagai pendekatan telah dikembangkan untuk meningkatkan keberagaman rekomendasi, termasuk teknik *Maximal Marginal Relevance* (MMR) yang memungkinkan penyeimbangan antara relevansi dan keberagaman melalui parameter tunggal. Namun, pendekatan yang ada umumnya menggunakan parameter statis yang tidak dapat beradaptasi terhadap karakteristik dinamis domain pariwisata. Faktor kontekstual seperti kondisi cuaca, waktu kunjungan, dan preferensi pengguna yang bervariasi sangat memengaruhi keputusan wisatawan, namun belum terintegrasi secara adaptif dalam sistem diversifikasi. Lebih lanjut, eksplorasi sistematis mengenai optimasi parameter diversifikasi secara dinamis untuk mencapai keseimbangan optimal antara akurasi dan keberagaman dalam konteks pariwisata dengan keterbatasan data masih terbatas. Penelitian ini bertujuan mengembangkan dan mengevaluasi sistem rekomendasi adaptif yang mampu mengoptimalkan keseimbangan antara akurasi dan keberagaman melalui mekanisme pembelajaran parameter dinamis, serta memvalidasi dampaknya terhadap distribusi eksposur destinasi.

Penelitian ini menggunakan *Design Science Research Methodology* (DSRM) untuk mengembangkan artefak berupa sistem rekomendasi adaptif dengan arsitektur hibrida yang mengintegrasikan *Collaborative Filtering*, *Content-Based Filtering*, dan komponen *Context-Aware* yang memproses informasi kontekstual secara *real-time*. Mekanisme pembelajaran adaptif diimplementasikan menggunakan algoritma *Multi-Armed Bandit* dengan pendekatan kontekstual yang memilih parameter diversifikasi secara dinamis berdasarkan fungsi *reward* yang mempertimbangkan akurasi, keberagaman, dan kebaruan. Evaluasi dilakukan terhadap dataset pariwisata Kabupaten Sumedang yang telah dipreproses, menghasilkan data akhir dengan karakteristik *high sparsity*, untuk mengukur performa sistem dibandingkan dengan model baseline melalui metrik standar sistem rekomendasi.

Hasil evaluasi kuantitatif menunjukkan bahwa sistem yang dikembangkan berhasil meningkatkan keberagaman rekomendasi secara signifikan dibandingkan model baseline, dengan tetap mempertahankan tingkat akurasi yang setara secara statistik. Perbaikan juga teramati pada metrik distribusi, menunjukkan penurunan tingkat konsentrasi rekomendasi dan peningkatan cakupan katalog destinasi yang direkomendasikan. Analisis distribusi lebih lanjut mengungkapkan bahwa sistem mampu meningkatkan eksposur destinasi berkualitas tinggi yang sebelumnya kurang terekspos, dengan peningkatan frekuensi rekomendasi yang substansial pada kategori *long-tail*. Mekanisme pembelajaran adaptif menunjukkan kemampuan sistem dalam menyesuaikan strategi diversifikasi berdasarkan karakteristik data dan konteks pengguna, mengindikasikan efektivitas pendekatan *Multi-Armed Bandit* dalam domain pariwisata dengan keterbatasan data. Integrasi komponen kontekstual juga terbukti memberikan kontribusi positif terhadap relevansi dan keberagaman rekomendasi yang dihasilkan.

Penelitian ini memberikan kontribusi teoretis berupa demonstrasi empiris bahwa pendekatan pembelajaran adaptif menggunakan *Multi-Armed Bandit* dapat mengatasi permasalahan *trade-off* antara akurasi dan keberagaman dalam sistem rekomendasi pariwisata. Temuan menunjukkan bahwa optimasi parameter diversifikasi secara dinamis lebih efektif dibandingkan pendekatan statis konvensional dalam konteks data dengan sparsitas tinggi. Dari perspektif praktis, sistem yang dikembangkan menawarkan solusi algoritmik untuk mendukung pemerataan distribusi pariwisata dan meningkatkan visibilitas destinasi berkualitas yang kurang terekspos, dengan implikasi positif bagi pengelola destinasi wisata dan pembuat kebijakan dalam upaya pengembangan pariwisata berkelanjutan. Keterbatasan penelitian meliputi cakupan geografis yang terbatas pada satu kabupaten dan evaluasi yang dilakukan secara *offline* menggunakan data historis.

**Kata Kunci:** Sistem Rekomendasi Adaptif, *Multi-Armed Bandit*, *Maximal Marginal Relevance*, Bias Popularitas, Pariwisata Berkelanjutan, *Distribusi Long-Tail*

---

# ABSTRACT

**DEVELOPMENT OF AN ADAPTIVE REAL-TIME RECOMMENDATION SYSTEM FOR TOURIST DESTINATIONS: OPTIMIZING DIVERSITY AND COVERAGE TO PROMOTE EQUITABLE TOURISM DISTRIBUTION**

By

M Egypt Pratama

Student ID: 23523311

(Master's Program in Informatics)

---

The digital transformation in the tourism industry has introduced fundamental challenges concerning uneven visitor distribution. The popularity bias phenomenon in conventional recommendation systems contributes to the concentration of tourist visits at a small subset of popular destinations, while potentially valuable alternative destinations experience marginalization. Global data indicates that the majority of tourist arrivals are concentrated at already-popular destinations, creating unsustainable distribution imbalances. In Sumedang Regency, similar patterns are observed where the majority of visits are concentrated at a limited number of destinations, while other destinations face challenges in attracting visitor attention. Traditional *Collaborative Filtering*-based recommendation systems tend to reinforce majority preferences through feedback loop mechanisms, thereby exacerbating the inequality in destination exposure distribution.

Within the context of recommendation systems literature, various approaches have been developed to enhance recommendation diversity, including the *Maximal Marginal Relevance* (MMR) technique which enables balancing between relevance and diversity through a single parameter. However, existing approaches typically employ static parameters that cannot adapt to the dynamic characteristics of the tourism domain. Contextual factors such as weather conditions, visit timing, and varying user preferences significantly influence tourist decision-making, yet have not been adaptively integrated into diversification systems. Furthermore, systematic exploration of dynamic diversification parameter optimization to achieve optimal balance between accuracy and diversity in tourism contexts with data limitations remains constrained. This research aims to develop and evaluate an adaptive recommendation system capable of optimizing the balance between accuracy and diversity through dynamic parameter learning mechanisms, and to validate its impact on destination exposure distribution.

This research employs *Design Science Research Methodology* (DSRM) to develop an artifact in the form of an adaptive recommendation system with hybrid architecture integrating *Collaborative Filtering*, *Content-Based Filtering*, and *Context-Aware* components that process contextual information in *real-time*. The adaptive learning mechanism is implemented using *Multi-Armed Bandit* algorithms with a contextual approach that dynamically selects diversification parameters based on a *reward* function considering accuracy, diversity, and novelty. Evaluation was conducted on a preprocessed tourism dataset from Sumedang Regency, yielding final data with *high sparsity* characteristics, to measure system performance compared to baseline models through standard recommendation system metrics.

Quantitative evaluation results demonstrate that the developed system successfully enhanced recommendation diversity significantly compared to baseline models, while maintaining statistically equivalent accuracy levels. Improvements were also observed in distribution metrics, indicating reduced recommendation concentration and increased coverage of recommended destination catalogs. Further distribution analysis revealed that the system effectively increased exposure for high-quality yet previously underexposed destinations, with substantial frequency increases in the *long-tail* category. The adaptive learning mechanism demonstrated the system's capability to adjust diversification strategies based on data characteristics and user context, indicating the effectiveness of the *Multi-Armed Bandit* approach in tourism domains with data constraints. The integration of contextual components also proved to contribute positively to the relevance and diversity of generated recommendations.

This research provides theoretical contributions in the form of empirical demonstration that adaptive learning approaches using *Multi-Armed Bandit* can address the *trade-off* problem between accuracy and diversity in tourism recommendation systems. Findings indicate that dynamic diversification parameter optimization is more effective than conventional static approaches in contexts with high data sparsity. From a practical perspective, the developed system offers an algorithmic solution to support equitable tourism distribution and enhance visibility for underexposed quality destinations, with positive implications for destination managers and policymakers in sustainable tourism development efforts. Research limitations include geographical scope restricted to one regency and *offline* evaluation conducted using historical data.

**Keywords:** Adaptive Recommendation System, *Multi-Armed Bandit*, *Maximal Marginal Relevance*, Popularity Bias, Sustainable Tourism, *Long-Tail Distribution*

---

**Catatan:** Abstrak ini disesuaikan dengan hasil evaluasi kuantitatif menggunakan proper preprocessed dataset (239 pengguna, 192 destinasi, 2.123 ratings) yang dievaluasi pada 1 Januari 2026.

**Note:** This abstract has been adapted based on quantitative evaluation results using the proper preprocessed dataset (239 users, 192 destinations, 2,123 ratings) evaluated on January 1, 2026.
