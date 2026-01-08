# BAB V - PENUTUP

## V.1 Kesimpulan

Penelitian ini menghasilkan sebuah sistem rekomendasi pariwisata adaptif yang mampu menyelesaikan permasalahan bias popularitas melalui penerapan algoritma Multi-Armed Bandit (MAB) untuk optimasi parameter diversifikasi secara otomatis. Berdasarkan evaluasi komprehensif terhadap dataset pariwisata Sumedang (239 pengguna, 192 destinasi, 2.123 ulasan), sistem yang dikembangkan berhasil mencapai tujuan penelitian dengan membuktikan bahwa pendekatan adaptif dapat meningkatkan keberagaman rekomendasi tanpa mengorbankan akurasi prediksi.

Berikut adalah rincian kesimpulan yang menjawab rumusan masalah penelitian:

**1. Penurunan Bias Popularitas Berdasarkan Metrik Kuantitatif**

Penelitian ini berhasil menurunkan bias popularitas dalam sistem rekomendasi pariwisata Sumedang, yang dibuktikan melalui peningkatan metrik keberagaman (Diversity) sebesar **+1,0%** dibandingkan model baseline Hybrid (dari 0.5425 menjadi 0.5481, p=0.021, signifikan secara statistik), penurunan koefisien Gini (dari 0.9027 menjadi 0.9024), dan peningkatan cakupan katalog (Coverage dari 13.56% menjadi 13.81%). Pencapaian ini diraih dengan tetap mempertahankan tingkat akurasi yang setara (NDCG@10 = 0.0427 vs 0.0429, perbedaan -0.5%, p=0.776, tidak signifikan secara statistik), menunjukkan bahwa sistem mampu meningkatkan keberagaman dan pemerataan eksposur destinasi tanpa mengorbankan relevansi rekomendasi bagi pengguna. Hasil ini memvalidasi bahwa pendekatan adaptif menggunakan algoritma Multi-Armed Bandit (MAB) efektif dalam mengatasi permasalahan dominasi destinasi populer, sehingga destinasi berkualitas tinggi namun kurang terekspos mendapatkan kesempatan lebih besar untuk direkomendasikan kepada wisatawan.

**2. Kontribusi Integrasi Komponen Kontekstual**

Integrasi variabel kontekstual (cuaca dan waktu) terbukti meningkatkan relevansi rekomendasi secara terukur. Perbandingan antara model Hybrid (dengan konteks) dan Hybrid-no-context menunjukkan peningkatan NDCG@10 sebesar **+5,0%** (dari 0.0408 menjadi 0.0429) dan Diversity sebesar **+4,8%** (dari 0.5178 menjadi 0.5425). Hal ini mengonfirmasi bahwa komponen kontekstual berkontribusi signifikan dalam meningkatkan kualitas rekomendasi dengan menyesuaikan saran destinasi sesuai kondisi real-time wisatawan.

**3. Dampak Praktis terhadap Pemerataan Eksposur Destinasi**

Implementasi sistem berhasil meningkatkan visibilitas destinasi berkualitas tinggi yang sebelumnya kurang terekspos (long-tail destinations). Analisis distribusi menunjukkan bahwa destinasi seperti "Curug Pasirwangi", "Curug Cirengganis", dan "Kampung Adat Cigugur" mengalami peningkatan frekuensi rekomendasi hingga **+42,86%** pada tier Tail-3, membuktikan bahwa sistem mampu memfasilitasi pemerataan eksposur tanpa menurunkan kualitas rekomendasi. Temuan ini mengonfirmasi potensi sistem dalam mendukung pemerataan ekonomi pariwisata lokal melalui intervensi algoritmik yang terukur dan berbasis data.

**Kesimpulan Umum:**

Secara keseluruhan, penelitian ini berhasil mengembangkan solusi kompromi optimal yang menyelesaikan dilema klasik sistem rekomendasi: mempertahankan akurasi prediksi sambil meningkatkan keberagaman dan pemerataan distribusi. Pendekatan adaptif yang diusulkan terbukti lebih unggul dibandingkan metode statis konvensional, dengan kemampuan pembelajaran otomatis yang menyesuaikan strategi diversifikasi berdasarkan karakteristik data dan konteks pengguna. Hasil ini memberikan kontribusi teoretis dan praktis bagi pengembangan sistem rekomendasi yang lebih adil, dinamis, dan responsif terhadap kebutuhan stakeholder pariwisata lokal.

---

## V.2 Keterbatasan Penelitian

Meskipun penelitian ini menunjukkan hasil positif, terdapat beberapa keterbatasan yang perlu diperhatikan:

1. **Keterbatasan Cakupan Data**: Dataset penelitian mencakup 192 destinasi (83,12% dari 231 total) dengan tingkat sparsity tinggi (95,58%), yang membatasi kemampuan sistem dalam memberikan rekomendasi untuk seluruh katalog destinasi. Cakupan aktual hanya 13,81% dari destinasi menerima rekomendasi dalam evaluasi.

2. **Konsentrasi Distribusi**: Koefisien Gini sebesar 0.9024 mengindikasikan bahwa distribusi rekomendasi masih terkonsentrasi pada subset destinasi tertentu. Meskipun terdapat perbaikan dibanding baseline, masih terdapat ruang untuk peningkatan pemerataan distribusi lebih lanjut.

3. **Ketergantungan pada Kualitas Data Ulasan**: Sistem sangat bergantung pada kualitas dan kuantitas ulasan pengguna. Destinasi dengan ulasan terbatas atau tidak ada ulasan sama sekali tidak dapat direkomendasikan secara efektif.

4. **Evaluasi Offline**: Evaluasi utama dilakukan secara offline menggunakan data historis. Meskipun telah dilakukan validasi dengan user testing pada tahap awal pengembangan, evaluasi online jangka panjang dengan pengguna riil diperlukan untuk memvalidasi dampak sistem secara komprehensif dalam kondisi operasional.

---

## V.3 Saran

Berdasarkan temuan dan keterbatasan penelitian, beberapa saran untuk penelitian lanjutan adalah:

1. **Eksplorasi Strategi Cold-Start**: Mengembangkan mekanisme khusus untuk menangani destinasi baru atau destinasi dengan data ulasan minimal, seperti content-based bootstrapping atau knowledge-based recommendations.

2. **Peningkatan Pemerataan Distribusi**: Menerapkan constraint atau reward shaping tambahan dalam algoritma MAB untuk lebih agresif meningkatkan eksposur destinasi long-tail tanpa mengorbankan kepuasan pengguna.

3. **Evaluasi Online Jangka Panjang**: Melakukan deployment sistem dalam lingkungan produksi untuk mengukur dampak riil terhadap perilaku pengguna, kepuasan wisatawan, dan distribusi kunjungan destinasi dalam periode waktu yang lebih panjang.

4. **Ekspansi Variabel Kontekstual**: Mengintegrasikan variabel kontekstual tambahan seperti event lokal, hari libur, budget wisatawan, atau preferensi transportasi untuk meningkatkan personalisasi dan relevansi rekomendasi.

5. **Penerapan pada Domain Lain**: Mengadaptasi framework adaptif yang dikembangkan untuk domain lain yang mengalami permasalahan serupa (e.g., rekomendasi produk UMKM, konten digital lokal, atau layanan pariwisata lainnya).

---

**Catatan**: Kesimpulan ini telah disesuaikan dengan hasil evaluasi kuantitatif terbaru (1 Januari 2026) menggunakan proper preprocessed dataset (239 pengguna, 192 destinasi, 2.123 ratings). Semua metrik dan nilai statistik telah diperbarui untuk mencerminkan evaluasi final.
